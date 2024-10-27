# main.py
from flask import Flask, render_template, request, jsonify, send_file
import pytesseract
from PIL import Image
import io
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 確保上傳目錄存在
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test-ocr')
def test_ocr():
    """測試 OCR 是否正常工作"""
    try:
        version = pytesseract.get_tesseract_version()
        languages = pytesseract.get_languages()
        return jsonify({
            'status': 'ok',
            'version': str(version),
            'languages': languages
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': '未找到檔案'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未選擇檔案'}), 400

        # 讀取圖片
        image = Image.open(file.stream)

        try:
            # OCR 識別
            text = pytesseract.image_to_string(image, lang='eng+chi_tra')
        except Exception as e:
            print(f"OCR Error: {str(e)}")
            return jsonify({'error': '文字識別失敗，請確認圖片清晰度'}), 500

        return jsonify({
            'success': True,
            'text': text
        })

    except Exception as e:
        print(f"General Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_text():
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': '沒有文字可供下載'}), 400

        # 建立記憶體檔案
        file_stream = io.BytesIO()
        file_stream.write(text.encode('utf-8'))
        file_stream.seek(0)

        return send_file(
            file_stream,
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'OCR結果_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 測試 OCR 是否可用
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract version: {version}")
        print(f"Available languages: {pytesseract.get_languages()}")
    except Exception as e:
        print(f"Warning: Tesseract initialization error: {e}")

    app.run(host='0.0.0.0', port=8080)