# 🤖 智能食物管理助手

一個基於 LangChain 和 OpenAI 的智能食物管理 AI Agent，可以幫助你管理食材庫存、推薦食譜、查詢營養資訊等。

## ✨ 功能特色

### 🥬 食材管理
- **查看庫存**: 顯示所有食材的庫存狀況
- **添加食材**: 新增食材到庫存中
- **檢查過期**: 提醒即將過期的食材

### 🍽️ 食譜推薦
- **智能推薦**: 根據現有食材推薦適合的食譜
- **詳細步驟**: 提供食譜的完整製作步驟
- **難度評估**: 顯示烹飪時間和難度

### 🥗 營養查詢
- **營養資訊**: 查詢食物的詳細營養成分
- **熱量計算**: 提供每100g的營養數據

### 🌤️ 天氣查詢
- **天氣資訊**: 提供天氣狀況和溫度
- **保存建議**: 根據天氣提供食材保存建議

## 🛠️ 技術架構

- **AI Agent**: 使用 LangChain 的 Agent 系統
- **LLM**: OpenAI GPT-4o-mini
- **框架**: FastAPI + LINE Bot SDK
- **工具系統**: 模組化的工具函數

## 📦 安裝與設定

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 環境變數設定
創建 `.env` 檔案：
```env
OPENAI_API_KEY=your_openai_api_key_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
```

### 3. 啟動服務
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 使用方式

### LINE Bot 指令
- `ping` - 測試連線
- `help` 或 `幫助` - 顯示幫助資訊
- `tools` 或 `工具` - 顯示可用工具列表

### 自然語言指令
你可以用自然語言與 Agent 互動：

```
查看食材庫存
推薦一個食譜
今天天氣如何
檢查即將過期的食材
查詢牛奶的營養資訊
添加蘋果 5個 後天到期 冷藏
獲取番茄炒蛋的詳細步驟
```

## 🧪 測試

運行測試腳本：
```bash
python3 test_agent.py
```

## 📁 專案結構

```
food-agent/
├── app.py              # FastAPI 主應用程式
├── agent.py            # AI Agent 核心邏輯
├── tools.py            # 工具函數集合
├── parser_chain.py     # 原始解析器（保留）
├── requirements.txt    # 依賴套件
├── test_agent.py       # 測試腳本
├── .env               # 環境變數（不提交）
├── .gitignore         # Git 忽略檔案
└── README.md          # 專案說明
```

## 🔧 工具函數

### 食材管理工具
- `add_ingredient` - 添加食材到庫存
- `get_ingredient_list` - 獲取食材庫存列表
- `check_expiring_ingredients` - 檢查即將過期的食材

### 食譜工具
- `recommend_recipe` - 推薦食譜
- `get_recipe_details` - 獲取食譜詳細步驟

### 其他工具
- `get_weather_info` - 查詢天氣資訊
- `get_nutrition_info` - 查詢營養資訊

## 📝 日誌功能

系統會自動記錄詳細的處理過程：
- 用戶輸入
- Agent 思考過程
- 工具調用
- GPT 回應
- 錯誤處理

日誌檔案：`food_agent.log`

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License
