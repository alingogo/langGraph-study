from langchain_community.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
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
            """
        与えられたメッセージに従って計算処理を呼び出してください

        """,
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
# 2 定義した関数をLLMの実行に紐づける
chain = prompt | llm.bind_tools([add])
result = chain.invoke({'messages': ['2000 + 23']})
# result = chain.invoke({'messages': ['hello world']}) # output: result.tool_calls -> IndexError: list index out of range

# 引数のみで呼び出す
print(add.invoke(result.tool_calls[0]['args'])) # output: 2025
# 3 LLMから呼び出された関数を実際に実行する
print(add.invoke(result.tool_calls[0])) # output: content='2025' name='add' tool_call_id='call_gvxfJGwhPPa7mOtl8Rt6Fegv'