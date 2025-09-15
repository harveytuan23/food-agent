# tools.py
import random
import requests
import logging
from datetime import date, timedelta
from typing import Dict, List, Any
from langchain.tools import Tool
from pydantic import BaseModel, Field

from google_sheets_storage import get_google_sheets_storage

logger = logging.getLogger(__name__)

# ==================== 食材管理工具 ====================

class IngredientInfo(BaseModel):
    name: str = Field(..., description="食材名稱")
    quantity: float | None = Field(1, description="數量")
    unit: str | None = Field(None, description="單位")
    expires_at: str | None = Field(None, description="到期日 YYYY-MM-DD")
    location: str | None = Field(None, description="冷藏/冷凍/室溫")
    notes: str | None = Field(None, description="其他備註")

def parse_ingredient_from_text(text: str) -> str:
    """從用戶輸入解析食材資訊"""
    # 這裡可以整合之前的 LangChain 解析邏輯
    # 暫時返回模擬數據
    return f"解析食材資訊: {text}"

# 模擬食材庫存
ingredient_storage = [
    {"name": "牛奶", "quantity": 500, "unit": "ml", "expires_at": "2025-09-15", "location": "冷藏"},
    {"name": "雞蛋", "quantity": 12, "unit": "顆", "expires_at": "2025-09-20", "location": "冷藏"},
    {"name": "麵包", "quantity": 1, "unit": "條", "expires_at": "2025-09-16", "location": "室溫"},
]

def add_ingredient(ingredient_info: str) -> str:
    """添加食材到庫存，格式: 名稱,數量,單位,到期日,存放位置"""
    try:
        parts = ingredient_info.split(',')
        if len(parts) < 1:
            return "❌ 請提供食材名稱"
        
        name = parts[0].strip()
        quantity = float(parts[1].strip()) if len(parts) > 1 and parts[1].strip() else 1
        unit = parts[2].strip() if len(parts) > 2 and parts[2].strip() else None
        expires_at = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None
        location = parts[4].strip() if len(parts) > 4 and parts[4].strip() else None
        
        # 使用 Google Sheets 儲存
        logger.info(f"🔄 正在添加食材到 Google Sheets: {name}")
        storage = get_google_sheets_storage()
        result = storage.add_ingredient(
            name=name,
            quantity=quantity,
            unit=unit,
            expires_at=expires_at,
            location=location
        )
        
        # 同時更新本地記憶體（作為快取）
        new_ingredient = {
            "name": name,
            "quantity": quantity,
            "unit": unit,
            "expires_at": expires_at,
            "location": location
        }
        ingredient_storage.append(new_ingredient)
        
        return result
    except Exception as e:
        logger.error(f"❌ 添加食材失敗: {str(e)}")
        return f"❌ 添加食材失敗: {str(e)}"

def get_ingredient_list(query: str = "") -> str:
    """獲取食材庫存列表"""
    try:
        # 優先從 Google Sheets 獲取
        logger.info("🔄 正在從 Google Sheets 獲取食材列表")
        storage = get_google_sheets_storage()
        result = storage.get_ingredient_list()
        return result
    except Exception as e:
        logger.error(f"❌ 從 Google Sheets 獲取失敗，使用本地快取: {str(e)}")
        # 如果 Google Sheets 失敗，使用本地快取
        if not ingredient_storage:
            return "📦 目前沒有食材庫存"
        
        result = "📦 食材庫存列表 (本地快取):\n"
        for i, item in enumerate(ingredient_storage, 1):
            result += f"{i}. {item['name']} {item['quantity']}{item['unit'] or ''} (到期: {item['expires_at']}, 存放: {item['location']})\n"
        return result

def check_expiring_ingredients(query: str = "") -> str:
    """檢查即將過期的食材"""
    try:
        # 優先從 Google Sheets 檢查
        logger.info("🔄 正在從 Google Sheets 檢查過期食材")
        storage = get_google_sheets_storage()
        result = storage.check_expiring_ingredients()
        return result
    except Exception as e:
        logger.error(f"❌ 從 Google Sheets 檢查失敗，使用本地快取: {str(e)}")
        # 如果 Google Sheets 失敗，使用本地快取
        today = date.today()
        expiring_soon = []
        
        for item in ingredient_storage:
            if item['expires_at']:
                expires_date = date.fromisoformat(item['expires_at'])
                days_left = (expires_date - today).days
                if days_left <= 3:
                    expiring_soon.append((item, days_left))
        
        if not expiring_soon:
            return "✅ 沒有即將過期的食材"
        
        result = "⚠️ 即將過期的食材 (本地快取):\n"
        for item, days_left in expiring_soon:
            result += f"- {item['name']} 還有 {days_left} 天到期\n"
        return result

