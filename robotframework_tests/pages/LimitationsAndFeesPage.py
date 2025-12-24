"""
Page Object Model for Limitations and Fees Page
使用 Page Object Pattern 封裝網頁元素與操作
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Dict, Any, Optional


class LimitationsAndFeesPage:
    """
    限制與費用頁面的 Page Object
    """
    
    def __init__(self, driver):
        """
        初始化頁面物件
        
        Args:
            driver: Selenium WebDriver 實例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def navigate_to_page(self, url: str = "https://www.bitopro.com/limitations-and-fees"):
        """
        導航到限制與費用頁面
        
        Args:
            url: 頁面 URL
        """
        self.driver.get(url)
        self.wait_for_page_load()
    
    def wait_for_page_load(self, timeout: int = 10):
        """
        等待頁面載入完成
        
        Args:
            timeout: 等待超時時間（秒）
        """
        try:
            # 等待頁面主要內容載入
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            raise Exception("頁面載入超時")
    
    def get_fee_data_from_page(self) -> Dict[str, Any]:
        """
        從網頁上提取費用資料
        
        Returns:
            包含費用資料的字典
        """
        fee_data = {}
        
        try:
            # 這裡需要根據實際網頁結構調整選擇器
            # 以下是範例，實際使用時需要根據 BitoPro 網頁結構調整
            
            # 範例：提取存款手續費
            # deposit_fee_element = self.driver.find_element(By.XPATH, "//div[@class='deposit-fee']")
            # fee_data['deposit'] = deposit_fee_element.text
            
            # 範例：提取提款手續費
            # withdrawal_fee_element = self.driver.find_element(By.XPATH, "//div[@class='withdrawal-fee']")
            # fee_data['withdrawal'] = withdrawal_fee_element.text
            
            # 範例：提取交易手續費
            # trading_fee_element = self.driver.find_element(By.XPATH, "//div[@class='trading-fee']")
            # fee_data['trading'] = trading_fee_element.text
            
            # 注意：實際實作時需要根據 BitoPro 網頁的實際 HTML 結構調整選擇器
            # 這裡提供一個通用的方法框架
            
            fee_data = {
                'deposit': self._extract_text_by_selector("deposit-fee-selector"),
                'withdrawal': self._extract_text_by_selector("withdrawal-fee-selector"),
                'trading': self._extract_text_by_selector("trading-fee-selector"),
            }
            
        except NoSuchElementException as e:
            raise Exception(f"無法找到頁面元素: {str(e)}")
        
        return fee_data
    
    def _extract_text_by_selector(self, selector_type: str) -> str:
        """
        根據選擇器類型提取文字（需要根據實際網頁調整）
        
        Args:
            selector_type: 選擇器類型
        
        Returns:
            提取的文字內容
        """
        # 這裡需要根據實際網頁結構實作
        # 以下是範例實作
        try:
            # 實際使用時需要替換為真實的選擇器
            element = self.driver.find_element(By.CLASS_NAME, selector_type)
            return element.text.strip()
        except NoSuchElementException:
            return ""
    
    def get_limit_data_from_page(self) -> Dict[str, Any]:
        """
        從網頁上提取限制資料
        
        Returns:
            包含限制資料的字典
        """
        limit_data = {}
        
        try:
            # 根據實際網頁結構提取限制資料
            # 範例：提取最小存款金額
            # min_deposit_element = self.driver.find_element(By.XPATH, "//div[@class='min-deposit']")
            # limit_data['min_deposit'] = min_deposit_element.text
            
            limit_data = {
                'min_deposit': self._extract_text_by_selector("min-deposit-selector"),
                'max_withdrawal': self._extract_text_by_selector("max-withdrawal-selector"),
            }
            
        except NoSuchElementException as e:
            raise Exception(f"無法找到頁面元素: {str(e)}")
        
        return limit_data
    
    def get_currency_unit(self) -> str:
        """
        從網頁上提取貨幣單位
        
        Returns:
            貨幣單位（例如：TWD, USD）
        """
        try:
            # 根據實際網頁結構提取貨幣單位
            # 範例：從頁面標題或特定元素提取
            currency_element = self.driver.find_element(By.XPATH, "//span[@class='currency-unit']")
            return currency_element.text.strip()
        except NoSuchElementException:
            # 如果找不到，返回預設值或從 URL 判斷
            return "TWD"
    
    def is_page_loaded(self) -> bool:
        """
        檢查頁面是否已載入
        
        Returns:
            頁面是否已載入
        """
        try:
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            return True
        except TimeoutException:
            return False

