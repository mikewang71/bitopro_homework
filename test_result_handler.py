#!/usr/bin/env python3
"""
測試結果處理腳本
功能：
1. 解析測試結果（Robot Framework 和 Jest）
2. 發送 Slack 通知
3. 將測試結果寫入 Google Sheets
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any, Optional
import argparse

# Slack SDK
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Google Sheets API
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class TestResultHandler:
    """測試結果處理器"""
    
    def __init__(self, slack_token: Optional[str] = None, 
                 google_credentials_path: Optional[str] = None,
                 google_sheet_id: Optional[str] = None):
        """
        初始化測試結果處理器
        
        Args:
            slack_token: Slack Bot Token (格式: xoxb-...)
            google_credentials_path: Google Service Account 憑證檔案路徑
            google_sheet_id: Google Sheets 試算表 ID
        """
        self.slack_token = slack_token or os.getenv('SLACK_BOT_TOKEN')
        self.google_credentials_path = google_credentials_path or os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
        self.google_sheet_id = google_sheet_id or os.getenv('GOOGLE_SHEET_ID')
        
        self.slack_client = None
        self.gc = None
        
        # 初始化 Slack 客戶端
        if self.slack_token:
            self.slack_client = WebClient(token=self.slack_token)
        
        # 初始化 Google Sheets 客戶端
        if os.path.exists(self.google_credentials_path):
            try:
                # 定義權限範圍
                scope = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                # 使用 oauth2client 連接 Google Sheets
                creds = ServiceAccountCredentials.from_json_keyfile_name(
                    self.google_credentials_path, scope
                )
                self.gc = gspread.authorize(creds)
            except Exception as e:
                print(f"警告: 無法初始化 Google Sheets 客戶端: {e}")
    
    def parse_robot_framework_results(self, output_xml_path: str) -> Dict[str, Any]:
        """
        解析 Robot Framework 測試結果
        
        Args:
            output_xml_path: Robot Framework output.xml 檔案路徑
        
        Returns:
            包含測試結果的字典
        """
        if not os.path.exists(output_xml_path):
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'execution_time': 0
            }
        
        try:
            tree = ET.parse(output_xml_path)
            root = tree.getroot()
            
            # 取得統計資訊
            stats = root.find('statistics/total/stat')
            total = int(stats.get('pass', 0)) + int(stats.get('fail', 0))
            passed = int(stats.get('pass', 0))
            failed = int(stats.get('fail', 0))
            
            # 取得執行時間
            suite = root.find('suite')
            execution_time = float(suite.get('elapsed', 0)) if suite is not None else 0
            
            return {
                'total': total,
                'passed': passed,
                'failed': failed,
                'execution_time': execution_time,
                'framework': 'Robot Framework'
            }
        except Exception as e:
            print(f"解析 Robot Framework 結果時發生錯誤: {e}")
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'execution_time': 0,
                'framework': 'Robot Framework'
            }
    
    def parse_jest_results(self, jest_json_path: Optional[str] = None) -> Dict[str, Any]:
        """
        解析 Jest 測試結果 JSON 檔案
        
        Args:
            jest_json_path: Jest 測試結果 JSON 檔案路徑（預設: results/jest-results.json）
        
        Returns:
            包含測試結果的字典
        """
        if jest_json_path is None:
            jest_json_path = 'results/jest-results.json'
        
        if not os.path.exists(jest_json_path):
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'execution_time': 0,
                'framework': 'Jest'
            }
        
        try:
            with open(jest_json_path, 'r', encoding='utf-8') as f:
                jest_data = json.load(f)
            
            return {
                'total': jest_data.get('numTotalTests', 0),
                'passed': jest_data.get('numPassedTests', 0),
                'failed': jest_data.get('numFailedTests', 0),
                'execution_time': jest_data.get('executionTime', 0),
                'framework': 'Jest'
            }
        except Exception as e:
            print(f"解析 Jest 結果時發生錯誤: {e}")
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'execution_time': 0,
                'framework': 'Jest'
            }
    
    def send_slack_notification(self, channel: str, test_results: Dict[str, Any]) -> bool:
        """
        發送 Slack 通知
        
        Args:
            channel: Slack 頻道名稱或 ID (例如: #testing 或 C1234567890)
            test_results: 測試結果字典
        
        Returns:
            是否成功發送
        """
        if not self.slack_client:
            print("警告: Slack 客戶端未初始化，跳過通知")
            return False
        
        try:
            # 格式化日期
            current_date = datetime.now().strftime('%Y/%m/%d')
            
            # 建立訊息
            total = test_results.get('total', 0)
            passed = test_results.get('passed', 0)
            failed = test_results.get('failed', 0)
            execution_time = test_results.get('execution_time', 0)
            framework = test_results.get('framework', 'Unknown')
            
            # 計算通過率
            pass_rate = (passed / total * 100) if total > 0 else 0
            
            # 建立訊息區塊
            message = f"{current_date} 測試執行完畢\n\n"
            message += f"測試框架: {framework}\n"
            message += f"總測試數: {total}\n"
            message += f"通過: {passed}\n"
            message += f"失敗: {failed}\n"
            message += f"執行時間: {execution_time:.2f} 秒\n"
            message += f"通過率: {pass_rate:.2f}%"
            
            # 決定顏色（根據通過率）
            color = "good" if failed == 0 else "warning" if pass_rate >= 50 else "danger"
            
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
            
            # 發送訊息
            response = self.slack_client.chat_postMessage(
                channel=channel,
                text=f"{current_date} 測試執行完畢",
                blocks=blocks
            )
            
            print(f"Slack 通知已發送到 {channel}")
            return True
            
        except SlackApiError as e:
            print(f"發送 Slack 通知時發生錯誤: {e.response['error']}")
            return False
        except Exception as e:
            print(f"發送 Slack 通知時發生未預期的錯誤: {e}")
            return False
    
    def write_to_google_sheets(self, test_results: Dict[str, Any], 
                               worksheet_name: str = "測試結果") -> bool:
        """
        將測試結果寫入 Google Sheets
        
        Args:
            test_results: 測試結果字典
            worksheet_name: 工作表名稱
        
        Returns:
            是否成功寫入
        """
        if not self.gc:
            print("警告: Google Sheets 客戶端未初始化，跳過寫入")
            return False
        
        if not self.google_sheet_id:
            print("警告: Google Sheet ID 未設定，跳過寫入")
            return False
        
        try:
            # 開啟試算表
            sheet = self.gc.open_by_key(self.google_sheet_id)
            
            # 取得或建立工作表
            try:
                worksheet = sheet.worksheet(worksheet_name)
            except gspread.exceptions.WorksheetNotFound:
                worksheet = sheet.add_worksheet(title=worksheet_name, rows=1000, cols=10)
                # 建立標題列
                worksheet.append_row([
                    '日期', '測試框架', '總測試數', '通過', '失敗', 
                    '執行時間(秒)', '通過率(%)', '時間戳記'
                ])
            
            # 準備資料
            current_date = datetime.now().strftime('%Y/%m/%d')
            total = test_results.get('total', 0)
            passed = test_results.get('passed', 0)
            failed = test_results.get('failed', 0)
            execution_time = test_results.get('execution_time', 0)
            framework = test_results.get('framework', 'Unknown')
            pass_rate = (passed / total * 100) if total > 0 else 0
            timestamp = datetime.now().isoformat()
            
            # 寫入資料
            worksheet.append_row([
                current_date,
                framework,
                total,
                passed,
                failed,
                f"{execution_time:.2f}",
                f"{pass_rate:.2f}",
                timestamp
            ])
            
            print(f"測試結果已寫入 Google Sheets: {worksheet_name}")
            return True
            
        except Exception as e:
            print(f"寫入 Google Sheets 時發生錯誤: {e}")
            return False
    
    def process_results(self, robot_output_xml: Optional[str] = None,
                       jest_json_path: Optional[str] = None,
                       slack_channel: Optional[str] = None,
                       google_sheet_name: str = "測試結果") -> Dict[str, bool]:
        """
        處理測試結果（整合所有功能）
        
        Args:
            robot_output_xml: Robot Framework output.xml 路徑
            jest_json_path: Jest 測試結果 JSON 檔案路徑（可選）
            slack_channel: Slack 頻道名稱
            google_sheet_name: Google Sheets 工作表名稱
        
        Returns:
            處理結果字典
        """
        results = {
            'slack_sent': False,
            'sheets_written': False
        }
        
        # 解析測試結果
        test_results = {}
        
        if robot_output_xml:
            test_results = self.parse_robot_framework_results(robot_output_xml)
        elif jest_json_path:
            test_results = self.parse_jest_results(jest_json_path)
        else:
            # 嘗試自動尋找結果檔案
            if os.path.exists('results/output.xml'):
                test_results = self.parse_robot_framework_results('results/output.xml')
            elif os.path.exists('results/jest-results.json'):
                test_results = self.parse_jest_results('results/jest-results.json')
            else:
                print("警告: 沒有提供測試結果，且無法自動找到結果檔案")
                return results
        
        # 發送 Slack 通知
        if slack_channel:
            results['slack_sent'] = self.send_slack_notification(slack_channel, test_results)
        
        # 寫入 Google Sheets
        results['sheets_written'] = self.write_to_google_sheets(test_results, google_sheet_name)
        
        return results


def main():
    """主程式入口"""
    parser = argparse.ArgumentParser(description='處理測試結果並發送通知')
    parser.add_argument('--robot-output', type=str, help='Robot Framework output.xml 路徑')
    parser.add_argument('--jest-json', type=str, help='Jest 測試結果 JSON 檔案路徑')
    parser.add_argument('--slack-channel', type=str, help='Slack 頻道名稱')
    parser.add_argument('--slack-token', type=str, help='Slack Bot Token')
    parser.add_argument('--google-credentials', type=str, help='Google 憑證檔案路徑')
    parser.add_argument('--google-sheet-id', type=str, help='Google Sheet ID')
    parser.add_argument('--worksheet-name', type=str, default='測試結果', help='工作表名稱')
    
    args = parser.parse_args()
    
    # 建立處理器
    handler = TestResultHandler(
        slack_token=args.slack_token,
        google_credentials_path=args.google_credentials,
        google_sheet_id=args.google_sheet_id
    )
    
    # 處理結果
    results = handler.process_results(
        robot_output_xml=args.robot_output,
        jest_json_path=args.jest_json,
        slack_channel=args.slack_channel,
        google_sheet_name=args.worksheet_name
    )
    
    # 輸出結果
    print("\n處理結果:")
    print(f"  Slack 通知: {'成功' if results['slack_sent'] else '失敗或跳過'}")
    print(f"  Google Sheets: {'成功' if results['sheets_written'] else '失敗或跳過'}")


if __name__ == '__main__':
    main()

