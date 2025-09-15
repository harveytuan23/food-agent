# n8n 自動推送通知設置指南

## 概述
這個指南將幫助您設置 n8n 工作流程，每天自動檢查食材庫存並推送過期提醒。

## ⚠️ 重要通知
**LINE Notify 服務將於 2025年3月31日停止服務**
- 如果您目前使用 LINE Notify，請盡快遷移到 LINE Messaging API
- 建議使用 Discord、Telegram 或 Email 作為替代通知方式

## 前置條件
1. 已部署的 food-agent API 服務
2. n8n 實例（本地或雲端）
3. 通知方式（LINE、Email、Slack 等）

## API 端點
您的 food-agent 現在提供以下 API 端點：

```
GET /api/expiring-ingredients
```

### 回應格式
```json
{
  "success": true,
  "has_expiring": true,
  "message": "⚠️ 即將過期的食材 (未來3天內):\n- 牛奶 還有 2 天到期\n- 麵包 還有 1 天到期",
  "timestamp": "2025-09-14T12:00:00Z"
}
```

## n8n 工作流程設置

### 步驟 1: 創建新的工作流程
1. 登入您的 n8n 實例
2. 點擊 "New workflow"
3. 命名為 "Food Agent Daily Check"

### 步驟 2: 添加定時觸發器
1. 從左側面板拖拽 "Schedule Trigger" 節點
2. 配置為每天上午 9:00 執行：
   - Rule: `0 9 * * *` (Cron 表達式)
   - 或使用 UI 選擇 "Daily at 9:00 AM"

### 步驟 3: 添加 HTTP Request 節點
1. 拖拽 "HTTP Request" 節點
2. 連接到 Schedule Trigger
3. 配置：
   - Method: `GET`
   - URL: `https://your-domain.com/api/expiring-ingredients`
   - Headers: (如果需要認證)
   - Response Format: `JSON`

### 步驟 4: 添加條件判斷
1. 拖拽 "IF" 節點
2. 連接到 HTTP Request
3. 配置條件：
   - Condition: `{{ $json.has_expiring }}`
   - Operation: `Equal`
   - Value: `true`

### 步驟 5: 配置通知方式

#### 選項 A: LINE 通知 (已停用)
⚠️ **重要通知**: LINE Notify 服務將於 2025年3月31日停止服務

**替代方案**: 使用 LINE Messaging API
1. 拖拽 "LINE" 節點（需要安裝 LINE 節點）
2. 連接到 IF 節點的 "true" 分支
3. 配置：
   - Channel Access Token: 您的 LINE Messaging API Token
   - To: 用戶 ID 或群組 ID
   - Message: `{{ $json.message }}`

**詳細設置**: 請參考 `LINE_MESSAGING_API_SETUP.md` 指南

**注意**: 
- 需要設置 LINE Official Account
- 每月有 500 則免費訊息額度
- 需要獲取您的 User ID

#### 選項 B: Email 通知
1. 拖拽 "Email" 節點
2. 連接到 IF 節點的 "true" 分支
3. 配置：
   - To: 您的 email 地址
   - Subject: "🍎 食材過期提醒"
   - Message: `{{ $json.message }}`

#### 選項 C: Slack 通知
1. 拖拽 "Slack" 節點
2. 連接到 IF 節點的 "true" 分支
3. 配置：
   - Channel: 您的 Slack 頻道
   - Text: `{{ $json.message }}`

#### 選項 D: Discord 通知 (推薦)
1. 拖拽 "Discord" 節點
2. 連接到 IF 節點的 "true" 分支
3. 配置：
   - Webhook URL: 您的 Discord Webhook URL
   - Content: `{{ $json.message }}`

#### 選項 E: Telegram 通知
1. 拖拽 "Telegram" 節點
2. 連接到 IF 節點的 "true" 分支
3. 配置：
   - Bot Token: 您的 Telegram Bot Token
   - Chat ID: 您的 Telegram Chat ID
   - Text: `{{ $json.message }}`

### 步驟 6: 添加日誌記錄
1. 拖拽 "Set" 節點
2. 連接到 IF 節點的 "false" 分支
3. 配置：
   - Name: `no_expiring_items`
   - Value: `今天沒有即將過期的食材 ✅`

## 完整工作流程圖
```
Schedule Trigger (每天 9:00)
    ↓
HTTP Request (GET /api/expiring-ingredients)
    ↓
IF (has_expiring == true)
    ↓                    ↓
true: 發送通知        false: 記錄日誌
```

## 測試工作流程
1. 點擊 "Execute Workflow" 按鈕
2. 檢查每個節點的輸出
3. 確認通知是否正確發送

## 進階配置

### 自定義檢查天數
如果您想檢查不同天數內過期的食材，可以修改 API 調用：

```
GET /api/expiring-ingredients?days=7
```

### 多個通知方式
您可以同時配置多種通知方式：
- LINE Messaging API 通知 (需要 Official Account)
- Email 通知
- Slack 通知
- Discord 通知 (推薦)
- Telegram 通知

### 錯誤處理
添加 "Error Trigger" 節點來處理 API 調用失敗的情況。

## 部署建議
1. 確保您的 food-agent API 服務穩定運行
2. 設置監控來確保 n8n 工作流程正常執行
3. 定期檢查日誌以確保通知正常發送

## 故障排除
1. **API 調用失敗**: 檢查 URL 和網路連接
2. **通知未發送**: 檢查通知服務的認證設定
3. **定時器不工作**: 檢查 Cron 表達式或時區設定

## 安全注意事項
1. 不要在 n8n 中硬編碼敏感信息
2. 使用環境變數存儲 API keys 和 tokens
3. 定期更新認證信息
