import streamlit as st
from langchain_openai import ChatOpenAI
import os

# Streamlit 앱 제목
st.titles("LangChain 기반 관광지 추천 앱")

# API 키 입력
#openai_api_key = 'sk-9MjbuX-2WHBQyfC0k-EI0cpWwgp6r__w75Qqg-xBmRT3BlbkFJbdEIdb0U_kIE1jakSyo-Kq6BeKzdTZH0TgR5GkjxQA'
openai_api_key='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'


if openai_api_key:
    os.environ['OPENAI_API_KEY'] = openai_api_key
    llm = ChatOpenAI(model="gpt-4o")

    # 버튼으로 주요 도시 선택
    st.subheader("빠른 선택을 위해 아래 버튼을 클릭하세요:")
    col1, col2, col3 = st.columns(3)

    selected_city = None  # 선택된 도시를 저장할 변수

    with col1:
        if st.button("서울"):
            selected_city = "서울"
    with col2:
        if st.button("부산"):
            selected_city = "부산"
    with col3:
        if st.button("제주"):
            selected_city = "제주"

    # 사용자 입력 박스
    st.subheader("도시를 직접 입력하세요:")
    target = st.text_input("도시 이름 (버튼 클릭 시 무시됨)", value="")

    # 버튼 선택이 우선, 그다음 입력값
    city = selected_city if selected_city else target

    if city and st.button("추천 받기"):
        msg = f"{city} 대표적 관광지 3군데는?"
        try:
            result = llm.invoke(msg)
            st.success(f"{city}의 추천 관광지:")
            st.write(result)
        except Exception as e:
            st.error(f"오류 발생: {e}")
else:
    st.info("API Key를 입력해야 LangChain 서비스를 이용할 수 있습니다.")
