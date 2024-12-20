import streamlit as st
import time
from rag import *  # 필요한 모듈 가져오기

st.title("💊AI Pharmacist💊")
st.write("약 복용 고민을 작성하면 AI 약사가 상담을 해드립니다 ☺️")

# 초기 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요. 무엇을 도와드릴까요?"}]
if "chat_active" not in st.session_state:
    st.session_state.chat_active = True  # 상담 활성화 상태
if "question_count" not in st.session_state:
    st.session_state.question_count = 0  # 질문 횟수 초기화

# 사이드바 약물 이름 입력
with st.sidebar:
    medicine_name = st.text_input('약물의 이름을 입력하세요: ')
    if medicine_name:
        st.sidebar.write(f"약물명이 정상적으로 입력되었습니다: {medicine_name}")

# 기존 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 상담 종료 버튼 (질문 1회 이상 시 활성화)
if st.session_state.question_count > 0:
    if st.button("상담 종료"):
        st.session_state.chat_active = False  # 상담 비활성화

# 상담 진행
if st.session_state.chat_active:
    # 사용자 입력
    question = st.text_input("메세지를 입력하세요", key=f"user_input_{len(st.session_state.messages)}")

    if question:
        # 사용자 메시지 저장
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)

        # 질문 횟수 증가
        st.session_state.question_count += 1

        # 챗봇 로딩 메시지
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.write("답변을 작성 중입니다... 잠시만 기다려주세요 ⏳")
            time.sleep(2)  # 로딩 시간

            # AI 응답 생성
            merged_dict = merge_dict(medicine_name)
            response = ai_pharmacist(question, merged_dict)
            placeholder.empty()  # 로딩 메시지 제거
            st.write(response)

            # 챗봇 응답 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.write("상담이 종료되었습니다. 다시 상담하려면 새로고침 해주세요. 🩺")
