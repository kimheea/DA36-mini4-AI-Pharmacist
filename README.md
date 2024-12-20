# DA36-mini4-ai-phramcist
- LLM - RAG chatbot Project
- 김해빈-김희애-조한희

## 1. 프로젝트 개요
***구현 목표 : 임산부를 위한 복용 가능 약물 검색***
### 1. 정보신뢰성
![image](https://github.com/user-attachments/assets/19b5338a-001b-4dd0-b9e1-b78d981d0337)

### 2. 시장분석
![image](https://github.com/user-attachments/assets/2135a49b-ce6e-4579-aab9-5faa6878817d)

### 3. LLM-RAG 한계
![image](https://github.com/user-attachments/assets/f826fee9-a19d-4d27-9911-be3e3e7d7e1f)

#### 예시)
![image](https://github.com/user-attachments/assets/872c65b8-0daf-4b9a-96f0-ba4fbf9ebbcb)
실제 제품명을 chat-gpt한테 물어보면 틀린 정보를 제공

## 구현과정
### 1. DATA
CSV1 = 의약품통합정보시스템 크롤링(약 제품명, 성분, 용법용량, 병용금지, 등 정보 포힘)
CSV2 = 건강보험심사평가원 : 의약품안전사용서비스 DUR  의약품 목록(임산부 금기)

### 2. User Journey
![image](https://github.com/user-attachments/assets/5b4477b3-5a7c-47a9-ac43-f9f4f1d7de87)

### 3-1. Model structure
![image](https://github.com/user-attachments/assets/87d464a3-63cf-455d-920f-c529273fbd6d)

### 3-2. 내부 로직
![RAG_](https://github.com/user-attachments/assets/fe5002f8-4d96-41ab-9596-3a8a0faba6b0)
두 개의 csv 파일을 전처리
pinecone 내부 vectorDB 저장, 질문 조회
유사도 기반 데이터 조회 + LLM(prompt)
user의 질의응답

### 4. 시연
![image](https://github.com/user-attachments/assets/ffa62269-aed5-408a-821a-42dfacc79131)

약물명 입력 후 질문을 하면 해당 약물에 대한 설명 출력

## 결론
### 기대효과
편의성 : 임산부가 쉽고 빠르게 약물 복용 가능 여부 확인할 수 있다.
전문성 : 해당 약물에 성분, 용법용량, 병용금지 약물, 사용상의 주의사항 등 정보 취득이 가능하다.
