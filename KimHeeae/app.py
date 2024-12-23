import streamlit as st
import random
from rag import ai_pharmacist

st.title("💊AI Medicine💊")
st.write("약 복용 고민을 작성하면 AI 약사가 상담을 해드립니다 ☺️")

with st.sidebar:
    st.text_input('약물의 이름을 입력하세요.')


with st.chat_message("assistant"):
    st.write("안녕하세요.")

prompt = st.text_input("메세지 입력하세요.")
if prompt:
    response = ai_pharmacist()
    st.write(f"당신 : {prompt}")


