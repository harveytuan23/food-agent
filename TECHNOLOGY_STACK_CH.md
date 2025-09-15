# 🛠️ 技術架構文檔

## 專案概述
智能食物管理助手是一個基於 AI 的食材庫存管理系統，整合了多種現代技術來提供智能化的食材管理體驗。

## 🏗️ 整體架構

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LINE Bot      │    │   FastAPI       │    │   Google Sheets │
│   (用戶界面)     │◄──►│   (API 服務)     │◄──►│   (數據存儲)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   LangChain     │
                       │   (AI Agent)    │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   OpenAI        │
                       │   (GPT-4o-mini) │
                       └─────────────────┘
```

## 🔧 核心技術棧

### 1. 後端框架
- **FastAPI** - 現代化的 Python Web 框架
  - 高性能異步處理
  - 自動 API 文檔生成
  - 類型提示支持
  - 內建數據驗證

### 2. AI 與機器學習
- **LangChain** - AI 應用開發框架
  - Agent 系統管理
  - 工具鏈整合
  - 提示詞模板管理
  - 輸出解析器

- **OpenAI GPT-4o-mini** - 大型語言模型
  - 自然語言理解
  - 智能決策制定
  - 工具調用能力
  - 上下文記憶

### 3. 數據存儲
- **Google Sheets API** - 雲端表格服務
  - 實時數據同步
  - 自動備份
  - 協作功能
  - 版本控制

### 4. 通訊與通知
- **LINE Messaging API** - 即時通訊平台
  - 用戶互動界面
  - 推送通知
  - 富媒體支持
  - 群組管理

- **n8n** - 工作流程自動化
  - 定時任務調度
  - API 整合
  - 條件邏輯處理
  - 多平台通知

## 📚 開發工具與庫

### Python 核心庫
```python
# Web 框架
fastapi==0.104.1
uvicorn==0.24.0

# AI 與機器學習
langchain==0.1.0
langchain-openai==0.0.2
langchain-core==0.1.0
openai==1.3.0

# 數據處理
pydantic==2.5.0
python-dotenv==1.0.0

# Google 服務
google-auth==2.23.0
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
gspread==5.12.0

# LINE Bot
line-bot-sdk==3.5.0

# HTTP 請求
httpx==0.25.0
requests==2.31.0

# 日誌與監控
logging
datetime
```

### 開發環境工具
- **Python 3.11+** - 程式語言
- **pip** - 套件管理
- **venv** - 虛擬環境
- **Git** - 版本控制

## 🔄 系統流程

### 1. 用戶互動流程
```
用戶發送訊息 → LINE Bot → FastAPI → LangChain Agent → 工具調用 → Google Sheets → 回應用戶
```

### 2. 自動化通知流程
```
定時觸發器 → n8n → API 調用 → 檢查過期食材 → 發送通知 → LINE 用戶
```

### 3. 數據處理流程
```
用戶輸入 → 文字解析 → 結構化數據 → Google Sheets 存儲 → 實時同步
```

## 🏛️ 架構模式

### 1. Agent 模式
- **智能代理**: LangChain Agent 作為核心決策引擎
- **工具調用**: 動態選擇和執行適當的工具
- **狀態管理**: 維護對話上下文和記憶

### 2. 微服務架構
- **API 服務**: FastAPI 提供 RESTful API
- **數據服務**: Google Sheets 作為數據層
- **通知服務**: LINE 和 n8n 處理通知

### 3. 事件驅動架構
- **Webhook**: LINE Bot 事件處理
- **定時任務**: n8n 工作流程調度
- **異步處理**: FastAPI 異步請求處理

## 🔐 安全與認證

### 1. API 安全
- **環境變數**: 敏感信息加密存儲
- **簽名驗證**: LINE Webhook 簽名驗證
- **錯誤處理**: 完整的異常處理機制

### 2. 數據安全
- **Google OAuth**: 服務帳戶認證
- **權限控制**: 最小權限原則
- **數據加密**: 傳輸和存儲加密

### 3. 訪問控制
- **API 限制**: 請求頻率限制
- **用戶驗證**: LINE 用戶身份驗證
- **日誌記錄**: 完整的操作日誌

## 📊 數據模型

### 1. 食材數據結構
```python
class IngredientInfo(BaseModel):
    name: str                    # 食材名稱
    quantity: float | None       # 數量
    unit: str | None            # 單位
    expires_at: str | None      # 到期日
    location: str | None        # 存放位置
    notes: str | None           # 備註
