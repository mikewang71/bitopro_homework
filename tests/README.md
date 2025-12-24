# BitoPro OHLC 資料 API 測試

本專案使用 Jest + JavaScript (axios) 測試 BitoPro 的 OHLC 資料 API。

## API 資訊

- **API 文檔**: https://bitoex.gitbook.io/bitopro-api-docs/api/v3/public/get_ohlc_data
- **API Endpoint**: `GET https://api.bitopro.com/v3/trading-history/{pair}`
- **測試交易對**: `btc_twd`

## 專案結構

```
bitopro_homework/
├── tests/
│   ├── ohlc.test.js          # OHLC API 測試用例
│   └── README.md             # 本檔案
├── package.json              # 專案依賴和腳本
├── jest.config.js           # Jest 配置
└── coverage/                # 測試覆蓋率報告（執行後產生）
```

## 安裝依賴

```bash
npm install
```

## 執行測試

### 基本執行

```bash
# 執行所有測試
npm test

# 監聽模式（自動重新執行測試）
npm run test:watch
```

### 產生測試覆蓋率報告

```bash
# 產生覆蓋率報告（文字、HTML、JSON）
npm run test:coverage

# 詳細輸出模式
npm run test:verbose
```

### 查看覆蓋率報告

執行 `npm run test:coverage` 後，可以查看：

- **文字報告**: 在終端機中直接顯示
- **HTML 報告**: 開啟 `coverage/lcov-report/index.html`
- **JSON 報告**: `coverage/coverage-final.json`

```bash
# 在瀏覽器中開啟 HTML 報告（macOS）
open coverage/lcov-report/index.html

# 在瀏覽器中開啟 HTML 報告（Linux）
xdg-open coverage/lcov-report/index.html

# 在瀏覽器中開啟 HTML 報告（Windows）
start coverage/lcov-report/index.html
```

## 測試用例說明

### TC001: 驗證 API 回應狀態碼為 200
- 確保 API 端點正常運作
- 驗證 HTTP 狀態碼為 200

### TC002: 驗證回傳資料結構正確
- 驗證回應包含 `data` 欄位
- 驗證 `data` 是陣列
- 驗證每筆資料包含必要欄位：`timestamp`, `open`, `high`, `low`, `close`, `volume`

### TC003: 驗證資料型態正確
- 驗證 `timestamp` 是數字（毫秒時間戳）
- 驗證價格欄位（`open`, `high`, `low`, `close`）是字串
- 驗證 `volume` 是字串
- 驗證所有字串欄位可以轉換為數字

### TC004: 驗證 high >= low 的邏輯正確性
- 驗證所有價格為正數
- 驗證 `high >= low`
- 驗證 `high >= open` 且 `high >= close`
- 驗證 `low <= open` 且 `low <= close`
- 驗證 `volume >= 0`

### TC005: 驗證時間戳記格式正確
- 驗證 `timestamp` 是有效的 Unix 時間戳（毫秒）
- 驗證時間戳在合理範圍內
- 驗證可以轉換為有效的 Date 物件
- 驗證資料按時間順序排列

### TC006: 驗證錯誤處理
- 測試不存在的交易對
- 測試缺少必要參數的情況

### TC007: 驗證不同時間解析度
- 測試多種 `resolution` 參數：`1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `1d`

### TC008: 驗證資料不應為空
- 對於有效的交易對，應該回傳正確的資料結構

## API 請求參數

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `resolution` | string | 是 | 時間解析度：`1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `1d` |
| `from` | number | 是 | 開始時間（Unix 時間戳，秒） |
| `to` | number | 是 | 結束時間（Unix 時間戳，秒） |

## API 回應格式

```json
{
  "data": [
    {
      "timestamp": 1765497600000,
      "open": "2889598",
      "high": "2899583",
      "low": "2804953",
      "close": "2827454",
      "volume": "4.95152233"
    }
  ]
}
```

## 技術細節

### 使用的技術
- **Jest**: JavaScript 測試框架
- **axios**: HTTP 客戶端庫
- **Node.js**: 執行環境

### 測試覆蓋率目標
- Branches: 70%
- Functions: 70%
- Lines: 70%
- Statements: 70%

## 疑難排解

### 測試失敗：網路連線問題
- 確認網路連線正常
- 確認 API 端點可訪問

### 測試失敗：API 回應 404
- 確認交易對名稱正確（例如：`btc_twd`）
- 確認 API 端點路徑正確

### 測試超時
- 預設超時時間為 15 秒
- 可以在 `jest.config.js` 中調整 `testTimeout`

## 注意事項

1. 測試會實際呼叫 BitoPro API，請注意 API 使用限制
2. 如果時間範圍內沒有交易資料，`data` 陣列可能為空，這是正常情況
3. 所有價格和成交量欄位都是字串格式，需要轉換為數字進行數值比較

## 授權

本專案為面試作業專案。

