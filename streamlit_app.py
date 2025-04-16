import streamlit as st
import re
from datetime import datetime
import random
import base64

# 페이지 설정
st.set_page_config(
    page_title="축의금 마법사 AI",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 사용자 정의 CSS
def add_bg_from_local(color):
    custom_css = f"""
    <style>
    .stApp {{
        background-color: {color};
        background-size: cover;
    }}
    
    .main-title {{
        text-align: center;
        font-size: 2.5rem;
        color: white;
        margin-bottom: 1rem;
        font-weight: bold;
    }}
    
    .subtitle {{
        text-align: center;
        font-size: 1rem;
        color: #E0E0FF;
        margin-bottom: 2rem;
    }}
    
    .result-box {{
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }}
    
    .highlight {{
        font-weight: bold;
        color: #FFD700;
    }}
    
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }}
    
    .stDateInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }}
    
    .stTextArea > div > div > textarea {{
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
    }}
    
    .stButton > button {{
        background-color: #9370DB;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background-color: #8A2BE2;
    }}
    
    .emoji-title {{
        font-size: 3rem;
        text-align: center;
        margin-bottom: 0;
    }}
    
    .recommendation {{
        font-size: 1.5rem;
        color: #FFD700;
        text-align: center;
        margin: 1rem 0;
    }}
    
    .explanation {{
        font-size: 1rem;
        color: white;
        margin: 1rem 0;
    }}
    
    .funny-note {{
        font-style: italic;
        color: #E0E0FF;
        margin-top: 1rem;
        text-align: center;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# 배경색 설정
add_bg_from_local("#2E1A47")

# 타이틀 및 소개
st.markdown("<div class='emoji-title'>💸</div>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>축의금 마법사 AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>대화 내용을 분석해서 딱 맞는 축의금을 알려드려요 ✨</p>", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.title("📝 도움말")
    st.write("1️⃣ 축의금을 보낼 상대방과의 대화 내용을 입력하세요.")
    st.write("2️⃣ 간단한 관계 정보를 선택하세요.")
    st.write("3️⃣ '분석하기' 버튼을 누르면 AI가 최적의 축의금을 추천해드립니다.")
    st.write("4️⃣ 결과는 재미로만 봐주세요! 😉")

# 입력 폼
with st.form(key='chat_form'):
    col1, col2 = st.columns(2)
    
    with col1:
        event_type = st.selectbox(
            "🎊 어떤 경조사인가요?",
            ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"]
        )
    
    with col2:
        relationship = st.selectbox(
            "👥 상대방과의 관계는?",
            ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"]
        )
    
    conversation = st.text_area(
        "💬 대화 내용을 복사해서 붙여넣으세요",
        height=200,
        placeholder="카카오톡, 문자, SNS 등의 대화 내용을 붙여넣으세요. 내용이 많을수록 정확도가 올라갑니다!"
    )
    
    submit_button = st.form_submit_button(label='✨ 분석하기')

# 대화 분석 함수
def analyze_conversation(conversation, event_type, relationship):
    # 분석 결과 생성 (재미있게)
    
    # 1. 대화량 분석
    chat_length = len(conversation)
    
    # 2. 이모티콘/이모지 수 분석
    emoji_count = len(re.findall(r'[^\w\s,.]', conversation))
    
    # 3. 웃음 표현 분석
    laugh_count = len(re.findall(r'ㅋ+|ㅎ+|😂|🤣', conversation))
    
    # 4. 친밀도 점수 계산
    intimacy_score = min(100, chat_length // 50 + emoji_count * 2 + laugh_count * 3)
    
    # 5. 특별 키워드 검색 (식사, 만남 등)
    meet_count = len(re.findall(r'만나|식사|밥|술|커피|점심|저녁|아침|브런치|모임', conversation))
    
    # 6. 대화 기간 추정 (날짜 언급 횟수)
    dates_mentioned = len(re.findall(r'\d{1,2}월|\d{1,2}일|\d{4}년|주말|휴일|평일', conversation))
    
    # 기본 추천 금액 설정 (행사 유형에 따라)
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
    
    # 관계에 따른 가중치
    relationship_factors = {
        "친구": 1.2,
        "회사동료": 1.0,
        "선후배": 1.1,
        "가족/친척": 1.5,
        "지인": 0.8,
        "SNS친구": 0.5
    }
    
    # 최종 추천 금액 계산
    base_amount = base_amounts[event_type]
    relationship_factor = relationship_factors[relationship]
    
    # 친밀도와 만남 횟수에 따른 조정
    intimacy_factor = 0.5 + (intimacy_score / 100)
    meet_factor = 1.0 + (meet_count * 0.05)
    
    # 최종 금액 계산 (재미있게 약간의 랜덤성 추가)
    final_amount = int(base_amount * relationship_factor * intimacy_factor * meet_factor)
    
    # 금액 반올림 (만원 단위로)
    final_amount = round(final_amount / 10000) * 10000
    
    # 최소/최대 금액 제한
    if final_amount < 10000:
        final_amount = 10000
    elif final_amount > 200000:
        final_amount = 200000
    
    # 분석 결과 메시지 생성
    analysis_results = {
        "amount": final_amount,
        "intimacy_score": intimacy_score,
        "laugh_score": laugh_count,
        "emoji_score": emoji_count,
        "meet_count": meet_count,
        "special_factors": []
    }
    
    # 특별 요인 추가 (재미 요소)
    if "고마워" in conversation or "감사" in conversation:
        analysis_results["special_factors"].append("감사 표현이 많음 (+5,000원)")
        analysis_results["amount"] += 5000
    
    if "언제" in conversation and "보" in conversation:
        analysis_results["special_factors"].append("만남 약속 시도 (+3,000원)")
        analysis_results["amount"] += 3000
    
    if laugh_count > 20:
        analysis_results["special_factors"].append("웃음 폭탄이 많음 (+2,000원)")
        analysis_results["amount"] += 2000
    
    if emoji_count > 15:
        analysis_results["special_factors"].append("이모지 남용러 (+2,000원)")
        analysis_results["amount"] += 2000
    
    # 재미있는 메시지 추가
    funny_messages = [
        f"이 금액이면 다음에 만났을 때 밥은 살 수 있어요!",
        f"이 정도면 체면은 지킬 수 있어요~ 아마도...",
        f"축의금이 이것보다 적으면 카톡 차단당할 확률 78.4%!",
        f"이 금액은 당신의 케케묵은 우정을 지킬 수 있는 최소 금액입니다.",
        f"더 내면 '너무 많이 줬어' 덜 내면 '뭐야 이거'",
        f"정확히 이 금액이면 상대방 표정에서 '오오~' 효과를 볼 수 있어요!",
        f"이 금액이면 상대방 부모님도 '저 친구 괜찮네~'라고 할 거예요.",
        f"계좌이체시 메모에 '축하해~'는 필수, 이모티콘은 +3,000원 효과!"
    ]
    
    analysis_results["funny_message"] = random.choice(funny_messages)
    
    return analysis_results

# 결과 출력
if submit_button and conversation:
    st.markdown("<hr>", unsafe_allow_html=True)
    
    with st.spinner('🧙‍♂️ 축의금 마법사가 열심히 분석 중입니다...'):
        # 효과를 위한 지연
        import time
        time.sleep(1.5)
        
        # 분석 결과
        results = analyze_conversation(conversation, event_type, relationship)
        
        # 결과 표시 애니메이션
        st.balloons()
        
        # 예쁘게 결과 표시
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        
        # 축의금 추천 금액
        st.markdown(f"<h2 class='recommendation'>💰 추천 축의금: {results['amount']:,}원</h2>", unsafe_allow_html=True)
        
        # 분석 이유 설명
        st.markdown("<h3>🔍 이렇게 분석했어요</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"🤝 관계: <span class='highlight'>{relationship}</span>", unsafe_allow_html=True)
            st.markdown(f"🎭 친밀도 점수: <span class='highlight'>{results['intimacy_score']}/100</span>", unsafe_allow_html=True)
            st.markdown(f"😂 웃음 표현: <span class='highlight'>{results['laugh_score']}회</span>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"🎁 행사 유형: <span class='highlight'>{event_type}</span>", unsafe_allow_html=True)
            st.markdown(f"😊 이모지 횟수: <span class='highlight'>{results['emoji_score']}개</span>", unsafe_allow_html=True)
            st.markdown(f"🍽️ 만남/식사 언급: <span class='highlight'>{results['meet_count']}회</span>", unsafe_allow_html=True)
        
        # 특별 요인
        if results["special_factors"]:
            st.markdown("<h3>✨ 특별 가산점</h3>", unsafe_allow_html=True)
            for factor in results["special_factors"]:
                st.markdown(f"• {factor}", unsafe_allow_html=True)
        
        # 재미있는 메시지
        st.markdown(f"<p class='funny-note'>💡 {results['funny_message']}</p>", unsafe_allow_html=True)
        
        # 면책 문구
        st.markdown("<p class='funny-note'>⚠️ 이 결과는 100% 과학적이고 진지합니다... 라고 하면 거짓말이겠죠? 재미로만 봐주세요!</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# 추가 정보
st.markdown("<br>", unsafe_allow_html=True)
expander = st.expander("💡 알아두세요!")
with expander:
    st.markdown("""
    - 축의금은 정해진 규칙이 없어요. 자신의 경제 상황과 관계를 고려하세요.
    - 직장 동료는 보통 5~10만원, 친한 친구는 5~10만원, 친척은 관계에 따라 10~30만원이 일반적입니다.
    - 축의금보다 마음이 더 중요해요! 진심 어린 축하 메시지를 잊지 마세요.
    """)

# 푸터
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 0.8rem;'>© 2025 축의금 마법사 AI - 언제나 당신의 지갑을 지켜드립니다 💰</p>", unsafe_allow_html=True)
