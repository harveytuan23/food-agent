# parser_chain.py
import os
from datetime import date, timedelta
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    return langchain_chain.invoke({"user_text": user_text})
