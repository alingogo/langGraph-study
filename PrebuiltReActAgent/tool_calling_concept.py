from langchain_community.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# .envファイルのパスを指定して読み込む
load_dotenv('.env')

# toolの定義
@tool
def add(a: int, b: int) -> int:
    """2つの値を足し算して返す"""
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
# bind_toolsでLLMモデルとtoolを紐づける
chain = prompt | llm.bind_tools([add])
# LLMから関数の呼び出し結果を取得
result = chain.invoke({'messages': ['3 + 4']})

# 引数のみで呼び出す
print(add.invoke(result.tool_calls[0]['args']))
# LLMからtool_callの値をそのままadd関数に渡して関数を実行
print(add.invoke(result.tool_calls[0]))