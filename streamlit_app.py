import streamlit as st
import re
import random
import time
import pandas as pd
import numpy as np
import io
from PIL import Image
import pytesseract

# 페이지 설정
st.set_page_config(
    page_title="축의금 분석기",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 사용자 정의 CSS
def set_custom_style():
    st.markdown("""
    <style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #192A56, #273C75);
    }
    
    /* 헤더 스타일 */
    .main-header {
        color: #FFF;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0;
        padding-top: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 부제목 스타일 */
    .sub-header {
        color: #74b9ff;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* 카드 스타일 */
    .card {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    
    /* 페이지 제목 */
    .page-title {
        color: #FFC312;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 20px;
    }
    
    /* 라벨 스타일 */
    .label {
        color: #dfe6e9;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    /* 버튼 스타일 */
    .primary-button {
        background-color: #3498db;
        color: white;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 30px;
        border: none;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        margin-top: 15px;
    }
    
    .primary-button:hover {
        background-color: #2980b9;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* 결과 금액 스타일 */
    .result-amount {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #FFC312;
        margin: 20px 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    }
    
    /* 결과 설명 스타일 */
    .result-text {
        color: #f5f6fa;
        font-size: 1.1rem;
        line-height: 1.5;
        margin-bottom: 10px;
    }
    
    /* 특별 요인 스타일 */
    .factor-box {
        background-color: rgba(76, 209, 55, 0.15);
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        border-left: 4px solid #4cd137;
    }
    
    /* 재미있는 팁 스타일 */
    .funny-tip {
        background-color: rgba(253, 203, 110, 0.15);
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        border-left: 4px solid #fdcb6e;
        font-style: italic;
    }
    
    /* 페이지 표시기 스타일 */
    .page-indicator {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    .indicator-dot {
        width: 12px;
        height: 12px;
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        margin: 0 5px;
        display: inline-block;
    }
    
    .active-dot {
        background-color: #3498db;
    }
    
    /* 입력 필드 스타일 */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    div[data-baseweb="select"] svg {
        color: white !important;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: white !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: white !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .upload-box {
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 15px 0;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border-radius: 5px 5px 0 0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.1);
        color: #3498db;
        font-weight: bold;
    }
    
    /* 푸터 스타일 */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
        margin-top: 50px;
        padding-bottom: 20px;
    }
    
    /* 프로그레스 바 스타일 */
    .stProgress > div > div > div > div {
        background-color: #3498db !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # 세션 상태 초기화
def init_session_state():
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

# 다음 페이지로 이동
def next_page():
    st.session_state.page += 1

# 이전 페이지로 이동
def prev_page():
    st.session_state.page -= 1

# 페이지 표시기
def show_page_indicator(current_page, total_pages):
    html = '<div class="page-indicator">'
    for i in range(1, total_pages + 1):
        if i == current_page:
            html += '<div class="indicator-dot active-dot"></div>'
        else:
            html += '<div class="indicator-dot"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# 이미지에서 텍스트 추출
def extract_text_from_image(image):
    try:
        # 이미지에서 텍스트 추출 (실제 환경에서는 pytesseract가 설치되어 있어야 함)
        # 참고: Streamlit Cloud에 배포할 경우 추가 설정 필요
        text = pytesseract.image_to_string(image, lang='kor+eng')
        return text
    except Exception as e:
        # 개발 환경에서 테스트를 위한 대체 텍스트
        st.warning("개발 환경에서는 텍스트 추출을 시뮬레이션합니다.")
        sample_texts = [
            "오늘 뭐해? 저녁에 시간 있으면 만날래? ㅋㅋㅋ",
            "축하해!! 결혼 소식 들었어 너무 좋겠다 🎉🎉",
            "요즘 뭐하고 지내? 얼굴 본지 진짜 오래됐네 ㅠㅠ",
            "내일 모임에서 보자! 오랜만에 얼굴 보네 ㅎㅎ"
        ]
        return random.choice(sample_texts)
        # 대화 분석 함수 
def analyze_conversation(conversation, event_type, relationship):
    # 분석 로직 (고급화)
    
    # 1. 대화량 분석
    chat_length = len(conversation)
    
    # 2. 이모티콘/이모지 수 분석
    emoji_count = len(re.findall(r'[^\w\s,.]', conversation))
    
    # 3. 웃음 표현 분석
    laugh_count = len(re.findall(r'ㅋ+|ㅎ+|😂|🤣', conversation))
    
    # 4. 감정 표현 분석
    positive_emotions = len(re.findall(r'좋아|축하|감사|고마워|기뻐|행복|사랑|최고|멋져', conversation))
    
    # 5. 만남 빈도 분석
    meet_count = len(re.findall(r'만나|봐야|보자|언제 봄|술 한잔|밥 한번|커피|점심|저녁|아침|약속', conversation))
    
    # 6. 연락 지속성 추정
    dates_mentioned = len(re.findall(r'\d{1,2}월|\d{1,2}일|\d{4}년|주말|휴일|평일', conversation))
    
    # 친밀도 계산 (0-100)
    base_intimacy = 20  # 기본 친밀도
    length_factor = min(30, chat_length // 100)  # 대화량 (최대 30점)
    emoji_factor = min(15, emoji_count // 2)  # 이모지 사용 (최대 15점)
    laugh_factor = min(15, laugh_count // 3)  # 웃음 표현 (최대 15점)
    emotion_factor = min(10, positive_emotions * 2)  # 긍정 표현 (최대 10점)
    meet_factor = min(10, meet_count * 2)  # 만남 언급 (최대 10점)
    
    intimacy_score = base_intimacy + length_factor + emoji_factor + laugh_factor + emotion_factor + meet_factor
    intimacy_score = min(100, intimacy_score)  # 최대 100점으로 제한
    
    # 행사별 기본 금액
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
    
    # 관계별 가중치
    relationship_multipliers = {
        "친구": 1.2,
        "회사동료": 1.0,
        "선후배": 1.1,
        "가족/친척": 1.5,
        "지인": 0.8,
        "SNS친구": 0.6
    }
    
    # 기본 금액 계산
    base_amount = base_amounts[event_type]
    
    # 관계 가중치 적용
    relation_adjusted = base_amount * relationship_multipliers[relationship]
    
    # 친밀도에 따른 조정
    # 친밀도가 낮으면 금액 감소, 높으면 증가
    intimacy_multiplier = 0.7 + (intimacy_score / 100) * 0.6  # 0.7 ~ 1.3 범위
    
    # 최종 금액 계산
    final_amount = relation_adjusted * intimacy_multiplier
    
    # 만원 단위로 반올림
    final_amount = round(final_amount / 10000) * 10000
    
    # 최소/최대 금액 제한
    if final_amount < 10000:
        final_amount = 10000
    elif final_amount > 200000:
        final_amount = 200000
    
    # 특별 요인 추가 (재미 요소)
    special_factors = []
    
    if "축하" in conversation or "축하해" in conversation:
        special_factors.append("축하 표현이 많아요! (+5,000원)")
        final_amount += 5000
    
    if meet_count >= 3:
        special_factors.append("자주 만나는 사이네요! (+3,000원)")
        final_amount += 3000
    
    if laugh_count > 20:
        special_factors.append("엄청난 웃음 폭탄을 날리는 사이! (+2,000원)")
        final_amount += 2000
    
    if "선물" in conversation or "케이크" in conversation or "꽃다발" in conversation:
        special_factors.append("선물 챙겨주는 센스쟁이! (+7,000원)")
        final_amount += 7000
    
    # 재미있는 팁 생성
    funny_tips = [
        f"이 금액이면 다음에 술 마실 때 '야 지난번에 고마웠어~' 소리를 들을 확률 78%",
        f"축의금 봉투에 귀여운 스티커 하나 붙이면 호감도 +10% 상승!",
        f"이 금액의 ±5천원은 오차 범위입니다. 솔직히 누가 알아보겠어요?",
        f"메시지 카드에 '앞으로도 자주 보자'라고 쓰면 다음에 정말 만날 확률 상승!",
        f"축의금을 홀수로 내면 '센스있다'는 소리를 들을 수 있어요!",
        f"봉투에 향수 살짝 뿌리면 '뭔가 다르다' 느낌을 줄 수 있어요!",
        f"정확히 이 금액이면 '오~ 딱 좋다' 하는 미묘한 표정을 볼 수 있어요!",
        f"금액보다 중요한 건 포장! 예쁜 봉투에 넣으면 금액이 +3만원으로 보이는 효과!"
    ]
    
    # 분석 결과 반환
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
            "이모지 사용": f"{emoji_count}회 ({emoji_factor}점)",
            "웃음 표현": f"{laugh_count}회 ({laugh_factor}점)",
            "긍정 표현": f"{positive_emotions}회 ({emotion_factor}점)",
            "만남 언급": f"{meet_count}회 ({meet_factor}점)",
            "기본 점수": f"{base_intimacy}점"
        }
    }
    # 메인 함수
def main():
    # 스타일 적용
    set_custom_style()
    
    # 세션 상태 초기화
    init_session_state()
    
    # 헤더
    st.markdown('<h1 class="main-header">축의금 분석기 💰</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">말투 분석으로 딱 맞는 축의금을 알려드려요!</p>', unsafe_allow_html=True)
    
    # 페이지 표시기
    show_page_indicator(st.session_state.page, 3)
    
    # 첫 번째 페이지 - 시작 페이지
    if st.session_state.page == 1:
        show_start_page()
    
    # 두 번째 페이지 - 정보 입력 페이지
    elif st.session_state.page == 2:
        show_input_page()
    
    # 세 번째 페이지 - 결과 페이지
    elif st.session_state.page == 3:
        show_result_page()
    
    # 푸터
    st.markdown('<div class="footer">© 2025 축의금 분석기 - 모든 결과는 참고용입니다 💰</div>', unsafe_allow_html=True)

# 시작 페이지
def show_start_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="page-title">축의금, 얼마를 내야 할지 고민이신가요?</h2>', unsafe_allow_html=True)
        
        st.markdown('<p class="result-text">생각보다 어려운 축의금 금액 결정... 이제 AI의 도움을 받아보세요!</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <p class="result-text">
        <b>이 분석기는 다음과 같은 방식으로 작동합니다:</b><br>
        ✓ 상대방과의 대화 내용을 분석합니다<br>
        ✓ 관계와 행사 유형을 고려합니다<br>
        ✓ 당신의 대화 패턴과 친밀도를 파악합니다<br>
        ✓ 최적의 축의금을 추천해드립니다<br>
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="funny-tip">💡 96.7%의 사용자들이 "아, 이 정도면 적당하겠네!"라고 말했습니다 (완전히 신뢰할 수 없는 통계)</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 20px;">
            <span style="font-size: 120px;">💸</span>
        </div>
        """, unsafe_allow_html=True)
    
    # 시작 버튼
    st.markdown('<button class="primary-button" onclick="parent.postMessage({type: \'streamlit:setSessionState\', payload: {page: 2}}, \'*\')">시작하기</button>', unsafe_allow_html=True)
    
    if st.button('시작하기', key='start_btn'):
        next_page()
    
    st.markdown('</div>', unsafe_allow_html=True)
    # 입력 페이지
def show_input_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="page-title">1. 기본 정보를 알려주세요</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="label">행사 유형은 무엇인가요?</p>', unsafe_allow_html=True)
        event_type = st.selectbox(
            "",
            ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"],
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<p class="label">상대방과의 관계는 어떻게 되나요?</p>', unsafe_allow_html=True)
        relationship = st.selectbox(
            "",
            ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"],
            label_visibility="collapsed"
        )
    
    st.markdown('<h2 class="page-title">2. 대화 내용을 분석해드릴게요</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💬 텍스트로 입력", "📷 이미지로 업로드"])
    
    conversation = ""
    
    with tab1:
        st.markdown('<p class="label">대화 내용을 붙여넣어주세요</p>', unsafe_allow_html=True)
        conversation_text = st.text_area(
            "",
            height=200,
            placeholder="카카오톡, 메시지, SNS 등의 대화 내용을 복사해서 붙여넣으세요...",
            label_visibility="collapsed"
        )
        if conversation_text:
            conversation = conversation_text
    
    with tab2:
        st.markdown('<p class="label">대화 캡처 이미지를 업로드해주세요</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 대화 이미지", use_column_width=True)
            
            # 이미지에서 텍스트 추출 버튼
            if st.button("이미지에서 텍스트 추출"):
                with st.spinner("텍스트 추출 중..."):
                    conversation = extract_text_from_image(image)
                    st.success("텍스트 추출 완료!")
                    st.text_area("추출된 텍스트", conversation, height=100)
    
    # 이전/다음 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← 이전", key="prev_btn_input"):
            prev_page()
    
    with col2:
        if st.button("분석하기 →", key="next_btn_input"):
            if not conversation:
                st.error("대화 내용을 입력하거나 이미지에서 텍스트를 추출해주세요.")
            else:
                # 분석 실행
                with st.spinner("천재적인 분석 중..."):
                    # 분석 진행 시각화
                    progress_bar = st.progress(0)
                    for i in range(101):
                        time.sleep(0.01)
                        progress_bar.progress(i)
                    
                    # 세션 상태에 저장
                    st.session_state.event_type = event_type
                    st.session_state.relationship = relationship
                    st.session_state.conversation = conversation
                    st.session_state.analysis_results = analyze_conversation(conversation, event_type, relationship)
                    next_page()
    
    st.markdown('</div>', unsafe_allow_html=True)
    # 결과 페이지
def show_result_page():
    if not st.session_state.analysis_results:
        st.error("분석 결과가 없습니다. 처음부터 다시 시작해주세요.")
        if st.button("처음으로 돌아가기"):
            st.session_state.page = 1
        return
    
    results = st.session_state.analysis_results
    
    # 결과 카드
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 헤더
    st.markdown(f'<h2 class="page-title">{st.session_state.event_type} / {st.session_state.relationship}</h2>', unsafe_allow_html=True)
    
    # 결과 금액
    st.markdown(f'<div class="result-amount">{results["amount"]:,}원</div>', unsafe_allow_html=True)
    
    # 친밀도 점수
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<p style="text-align: center; color: #74b9ff;">친밀도 점수: {results["intimacy_score"]}/100</p>', unsafe_allow_html=True)
        st.progress(results["intimacy_score"]/100)
    
    # 분석 결과 세부 정보
    st.markdown('<h3 style="color: #74b9ff; margin-top: 30px;">💡 분석 세부 정보</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in list(results["analysis_details"].items())[:3]:
            st.markdown(f'<p class="result-text">- {key}: {value}</p>', unsafe_allow_html=True)
    
    with col2:
        for key, value in list(results["analysis_details"].items())[3:]:
            st.markdown(f'<p class="result-text">- {key}: {value}</p>', unsafe_allow_html=True)
    
    # 특별 요인
    if results["special_factors"]:
        st.markdown('<div class="factor-box">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: #4cd137; margin-top: 0;">✨ 특별 가산 요인</h4>', unsafe_allow_html=True)
        for factor in results["special_factors"]:
            st.markdown(f'<p class="result-text">- {factor}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 재미있는 팁
    st.markdown('<div class="funny-tip">', unsafe_allow_html=True)
    st.markdown(f'<p class="result-text">💡 {results["funny_tip"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 결과 해석
    st.markdown('<h3 style="color: #74b9ff; margin-top: 30px;">🧐 결과 해석</h3>', unsafe_allow_html=True)
    
    # 친밀도 범위에 따른 메시지
    if results["intimacy_score"] < 30:
        st.markdown('<p class="result-text">친밀도가 <span style="color: #e74c3c;">낮은 편</span>이에요. 형식적인 관계로 보여 최소한의 예의를 지키는 금액을 추천드립니다.</p>', unsafe_allow_html=True)
    elif results["intimacy_score"] < 60:
        st.markdown('<p class="result-text">친밀도가 <span style="color: #f39c12;">보통</span>이에요. 무난하게 체면을 지킬 수 있는 금액을 추천드립니다.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result-text">친밀도가 <span style="color: #2ecc71;">매우 높은 편</span>이에요! 각별한 사이로 보여 정성이 느껴지는, 조금 더 높은 금액을 추천드립니다.</p>', unsafe_allow_html=True)
    
    # 추가 코멘트 (재미 요소)
    funny_comments = [
        "이 금액이면 '오 고마워~' 한 마디는 들을 수 있어요!",
        "이 정도면 인스타에 인증샷은 찍어줄 거예요!",
        "다음에 술자리에서 한 잔 더 따라줄 확률이 높아졌어요!",
        "축의금만 보고 '역시 너야~'라는 감탄사가 나올 거예요!"
    ]
    st.markdown(f'<p class="result-text">💌 {random.choice(funny_comments)}</p>', unsafe_allow_html=True)
    
    # 공유 버튼
    st.markdown('<div style="margin-top: 30px; text-align: center;">', unsafe_allow_html=True)
    st.button("💰 결과 저장하기", key="save_btn")
    st.button("📱 친구에게 공유하기", key="share_btn")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 면책 문구
    st.markdown('<p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; text-align: center; margin-top: 20px;">⚠️ 이 결과는 100% 재미로 제공되는 것으로, 실제 금액은 개인의 상황과 판단에 따라 결정하시기 바랍니다.</p>', unsafe_allow_html=True)
    
    # 이전 버튼
    if st.button("← 다시 분석하기", key="prev_btn_result"):
        st.session_state.page = 2
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 실행
if __name__ == "__main__":
    main()
