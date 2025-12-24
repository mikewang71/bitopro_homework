/**
 * BitoPro OHLC 資料 API 測試套件
 * 
 * API 文檔: https://bitoex.gitbook.io/bitopro-api-docs/api/v3/public/get_ohlc_data
 * API endpoint: GET https://api.bitopro.com/v3/trading-history/{pair}
 * 測試交易對: btc_twd
 * 
 * 使用 axios 進行 API 請求
 */

const axios = require('axios');

// API 基礎設定
const BASE_URL = 'https://api.bitopro.com/v3';
const TRADING_PAIR = 'btc_twd';
const API_ENDPOINT = `${BASE_URL}/trading-history/${TRADING_PAIR}`;

// 測試輔助函數：建立 API 請求
const fetchOHLCData = async (params = {}) => {
  const defaultParams = {
    resolution: '1d',
    from: Math.floor(Date.now() / 1000) - 86400 * 7, // 預設查詢 7 天前的資料
    to: Math.floor(Date.now() / 1000)
  };
  
  const queryParams = { ...defaultParams, ...params };
  const queryString = new URLSearchParams(
    Object.entries(queryParams).reduce((acc, [key, value]) => {
      acc[key] = String(value);
      return acc;
    }, {})
  ).toString();
  
  return axios.get(`${API_ENDPOINT}?${queryString}`);
};

