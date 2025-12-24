#!/bin/bash
# 執行所有測試並處理結果的腳本

set -e  # 遇到錯誤時停止執行

echo "=========================================="
echo "開始執行測試套件"
echo "=========================================="

# 建立結果目錄
mkdir -p results

# 執行 Robot Framework 測試
echo ""
echo "執行 Robot Framework Web 自動化測試..."
robot --outputdir results \
      --log results/log.html \
      --report results/report.html \
      robotframework_tests/tests/limitations_and_fees_tests.robot

ROBOT_EXIT_CODE=$?

# 執行 Jest API 測試
echo ""
echo "執行 Jest API 測試..."
npm run test:json

JEST_EXIT_CODE=$?

# 處理測試結果
echo ""
echo "處理測試結果並發送通知..."

# 檢查環境變數
if [ -z "$SLACK_BOT_TOKEN" ]; then
    echo "警告: SLACK_BOT_TOKEN 未設定，將跳過 Slack 通知"
fi

if [ -z "$GOOGLE_SHEET_ID" ]; then
    echo "警告: GOOGLE_SHEET_ID 未設定，將跳過 Google Sheets 寫入"
fi

# 執行結果處理腳本（處理 Robot Framework 結果）
python test_result_handler.py \
    --robot-output results/output.xml \
    --slack-channel "${SLACK_CHANNEL:-#testing}" \
    --slack-token "${SLACK_BOT_TOKEN:-}" \
    --google-credentials "${GOOGLE_CREDENTIALS_PATH:-credentials.json}" \
    --google-sheet-id "${GOOGLE_SHEET_ID:-}" \
    --worksheet-name "Robot Framework 測試結果"

# 處理 Jest 測試結果
if [ -f "results/jest-results.json" ]; then
    python test_result_handler.py \
        --jest-json results/jest-results.json \
        --slack-channel "${SLACK_CHANNEL:-#testing}" \
        --slack-token "${SLACK_BOT_TOKEN:-}" \
        --google-credentials "${GOOGLE_CREDENTIALS_PATH:-credentials.json}" \
        --google-sheet-id "${GOOGLE_SHEET_ID:-}" \
        --worksheet-name "Jest API 測試結果"
fi

echo ""
echo "=========================================="
echo "測試執行完成"
echo "=========================================="
echo "Robot Framework 測試結果: results/report.html"
echo "Jest 測試覆蓋率: coverage/index.html"

# 如果任一測試失敗，回傳非零退出碼
if [ $ROBOT_EXIT_CODE -ne 0 ] || [ $JEST_EXIT_CODE -ne 0 ]; then
    exit 1
fi

exit 0

