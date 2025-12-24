module.exports = {
  // 測試環境
  testEnvironment: 'node',
  
  // 詳細輸出
  verbose: true,
  
  // 收集測試覆蓋率
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json'],
  
  // 測試檔案匹配模式
  testMatch: [
    '**/tests/**/*.test.js',
    '**/__tests__/**/*.js'
  ],
  
  // 測試超時時間（毫秒）
  testTimeout: 15000,
  
  // 覆蓋率閾值（可選）
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  }
};

