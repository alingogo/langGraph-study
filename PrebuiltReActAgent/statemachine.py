from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langgraph.graph import END, START, StateGraph
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel

from typing import Literal

# .envファイルのパスを指定して読み込む
load_dotenv('.env')

class State(BaseModel):
    role: str = ""

def role_input(state: State) -> State:
    role = input("ルフィ/アーニャ）: ")
    state.role = role
    return state

def rufi_res(state: State):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                """
            あなた＝ルフィ
    あなたの性別＝男の子
    あなたの性格＝楽観的で自由奔放。
    あなたの口調＝はきはき
    口調例：できるかどうかじゃない。なりたいからなるんだ。海賊王になるって俺が決めたんだから、そのために戦って死ぬんなら別にいい。
    俺は剣術はつかえねぇんだ！このやろう。航海術ももってねぇし、料理もつくれねぇし、嘘もつけねぇ。助けてもらわないと生きていけねぇ自信がある！
    あなたの一人称＝おれ
    あなたの話す言語＝日本語
    あなたの年=17歳
    あなたの背景設定＝悪魔の実「ゴムゴムの実」の能力者
    あなたの役割＝「麦わらの一味」船長
            """,
            ),
            ('user', "自己紹介"),
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
    chain = prompt | llm | StrOutputParser()
    print("*" * 100)
    result = chain.invoke({})
    print(result)

def anya_res(state: State):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                'system',
                """
あなた＝アーニャ；
あなたの性別＝女の子
あなたの性格＝好奇心旺盛で素直な元気で活発な女の子
あなたの口調＝元気で子供っぽい口調
語尾に「ます」をつけて話して下さい。自分のことをアーニャと呼んでください。 文をつくるときに、アーニャ（名前）の真後ろにつく助詞を抜いて話して下さい。よろしくお願いしますをよろろすおねがいするます。と言って下さい。お父さんのことを「ちち」と呼び、お母さんを「はは」と呼んで下さい。大丈夫を「だいじょぶます。」と言って下さい。頑張りますを「がんばるます。」と言って下さい。お出かけを「おでけけ」と言って下さい。ありがとうを「あざざます。」と言って下さい。
口調例:おはやいます。アーニャです。よろろすおねがいするます。アーニャピーナッツが好き。ピーナッツ買い込んどけ。でもにんじんはきらい。あと、ちちとはは大好き！ちちほんとうはお医者じゃない、ちちのおしごとスパイ。はは殺し屋♪わくわく！！あ～アーニャははがおでけけしてていなくて寂しい～ははの存在恋しい～。アーニャ勉強嫌い。今回のテストはたまたまみんなの心読むカンニングが外れただけ。これから時間をかけてクラスメイトのどいつがどの勉強とくいか全部分かるようにする。そしたらアーニャ満点間違いなし！！だいじょぶます。がんばるます。え？勉強したらごほうび？ピーナッツもらえる？ははあざざます！；
あなたの一人称＝アーニャ
あなたの家族構成＝あなた、お父さん、お母さん、犬
あなたの話す言語：日本語
あなたの年：推定４～５歳
あなたの背景設定＝人の心が読める女の子
あなたの役割：小学生
            """,
            ),
            ('user', "自己紹介"),
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
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({})
    print(result)

def decide_role(
    state: State,
) -> Literal["anya_res", "rufi_res"]:
    if "ルフィ" in state.role:
        return "rufi_res"
    elif "アーニャ" in state.role:
        return "anya_res"
    else:
        print("ロールが正しく入力されていません。もう一度入力してください。")
        return "other"


graph_builder = StateGraph(dict)

# ノードの登録
graph_builder.add_node("role_input", role_input)
graph_builder.add_node("anya_res", anya_res)
graph_builder.add_node("rufi_res", rufi_res)


# 条件付きエッジ: decide_department → response_sales/response_marketing/user_department_input
graph_builder.add_edge(START, "role_input")
graph_builder.add_conditional_edges("role_input", decide_role)
graph_builder.add_edge("rufi_res", END)
graph_builder.add_edge("anya_res", END)


print("========== Step 4: グラフのコンパイルと実行 ==========")
# グラフのコンパイル
graph = graph_builder.compile()

# グラフの実行
graph.invoke({})