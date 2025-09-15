# 🤖 智能食物管理助手

一個基於 LangChain 和 OpenAI 的智能食物管理 AI Agent，專注於食材庫存管理，支援 Google Sheets 整合和自動化通知。

## ✨ 核心功能

### 🥬 食材管理
- **添加食材**: 智能解析食材資訊並存儲到 Google Sheets
- **查看庫存**: 顯示所有食材的庫存狀況
- **檢查過期**: 提醒即將過期的食材（3天內）
- **減少數量**: 使用食材時自動減少庫存
- **刪除食材**: 完全移除不需要的食材

### 🔄 自動化通知
- **每日檢查**: 自動檢查即將過期的食材
- **LINE 通知**: 通過 LINE Messaging API 發送提醒
- **n8n 整合**: 支援 n8n 工作流程自動化

### 📊 數據存儲
- **Google Sheets**: 所有食材數據存儲在 Google Sheets
- **實時同步**: 本地快取與雲端數據同步
- **備份安全**: 數據自動備份到 Google Drive

## 🛠️ 技術架構

- **AI Agent**: LangChain Agent 系統
- **LLM**: OpenAI GPT-4o-mini
- **框架**: FastAPI + LINE Bot SDK
- **存儲**: Google Sheets API
- **自動化**: n8n 工作流程
- **通知**: LINE Messaging API

## 📦 快速開始

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 環境變數設定
創建 `.env` 檔案：
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# LINE Bot
LINE_CHANNEL_SECRET=your_line_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
GOOGLE_SHEET_NAME=your_sheet_name
GOOGLE_WORKSHEET_NAME=ingredients
```

### 3. 設置 Google Sheets
參考 [Google Sheets 設置指南](GOOGLE_SHEETS_SETUP.md)

### 4. 啟動服務
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 使用方式

### LINE Bot 指令
- `ping` - 測試連線
- `help` 或 `幫助` - 顯示幫助資訊
- `tools` 或 `工具` - 顯示可用工具列表

### 自然語言指令
```
查看食材庫存
添加牛奶 500ml 明天到期 冷藏
檢查即將過期的食材
減少蘋果 2個
刪除過期的香蕉
```

## 🔧 可用工具

### 食材管理工具
- `add_ingredient` - 添加食材到庫存
- `get_ingredient_list` - 獲取食材庫存列表
- `check_expiring_ingredients` - 檢查即將過期的食材
- `delete_ingredient` - 完全刪除食材項目
- `reduce_ingredient_quantity` - 減少食材數量

## 🔄 自動化設置

### n8n 工作流程
設置每日自動檢查過期食材並發送通知：

1. **參考指南**: [n8n 設置指南](N8N_SETUP_GUIDE.md)
2. **LINE 通知**: [LINE Messaging API 設置](LINE_MESSAGING_API_SETUP.md)
3. **配置範例**: `n8n_line_config_example.json`

### API 端點
- `GET /api/expiring-ingredients` - 獲取即將過期的食材（供 n8n 調用）

## 🛠️ 輔助工具

### 獲取 LINE User ID
```bash
python3 get_user_id.py
```
向您的 LINE Bot 發送任意訊息，工具會顯示您的 User ID。

## 📁 專案結構

```
food-agent/
├── app.py                          # FastAPI 主應用程式
├── agent.py                        # AI Agent 核心邏輯
├── tools.py                        # 工具函數集合
├── parser_chain.py                 # 文字解析器
├── google_sheets_storage.py        # Google Sheets 整合
├── get_user_id.py                  # LINE User ID 獲取工具
├── requirements.txt                # 依賴套件
├── .env                           # 環境變數（不提交）
├── .gitignore                     # Git 忽略檔案
├── GOOGLE_SHEETS_SETUP.md         # Google Sheets 設置指南
├── LINE_MESSAGING_API_SETUP.md    # LINE Messaging API 設置指南
├── N8N_SETUP_GUIDE.md             # n8n 工作流程設置指南
├── n8n_line_config_example.json   # n8n 配置範例
└── README.md                      # 專案說明
```

## 🧪 測試

### 測試 AI Agent
```bash
python3 test_agent.py
```

### 測試 Google Sheets 整合
```bash
python3 test_google_sheets.py
```

## 📝 日誌功能

系統會自動記錄詳細的處理過程：
- 用戶輸入和解析
- Agent 思考過程
- 工具調用結果
- Google Sheets 操作
- 錯誤處理

日誌檔案：`food_agent.log`

## 🔒 安全注意事項

1. **環境變數**: 不要在代碼中硬編碼敏感信息
2. **Google Sheets**: 定期檢查服務帳戶權限
3. **LINE API**: 定期更新 Access Token
4. **數據備份**: 定期備份 Google Sheets 數據

## 🚨 重要提醒

- **LINE Notify 停用**: LINE Notify 服務將於 2025年3月31日停止，請使用 LINE Messaging API
- **日期處理**: 系統自動使用當前日期（2025年）處理食材到期日
- **免費額度**: LINE Messaging API 每月有 500 則免費訊息

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

---

## 📞 支援

如果您遇到問題，請檢查：
1. 環境變數是否正確設置
2. Google Sheets 權限是否正確
3. LINE Bot 設定是否完成
4. 查看日誌檔案了解詳細錯誤信息