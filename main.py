from flask import Flask, render_template, request, jsonify, send_file
import pytesseract
from PIL import Image, ImageEnhance
import numpy as np
import io
import os
import sys
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def preprocess_image(image):
    """圖片預處理以提高識別率"""
    try:
        # 轉換為RGB模式
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # 調整大小（如果圖片太小）
        min_size = 1000
        ratio = min_size / min(image.size)
        if ratio > 1:
            new_size = tuple([int(dim * ratio) for dim in image.size])
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        # 增強對比度
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        # 增強銳利度
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.5)

        return image
    except Exception as e:
        print(f"圖片預處理錯誤: {e}")
        return image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("收到上傳請求")
    try:
        if 'file' not in request.files:
            return jsonify({'error': '未找到檔案'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '未選擇檔案'}), 400

        print(f"處理檔案: {file.filename}")

        # 讀取並預處理圖片
        image = Image.open(file.stream)
        image = preprocess_image(image)

        try:
            # 使用繁體中文和英文進行識別
            text = pytesseract.image_to_string(
                image,
                lang='chi_tra+eng',
                config='--psm 3 --oem 1 -c preserve_interword_spaces=1'
            )

            # 清理文字
            text = text.replace(' ', ' ').strip()
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            text = '\n'.join(lines)

            print(f"識別結果長度: {len(text)}")
            print("識別結果:")
            print(text)

            return jsonify({
                'success': True,
                'text': text
            })

        except Exception as ocr_error:
            print(f"OCR 識別錯誤: {ocr_error}")
            return jsonify({
                'error': f'識別錯誤: {str(ocr_error)}'
            }), 500

    except Exception as e:
        print(f"處理錯誤: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_text():
    try:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': '沒有文字可供下載'}), 400

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
    print("\n=== OCR 服務啟動 ===")
    print(f"Tesseract 版本: {pytesseract.get_tesseract_version()}")
    print(f"可用語言: {pytesseract.get_languages()}")
    app.run(host='0.0.0.0', port=8080, debug=True)