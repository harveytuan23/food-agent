#!/usr/bin/env python3
# get_user_id.py
"""
輔助工具：獲取 LINE User ID
用於設置 LINE Messaging API 通知
"""

import os
import json
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()

# LINE 設定
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    print("❌ 請在 .env 文件中設置 LINE_CHANNEL_SECRET 和 LINE_CHANNEL_ACCESS_TOKEN")
    exit(1)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

app = FastAPI()

# 存儲 User ID 的列表
user_ids = []

@app.post("/line/webhook")
async def line_webhook(request: Request):
    """LINE Webhook 處理器，用於獲取 User ID"""
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            text = event.message.text.strip()
            user_id = event.source.user_id if hasattr(event.source, 'user_id') else None
            
            if user_id:
                if user_id not in user_ids:
                    user_ids.append(user_id)
                    logger.info(f"✅ 新增 User ID: {user_id}")
                
                # 回覆用戶
                reply_text = f"✅ 已獲取您的 User ID: {user_id}\n\n請複製此 ID 用於 n8n 配置"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
                
                # 在控制台顯示
                print(f"\n🎉 成功獲取 User ID: {user_id}")
                print("請複製此 ID 用於 n8n 的 LINE 節點配置")
                print("=" * 50)

    return "OK"

@app.get("/user-ids")
def get_user_ids():
    """獲取所有已記錄的 User ID"""
    return {"user_ids": user_ids}

@app.get("/")
def root():
    return {
        "message": "LINE User ID 獲取工具",
        "instructions": [
            "1. 確保您的 LINE Bot 已設置 webhook URL",
            "2. 向您的 LINE Bot 發送任意訊息",
            "3. 查看控制台輸出獲取 User ID",
            "4. 複製 User ID 用於 n8n 配置"
        ],
        "webhook_url": "/line/webhook",
        "current_user_ids": user_ids
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 啟動 LINE User ID 獲取工具")
    print("=" * 50)
    print("📋 使用說明:")
    print("1. 確保您的 LINE Bot webhook URL 指向此服務")
    print("2. 向您的 LINE Bot 發送任意訊息")
    print("3. 查看下方輸出獲取 User ID")
    print("4. 複製 User ID 用於 n8n 配置")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
