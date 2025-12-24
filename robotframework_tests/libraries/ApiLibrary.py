"""
API Library for BitoPro
封裝 public/get_limitations_and_fees API 呼叫的 Python 關鍵字
"""
import requests
import json
from typing import Dict, Any, Optional


class ApiLibrary:
    """
    BitoPro API Library
    提供 API 呼叫的關鍵字方法
    """
    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    
    def __init__(self, base_url: str = "https://api.bitopro.com/v3"):
        """
        初始化 API Library
        
        Args:
            base_url: BitoPro API 基礎 URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.last_response = None
    
    def get_limitations_and_fees(self) -> Dict[str, Any]:
        """
        呼叫 public/get_limitations_and_fees API
        
        Returns:
            API 回應的 JSON 資料
        """
        endpoint = f"{self.base_url}/public/get_limitations_and_fees"
        try:
            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()
            self.last_response = response
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 呼叫失敗: {str(e)}")
    
    def get_api_response_status_code(self) -> int:
        """
        取得最後一次 API 呼叫的狀態碼
        
        Returns:
            狀態碼
        """
        if self.last_response is None:
            raise Exception("尚未執行 API 呼叫")
        return self.last_response.status_code
    
    def get_api_data_by_key(self, key: str) -> Any:
        """
        從 API 回應中取得指定 key 的資料
        
        Args:
            key: 要取得的資料 key (支援巢狀路徑，例如 "data.fees.deposit")
        
        Returns:
            對應的資料值
        """
        if self.last_response is None:
            raise Exception("尚未執行 API 呼叫")
        
        data = self.last_response.json()
        keys = key.split('.')
        
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                raise KeyError(f"找不到 key: {key}")
        
        return data
    
    def verify_api_response_structure(self, expected_keys: list) -> bool:
        """
        驗證 API 回應結構是否包含預期的 keys
        
        Args:
            expected_keys: 預期的 key 列表
        
        Returns:
            驗證是否通過
        """
        if self.last_response is None:
            raise Exception("尚未執行 API 呼叫")
        
        data = self.last_response.json()
        
        def check_keys(obj: dict, keys: list) -> bool:
            for key in keys:
                if '.' in key:
                    # 處理巢狀 key
                    parts = key.split('.')
                    current = obj
                    for part in parts:
                        if isinstance(current, dict) and part in current:
                            current = current[part]
                        else:
                            return False
                else:
                    if key not in obj:
                        return False
            return True
        
        return check_keys(data, expected_keys)