```

### 2. Google Sheets 結構
```
| ID | 名稱 | 數量 | 單位 | 到期日 | 存放位置 | 備註 | 創建時間 | 更新時間 |
```

### 3. API 回應格式
```json
{
  "success": true,
  "has_expiring": true,
  "message": "過期提醒內容",
  "timestamp": "2025-09-14T12:00:00Z"
}
```

## 🚀 部署與運維

### 1. 本地開發
```bash
# 環境設置
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 啟動服務
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 2. 生產環境
- **容器化**: Docker 支持
- **負載均衡**: 多實例部署
- **監控**: 日誌和指標收集
- **備份**: 自動數據備份

### 3. CI/CD
- **版本控制**: Git 工作流
- **自動測試**: 單元測試和整合測試
- **部署**: 自動化部署流程

## 🔧 工具與服務

### 1. 開發工具
- **IDE**: VS Code, PyCharm
- **API 測試**: Postman, curl
- **數據庫管理**: Google Sheets Web UI
- **日誌分析**: 內建日誌系統

### 2. 第三方服務
- **OpenAI API**: AI 模型服務
- **Google Cloud**: 表格和認證服務
- **LINE Platform**: 通訊和通知服務
- **n8n**: 工作流程自動化

### 3. 監控與分析
- **應用日誌**: 結構化日誌記錄
- **錯誤追蹤**: 異常處理和報告
- **性能監控**: 響應時間和吞吐量
- **使用統計**: 用戶行為分析

## 📈 擴展性設計

### 1. 水平擴展
- **無狀態設計**: 服務間無依賴
- **負載均衡**: 多實例部署
- **數據分片**: Google Sheets 分區

### 2. 功能擴展
- **插件架構**: 工具模組化設計
- **API 版本控制**: 向後兼容
- **配置管理**: 環境變數配置

### 3. 性能優化
- **快取機制**: 本地數據快取
- **異步處理**: 非阻塞操作
- **連接池**: 數據庫連接優化

## 🔮 未來技術規劃

### 1. 短期目標
- **數據分析**: 食材使用模式分析
- **預測功能**: 過期時間預測
- **多語言支持**: 國際化支持

### 2. 中期目標
- **機器學習**: 智能推薦系統
- **圖像識別**: 食材圖片識別
- **語音交互**: 語音指令支持

### 3. 長期目標
- **IoT 整合**: 智能冰箱連接
- **區塊鏈**: 食品安全追溯
- **AR/VR**: 虛擬廚房體驗

## 📝 技術決策記錄

### 1. 為什麼選擇 FastAPI？
- 高性能異步處理
- 自動 API 文檔生成
- 現代化的 Python 特性支持
- 活躍的社區和生態系統

### 2. 為什麼選擇 LangChain？
- 成熟的 AI Agent 框架
- 豐富的工具生態
- 良好的 OpenAI 整合
- 靈活的提示詞管理

### 3. 為什麼選擇 Google Sheets？
- 無需額外數據庫設置
- 實時協作功能
- 自動備份和版本控制
- 易於查看和編輯

### 4. 為什麼選擇 LINE？
- 在台灣的高普及率
- 豐富的 API 功能
- 良好的用戶體驗
- 穩定的服務品質

---

## 📞 技術支援

如有技術問題，請參考：
- [FastAPI 官方文檔](https://fastapi.tiangolo.com/)
- [LangChain 官方文檔](https://python.langchain.com/)
- [Google Sheets API 文檔](https://developers.google.com/sheets/api)
- [LINE Messaging API 文檔](https://developers.line.biz/en/docs/messaging-api/)
- [n8n 官方文檔](https://docs.n8n.io/)
