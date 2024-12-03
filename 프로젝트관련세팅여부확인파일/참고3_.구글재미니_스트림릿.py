import streamlit as st
import google.generativeai as genai
import os

# Google Generative AI API 키 설정
key = 'AIzaSyC8bNIQpP4Y_ITzqCsofhca-rW7ykJ2csU'  # 여기에 API 키 입력
genai.configure(api_key=key)

# Streamlit 페이지 설정
st.set_page_config(page_title="Google Generative AI Demo", layout="wide")
st.title("🧠 Google Generative AI Demo")
st.subheader("gemini-1.5-flash-latest 모델로 텍스트 생성")

# 모델 정보 설정
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# 사용자 입력
st.write("**텍스트 생성 요청:**")
prompt = st.text_input("생성할 텍스트에 대한 요청을 입력하세요", value="인공지능에 대해 한 문장으로 설명하세요.")

# 버튼 클릭 시 AI 응답 생성
if st.button("텍스트 생성"):
    if prompt:
        with st.spinner("AI 응답 생성 중..."):
            try:
                response = model.generate_content(prompt)
                st.success("생성 완료!")
                st.write(f"**AI 응답:**\n{response.text}")
            except Exception as e:
                st.error(f"에러 발생: {e}")
    else:
        st.warning("요청 문장을 입력하세요.")

# 모델 리스트 표시
if st.button("모델 목록 보기"):
    with st.spinner("모델 목록 가져오는 중..."):
        try:
            models = list(genai.list_models())
            st.success("모델 목록 가져오기 완료!")
            st.write("**사용 가능한 모델:**")
            for model_info in models:
                st.write(f"- {model_info['name']}")
        except Exception as e:
            st.error(f"에러 발생: {e}")
