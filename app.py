import streamlit as st
from PIL import Image
import requests
from io import BytesIO
# from ai_medicine_rag import ai_medicine_rag


# 제목과 설명
st.title("💊AI Pharmacist💊")
st.write("약 복용 고민을 작성하면 AI 약사가 상담을 해드립니다 ☺️")