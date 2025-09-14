# parser_chain.py
import os
import logging
from datetime import date, timedelta
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

class AddIngredient(BaseModel):
    name: str = Field(..., description="食材名稱")
    quantity: float | None = Field(1, description="數量")
    unit: str | None = Field(None, description="單位")
    expires_at: str | None = Field(None, description="到期日 YYYY-MM-DD")
    location: str | None = Field(None, description="冷藏/冷凍/室溫")
    notes: str | None = Field(None, description="其他備註")

parser_struct = PydanticOutputParser(pydantic_object=AddIngredient)

prompt = PromptTemplate(
    template=(
        "你是食材輸入解析助手，請把使用者輸入轉成結構化JSON。\n"
        "若有相對日期（明天、後天、下週三），請換算成 YYYY-MM-DD，今天是 {today}。\n"
        "輸入：{user_text}\n"
        "{format_instructions}"
    ),
    input_variables=["user_text"],
    partial_variables={
        "format_instructions": parser_struct.get_format_instructions(),
        "today": date.today().isoformat(),
    },
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
langchain_chain = prompt | llm | parser_struct

def parse_text_to_ingredient(user_text: str) -> AddIngredient:
    """呼叫 LangChain 解析文字，回傳結構化 AddIngredient 物件"""
    logger.info(f"🔍 收到用戶輸入: '{user_text}'")
    
    try:
        # 記錄發送給 GPT 的 prompt
        formatted_prompt = prompt.format(user_text=user_text)
        logger.info(f"📤 發送給 GPT 的 prompt:\n{formatted_prompt}")
        
        # 呼叫 LangChain
        logger.info("🤖 正在呼叫 OpenAI GPT-4o-mini...")
        result = langchain_chain.invoke({"user_text": user_text})
        
        # 記錄 GPT 的回應
        logger.info(f"✅ GPT 解析成功:")
        logger.info(f"   - 名稱: {result.name}")
        logger.info(f"   - 數量: {result.quantity}")
        logger.info(f"   - 單位: {result.unit}")
        logger.info(f"   - 到期日: {result.expires_at}")
        logger.info(f"   - 存放位置: {result.location}")
        logger.info(f"   - 備註: {result.notes}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ GPT 解析失敗: {str(e)}")
        logger.error(f"   輸入文字: '{user_text}'")
        raise e
