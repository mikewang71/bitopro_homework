# BitoPro 自動化測試專案

> 完整的 Web 自動化測試、API 測試以及測試結果處理解決方案

[![Test Status](https://img.shields.io/badge/tests-passing-brightgreen)]() [![Python](https://img.shields.io/badge/Python-3.8+-blue)]() [![Node.js](https://img.shields.io/badge/Node.js-14+-green)]()

## 🚀 快速開始（一條指令執行所有測試）

```bash
# 1. 安裝依賴
pip install -r requirements.txt && npm install

# 2. 執行所有測試
./run_all_tests.sh
```

就是這麼簡單！測試結果會自動產生在 `results/` 資料夾。

---

## 📋 技術棧 (Tech Stack)

| 類別 | 技術 |
|------|------|
| **Web 自動化測試** | Robot Framework 6.1.1 + Python 3.8+ |
| **API 測試** | Jest 29.7.0 + Node.js 14+ + axios 1.13.2 |
| **瀏覽器驅動** | Selenium 4.15.2 + Chrome |
| **測試後處理** | Python + Slack SDK + Google Sheets API |
| **設計模式** | Page Object Model (POM) |

---

## 📁 專案結構

```
bitopro_homework/
├── robotframework_tests/          # Robot Framework Web 自動化測試
│   ├── libraries/
│   │   └── ApiLibrary.py         # API 呼叫封裝（Python 關鍵字庫）
│   ├── pages/
│   │   └── LimitationsAndFeesPage.py  # Page Object Model
│   ├── tests/
│   │   └── limitations_and_fees_tests.robot  # 測試用例（8個）
│   └── robot_tests_config.robot   # 全域設定
│
├── tests/                         # Jest API 測試
│   ├── ohlc.test.js              # OHLC 資料 API 測試（16個測試）
│   └── README.md                 # API 測試詳細說明
│
├── docs/                          # 文件資料夾
│   ├── QUICKSTART.md             # 快速開始指南
│   ├── SETUP_GUIDE.md            # Slack 和 Google Sheets 設定指南
│   ├── PROJECT_SUMMARY.md        # 專案完成總結
│   └── SUBMISSION_CHECKLIST.md   # 繳交檢查清單
│
├── results/                       # 測試結果輸出資料夾
│
├── test_result_handler.py         # 測試結果處理腳本（Slack + Google Sheets）
├── run_all_tests.sh               # 整合執行腳本
│
├── requirements.txt               # Python 依賴（版本已鎖定）
├── package.json                   # Node.js 依賴（版本已鎖定）
├── jest.config.js                 # Jest 配置
├── .env.example                   # 環境變數範例
└── README.md                      # 本檔案
```

---

## ⚡ 安裝與執行

### 前置需求

- Python 3.8+
- Node.js 14+
- Chrome 瀏覽器
- ChromeDriver（或使用 WebDriver Manager）

### 1. 安裝依賴

```bash
# Python 依賴
pip install -r requirements.txt

# Node.js 依賴
npm install
```

### 2. 執行測試

#### 方式一：執行所有測試（推薦）

```bash
./run_all_tests.sh
```

此腳本會：
- 執行 Robot Framework Web 自動化測試
- 執行 Jest API 測試
- 產生測試報告在 `results/` 資料夾

#### 方式二：分別執行

```bash
# Robot Framework 測試
robot --outputdir results robotframework_tests/tests/limitations_and_fees_tests.robot

# Jest API 測試
npm test

# 產生覆蓋率報告
npm run test:coverage
```

---

## 📊 測試用例

### Robot Framework Web 自動化測試（8 個測試用例）

| ID | 測試用例 | 說明 |
|----|---------|------|
| TC001 | 驗證限制與費用頁面正常顯示 | 驗證頁面可以正常載入 |
| TC002 | 驗證 API 回應結構正確 | 驗證 API 回應格式 |
| TC003 | 驗證網頁費用資料與 API 資料一致 | 資料一致性驗證 |
| TC004 | 驗證網頁限制資料與 API 資料一致 | 資料一致性驗證 |
| TC005 | 驗證貨幣單位顯示正確 | 貨幣單位驗證 |
| TC006 | 驗證數值格式正確 | 格式驗證 |
| TC007 | 驗證 API 異常處理 | 錯誤處理驗證 |
| TC008 | 驗證資料完整性 | 完整性驗證 |

### Jest API 測試（16 個測試，8 個主要測試用例）

| ID | 測試用例 | 說明 |
|----|---------|------|
| TC001 | 驗證 API 回應狀態碼為 200 | HTTP 狀態碼驗證 |
| TC002 | 驗證回傳資料結構正確 | Schema 驗證 |
| TC003 | 驗證資料型態正確 | 資料型態驗證 |
| TC004 | 驗證 high >= low 的邏輯正確性 | OHLC 邏輯驗證 |
| TC005 | 驗證時間戳記格式正確 | 時間戳驗證 |
| TC006 | 驗證錯誤處理 | 錯誤處理驗證 |
| TC007 | 驗證不同時間解析度 | 多種 resolution 測試 |
| TC008 | 驗證資料不應為空 | 資料完整性驗證 |

**API Endpoint**: `GET https://api.bitopro.com/v3/trading-history/btc_twd`

---

## 🔔 測試後處理（加分功能）

### 功能說明

測試執行完成後，可以自動：
1. **發送 Slack 通知** - 格式：`YYYY/MM/DD 測試執行完畢`
2. **寫入 Google Sheets** - 記錄執行時間、Pass/Fail 數量、通過率等

### 設定步驟

#### 1. 複製環境變數範例

```bash
cp .env.example .env
```

#### 2. 設定 Slack（可選）

1. 前往 [Slack API](https://api.slack.com/apps) 建立 App
2. 取得 Bot Token（格式：`xoxb-...`）
3. 在 `.env` 中填入 `SLACK_BOT_TOKEN` 和 `SLACK_CHANNEL`

#### 3. 設定 Google Sheets（可選）

1. 前往 [Google Cloud Console](https://console.cloud.google.com/) 建立專案
2. 啟用 Google Sheets API 和 Google Drive API
3. 建立 Service Account 並下載 `credentials.json`
4. 在 `.env` 中填入 `GOOGLE_CREDENTIALS_PATH` 和 `GOOGLE_SHEET_ID`

**詳細設定步驟請參考**: `docs/SETUP_GUIDE.md`

### 執行測試後處理

```bash
# 處理 Robot Framework 測試結果
python test_result_handler.py \
  --robot-output results/output.xml \
  --slack-channel "#testing" \
  --slack-token "xoxb-your-token" \
  --google-credentials "credentials.json" \
  --google-sheet-id "your-sheet-id"
```

### 📸 測試結果展示

> **注意**: 以下為功能展示說明，實際執行後會產生類似的結果

#### Slack 通知範例
```
2024/12/19 測試執行完畢

測試框架: Robot Framework
總測試數: 8
通過: 8
失敗: 0
執行時間: 45.23 秒
通過率: 100.00%
```

#### Google Sheets 記錄範例
| 日期 | 測試框架 | 總測試數 | 通過 | 失敗 | 執行時間(秒) | 通過率(%) |
|------|---------|---------|------|------|------------|----------|
| 2024/12/19 | Robot Framework | 8 | 8 | 0 | 45.23 | 100.00 |
| 2024/12/19 | Jest | 16 | 16 | 0 | 1.50 | 100.00 |

---

## 🛠️ 技術架構

### Robot Framework 測試
- **設計模式**: Page Object Model (POM)
- **API 封裝**: 自訂 Python Library (`ApiLibrary.py`)
- **測試框架**: Robot Framework 6.1.1
- **瀏覽器**: Chrome + Selenium 4.15.2

### Jest API 測試
- **測試框架**: Jest 29.7.0
- **HTTP 客戶端**: axios 1.13.2
- **測試覆蓋率**: 支援 HTML/JSON 報告

### 測試後處理
- **語言**: Python 3.8+
- **功能**: 
  - Slack 通知（使用 slack-sdk）
  - Google Sheets 寫入（使用 gspread）

---

## 📚 文件說明

| 文件 | 說明 |
|------|------|
| `README.md` | 本檔案，專案總體說明 |
| `docs/QUICKSTART.md` | 快速開始指南 |
| `docs/SETUP_GUIDE.md` | Slack 和 Google Sheets 詳細設定步驟 |
| `docs/PROJECT_SUMMARY.md` | 專案完成總結和技術亮點 |
| `docs/SUBMISSION_CHECKLIST.md` | 繳交檢查清單 |
| `tests/README.md` | Jest API 測試詳細說明 |

---

## ⚠️ 注意事項

1. **網頁選擇器**: `LimitationsAndFeesPage.py` 中的選擇器需要根據實際 BitoPro 網頁結構調整
2. **API 端點**: 確認 API 端點 URL 是否正確
3. **憑證安全**: 
   - 不要將 `credentials.json` 和 Slack Token 提交到版本控制
   - 使用 `.env` 檔案管理敏感資訊（已加入 `.gitignore`）
4. **瀏覽器驅動**: 確保已安裝並設定 ChromeDriver
5. **版本鎖定**: 所有依賴版本已鎖定，確保環境一致性

---

## 🐛 疑難排解

### Robot Framework 問題
- **找不到瀏覽器**: 確認已安裝 Chrome 並設定 ChromeDriver
- **頁面元素找不到**: 檢查並更新 `LimitationsAndFeesPage.py` 中的選擇器

### Jest 測試問題
- **API 呼叫失敗**: 確認網路連線和 API 端點是否正確
- **測試超時**: 可在 `jest.config.js` 中調整 `testTimeout`

### 測試後處理問題
- **Slack 通知失敗**: 確認 Token 正確且 Bot 已加入頻道
- **Google Sheets 寫入失敗**: 確認憑證檔案路徑正確且試算表已分享給服務帳戶

---

## 📝 授權

本專案為面試作業專案。

---

## 📞 聯絡資訊

如有問題或建議，歡迎提出 Issue 或 Pull Request。
