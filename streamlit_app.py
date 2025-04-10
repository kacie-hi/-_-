import streamlit as st
import random
import time
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
import base64
from streamlit_lottie import st_lottie
import requests
import json
import pytesseract
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="그래서..얼마면 돼? | 축의금 결정기",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 적용
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    h1, h2, h3 {
        font-weight: 700 !important;
    }
    
    .main-title {
        font-size: 3rem !important;
        font-weight: 900 !important;
        background: linear-gradient(to right, #FF4B91, #FF9BD2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
        text-align: center;
    }
    
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    
    .stTextInput, .stTextArea {
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        padding: 10px;
    }
    
    .stButton>button {
        background-color: #FF4B91;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #FF287B;
        box-shadow: 0 4px 10px rgba(255, 75, 145, 0.3);
        transform: translateY(-2px);
    }
    
    .secondary-button>button {
        background-color: #6c757d;
    }
    
    .secondary-button>button:hover {
        background-color: #5a6268;
        box-shadow: 0 4px 10px rgba(108, 117, 125, 0.3);
    }
    
    .result-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    .amount {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(to right, #FF4B91, #FF9BD2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 30px 0;
        animation: pulse 2s infinite;
    }
    
    .progress-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 5px;
    }
    
    .progress-label span:first-child {
        font-weight: 500;
    }
    
    .progress-label span:last-child {
        color: #6c757d;
    }
    
    .analysis-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
    }
    
    .analysis-title {
        font-weight: 700;
        margin-bottom: 15px;
        font-size: 1.2rem;
    }
    
    .footer {
        text-align: center;
        color: #6c757d;
        font-size: 0.8rem;
        margin-top: 30px;
    }
    
    .highlight {
        background: linear-gradient(to right, #FF4B91, #FF9BD2);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        font-weight: 700;
    }
    
    .emoji-bullet {
        margin-right: 8px;
    }
    
    .st-emotion-cache-16txtl3 h1 {
        text-align: center;
    }
    
    /* 로딩 애니메이션 스타일 */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        margin: 30px 0;
    }
    
    /* 결과 애니메이션 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .fadeIn {
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    /* 단계별 UI */
    .step-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .step-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
    }
    
    .step-indicator {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .step-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background-color: #e9ecef;
        margin: 0 5px;
    }
    
    .step-dot.active {
        background-color: #FF4B91;
        transform: scale(1.2);
    }
    
    .step-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .step-description {
        color: #6c757d;
        margin-bottom: 30px;
    }
    
    /* 카드 스타일 */
    .option-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    
    .option-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    }
    
    .option-card.selected {
        border-color: #FF4B91;
        background-color: rgba(255, 75, 145, 0.05);
    }
    
    .option-card-title {
        font-weight: 700;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
    }
    
    .option-card-description {
        color: #6c757d;
        font-size: 0.9rem;
    }
    
    /* 결과 페이지 스타일 */
    .result-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .result-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .result-subtitle {
        color: #6c757d;
    }
    
    .result-section {
        margin-bottom: 30px;
    }
    
    .result-section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .result-section-title svg {
        margin-right: 10px;
    }
    
    .funny-suggestion {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        border-left: 4px solid #FF4B91;
    }
    
    .funny-suggestion-title {
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .funny-suggestion-description {
        color: #6c757d;
    }
    
    /* 이미지 업로드 스타일 */
    .upload-container {
        border: 2px dashed #e9ecef;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s;
    }
    
    .upload-container:hover {
        border-color: #FF4B91;
    }
    
    .upload-icon {
        font-size: 3rem;
        color: #6c757d;
        margin-bottom: 15px;
    }
    
    .upload-text {
        color: #6c757d;
        margin-bottom: 15px;
    }
    
    /* 재미있는 결과 카드 */
    .fun-result-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .fun-result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(to right, #FF4B91, #FF9BD2);
    }
    
    .fun-result-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .fun-result-content {
        margin-bottom: 15px;
    }
    
    .fun-result-footer {
        font-size: 0.8rem;
        color: #6c757d;
        text-align: right;
    }
    
    /* 애니메이션 */
    @keyframes slideInRight {
        from { transform: translateX(50px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .slide-in-right {
        animation: slideInRight 0.5s forwards;
    }
    
    /* 프로그레스 바 스타일 커스텀 */
    .stProgress > div > div {
        background-color: #FF4B91;
    }
</style>
""", unsafe_allow_html=True)

# Lottie 애니메이션 로드 함수
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# 이미지에서 텍스트 추출 함수
def extract_text_from_image(image):
    try:
        # 이미지 처리
        img_array = np.array(image)
        
        # pytesseract로 텍스트 추출 (한국어 지원)
        text = pytesseract.image_to_string(img_array, lang='kor+eng')
        return text
    except Exception as e:
        st.error(f"이미지 처리 중 오류가 발생했습니다: {e}")
        return ""

# 재미있는 분석 문구 생성 함수
def generate_funny_analysis(closeness, formality, sentiment, keywords):
    closeness_comments = [
        f"친밀도 {closeness}%! 이 정도면 {random.choice(['친구', '지인', '동료'])}를 넘어 {random.choice(['가족', '영혼의 단짝', '전생의 연인'])} 수준이네요! 🔥",
        f"친밀도가 {closeness}%라니! 혹시 {random.choice(['비밀 연애 중', '몰래 술 마시는 사이', '같이 복권 사는 사이'])}는 아니죠? 👀",
        f"친밀도 {closeness}%... {random.choice(['카톡 1순위', '인스타 베프', '서로 냉장고 털어먹는 사이'])} 맞죠? 인정하세요! 😏"
    ] if closeness > 80 else [
        f"친밀도 {closeness}%는 {random.choice(['점심 같이 먹는 사이', '가끔 안부 묻는 사이', '명절에만 보는 친척'])} 수준이네요. 무난무난~ 😌",
        f"친밀도 {closeness}%... {random.choice(['서로 집 주소는 아는', '생일은 기억하는', '연락처는 저장된'])} 그런 사이군요! 👍",
        f"친밀도 {closeness}%로 {random.choice(['같은 동아리', '같은 팀', '같은 학교'])} 출신의 우정이 느껴집니다! 🤝"
    ] if closeness > 50 else [
        f"친밀도 {closeness}%... 혹시 {random.choice(['처음 만난 사이', '지하철에서 눈 마주친 사이', '배달음식 리뷰만 본 사이'])}는 아니죠? 😅",
        f"친밀도가 {closeness}%라니, {random.choice(['서로 성만 아는 사이', '연락처 교환만 한 사이', '얼굴만 아는 사이'])}인가요? 🧐",
        f"친밀도 {closeness}%... 이 자리가 {random.choice(['첫 만남', '소개팅', '업무 미팅'])}은 아니겠죠? 😳"
    ]
    
    formality_comments = [
        f"격식도 {formality}%! {random.choice(['대통령 연설문', '입사 지원서', '시어머니와의 첫 대화'])}급 존댓말이네요! 👑",
        f"격식도 {formality}%라니, {random.choice(['국회의원', '교수님', '사장님'])}과 대화하는 줄 알았어요! 🧐",
        f"격식도가 무려 {formality}%! 혹시 {random.choice(['면접관', '상사', '선생님'])}과 대화 중인가요? 🙇‍♂️"
    ] if formality > 80 else [
        f"격식도 {formality}%는 {random.choice(['동료', '선배', '친구의 친구'])}와의 대화 같아요. 적당한 예의! 👔",
        f"격식도 {formality}%... {random.choice(['반말과 존댓말을 섞는', '가끔 높임말을 쓰는', '친하지만 예의는 지키는'])} 그런 사이군요! 😊",
        f"격식도 {formality}%로 {random.choice(['소개팅 2차', '친구의 소개', '동아리 선후배'])} 같은 미묘한 관계가 느껴집니다! 🤔"
    ] if formality > 40 else [
        f"격식도 {formality}%... {random.choice(['절친', '오랜 친구', '형제자매'])} 사이 맞죠? 완전 편하게 대화하네요! 😎",
        f"격식도가 {formality}%라니, {random.choice(['어릴 때부터 알던 친구', '매일 보는 룸메이트', '매일 카톡하는 베프'])}인가요? 🤟",
        f"격식도 {formality}%... 이 정도면 {random.choice(['욕도 서슴없이 하는', '냉장고도 마음대로 여는', '집 비밀번호도 아는'])} 사이네요! 🔥"
    ]
    
    sentiment_comments = [
        f"대화 분위기가 {sentiment}%로 {random.choice(['꽃밭', '봄날', '휴가'])}같이 화사하네요! 🌸",
        f"감정 지수 {sentiment}%! 이 대화를 읽으니 저까지 {random.choice(['기분이 좋아지네요', '미소가 지어져요', '행복해지네요'])}! 😄",
        f"긍정 지수 {sentiment}%라니! {random.choice(['로또 당첨', '승진 소식', '연애 성공'])} 얘기라도 나눈 건가요? 🎉"
    ] if sentiment > 75 else [
        f"대화 분위기 {sentiment}%... {random.choice(['무난한 일상', '평범한 대화', '일반적인 안부'])}를 나누는 것 같네요. 😌",
        f"감정 지수 {sentiment}%는 {random.choice(['커피 한 잔', '가벼운 점심', '동네 산책'])} 같은 편안함이 느껴집니다. ☕",
        f"중립적인 {sentiment}% 분위기... {random.choice(['날씨 얘기', '안부 확인', '일상 대화'])}가 주를 이루나요? 🌤️"
    ] if sentiment > 40 else [
        f"대화 분위기가 {sentiment}%... 혹시 {random.choice(['싸운 적', '오해가 있었던', '불편한 주제'])}이 있었나요? 😟",
        f"감정 지수 {sentiment}%라니, {random.choice(['월요일 아침', '야근 중', '시험 기간'])} 같은 무거움이 느껴집니다. 😩",
        f"분위기 {sentiment}%... 이 대화 후에 {random.choice(['한잔 하러', '맛있는 거 먹으러', '기분 전환하러'])} 가셨나요? 🍻"
    ]
    
    # 키워드 기반 코멘트
    keyword_comments = []
    if "축하" in keywords or "축복" in keywords or "행복" in keywords:
        keyword_comments.append(f"'{random.choice(['축하', '축복', '행복'])}' 키워드가 보이네요! 경사스러운 일이 있으신가봐요! 🎊")
    
    if "고마워" in keywords or "감사" in keywords or "고맙" in keywords:
        keyword_comments.append(f"'{random.choice(['감사', '고마움'])}' 표현이 많네요. 받은 게 많은 만큼 축의금도 넉넉히...? 💸")
    
    if "오랜만" in keywords or "그동안" in keywords or "요즘" in keywords:
        keyword_comments.append(f"'{random.choice(['오랜만', '그동안', '요즘'])}' 이야기가 보이네요. 얼마나 안 만났길래! 시간=돈? 💰")
    
    if "바쁘" in keywords or "시간" in keywords or "일정" in keywords:
        keyword_comments.append(f"'{random.choice(['바쁨', '시간', '일정'])}' 언급이 있네요. 바쁜 와중에 참석하시는 거라면 축의금에 성의를 좀 더...? 💼")
    
    if "선물" in keywords or "준비" in keywords or "챙기" in keywords:
        keyword_comments.append(f"'{random.choice(['선물', '준비', '챙김'])}' 이야기가 보여요. 선물 대신 현금이 최고라는 거 아시죠? 🎁💵")
    
    # 랜덤하게 3개 선택 (키워드 코멘트가 있으면 1개는 포함)
    selected_comments = []
    selected_comments.append(random.choice(closeness_comments))
    selected_comments.append(random.choice(formality_comments))
    selected_comments.append(random.choice(sentiment_comments))
    
    if keyword_comments:
        selected_comments.append(random.choice(keyword_comments))
    
    # 결론 코멘트
    amount_comments = [
        f"이 모든 것을 고려해서 AI가 분석한 결과... 축의금으로 {random.choice(['딱!', '정확히!', '바로!'])} 이 금액이 적절합니다! 💯",
        f"우정과 예의, 그리고 약간의 {random.choice(['센스', '여유', '정성'])}를 담아 이 정도면 완벽합니다! 👌",
        f"이 금액이면 상대방도 {random.choice(['감동', '만족', '기쁨'])}할 거예요! 축하의 마음이 전해질 겁니다! 🎊",
        f"너무 많으면 부담, 너무 적으면 섭섭... 이 금액이 {random.choice(['황금 비율', '완벽한 균형', '최적의 선택'])}입니다! ⚖️"
    ]
    selected_comments.append(random.choice(amount_comments))
    
    return selected_comments

# 대화 분석 함수
def analyze_conversation(conversation):
    # 분석 시작을 보여주는 프로그레스 바
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 로딩 애니메이션 (Lottie)
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_x17ybolp.json"
    lottie_json = load_lottieurl(lottie_url)
    
    with st.container():
        st.markdown('<div class="loading-animation">', unsafe_allow_html=True)
        lottie_placeholder = st.empty()
        if lottie_json:
            with lottie_placeholder:
                st_lottie(lottie_json, speed=1, height=200, key="loading")
        status_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 분석 과정 시뮬레이션
    for i in range(101):
        if i < 20:
            status_placeholder.markdown("<p style='text-align:center'>대화 패턴 분석 중...</p>", unsafe_allow_html=True)
        elif i < 40:
            status_placeholder.markdown("<p style='text-align:center'>감정 분석 중...</p>", unsafe_allow_html=True)
        elif i < 60:
            status_placeholder.markdown("<p style='text-align:center'>관계 유형 파악 중...</p>", unsafe_allow_html=True)
        elif i < 80:
            status_placeholder.markdown("<p style='text-align:center'>축의금 데이터베이스 참조 중...</p>", unsafe_allow_html=True)
        else:
            status_placeholder.markdown("<p style='text-align:center'>최종 금액 계산 중...</p>", unsafe_allow_html=True)
        
        progress_bar.progress(i)
        time.sleep(0.03)
    
    # 분석 완료 후 로딩 UI 제거
    progress_bar.empty()
    status_text.empty()
    lottie_placeholder.empty()
    status_placeholder.empty()
    
    # 실제 분석 로직 (간단한 예시)
    # 1. 친밀도 분석
    words = re.findall(r'\w+', conversation.lower())
    total_words = len(words)
    
    # 친밀도 관련 단어 및 패턴
    closeness_words = ['친구', '좋아', '사랑', '그리워', '보고싶', '친한', '우리', '같이', '함께', 
                       '추억', '기억', '재밌', '웃', '행복', '고마', '감사', '축하', '기쁘', '즐거']
    
    closeness_count = sum(1 for word in words if any(cw in word for cw in closeness_words))
    closeness_score = min(95, int(40 + (closeness_count / max(1, total_words * 0.1)) * 60))
    
    # 2. 격식 수준 분석
    formality_patterns = ['습니다', '니다', '세요', '입니다', '합니다', '드립니다', '까요', '군요', '네요', '십니까']
    informal_patterns = ['ㅋㅋ', 'ㅎㅎ', '야', '잉', '임', '쿠', '룰', '듯', '음', '엌', 'ㅇㅇ', 'ㄴㄴ']
    
    formality_count = sum(conversation.count(pattern) for pattern in formality_patterns)
    informal_count = sum(conversation.count(pattern) for pattern in informal_patterns)
    
    formality_ratio = formality_count / max(1, formality_count + informal_count)
    formality_score = min(95, int(30 + formality_ratio * 70))
    
    # 3. 감정 분석
    positive_words = ['좋아', '행복', '기쁘', '즐거', '감사', '고마', '축하', '사랑', '최고', '멋지', '예쁘', '환상', '대박']
    negative_words = ['싫', '짜증', '화나', '슬프', '아쉽', '실망', '안타깝', '힘들', '어렵', '불편', '죄송', '미안', '걱정']
    
    positive_count = sum(1 for word in words if any(pw in word for pw in positive_words))
    negative_count = sum(1 for word in words if any(nw in word for nw in negative_words))
    
    sentiment_score = min(95, int(50 + (positive_count - negative_count) / max(1, total_words * 0.05) * 50))
    
    # 4. 키워드 추출
    all_keywords = closeness_words + [w for p in formality_patterns for w in [p]] + [w for p in informal_patterns for w in [p]] + positive_words + negative_words
    keywords = [word for word in all_keywords if word in conversation.lower()]
    keywords = list(set(keywords))[:5]  # 중복 제거 후 최대 5개
    
    # 5. 축의금 계산
    base_amount = 50000
    closeness_factor = (closeness_score / 100) * 30000
    formality_factor = (formality_score / 100) * 20000
    sentiment_factor = (sentiment_score / 100) * 20000
    
    # 약간의 랜덤성 추가
    random_factor = random.randint(-5000, 5000)
    
    # 최종 금액 계산 (10000원 단위로 반올림)
    amount = base_amount + closeness_factor + formality_factor + sentiment_factor + random_factor
    amount = round(amount / 10000) * 10000
    
    # 금액 범위 제한 (3만원 ~ 10만원)
    amount = max(30000, min(100000, amount))
    
    # 재미있는 분석 코멘트 생성
    analysis_comments = generate_funny_analysis(closeness_score, formality_score, sentiment_score, keywords)
    
    
    # 재미있는 대안 제안
    funny_suggestions = [
        f"{int(amount/10000)-1}만원 + 마음을 담은 손편지 (진심이 통하는 법이죠!)",
        f"{int(amount/10000)-2}만원 + 신랑신부 집들이 초대권 획득 (밥 한끼 뚝딱!)",
        f"빈 봉투 + '다음에 밥 살게~' (진정한 절친이라면 이해해주겠죠?)"
    ]
    
    return {
        "amount": amount,
        "closeness": closeness_score,
        "formality": formality_score,
        "sentiment": sentiment_score,
        "keywords": keywords,
        "analysis": analysis_comments,
        "funny_suggestions": funny_suggestions
    }

# 로딩 애니메이션 표시 함수
def show_loading_animation(text="분석 중..."):
    # 로딩 애니메이션 (Lottie)
    lottie_url = "https://assets5.lottiefiles.com/packages/lf20_x17ybolp.json"
    lottie_json = load_lottieurl(lottie_url)
    
    with st.container():
        st.markdown('<div class="loading-animation">', unsafe_allow_html=True)
        lottie_placeholder = st.empty()
        if lottie_json:
            with lottie_placeholder:
                st_lottie(lottie_json, speed=1, height=200, key="loading")
        status_placeholder = st.empty()
        status_placeholder.markdown(f"<p style='text-align:center'>{text}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    return lottie_placeholder, status_placeholder

# 단계 표시 함수
def show_step_indicator(current_step, total_steps=4):
    st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
    for i in range(1, total_steps + 1):
        if i == current_step:
            st.markdown(f'<div class="step-dot active"></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="step-dot"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 시작 화면
def show_welcome_screen():
    st.markdown('<h1 class="main-title">그래서... 얼마면 돼?</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">대화 내용을 분석해서 유머러스하게 축의금을 결정해드립니다!</p>', unsafe_allow_html=True)
    
    # 로티 애니메이션
    lottie_url = "https://assets3.lottiefiles.com/packages/lf20_touohxv0.json"
    lottie_json = load_lottieurl(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=300, key="welcome")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("시작하기"):
            st.session_state.step = 1
            st.experimental_rerun()

# 입력 방식 선택 화면
def show_input_selection():
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="step-header">', unsafe_allow_html=True)
    show_step_indicator(1)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="step-title">대화 내용을 어떻게 입력할까요?</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-description">분석할 대화 내용을 입력하는 방법을 선택해주세요.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        text_card = st.container()
        with text_card:
            st.markdown(f"""
            <div class="option-card {'selected' if 'input_method' in st.session_state and st.session_state.input_method == 'text' else ''}" id="text-option">
                <div class="option-card-title">
                    <span>✏️ 텍스트로 입력하기</span>
                </div>
                <div class="option-card-description">
                    카톡, 문자 등의 대화 내용을 복사해서 붙여넣기
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("텍스트 입력 선택", key="select_text"):
                st.session_state.input_method = "text"
                st.session_state.step = 2
                st.experimental_rerun()
    
    with col2:
        image_card = st.container()
        with image_card:
            st.markdown(f"""
            <div class="option-card {'selected' if 'input_method' in st.session_state and st.session_state.input_method == 'image' else ''}" id="image-option">
                <div class="option-card-title">
                    <span>📷 이미지로 입력하기</span>
                </div>
                <div class="option-card-description">
                    대화 캡쳐 이미지를 업로드해서 자동으로 분석
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("이미지 입력 선택", key="select_image"):
                st.session_state.input_method = "image"
                st.session_state.step = 2
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 텍스트 입력 화면
def show_text_input():
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="step-header">', unsafe_allow_html=True)
    show_step_indicator(2)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="step-title">대화 내용 입력</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-description">상대방과의 카톡, 문자, 이메일 등의 대화 내용을 복사해서 붙여넣으세요.</p>', unsafe_allow_html=True)
    
    with st.form(key='conversation_form'):
        conversation = st.text_area("대화 내용", height=200, 
                                   placeholder="예시: 안녕하세요! 오랜만이에요. 결혼 축하드려요~ 꼭 가고 싶은데 일정이 어떻게 될지 모르겠네요. 최대한 참석하도록 할게요!")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            submit_button = st.form_submit_button(label="분석하기")
        
        with col2:
            back_button = st.form_submit_button(label="이전 단계로")
        
        if submit_button and conversation:
            st.session_state.conversation = conversation
            st.session_state.step = 3
            st.experimental_rerun()
        
        if back_button:
            st.session_state.step = 1
            st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 이미지 입력 화면
def show_image_input():
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="step-header">', unsafe_allow_html=True)
    show_step_indicator(2)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="step-title">대화 이미지 업로드</h2>', unsafe_allow_html=True)
    st.markdown('<p class="step-description">대화 캡쳐 이미지를 업로드하면 자동으로 텍스트를 추출하여 분석합니다.</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown('<div class="upload-icon">📷</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-text">이미지를 드래그하거나 클릭하여 업로드하세요</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("대화 이미지 업로드", type=["jpg", "jpeg", "png"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.button("이미지 분석하기"):
                # 이미지에서 텍스트 추출
                with st.spinner("이미지에서 텍스트를 추출하는 중..."):
                    extracted_text = extract_text_from_image(image)
                
                if extracted_text:
                    st.session_state.conversation = extracted_text
                    st.session_state.step = 3
                    st.experimental_rerun()
                else:
                    st.error("이미지에서 텍스트를 추출할 수 없습니다. 다른 이미지를 시도하거나 텍스트 입력 방식을 선택해주세요.")
        
        with col2:
            if st.button("이전 단계로", key="back_from_image"):
                st.session_state.step = 1
                st.experimental_rerun()
    else:
        col1, col2 = st.columns([2, 1])
        
        with col2:
            if st.button("이전 단계로", key="back_from_image_empty"):
                st.session_state.step = 1
                st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 분석 및 결과 화면
def show_analysis_and_result():
    st.markdown('<div class="step-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="step-header">', unsafe_allow_html=True)
    show_step_indicator(3)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 분석 중 화면 표시
    if 'result' not in st.session_state:
        st.markdown('<h2 class="step-title">대화 분석 중...</h2>', unsafe_allow_html=True)
        
        progress_bar = st.progress(0)
        lottie_placeholder, status_placeholder = show_loading_animation("대화 패턴 분석 중...")
        
        # 분석 과정 시뮬레이션
        for i in range(101):
            if i < 20:
                status_placeholder.markdown("<p style='text-align:center'>대화 패턴 분석 중...</p>", unsafe_allow_html=True)
            elif i < 40:
                status_placeholder.markdown("<p style='text-align:center'>감정 분석 중...</p>", unsafe_allow_html=True)
            elif i < 60:
                status_placeholder.markdown("<p style='text-align:center'>관계 유형 파악 중...</p>", unsafe_allow_html=True)
            elif i < 80:
                status_placeholder.markdown("<p style='text-align:center'>축의금 데이터베이스 참조 중...</p>", unsafe_allow_html=True)
            else:
                status_placeholder.markdown("<p style='text-align:center'>최종 금액 계산 중...</p>", unsafe_allow_html=True)
            
            progress_bar.progress(i)
            time.sleep(0.03)
        
        # 실제 분석 실행
        result = analyze_conversation(st.session_state.conversation)
        st.session_state.result = result
        
        # 로딩 UI 제거 및 페이지 새로고침
        progress_bar.empty()
        lottie_placeholder.empty()
        status_placeholder.empty()
        st.experimental_rerun()
    
    # 결과 화면 표시
    else:
        result = st.session_state.result
        
        st.markdown('<div class="result-header">', unsafe_allow_html=True)
        st.markdown('<h2 class="result-title">분석 완료! 🎉</h2>', unsafe_allow_html=True)
        st.markdown('<p class="result-subtitle">AI가 분석한 최적의 축의금은...</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 추천 금액
        st.markdown(f"<div class='amount'>{result['amount']:,}원</div>", unsafe_allow_html=True)
        
        # 분석 지표
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='progress-label'><span>친밀도</span><span>{0}%</span></div>".format(result['closeness']), unsafe_allow_html=True)
            st.progress(result['closeness']/100)
            
            st.markdown("<div class='progress-label'><span>감정 지수</span><span>{0}%</span></div>".format(result['sentiment']), unsafe_allow_html=True)
            st.progress(result['sentiment']/100)
        
        with col2:
            st.markdown("<div class='progress-label'><span>격식 수준</span><span>{0}%</span></div>".format(result['formality']), unsafe_allow_html=True)
            st.progress(result['formality']/100)
            
            # 키워드 표시
            st.markdown("<div class='progress-label'><span>주요 키워드</span></div>", unsafe_allow_html=True)
            keyword_html = ""
            for keyword in result['keywords'][:5]:
                keyword_html += f"<span style='display:inline-block; background-color:#f8f9fa; padding:5px 10px; border-radius:15px; margin:2px; font-size:0.8rem;'>#{keyword}</span>"
            st.markdown(f"<div style='margin-top:5px;'>{keyword_html}</div>", unsafe_allow_html=True)
        
        # 분석 코멘트
        st.markdown("<div class='analysis-box'>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-title'>✨ AI의 유머러스한 분석</div>", unsafe_allow_html=True)
        
        for comment in result['analysis']:
            st.markdown(f"<p style='margin-bottom:10px;'>💬 {comment}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 재미있는 대안 제안
        st.markdown("<h3 style='margin-top:30px; font-size:1.2rem;'>🎭 재미있는 대안 제안</h3>", unsafe_allow_html=True)
        
        for i, suggestion in enumerate(result['funny_suggestions']):
            st.markdown(f"""
            <div class="fun-result-card slide-in-right" style="animation-delay: {i * 0.2}s">
                <div class="fun-result-title">대안 {i+1}</div>
                <div class="fun-result-content">{suggestion}</div>
                <div class="fun-result-footer">* 실제 적용 시 책임지지 않습니다 😉</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 재시작 버튼
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("처음부터 다시하기"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun()
        
        with col2:
            if st.button("다른 대화 분석하기"):
                if 'result' in st.session_state:
                    del st.session_state['result']
                if 'conversation' in st.session_state:
                    del st.session_state['conversation']
                st.session_state.step = 1
                st.experimental_rerun()
        
        # 재미있는 면책 조항
        st.markdown("<div class='footer'>", unsafe_allow_html=True)
        st.markdown("⚠️ 이 분석은 100% 과학적이고 정확합니다... 라고 말하면 거짓말입니다! 😉<br>실제 축의금은 개인 상황과 관계에 따라 달라질 수 있습니다.", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 재미있는 통계 차트 (랜덤 데이터)
        if st.checkbox("🔍 전국 축의금 통계 보기"):
            st.markdown("<h3 style='margin-top:30px; font-size:1.2rem;'>전국 축의금 통계 (100% 신뢰할 수 없는 데이터)</h3>", unsafe_allow_html=True)
            
            # 랜덤 데이터 생성
            categories = ['친구', '직장동료', '친척', '지인', '학교선후배']
            amounts = [random.randint(30, 100) * 1000 for _ in range(5)]
            
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.bar(categories, amounts, color=['#FF4B91', '#FF9BD2', '#FFC2E2', '#FFD8D8', '#FFECEC'])
            
            # 바 위에 금액 표시
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1000,
                        f'{height:,}원', ha='center', va='bottom', fontsize=9)
            
            ax.set_ylabel('평균 축의금액 (원)')
            ax.set_title('관계별 평균 축의금 금액')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            st.pyplot(fig)
            
            st.markdown("<p style='text-align:center; font-size:0.8rem; color:#6c757d; margin-top:10px;'>* 이 통계는 AI가 상상한 데이터로, 실제와 관련이 없습니다 😉</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 앱 UI
def main():
    # 세션 상태 초기화
    if 'step' not in st.session_state:
        st.session_state.step = 0
    
    # 단계별 화면 표시
    if st.session_state.step == 0:
        show_welcome_screen()
    elif st.session_state.step == 1:
        show_input_selection()
    elif st.session_state.step == 2:
        if st.session_state.input_method == "text":
            show_text_input()
        else:
            show_image_input()
    elif st.session_state.step == 3:
        show_analysis_and_result()

# 앱 실행
if __name__ == "__main__":
    main()