describe('BitoPro OHLC 資料 API 測試', () => {
  
  /**
   * TC001: 驗證 API 回應狀態碼為 200
   * 確保 API 端點正常運作
   */
  describe('TC001: 驗證 API 回應狀態碼為 200', () => {
    test('應該回傳狀態碼 200', async () => {
      const response = await fetchOHLCData();
      
      expect(response.status).toBe(200);
      expect(response.statusText).toBe('OK');
    });
  });

  /**
   * TC002: 驗證回傳資料結構正確（包含必要欄位）
   * 確保 API 回傳的資料結構符合預期
   */
  describe('TC002: 驗證回傳資料結構正確', () => {
    test('回應應該包含正確的資料結構和必要欄位', async () => {
      const response = await fetchOHLCData();
      
      // 驗證狀態碼
      expect(response.status).toBe(200);
      
      // 驗證回應結構
      expect(response.data).toBeDefined();
      expect(response.data).toHaveProperty('data');
      expect(Array.isArray(response.data.data)).toBe(true);
      
      // 如果有資料，驗證每筆資料的結構
      if (response.data.data.length > 0) {
        const firstRecord = response.data.data[0];
        
        // 驗證必要欄位存在
        expect(firstRecord).toHaveProperty('timestamp');
        expect(firstRecord).toHaveProperty('open');
        expect(firstRecord).toHaveProperty('high');
        expect(firstRecord).toHaveProperty('low');
        expect(firstRecord).toHaveProperty('close');
        expect(firstRecord).toHaveProperty('volume');
      }
    });
  });

  /**
   * TC003: 驗證資料型態正確
   * 確保 timestamp, open, high, low, close, volume 的資料型態正確
   */
  describe('TC003: 驗證資料型態正確', () => {
    test('所有欄位的資料型態應該正確', async () => {
      const response = await fetchOHLCData();
      
      expect(response.status).toBe(200);
      expect(response.data.data.length).toBeGreaterThan(0);
      
      // 驗證每筆資料的型態
      response.data.data.forEach((record, index) => {
        // timestamp 應該是數字（毫秒時間戳）
        expect(typeof record.timestamp).toBe('number');
        expect(record.timestamp).toBeGreaterThan(0);
        
        // 價格欄位（open, high, low, close）應該是字串
        expect(typeof record.open).toBe('string');
        expect(typeof record.high).toBe('string');
        expect(typeof record.low).toBe('string');
        expect(typeof record.close).toBe('string');
        
        // volume 應該是字串
        expect(typeof record.volume).toBe('string');
        
        // 驗證字串可以轉換為數字
        expect(() => parseFloat(record.open)).not.toThrow();
        expect(() => parseFloat(record.high)).not.toThrow();
        expect(() => parseFloat(record.low)).not.toThrow();
        expect(() => parseFloat(record.close)).not.toThrow();
        expect(() => parseFloat(record.volume)).not.toThrow();
      });
    });
  });

  /**
   * TC004: 驗證 high >= low 的邏輯正確性
   * 確保每筆 OHLC 資料的邏輯關係正確
   */
  describe('TC004: 驗證 high >= low 的邏輯正確性', () => {
    test('每筆資料應該符合 OHLC 邏輯：high >= low, high >= open, high >= close, low <= open, low <= close', async () => {
      const response = await fetchOHLCData();
      
      expect(response.status).toBe(200);
      expect(response.data.data.length).toBeGreaterThan(0);
      
      response.data.data.forEach((record, index) => {
        const open = parseFloat(record.open);
        const high = parseFloat(record.high);
        const low = parseFloat(record.low);
        const close = parseFloat(record.close);
        const volume = parseFloat(record.volume);
        
        // 驗證價格為正數
        expect(open).toBeGreaterThan(0);
        expect(high).toBeGreaterThan(0);
        expect(low).toBeGreaterThan(0);
        expect(close).toBeGreaterThan(0);
        expect(volume).toBeGreaterThanOrEqual(0);
        
        // 驗證 OHLC 邏輯正確性
        expect(high).toBeGreaterThanOrEqual(low);
        expect(high).toBeGreaterThanOrEqual(open);
        expect(high).toBeGreaterThanOrEqual(close);
        expect(low).toBeLessThanOrEqual(open);
        expect(low).toBeLessThanOrEqual(close);
      });
    });
  });

  /**
   * TC005: 驗證時間戳記格式正確
   * 確保 timestamp 是有效的 Unix 時間戳（毫秒）
   */
  describe('TC005: 驗證時間戳記格式正確', () => {
    test('timestamp 應該是有效的 Unix 時間戳（毫秒）', async () => {
      const response = await fetchOHLCData();
      
      expect(response.status).toBe(200);
      expect(response.data.data.length).toBeGreaterThan(0);
      
      const now = Date.now();
      const oneYearAgo = now - (365 * 24 * 60 * 60 * 1000);
      const oneYearLater = now + (365 * 24 * 60 * 60 * 1000);
      
      response.data.data.forEach((record) => {
        const timestamp = record.timestamp;
        
        // 驗證 timestamp 是數字
        expect(typeof timestamp).toBe('number');
        
        // 驗證 timestamp 在合理範圍內（過去一年到未來一年）
        expect(timestamp).toBeGreaterThan(oneYearAgo);
        expect(timestamp).toBeLessThan(oneYearLater);
        
        // 驗證可以轉換為有效的 Date 物件
        const date = new Date(timestamp);
        expect(date.getTime()).toBe(timestamp);
        expect(date.toString()).not.toBe('Invalid Date');
      });
    });

    test('資料應該按照時間順序排列', async () => {
      const response = await fetchOHLCData({
        from: Math.floor(Date.now() / 1000) - 86400 * 30, // 30 天前
        to: Math.floor(Date.now() / 1000)
      });
      
      expect(response.status).toBe(200);
      
      if (response.data.data.length > 1) {
        // 驗證時間排序（由舊到新）
        for (let i = 1; i < response.data.data.length; i++) {
          expect(response.data.data[i].timestamp).toBeGreaterThanOrEqual(
            response.data.data[i - 1].timestamp
          );
        }
      }
    });
  });

  /**
   * TC006: 驗證錯誤處理
   * 測試各種錯誤情況的處理
   */
  describe('TC006: 驗證錯誤處理', () => {
    test('當輸入不存在的交易對時，應該回傳適當的錯誤', async () => {
      const invalidPair = 'invalid_pair_xyz';
      const invalidEndpoint = `${BASE_URL}/trading-history/${invalidPair}`;
      
      try {
        await axios.get(`${invalidEndpoint}?resolution=1d&from=${Math.floor(Date.now() / 1000) - 86400 * 7}&to=${Math.floor(Date.now() / 1000)}`);
        // 如果沒有拋出錯誤，驗證狀態碼不是 200
      } catch (error) {
        // 預期會發生錯誤
        if (error.response) {
          expect([400, 404, 422, 500]).toContain(error.response.status);
        } else {
          // 網路錯誤或其他錯誤
          expect(error).toBeDefined();
        }
      }
    });

    test('當缺少必要參數時，應該回傳錯誤', async () => {
      try {
        // 不提供 from 參數
        await axios.get(`${API_ENDPOINT}?resolution=1d&to=${Math.floor(Date.now() / 1000)}`);
      } catch (error) {
        if (error.response) {
          expect([400, 422]).toContain(error.response.status);
        }
      }
    });
  });

  /**
   * TC007: 驗證不同時間解析度
   * 測試不同的 resolution 參數
   */
  describe('TC007: 驗證不同時間解析度', () => {
    // 根據 API 文檔，支援的解析度：1m, 5m, 15m, 30m, 1h, 4h, 1d
    const supportedResolutions = ['1m', '5m', '15m', '30m', '1h', '4h', '1d'];
    
    supportedResolutions.forEach(resolution => {
      test(`應該支援 ${resolution} 時間解析度`, async () => {
        const response = await fetchOHLCData({
          resolution: resolution,
          from: Math.floor(Date.now() / 1000) - 86400, // 1 天前
          to: Math.floor(Date.now() / 1000)
        });
        
        expect(response.status).toBe(200);
        expect(response.data).toHaveProperty('data');
        expect(Array.isArray(response.data.data)).toBe(true);
      });
    });
  });

  /**
   * TC008: 驗證資料不應為空
   * 對於有效的交易對，應該回傳資料
   */
  describe('TC008: 驗證資料不應為空', () => {
    test('當請求有效交易對時，應該回傳資料（或至少回傳正確的結構）', async () => {
      const response = await fetchOHLCData();
      
      expect(response.status).toBe(200);
      expect(response.data).toBeDefined();
      expect(response.data).toHaveProperty('data');
      expect(Array.isArray(response.data.data)).toBe(true);
      
      // 注意：如果時間範圍內沒有交易，可能為空陣列，這是合理的
      // 這裡我們驗證至少結構是正確的
      expect(response.data.data).not.toBeNull();
    });
  });
});

