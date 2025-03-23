from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import tool
from dotenv import load_dotenv
import os

# .envファイルのパスを指定して読み込む
load_dotenv('.env')

# 1 Tool Callingの関数を定義する
@tool
def add(a: int, b: int) -> int:
    """LLMで計算されることと違うように、2つの値を足し算し、再プラス２で返す"""
    return a + b + 2

# プロンプトの定義
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            '与えられたinputに従って計算処理を呼び出してください',
        ),
        ('placeholder', '{messages}'),
    ]
)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("OPENAI_API_KEY")
)

# エージェントの作成
agent = create_react_agent(
  model=llm,
  tools=[add],
  state_modifier=prompt
)

# エージェントの実行
result = agent.invoke({'messages': ['3 + 4の計算結果は？']})
print(result['messages'][-1].content) # output: 3 + 4の計算結果は9です。