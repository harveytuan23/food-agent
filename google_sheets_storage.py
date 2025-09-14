# google_sheets_storage.py
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)

class GoogleSheetsStorage:
    """Google Sheets 資料儲存類別"""
    
    def __init__(self):
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "food_agent_ingredients")
        self.worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME", "ingredients")
        self.client = None
        self.worksheet = None
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化 Google Sheets 客戶端"""
        try:
            # 從環境變數讀取服務帳戶憑證
            credentials_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
            if not credentials_json:
                logger.error("❌ 未設定 GOOGLE_SERVICE_ACCOUNT_JSON 環境變數")
                return
            
            # 解析 JSON 憑證
            import json
            credentials_dict = json.loads(credentials_json)
            
            # 設定權限範圍
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # 創建憑證
            credentials = Credentials.from_service_account_info(
                credentials_dict, scopes=scopes
            )
            
            # 初始化客戶端
            self.client = gspread.authorize(credentials)
            
            # 開啟或創建試算表
            try:
                self.worksheet = self.client.open(self.sheet_name).worksheet(self.worksheet_name)
                logger.info(f"✅ 成功連接到 Google Sheets: {self.sheet_name}")
            except gspread.SpreadsheetNotFound:
                # 如果試算表不存在，創建新的
                spreadsheet = self.client.create(self.sheet_name)
                self.worksheet = spreadsheet.add_worksheet(title=self.worksheet_name, rows=1000, cols=10)
                self._setup_headers()
                logger.info(f"✅ 創建新的 Google Sheets: {self.sheet_name}")
            
        except Exception as e:
            logger.error(f"❌ Google Sheets 初始化失敗: {str(e)}")
            self.client = None
            self.worksheet = None
    
    def _setup_headers(self):
        """設定試算表標題行"""
        if self.worksheet:
            headers = ["ID", "名稱", "數量", "單位", "到期日", "存放位置", "備註", "創建時間", "更新時間"]
            self.worksheet.append_row(headers)
            logger.info("📋 已設定試算表標題行")
    
    def _get_next_id(self) -> int:
        """獲取下一個 ID"""
        if not self.worksheet:
            return 1
        
        try:
            # 獲取所有記錄
            records = self.worksheet.get_all_records()
            if not records:
                return 1
            
            # 找到最大的 ID
            max_id = max(int(record.get('ID', 0)) for record in records)
            return max_id + 1
        except Exception as e:
            logger.error(f"❌ 獲取 ID 失敗: {str(e)}")
            return 1
    
    def add_ingredient(self, name: str, quantity: float = 1, unit: str = None, 
                      expires_at: str = None, location: str = None, notes: str = None) -> str:
        """添加食材到 Google Sheets"""
        if not self.worksheet:
            return "❌ Google Sheets 未初始化"
        
        try:
            # 獲取下一個 ID
            ingredient_id = self._get_next_id()
            
            # 準備資料
            current_time = date.today().isoformat()
            row_data = [
                ingredient_id,
                name,
                quantity,
                unit or "",
                expires_at or "",
                location or "",
                notes or "",
                current_time,
                current_time
            ]
            
            # 添加到試算表
            self.worksheet.append_row(row_data)
            
            logger.info(f"✅ 已添加食材到 Google Sheets: {name}")
            return f"✅ 已添加食材: {name} {quantity}{unit or ''} (ID: {ingredient_id})"
            
        except Exception as e:
            error_msg = f"❌ 添加食材失敗: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def get_ingredient_list(self) -> str:
        """從 Google Sheets 獲取食材列表"""
        if not self.worksheet:
            return "❌ Google Sheets 未初始化"
        
        try:
            # 獲取所有記錄，指定預期的標題
            expected_headers = ["ID", "名稱", "數量", "單位", "到期日", "存放位置", "備註", "創建時間", "更新時間"]
            records = self.worksheet.get_all_records(expected_headers=expected_headers)
            
            if not records:
                return "📦 目前沒有食材庫存"
            
            result = "📦 食材庫存列表:\n"
            for i, record in enumerate(records, 1):
                name = record.get('名稱', '')
                quantity = record.get('數量', '')
                unit = record.get('單位', '')
                expires_at = record.get('到期日', '')
                location = record.get('存放位置', '')
                
                result += f"{i}. {name} {quantity}{unit} (到期: {expires_at}, 存放: {location})\n"
            
            logger.info(f"✅ 從 Google Sheets 獲取 {len(records)} 筆食材記錄")
            return result
            
        except Exception as e:
            error_msg = f"❌ 獲取食材列表失敗: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def check_expiring_ingredients(self, days: int = 3) -> str:
        """檢查即將過期的食材"""
        if not self.worksheet:
            return "❌ Google Sheets 未初始化"
        
        try:
            expected_headers = ["ID", "名稱", "數量", "單位", "到期日", "存放位置", "備註", "創建時間", "更新時間"]
            records = self.worksheet.get_all_records(expected_headers=expected_headers)
            today = date.today()
            expiring_soon = []
            
            for record in records:
                expires_at_str = record.get('到期日', '')
                if expires_at_str:
                    try:
                        expires_date = date.fromisoformat(expires_at_str)
                        days_left = (expires_date - today).days
                        if days_left <= days:
                            expiring_soon.append((record, days_left))
                    except ValueError:
                        continue
            
            if not expiring_soon:
                return "✅ 沒有即將過期的食材"
            
            result = f"⚠️ 即將過期的食材 (未來{days}天內):\n"
            for record, days_left in expiring_soon:
                name = record.get('名稱', '')
                result += f"- {name} 還有 {days_left} 天到期\n"
            
            logger.info(f"✅ 檢查到 {len(expiring_soon)} 項即將過期的食材")
            return result
            
        except Exception as e:
            error_msg = f"❌ 檢查過期食材失敗: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def delete_ingredient(self, ingredient_id: int) -> str:
        """刪除食材"""
        if not self.worksheet:
            return "❌ Google Sheets 未初始化"
        
        try:
            records = self.worksheet.get_all_records()
            
            # 找到要刪除的記錄
            for i, record in enumerate(records, 2):  # 從第2行開始（第1行是標題）
                if int(record.get('ID', 0)) == ingredient_id:
                    self.worksheet.delete_rows(i)
                    logger.info(f"✅ 已刪除食材 ID: {ingredient_id}")
                    return f"✅ 已刪除食材 ID: {ingredient_id}"
            
            return f"❌ 找不到 ID 為 {ingredient_id} 的食材"
            
        except Exception as e:
            error_msg = f"❌ 刪除食材失敗: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def update_ingredient(self, ingredient_id: int, **kwargs) -> str:
        """更新食材資訊"""
        if not self.worksheet:
            return "❌ Google Sheets 未初始化"
        
        try:
            records = self.worksheet.get_all_records()
            
            # 找到要更新的記錄
            for i, record in enumerate(records, 2):
                if int(record.get('ID', 0)) == ingredient_id:
                    # 更新欄位
                    if 'name' in kwargs:
                        self.worksheet.update_cell(i, 2, kwargs['name'])  # 名稱
                    if 'quantity' in kwargs:
                        self.worksheet.update_cell(i, 3, kwargs['quantity'])  # 數量
                    if 'unit' in kwargs:
                        self.worksheet.update_cell(i, 4, kwargs['unit'])  # 單位
                    if 'expires_at' in kwargs:
                        self.worksheet.update_cell(i, 5, kwargs['expires_at'])  # 到期日
                    if 'location' in kwargs:
                        self.worksheet.update_cell(i, 6, kwargs['location'])  # 存放位置
                    if 'notes' in kwargs:
                        self.worksheet.update_cell(i, 7, kwargs['notes'])  # 備註
                    
                    # 更新時間
                    self.worksheet.update_cell(i, 9, date.today().isoformat())  # 更新時間
                    
                    logger.info(f"✅ 已更新食材 ID: {ingredient_id}")
                    return f"✅ 已更新食材 ID: {ingredient_id}"
            
            return f"❌ 找不到 ID 為 {ingredient_id} 的食材"
            
        except Exception as e:
            error_msg = f"❌ 更新食材失敗: {str(e)}"
            logger.error(error_msg)
            return error_msg

# 創建全局實例（延遲初始化）
google_sheets_storage = None

def get_google_sheets_storage():
    """獲取 Google Sheets 儲存實例（延遲初始化）"""
    global google_sheets_storage
    if google_sheets_storage is None:
        google_sheets_storage = GoogleSheetsStorage()
    return google_sheets_storage
