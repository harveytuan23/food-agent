# Google Sheets 設定指南

## 📋 概述

這個 AI Agent 現在支援將食材資料儲存到 Google Sheets，提供更好的資料持久化和跨平台存取。

## 🔧 設定步驟

### 1. 創建 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 創建新專案或選擇現有專案
3. 啟用 Google Sheets API 和 Google Drive API

### 2. 創建服務帳戶

1. 在 Google Cloud Console 中，前往「IAM 和管理」→「服務帳戶」
2. 點擊「建立服務帳戶」
3. 填寫服務帳戶詳細資訊：
   - 名稱：`food-agent-service`
   - 描述：`Food Agent Google Sheets Service Account`
4. 點擊「建立並繼續」

### 3. 生成服務帳戶金鑰

1. 在服務帳戶列表中，點擊剛創建的服務帳戶
2. 前往「金鑰」分頁
3. 點擊「新增金鑰」→「建立新金鑰」
4. 選擇「JSON」格式
5. 下載 JSON 檔案

### 4. 創建 Google Sheets

1. 前往 [Google Sheets](https://sheets.google.com/)
2. 創建新的試算表
3. 將試算表命名為 `food_agent_ingredients`（或你喜歡的名稱）
4. 將試算表分享給服務帳戶的電子郵件地址
   - 權限設定為「編輯者」

### 5. 設定環境變數

在 `.env` 檔案中添加以下設定：

```env
# Google Sheets 設定
GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", "project_id": "your-project", "private_key_id": "...", "private_key": "...", "client_email": "...", "client_id": "...", "auth_uri": "...", "token_uri": "...", "auth_provider_x509_cert_url": "...", "client_x509_cert_url": "..."}'
GOOGLE_SHEET_NAME=food_agent_ingredients
GOOGLE_WORKSHEET_NAME=ingredients
```

**重要**：將整個 JSON 檔案內容放在單引號內作為一個字串。

## 📊 試算表結構

系統會自動創建以下欄位：

| 欄位 | 說明 |
|------|------|
| ID | 自動生成的唯一識別碼 |
| 名稱 | 食材名稱 |
| 數量 | 食材數量 |
| 單位 | 計量單位 |
| 到期日 | 到期日期 (YYYY-MM-DD) |
| 存放位置 | 存放位置（冷藏/冷凍/室溫） |
| 備註 | 額外備註 |
| 創建時間 | 記錄創建時間 |
| 更新時間 | 最後更新時間 |

## 🚀 部署到 n8n

### 環境變數設定

在 n8n 中設定以下環境變數：

```bash
OPENAI_API_KEY=your_openai_api_key
LINE_CHANNEL_SECRET=your_line_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", ...}'
GOOGLE_SHEET_NAME=food_agent_ingredients
GOOGLE_WORKSHEET_NAME=ingredients
```

### n8n 工作流程

你可以創建 n8n 工作流程來：
- 定期同步資料
- 發送過期提醒
- 生成報告
- 與其他系統整合

## 🔍 故障排除

### 常見問題

1. **權限錯誤**
   - 確保服務帳戶有試算表的編輯權限
   - 檢查 API 是否已啟用

2. **JSON 格式錯誤**
   - 確保 JSON 字串正確轉義
   - 檢查所有必要的欄位都存在

3. **試算表不存在**
   - 系統會自動創建試算表
   - 確保服務帳戶有創建試算表的權限

### 測試連線

```python
from google_sheets_storage import google_sheets_storage

# 測試連線
result = google_sheets_storage.get_ingredient_list()
print(result)
```

## 📈 優點

- **持久化儲存**：資料不會因為重啟而消失
- **跨平台存取**：可以在任何地方查看和編輯
- **備份和同步**：Google 自動處理備份
- **協作功能**：多人可以同時查看資料
- **n8n 整合**：容易與其他自動化工具整合

## 🔒 安全性

- 使用服務帳戶進行認證
- 最小權限原則
- 定期輪換金鑰
- 監控 API 使用情況
