# app.py
import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

from agent import food_agent

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
            
            if text_in.lower() == "help" or text_in.lower() == "幫助":
                logger.info("📋 用戶請求幫助資訊")
                help_text = (
                    "🤖 智能食物管理助手\n\n"
                    "我可以幫助你：\n"
                    "• 管理食材庫存\n"
                    "• 添加食材到庫存\n"
                    "• 查看食材列表\n"
                    "• 檢查即將過期的食材\n"
                    "• 刪除食材\n\n"
                    "試試說：「我想添加牛奶到庫存」或「查看食材庫存」"
                )
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=help_text))
                continue
            
            if text_in.lower() == "tools" or text_in.lower() == "工具":
                logger.info("🛠️ 用戶請求工具列表")
                tools_info = food_agent.get_available_tools_info()
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=tools_info))
                continue

            try:
                logger.info("🚀 Agent 開始處理用戶輸入...")
                # 使用 Agent 處理用戶輸入
                reply = food_agent.process_user_message(text_in)
                logger.info(f"📤 Agent 回覆用戶: {reply[:100]}...")
            except Exception as e:
                reply = f"❌ 處理失敗，請稍後再試。\n錯誤: {str(e)}"
                logger.error(f"❌ Agent 處理失敗: {str(e)}")

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

    return "OK"
