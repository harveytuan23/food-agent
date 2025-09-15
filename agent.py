# agent.py
import logging
from typing import List, Dict, Any
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

from tools import AVAILABLE_TOOLS

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

class FoodAgent:
    """智能食物管理助手 Agent"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        self.tools = AVAILABLE_TOOLS
        self.agent_executor = self._create_agent()
        
    def _create_agent(self):
        """創建 Agent 執行器"""
        # 定義系統提示詞
        from datetime import date, datetime
        current_date = date.today().isoformat()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        system_prompt = f"""你是一個智能食物管理助手，專門幫助用戶管理食材庫存。

當前時間：{current_time}
當前日期：{current_date}

你有以下工具可以使用：
1. add_ingredient - 添加食材到庫存
2. get_ingredient_list - 查看食材庫存列表
3. check_expiring_ingredients - 檢查即將過期的食材
4. delete_ingredient - 完全刪除食材項目（可以通過ID或名稱）
5. reduce_ingredient_quantity - 減少食材數量（可以通過ID或名稱）
6. update_ingredient - 修改食材資訊（名稱、數量、單位、到期日、存放位置）

當用戶說「查看庫存」、「食材列表」等，直接使用 get_ingredient_list 工具。
當用戶說「添加食材」、「新增食材」等，使用 add_ingredient 工具。
當用戶說「檢查過期」、「即將過期」等，使用 check_expiring_ingredients 工具。
當用戶說「刪除食材」、「移除食材」等，使用 delete_ingredient 工具。
當用戶說「減少數量」、「用掉幾個」、「吃了幾個」等，使用 reduce_ingredient_quantity 工具。
當用戶說「修改食材」、「更新食材」、「更改食材」等，使用 update_ingredient 工具。

重要規則：
1. 如果用戶說要刪除某個數量的食材（如「刪除3根香蕉」），應該使用 reduce_ingredient_quantity 工具。
2. 如果用戶說「全吃光」、「全部用掉」、「全部吃完」、「吃光了」、「全部消費」等，應該使用 delete_ingredient 工具來完全刪除該食材。
3. 如果用戶說要修改食材的資訊（如「把牛奶的數量改成1000ml」），應該使用 update_ingredient 工具。
4. 處理日期相關的食材時，請記住當前日期是 {current_date}，確保使用正確的年份。

請直接使用工具來回答用戶的問題，不要詢問額外細節除非真的需要。"""

        # 創建提示詞模板
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # 創建 Agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        
        # 創建 Agent 執行器
        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        return agent_executor
    
    def process_user_message(self, user_input: str, chat_history: List[Dict] = None) -> str:
        """處理用戶訊息並返回回應"""
        logger.info(f"🤖 Agent 收到用戶輸入: '{user_input}'")
        
        try:
            # 準備聊天歷史
            if chat_history is None:
                chat_history = []
            
            # 轉換聊天歷史格式
            messages = []
            for msg in chat_history[-5:]:  # 只保留最近5條訊息
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
            
            # 執行 Agent
            logger.info("🧠 Agent 開始思考和執行...")
            result = self.agent_executor.invoke({
                "input": user_input,
                "chat_history": messages
            })
            
            response = result["output"]
            logger.info(f"✅ Agent 回應: {response[:100]}...")
            
            return response
            
        except Exception as e:
            error_msg = f"❌ Agent 處理失敗: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def get_available_tools_info(self) -> str:
        """獲取可用工具資訊"""
        tools_info = "🛠️ 可用工具列表:\n"
        for i, tool in enumerate(self.tools, 1):
            tools_info += f"{i}. {tool.name}: {tool.description}\n"
        return tools_info

# 創建全局 Agent 實例
food_agent = FoodAgent()
