#!/bin/bash

# === 腳本開始 ===
echo "=== 開始設置 OCR 環境 ==="

# 1. 更新與安裝 Python 套件
echo "步驟 1: 安裝 Python 套件..."
pip install --upgrade pip
pip install pillow flask flask-cors pytesseract python-dotenv

# 2. 檢查 Tesseract 是否正確安裝
echo -e "\n步驟 2: 檢查 Tesseract 安裝..."
if which tesseract > /dev/null; then
    echo "✓ Tesseract 已安裝"
    echo "位置: $(which tesseract)"
    echo "版本資訊:"
    tesseract --version
else
    echo "✗ 找不到 Tesseract"
fi

# 3. 檢查環境變數
echo -e "\n步驟 3: 檢查環境變數..."
echo "TESSDATA_PREFIX = $TESSDATA_PREFIX"
if [ -z "$TESSDATA_PREFIX" ]; then
    echo "警告: TESSDATA_PREFIX 未設定"
fi

# 4. 檢查 Tesseract 語言數據
echo -e "\n步驟 4: 檢查可用的語言文件..."
if [ -d "$TESSDATA_PREFIX" ]; then
    echo "語言文件目錄存在: $TESSDATA_PREFIX"
    echo "可用的語言文件:"
    ls -l "$TESSDATA_PREFIX"/*.traineddata 2>/dev/null || echo "找不到語言文件"
else
    echo "警告: 找不到語言文件目錄"
fi

# 5. 顯示 PATH 環境變數
echo -e "\n步驟 5: 檢查系統路徑..."
echo "PATH = $PATH"

echo -e "\n=== 設置完成 ===\n"