import streamlit as st
import random

def analyze_conversation(conversation):
    """간단한 대화 분석 함수 (유머/센스 흉내내기)"""
    positive_keywords = ["축하", "기쁘", "잘 살", "행복", "예쁘", "멋지"]
    negative_keywords = ["힘들", "어렵", "눈물", "싸움", "걱정"]
    length = len(conversation.split())

    positive_count = sum(keyword in conversation for keyword in positive_keywords)
    negative_count = sum(keyword in conversation for keyword in negative_keywords)

    sentiment_score = positive_count - negative_count

    analysis_results = []
    if sentiment_score > 0:
        analysis_results.append("분위기가 아주 훈훈하네요! 🥰")
    elif sentiment_score < 0:
        analysis_results.append("음... 약간 걱정스러운 대화도 있었군요. 🤔")
    else:
        analysis_results.append("평범한 대화 속에 싹트는 우정! 🤝")

    if length > 50:
        analysis_results.append("꽤 많은 이야기를 나누셨군요! 그만큼 끈끈한 사이겠죠? 😉")
    elif length < 10:
        analysis_results.append("짧지만 강렬한 인상! 😎")

    # 임의의 유머/센스 코멘트 추가
    humor_comments = [
        "두 분, 천생연분 같아요! (제 점수는요...)",
        "이 대화... 축의금 액수를 올려야 할 것 같은데요? 😜",
        "다음 대화도 기대됩니다! (하지만 축의금은 이번에 결정하는 걸로...😅)",
        "대화 내용만 봐도 벌써 배부르네요! (하지만 봉투는 챙겨야겠죠? 💸)",
        "이 정도 대화면 거의 가족 아닌가요? 🤣"
    ]
    analysis_results.append(random.choice(humor_comments))

    return " ".join(analysis_results)

def suggest_contribution(relationship, event_type, analysis_score):
    """간단한 규칙 기반 축의금 제안 함수"""
    base_amount = 50000  # 기본 금액

    if relationship == "친한 친구":
        amount = base_amount + analysis_score * 10000 + random.randint(0, 20000)
    elif relationship == "직장 동료":
        amount = base_amount - 10000 + analysis_score * 5000 + random.randint(0, 10000)
    elif relationship == "가족":
        amount = base_amount + 20000 + analysis_score * 15000 + random.randint(0, 30000)
    else:  # 기타
        amount = base_amount - 5000 + analysis_score * 3000 + random.randint(0, 5000)

    if event_type == "결혼":
        amount += 20000
    elif event_type == "돌잔치":
        amount += 10000

    # 센스있는 마무리 멘트 추가
    if amount <= 30000:
        suggestion = f"음... 소중한 마음만으로도 충분할 거예요! 😉 (추천 금액: {amount:,}원)"
    elif 30000 < amount <= 70000:
        suggestion = f"두 분의 앞날을 축복하며... 이 정도면 어떨까요? 😊 (추천 금액: {amount:,}원)"
    else:
        suggestion = f"오래오래 행복하세요! 💖 (추천 금액: {amount:,}원)"

    return suggestion

st.title("그래서.. 얼마면 돼? 🤔")
st.subheader("당신과 상대방의 대화 내용을 분석해서 축의금을 결정해 드립니다!")

conversation = st.text_area("주고받은 대화 내용을 입력해 주세요:", height=200)

relationship = st.selectbox("두 분의 관계는?", ["친한 친구", "직장 동료", "가족", "기타"])
event_type = st.selectbox("어떤 행사에 대한 축의금을 결정하시나요?", ["결혼", "돌잔치", "생일", "집들이", "기타"])

if st.button("분석 & 축의금 결정!"):
    if conversation:
        analysis_result = analyze_conversation(conversation)
        st.subheader("대화 분석 결과:")
        st.write(analysis_result)

        # 간단한 분석 점수 (감정 점수 활용)
        analysis_score = sum(1 for word in conversation.split() if word in ["좋아", "사랑", "기대"]) - \
                         sum(1 for word in conversation.split() if word in ["힘들어", "슬퍼", "걱정"])

        suggestion = suggest_contribution(relationship, event_type, analysis_score)
        st.subheader("AI가 제안하는 축의금 액수는...")
        st.markdown(f"## 💰 {suggestion}")
    else:
        st.warning("대화 내용을 입력해 주세요!")
