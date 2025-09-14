#!/usr/bin/env python3
# test_agent.py
"""
測試 AI Agent 的各種功能
"""

from agent import food_agent

def test_agent_functions():
    """測試 Agent 的各種功能"""
    
    print("🤖 智能食物管理助手測試")
    print("=" * 50)
    
    # 測試用例
    test_cases = [
        "查看食材庫存",
        "推薦一個食譜",
        "今天天氣如何",
        "檢查即將過期的食材",
        "查詢牛奶的營養資訊",
        "添加蘋果 5個 後天到期 冷藏",
        "獲取番茄炒蛋的詳細步驟"
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 測試 {i}: {test_case}")
        print("-" * 30)
        
        try:
            result = food_agent.process_user_message(test_case)
            print(f"✅ 回應: {result}")
        except Exception as e:
            print(f"❌ 錯誤: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_agent_functions()
