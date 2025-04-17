import streamlit as st
import re
import random


# 페이지 설정
st.set_page_config(
    page_title="축의금 책정기",
    page_icon="💌",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'event_type' not in st.session_state:
    st.session_state.event_type = None
if 'relationship' not in st.session_state:
    st.session_state.relationship = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = None


# 페이지 이동 함수
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

def go_to_page(page_num):
    st.session_state.page = page_num


# Google Fonts 사용한 스타일 정의 (Noto Sans KR)
def set_custom_style():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap" rel="stylesheet">
    <style>
    html, body, div, p, span, h1, h2, h3, h4, h5, h6, button, input, textarea {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    .block-container {
        background-color: #F7D358;
        border-radius: 40px;
        padding: 80px 40px;
        max-width: 800px;
        margin: 80px auto;
        box-shadow: 0 12px 60px rgba(0, 0, 0, 0.12);
    }

    .page-indicator {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }

    .indicator-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: rgba(232, 160, 47, 0.3);
        margin: 0 8px;
    }

    .active-dot {
        background-color: #E8A02F;
    }

    .result-amount {
        font-size: 80px;
        font-weight: 700;
        color: #E8A02F;
        text-align: center;
        margin: 30px 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #452c22;
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        padding: 20px 0;
        color: #6D4C41;
        opacity: 0.8;
        font-size: 14px;
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)


def show_page_indicator(current_page, total_pages=3):
    html = '<div class="page-indicator">'
    for i in range(1, total_pages + 1):
        if i == current_page:
            html += '<div class="indicator-dot active-dot"></div>'
        else:
            html += '<div class="indicator-dot"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def get_envelope_svg(width=300, height=180):
    svg = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.15"/>
            </filter>
            <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FF6B6B" />
                <stop offset="100%" stop-color="#FF8E8E" />
            </linearGradient>
        </defs>
        <rect x="20" y="20" width="260" height="140" rx="10" ry="10" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="2" filter="url(#shadow)" />
        <path d="M20,20 L150,80 L280,20" fill="none" stroke="#EEEEEE" stroke-width="2" />
        <path d="M150,90 C150,70 135,60 125,60 C110,60 102,75 102,85 C102,95 115,105 150,125 C185,105 198,95 198,85 C198,75 190,60 175,60 C165,60 150,70 150,90 Z" fill="url(#heartGradient)" />
    </svg>
    """
    return svg

def show_envelope(width=300, height=180):
    envelope_svg = get_envelope_svg(width, height)
    st.markdown(f'<div style="text-align:center;">{envelope_svg}</div>', unsafe_allow_html=True)


def analyze_conversation(conversation, event_type, relationship):
    chat_length = len(conversation)
    emoji_count = len(re.findall(r'[^\w\s,.]', conversation))
    laugh_count = len(re.findall(r'ㅋ+|ㅎ+|😂|🤣', conversation))
    positive_emotions = len(re.findall(r'좋아|축하|감사|고마워|기뻐|행복|사랑|최고|멋져', conversation))
    meet_count = len(re.findall(r'만나|봐야|보자|언제 봄|술 한잔|밥 한번|커피|점심|저녁|아침|약속', conversation))

    base_intimacy = 20
    length_factor = min(30, chat_length // 100)
    emoji_factor = min(15, emoji_count // 2)
    laugh_factor = min(15, laugh_count // 3)
    emotion_factor = min(10, positive_emotions * 2)
    meet_factor = min(10, meet_count * 2)

    intimacy_score = min(100, base_intimacy + length_factor + emoji_factor + laugh_factor + emotion_factor + meet_factor)

    base_amounts = {
        "결혼식": 50000,
        "돌잔치": 30000,
        "백일": 30000,
        "집들이": 30000,
        "생일": 20000,
        "승진": 30000,
        "개업": 50000,
        "출산": 30000
    }

    relationship_multipliers = {
        "친구": 1.2,
        "회사동료": 1.0,
        "선후배": 1.1,
        "가족/친척": 1.5,
        "지인": 0.8,
        "SNS친구": 0.6
    }

    base_amount = base_amounts[event_type]
    relation_adjusted = base_amount * relationship_multipliers[relationship]
    intimacy_multiplier = 0.7 + (intimacy_score / 100) * 0.6
    final_amount = round((relation_adjusted * intimacy_multiplier) / 10000) * 10000

    final_amount = max(10000, min(200000, final_amount))

    special_factors = []
    if "축하" in conversation or "축하해" in conversation:
        special_factors.append("축하 표현이 많아요! (+5,000원)")
        final_amount += 5000
    if meet_count >= 3:
        special_factors.append("자주 만나는 사이네요! (+3,000원)")
        final_amount += 3000
    if laugh_count > 20:
        special_factors.append("웃음이 많은 대화를 나누는 사이네요! (+2,000원)")
        final_amount += 2000
    if "선물" in conversation or "케이크" in conversation or "꽃다발" in conversation:
        special_factors.append("선물 챙겨주는 센스가 있으시네요! (+7,000원)")
        final_amount += 7000

    funny_tips = [
        f"이 금액이면 다음에 술 마실 때 '지난번에 고마웠어~' 소리를 들을 확률 78%",
        f"축의금 봉투에 작은 메모를 넣으면 호감도가 10% 상승합니다",
        f"이 금액의 ±5천원은 오차 범위입니다. 솔직히 누가 알아보겠어요?",
        f"메시지 카드에 '앞으로도 자주 보자'라고 쓰면 다음에 정말 만날 확률 상승!",
        f"축의금을 홀수로 내면 '센스있다'는 소리를 들을 수 있어요!",
        f"포장에 신경 쓰면 금액이 +3만원으로 보이는 효과가 있습니다!",
        f"정확히 이 금액이면 '오~ 딱 좋다' 하는 미묘한 표정을 볼 수 있습니다",
        f"타이밍이 중요합니다! 행사 3일 전에 보내면 '준비성 있다' 점수 +5점!"
    ]

    return {
        "amount": int(final_amount),
        "intimacy_score": intimacy_score,
        "emoji_count": emoji_count,
        "laugh_count": laugh_count,
        "meet_count": meet_count,
        "special_factors": special_factors,
        "funny_tip": random.choice(funny_tips),
        "analysis_details": {
            "대화량": f"{chat_length}자 ({length_factor}점)",
            "이모지 사용": f"{emoji_count}개 ({emoji_factor}점)",
            "웃음 표현": f"{laugh_count}회 ({laugh_factor}점)",
            "긍정 표현": f"{positive_emotions}회 ({emotion_factor}점)",
            "만남 언급": f"{meet_count}회 ({meet_factor}점)",
            "기본 점수": f"{base_intimacy}점"
        }
    }


# 페이지 구성 함수들
def show_start_page():
    show_envelope(width=500, height=240)
    st.markdown("### 당신의 마음을 금액으로 표현해드립니다 ♥")
    if st.button("🎉 축의금 책정 시작하기"):
        next_page()

def show_input_page():
    st.subheader("🎁 축의금 정보를 입력해주세요")
    event_type = st.selectbox("행사 유형", ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"])
    relationship = st.selectbox("관계", ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"])
    conversation = st.text_area("대화 내용 (카톡 등 복사)", height=200)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전"):
            prev_page()
    with col2:
        if st.button("분석하기"):
            if not conversation:
                st.error("대화 내용을 입력해주세요.")
            else:
                st.session_state.event_type = event_type
                st.session_state.relationship = relationship
                st.session_state.conversation = conversation
                with st.spinner("분석 중..."):
                    st.session_state.analysis_results = analyze_conversation(conversation, event_type, relationship)
                    next_page()

def show_result_page():
    results = st.session_state.analysis_results
    if not results:
        st.error("분석 결과가 없습니다.")
        return

    st.subheader("🎉 축의금 분석 결과")
    st.markdown(f"**{results['amount']:,}원**")
    st.progress(results["intimacy_score"] / 100)

    st.markdown("### 📊 분석 요약")
    for key, val in results["analysis_details"].items():
        st.markdown(f"- {key}: {val}")

    if results["special_factors"]:
        st.markdown("### 💡 특별 요인")
        for item in results["special_factors"]:
            st.markdown(f"- {item}")

    st.markdown(f"💌 {results['funny_tip']}")

    if st.button("← 다시하기"):
        go_to_page(1)


def main():
    set_custom_style()
    show_page_indicator(st.session_state.page)

    if st.session_state.page == 1:
        show_start_page()
    elif st.session_state.page == 2:
        show_input_page()
    elif st.session_state.page == 3:
        show_result_page()

    st.markdown('<div class="footer">© 2025 축의금 책정기</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
