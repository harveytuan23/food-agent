# app.py
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

from parser_chain import parse_text_to_ingredient

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('food_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info("📨 收到 LINE webhook 請求")
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        events = parser.parse(body.decode("utf-8"), signature)
        logger.info(f"✅ LINE webhook 解析成功，收到 {len(events)} 個事件")
    except InvalidSignatureError:
        logger.error("❌ LINE webhook 簽名驗證失敗")
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
            text_in = event.message.text.strip()
            user_id = event.source.user_id if hasattr(event.source, 'user_id') else "unknown"
            
            logger.info(f"👤 用戶 {user_id} 發送訊息: '{text_in}'")

            if text_in.lower() == "ping":
                logger.info("🏓 收到 ping 命令，回覆 pong")
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="pong ✅ Connected"))
                continue

            try:
                logger.info("🚀 開始解析用戶輸入...")
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
                logger.info(f"📤 回覆用戶: {reply[:100]}...")
            except Exception as e:
                reply = f"❌ 解析失敗，請用更明確的格式輸入。\n錯誤: {str(e)}"
                logger.error(f"❌ 解析失敗: {str(e)}")

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    return "OK"