def delete_ingredient(ingredient_info: str) -> str:
    """刪除食材，格式: 食材ID 或 食材名稱"""
    try:
        # 先獲取食材列表來找到要刪除的食材
        storage = get_google_sheets_storage()
        
        # 嘗試解析為 ID
        try:
            ingredient_id = int(ingredient_info.strip())
            logger.info(f"🔄 正在刪除食材 ID: {ingredient_id}")
            result = storage.delete_ingredient(ingredient_id)
            return result
        except ValueError:
            # 如果不是數字，嘗試按名稱查找
            logger.info(f"🔄 正在按名稱刪除食材: {ingredient_info}")
            
            # 獲取食材列表來查找 ID
            try:
                expected_headers = ["ID", "名稱", "數量", "單位", "到期日", "存放位置", "備註", "創建時間", "更新時間"]
                records = storage.worksheet.get_all_records(expected_headers=expected_headers)
                
                # 查找匹配的食材
                for record in records:
                    if record.get('名稱', '').strip() == ingredient_info.strip():
                        ingredient_id = int(record.get('ID', 0))
                        result = storage.delete_ingredient(ingredient_id)
                        return result
                
                return f"❌ 找不到名稱為 '{ingredient_info}' 的食材"
                
            except Exception as e:
                return f"❌ 刪除食材失敗: {str(e)}"
        
    except Exception as e:
        logger.error(f"❌ 刪除食材失敗: {str(e)}")
        return f"❌ 刪除食材失敗: {str(e)}"

def reduce_ingredient_quantity(ingredient_info: str) -> str:
    """減少食材數量，格式: 食材名稱,減少數量 或 食材ID,減少數量"""
    try:
        parts = ingredient_info.split(',')
        if len(parts) < 2:
            return "❌ 請提供食材名稱和要減少的數量，格式：食材名稱,數量"
        
        ingredient_identifier = parts[0].strip()
        reduce_quantity = float(parts[1].strip())
        
        storage = get_google_sheets_storage()
        
        # 獲取食材列表來查找目標食材
        expected_headers = ["ID", "名稱", "數量", "單位", "到期日", "存放位置", "備註", "創建時間", "更新時間"]
        records = storage.worksheet.get_all_records(expected_headers=expected_headers)
        
        target_record = None
        target_row_index = None
        
        # 查找目標食材
        try:
            # 嘗試按 ID 查找
            ingredient_id = int(ingredient_identifier)
            for i, record in enumerate(records):
                if int(record.get('ID', 0)) == ingredient_id:
                    target_record = record
                    target_row_index = i + 2  # +2 因為第1行是標題，記錄從第2行開始
                    break
        except ValueError:
            # 按名稱查找
            for i, record in enumerate(records):
                if record.get('名稱', '').strip() == ingredient_identifier.strip():
                    target_record = record
                    target_row_index = i + 2
                    break
        
        if not target_record:
            return f"❌ 找不到食材：{ingredient_identifier}"
        
        # 獲取當前數量
        current_quantity = float(target_record.get('數量', 0))
        new_quantity = current_quantity - reduce_quantity
        
        if new_quantity < 0:
            return f"❌ 無法減少 {reduce_quantity} 個，當前只有 {current_quantity} 個 {target_record.get('名稱', '')}"
        
        if new_quantity == 0:
            # 如果數量變為0，直接刪除該行
            storage.worksheet.delete_rows(target_row_index)
            logger.info(f"✅ 已完全刪除食材: {target_record.get('名稱', '')}")
            return f"✅ 已完全刪除食材: {target_record.get('名稱', '')}"
        else:
            # 更新數量
            storage.worksheet.update_cell(target_row_index, 3, new_quantity)  # 第3列是數量
            storage.worksheet.update_cell(target_row_index, 9, date.today().isoformat())  # 更新時間
            
            logger.info(f"✅ 已減少食材數量: {target_record.get('名稱', '')} 從 {current_quantity} 減少到 {new_quantity}")
            return f"✅ 已減少食材數量: {target_record.get('名稱', '')} 從 {current_quantity} 減少到 {new_quantity}"
            
    except Exception as e:
        logger.error(f"❌ 減少食材數量失敗: {str(e)}")
        return f"❌ 減少食材數量失敗: {str(e)}"

