# app.py
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

from parser_chain import parse_text_to_ingredient

# --- Load ENV ---
load_dotenv()
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

# --- LINE setup ---
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

# --- FastAPI ---
app = FastAPI()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/line/webhook")
async def line_webhook(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            text_in = event.message.text.strip()

            if text_in.lower() == "ping":
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="pong ✅ Connected"))
                continue

            try:
                parsed = parse_text_to_ingredient(text_in)
                reply = (
                    f"解析結果：\n"
                    f"- 名稱: {parsed.name}\n"
                    f"- 數量: {parsed.quantity}\n"
                    f"- 單位: {parsed.unit}\n"
                    f"- 到期日: {parsed.expires_at}\n"
                    f"- 存放位置: {parsed.location}\n"
                    f"- 備註: {parsed.notes}"
                )
            except Exception as e:
                reply = f"❌ 解析失敗，請用更明確的格式輸入。\n錯誤: {str(e)}"

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    return "OK"
