import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import os

# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = "sk-9MjbuX-2WHBQyfC0k-EI0cpWwgp6r__w75Qqg-xBmRT3BlbkFJbdEIdb0U_kIE1jakSyo-Kq6BeKzdTZH0TgR5GkjxQA"  # 여기에 OpenAI API 키를 입력하세요

# Streamlit 페이지 설정
st.set_page_config(page_title="협상 시뮬레이션", layout="wide")

# OpenAI 모델 설정
llm = ChatOpenAI(temperature=0.7)

# 협상 프롬프트 생성
negotiation_prompt = PromptTemplate(
    input_variables=["item", "goal", "context", "user_response"],
    template="""\
당신은 협상 전문가입니다. 현재 사용자는 {item}에 대해 협상을 진행하고 있으며, 목표는 {goal}입니다.
다음은 협상 상황에 대한 컨텍스트입니다:
{context}

이제 당신은 '상대방' 역할을 맡아 사용자와 협상을 진행합니다. 사용자(구매자)가 마지막에 말한 내용은 다음과 같습니다:
"{user_response}"

사용자의 발언에 응답하며 다음 협상 단계를 이어가세요.
"""
)

# LLMChain 생성
negotiation_chain = LLMChain(
    llm=llm,
    prompt=negotiation_prompt,
    verbose=True
)

# 초기값 설정
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []  # 대화 기록 초기화
if "user_response" not in st.session_state:
    st.session_state.user_response = "1,000만 원은 너무 부담스럽습니다. 가격 조정 가능할까요?"

# 입력 필드 및 버튼
st.title("🛠 협상 시뮬레이션")
st.subheader("AI와 실시간 협상을 진행하세요!")

# 사용자 입력 필드
user_response = st.text_input(
    "구매자 (사용자)의 입력:", 
    value=st.session_state.user_response,
    key="user_input"
)

# 기본 협상 상황 설정
context = "중고차 가격은 1,000만 원이며, 목표는 850만 원으로 낮추는 것입니다."
item = "중고차 구매"
goal = "가격 850만 원으로 낮추기"

# "대화 시작" 버튼
if st.button("응답 생성"):
    # AI 응답 생성
    response = negotiation_chain.run({
        "item": item,
        "goal": goal,
        "context": context,
        "user_response": user_response,
    })

    # 대화 기록 추가
    st.session_state.conversation_history.append({
        "user": user_response,
        "ai": response
    })

    # 사용자 입력 필드 초기화
    st.session_state.user_response = ""

# 대화 기록 출력
st.write("### 대화 기록")
for i, entry in enumerate(st.session_state.conversation_history, 1):
    st.write(f"**[대화 {i}]**")
    st.write(f"- 사용자 (구매자): {entry['user']}")
    st.write(f"- 상대방 (판매자): {entry['ai']}")

# "종료" 버튼
if st.button("협상 종료"):
    st.write("### 협상이 종료되었습니다. 대화 기록은 다음과 같습니다:")
    for i, entry in enumerate(st.session_state.conversation_history, 1):
        st.write(f"**[대화 {i}]**")
        st.write(f"- 사용자 (구매자): {entry['user']}")
        st.write(f"- 상대방 (판매자): {entry['ai']}")
    st.session_state.conversation_history = []  # 대화 기록 초기화