def update_ingredient(ingredient_info: str) -> str:
    """修改食材資訊，格式: 食材ID或名稱,新名稱,新數量,新單位,新到期日,新存放位置"""
    try:
        parts = ingredient_info.split(',')
        if len(parts) < 2:
            return "❌ 請提供食材ID或名稱，以及要修改的資訊，格式：食材ID或名稱,新名稱,新數量,新單位,新到期日,新存放位置"
        
        ingredient_identifier = parts[0].strip()
        new_name = parts[1].strip() if len(parts) > 1 and parts[1].strip() else None
        new_quantity = float(parts[2].strip()) if len(parts) > 2 and parts[2].strip() else None
        new_unit = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None
        new_expires_at = parts[4].strip() if len(parts) > 4 and parts[4].strip() else None
        new_location = parts[5].strip() if len(parts) > 5 and parts[5].strip() else None
        
        storage = get_google_sheets_storage()
        
        # 獲取食材列表來查找目標食材
        expected_headers = ["ID", "名稱", "數量", "單位", "到期日", "存放位置", "備註", "創建時間", "更新時間"]
        records = storage.worksheet.get_all_records(expected_headers=expected_headers)
        
        target_record = None
        target_row_index = None
        
        # 查找目標食材
        try:
            # 嘗試按 ID 查找
            ingredient_id = int(ingredient_identifier)
            for i, record in enumerate(records):
                if int(record.get('ID', 0)) == ingredient_id:
                    target_record = record
                    target_row_index = i + 2  # +2 因為第1行是標題，記錄從第2行開始
                    break
        except ValueError:
            # 按名稱查找
            for i, record in enumerate(records):
                if record.get('名稱', '').strip() == ingredient_identifier.strip():
                    target_record = record
                    target_row_index = i + 2
                    break
        
        if not target_record:
            return f"❌ 找不到食材：{ingredient_identifier}"
        
        # 更新食材資訊
        updated_fields = []
        
        if new_name and new_name != target_record.get('名稱', ''):
            storage.worksheet.update_cell(target_row_index, 2, new_name)  # 第2列是名稱
            updated_fields.append(f"名稱: {target_record.get('名稱', '')} → {new_name}")
        
        if new_quantity is not None and new_quantity != float(target_record.get('數量', 0)):
            storage.worksheet.update_cell(target_row_index, 3, new_quantity)  # 第3列是數量
            updated_fields.append(f"數量: {target_record.get('數量', '')} → {new_quantity}")
        
        if new_unit and new_unit != target_record.get('單位', ''):
            storage.worksheet.update_cell(target_row_index, 4, new_unit)  # 第4列是單位
            updated_fields.append(f"單位: {target_record.get('單位', '')} → {new_unit}")
        
        if new_expires_at and new_expires_at != target_record.get('到期日', ''):
            storage.worksheet.update_cell(target_row_index, 5, new_expires_at)  # 第5列是到期日
            updated_fields.append(f"到期日: {target_record.get('到期日', '')} → {new_expires_at}")
        
        if new_location and new_location != target_record.get('存放位置', ''):
            storage.worksheet.update_cell(target_row_index, 6, new_location)  # 第6列是存放位置
            updated_fields.append(f"存放位置: {target_record.get('存放位置', '')} → {new_location}")
        
        # 更新修改時間
        storage.worksheet.update_cell(target_row_index, 9, date.today().isoformat())  # 第9列是更新時間
        
        if updated_fields:
            logger.info(f"✅ 已修改食材: {target_record.get('名稱', '')} - {', '.join(updated_fields)}")
            return f"✅ 已修改食材: {target_record.get('名稱', '')}\n" + "\n".join(updated_fields)
        else:
            return f"ℹ️ 食材 {target_record.get('名稱', '')} 的資訊沒有變化"
            
    except Exception as e:
        logger.error(f"❌ 修改食材失敗: {str(e)}")
        return f"❌ 修改食材失敗: {str(e)}"


# ==================== 工具初始化 ====================

# 食材管理工具
add_ingredient_tool = Tool(
    name="add_ingredient",
    func=add_ingredient,
    description="添加食材到庫存中，需要提供食材名稱、數量、單位、到期日和存放位置"
)

get_ingredient_list_tool = Tool(
    name="get_ingredient_list",
    func=get_ingredient_list,
    description="獲取當前食材庫存列表"
)

check_expiring_ingredients_tool = Tool(
    name="check_expiring_ingredients",
    func=check_expiring_ingredients,
    description="檢查即將過期（3天內）的食材"
)

delete_ingredient_tool = Tool(
    name="delete_ingredient",
    func=delete_ingredient,
    description="完全刪除食材項目，可以通過食材ID或食材名稱來刪除"
)

reduce_ingredient_quantity_tool = Tool(
    name="reduce_ingredient_quantity",
    func=reduce_ingredient_quantity,
    description="減少食材數量，格式：食材名稱,數量 或 食材ID,數量。如果數量變為0則自動刪除該食材"
)

update_ingredient_tool = Tool(
    name="update_ingredient",
    func=update_ingredient,
    description="修改食材資訊，格式：食材ID或名稱,新名稱,新數量,新單位,新到期日,新存放位置。可以只修改部分欄位"
)


# 所有可用工具列表
AVAILABLE_TOOLS = [
    add_ingredient_tool,
    get_ingredient_list_tool,
    check_expiring_ingredients_tool,
    delete_ingredient_tool,
    reduce_ingredient_quantity_tool,
    update_ingredient_tool
]
