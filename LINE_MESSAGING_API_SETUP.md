# LINE Messaging API 在 n8n 中的配置指南

## 前置條件
- ✅ 已設置 LINE Official Account
- ✅ 已獲取 Channel Access Token
- ✅ 已獲取您的 User ID
- ✅ n8n 實例已安裝 LINE 節點

## 獲取必要信息

### 1. Channel Access Token
1. 登入 [LINE Developers Console](https://developers.line.biz/)
2. 選擇您的 Provider 和 Channel
3. 在 "Messaging API" 標籤中找到 "Channel access token"
4. 複製完整的 token

### 2. User ID
有幾種方式獲取您的 User ID：

#### 方法 A: 通過 LINE Bot 獲取
1. 在您的 LINE Bot 中發送任意訊息
2. 查看 webhook 日誌，找到 `source.userId` 欄位
3. 複製該 User ID

#### 方法 B: 通過 LINE Login 獲取
1. 設置 LINE Login
2. 用戶授權後，從 ID Token 中獲取 `sub` 欄位

#### 方法 C: 通過 QR Code 獲取
1. 使用 LINE Messaging API 的 QR Code 功能
2. 掃描後獲取 User ID

## n8n 配置步驟

### 步驟 1: 安裝 LINE 節點
1. 在 n8n 中，點擊右上角的 "Settings"
2. 選擇 "Community Nodes"
3. 搜索 "LINE" 或 "line"
4. 安裝官方的 LINE 節點

### 步驟 2: 配置 LINE 節點
1. 在 n8n 工作流程中拖拽 "LINE" 節點
2. 連接到 IF 節點的 "true" 分支
3. 配置以下參數：

```
Resource: Message
Operation: Send Message
Channel Access Token: [您的 Channel Access Token]
To: [您的 User ID]
Message Type: Text
Message: {{ $json.message }}
```

### 步驟 3: 進階配置 (可選)

#### 自定義訊息格式
```
Message: 🍎 食材過期提醒

{{ $json.message }}

檢查時間: {{ $json.timestamp }}
```

#### 使用 Rich Menu (可選)
如果您設置了 Rich Menu，可以添加：
```
Rich Menu: [Rich Menu ID]
```

## 完整工作流程配置

### 工作流程結構
```
Schedule Trigger (每天 9:00)
    ↓
HTTP Request (GET /api/expiring-ingredients)
    ↓
IF (has_expiring == true)
    ↓
LINE Send Message
```

### 詳細配置

#### 1. Schedule Trigger
- Rule: `0 9 * * *` (每天上午 9:00)
- Timezone: 選擇您的時區

#### 2. HTTP Request
- Method: `GET`
- URL: `https://your-domain.com/api/expiring-ingredients`
- Response Format: `JSON`

#### 3. IF 條件
- Condition: `{{ $json.has_expiring }}`
- Operation: `Equal`
- Value: `true`

#### 4. LINE 節點
- Resource: `Message`
- Operation: `Send Message`
- Channel Access Token: `[您的 Token]`
- To: `[您的 User ID]`
- Message Type: `Text`
- Message: `{{ $json.message }}`

## 測試配置

### 1. 手動測試
1. 在 n8n 中點擊 "Execute Workflow"
2. 檢查每個節點的輸出
3. 確認 LINE 訊息是否發送成功

### 2. 檢查日誌
1. 在 LINE Developers Console 查看 webhook 日誌
2. 確認訊息發送狀態
3. 檢查是否有錯誤訊息

## 常見問題

### Q: 收到 "Invalid user ID" 錯誤
**A**: 檢查 User ID 是否正確，確保沒有多餘的空格或字符

### Q: 收到 "Invalid access token" 錯誤
**A**: 檢查 Channel Access Token 是否正確，確保沒有過期

### Q: 訊息發送成功但沒有收到
**A**: 檢查 User ID 是否正確，確保是您自己的 User ID

### Q: 如何獲取群組 ID？
**A**: 將 Bot 加入群組，然後從 webhook 日誌中獲取 `source.groupId`

## 進階功能

### 1. 發送圖片
```
Message Type: Image
Image URL: [圖片 URL]
```

### 2. 發送位置
```
Message Type: Location
Title: 食材位置
Address: 冰箱
Latitude: 25.0330
Longitude: 121.5654
```

### 3. 發送模板訊息
```
Message Type: Template
Template: [模板 JSON]
```

## 費用說明
- 每月前 500 則訊息免費
- 超過 500 則後，每則訊息收費
- 詳細費用請參考 [LINE Messaging API 費用](https://developers.line.biz/en/docs/messaging-api/pricing/)

## 安全注意事項
1. 不要在 n8n 中硬編碼敏感信息
2. 使用環境變數存儲 Channel Access Token
3. 定期更新 Access Token
4. 限制 User ID 的訪問權限

## 故障排除
1. **節點無法連接**: 檢查網路連接和 Token 有效性
2. **訊息格式錯誤**: 檢查 JSON 格式和變數引用
3. **權限問題**: 確認 Bot 有發送訊息的權限
