#!/usr/bin/env python3
# test_google_sheets.py
"""
測試 Google Sheets 連線和基本功能
"""

import os
import json
from dotenv import load_dotenv
from google_sheets_storage import get_google_sheets_storage

def test_google_sheets_connection():
    """測試 Google Sheets 連線"""
    print("🔗 測試 Google Sheets 連線...")
    print("=" * 50)
    
    # 載入環境變數
    load_dotenv()
    
    # 檢查環境變數
    google_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    sheet_name = os.getenv("GOOGLE_SHEET_NAME", "food_agent_ingredients")
    worksheet_name = os.getenv("GOOGLE_WORKSHEET_NAME", "ingredients")
    
    print(f"📋 試算表名稱: {sheet_name}")
    print(f"📄 工作表名稱: {worksheet_name}")
    
    if not google_json:
        print("❌ 未設定 GOOGLE_SERVICE_ACCOUNT_JSON 環境變數")
        return False
    
    try:
        # 測試 JSON 解析
        credentials_dict = json.loads(google_json)
        print("✅ 服務帳戶 JSON 解析成功")
        print(f"📧 服務帳戶郵箱: {credentials_dict.get('client_email', 'N/A')}")
        print(f"🏗️ 專案 ID: {credentials_dict.get('project_id', 'N/A')}")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 環境變數檢查失敗: {e}")
        return False
    
    return True

def test_google_sheets_operations():
    """測試 Google Sheets 操作"""
    print("\n🧪 測試 Google Sheets 操作...")
    print("=" * 50)
    
    try:
        # 獲取儲存實例
        storage = get_google_sheets_storage()
        
        # 測試 1: 獲取食材列表
        print("📋 測試 1: 獲取食材列表")
        result = storage.get_ingredient_list()
        print(f"結果: {result[:100]}...")
        
        # 測試 2: 添加測試食材
        print("\n➕ 測試 2: 添加測試食材")
        test_result = storage.add_ingredient(
            name="測試蘋果",
            quantity=3,
            unit="個",
            expires_at="2025-09-20",
            location="冷藏",
            notes="Google Sheets 連線測試"
        )
        print(f"結果: {test_result}")
        
        # 測試 3: 再次獲取列表（應該包含新添加的食材）
        print("\n📋 測試 3: 再次獲取食材列表")
        result = storage.get_ingredient_list()
        print(f"結果: {result[:200]}...")
        
        # 測試 4: 檢查過期食材
        print("\n⚠️ 測試 4: 檢查過期食材")
        expiring_result = storage.check_expiring_ingredients()
        print(f"結果: {expiring_result}")
        
        print("\n✅ 所有測試完成！")
        return True
        
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主測試函數"""
    print("🤖 Google Sheets 連線測試")
    print("=" * 60)
    
    # 測試 1: 環境變數和連線
    if not test_google_sheets_connection():
        print("\n❌ 連線測試失敗，請檢查設定")
        return
    
    # 測試 2: 實際操作
    if test_google_sheets_operations():
        print("\n🎉 Google Sheets 整合測試成功！")
        print("\n📝 下一步:")
        print("1. 前往 Google Sheets 查看你的試算表")
        print("2. 確認資料已正確寫入")
        print("3. 測試 AI Agent 的完整功能")
    else:
        print("\n❌ 操作測試失敗，請檢查權限設定")

if __name__ == "__main__":
    main()
