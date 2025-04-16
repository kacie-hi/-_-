import streamlit as st
import re
import random
import time
from PIL import Image
import pytesseract

# 페이지 설정
st.set_page_config(
    page_title="축의금 분석기",
    page_icon="💌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 사용자 정의 CSS
def set_custom_style():
    st.markdown("""
    <style>
    /* 기본 스타일 초기화 및 폰트 설정 */
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 전체 배경 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 헤더 스타일 */
    .main-title {
        color: #333333;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0;
        letter-spacing: -0.5px;
    }
    
    /* 부제목 스타일 */
    .sub-title {
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* 카드 스타일 */
    .card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
        border: 1px solid #F3F4F6;
    }
    
    /* 섹션 타이틀 */
    .section-title {
        color: #111827;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 16px;
        letter-spacing: -0.3px;
    }
    
    /* 라벨 스타일 */
    .label {
        color: #4B5563;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #4F46E5;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
    }
    
    /* 결과 금액 스타일 */
    .result-amount {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #4F46E5;
        margin: 24px 0;
    }
    
    /* 결과 텍스트 스타일 */
    .result-text {
        color: #374151;
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 8px;
    }
    
    /* 강조 텍스트 */
    .highlight-text {
        background-color: #F0F9FF;
        border-radius: 4px;
        padding: 4px 8px;
        color: #0369A1;
        font-weight: 500;
    }
    
    /* 페이지 인디케이터 */
    .step-indicator {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    .step {
        width: 80px;
        height: 4px;
        margin: 0 4px;
        background-color: #E5E7EB;
        border-radius: 2px;
    }
    
    .active-step {
        background-color: #4F46E5;
    }
    
    /* 입력 필드 스타일 */
    div[data-baseweb="select"] > div {
        border-radius: 8px;
        border-color: #E5E7EB !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 8px;
        border-color: #E5E7EB !important;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border-color: #E5E7EB !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #F3F4F6;
        color: #4F46E5;
        font-weight: 500;
    }
    
    /* 프로그레스 바 스타일 */
    .stProgress > div > div > div > div {
        background-color: #4F46E5 !important;
        border-radius: 4px;
    }
    
    /* 특별 요인 박스 */
    .factors-box {
        background-color: #F0F9FF;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        border-left: 4px solid #0EA5E9;
    }
    
    /* 팁 박스 */
    .tip-box {
        background-color: #ECFDF5;
        border-radius: 8px;
        padding: 16px;
        margin: 16px 0;
        border-left: 4px solid #10B981;
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        color: #9CA3AF;
        font-size: 0.8rem;
        margin-top: 32px;
        padding-bottom: 16px;
    }
    
    /* 이미지 업로드 영역 */
    .upload-area {
        border: 2px dashed #E5E7EB;
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        margin: 16px 0;
        transition: all 0.2s ease;
    }
    
    .upload-area:hover {
        border-color: #4F46E5;
    }
    
    /* 이모지 아이콘 */
    .emoji-icon {
        font-size: 40px;
        margin-bottom: 12px;
        display: block;
        text-align: center;
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

# 페이지 이동
def next_page():
    st.session_state.page += 1

def prev_page():
    st.session_state.page -= 1

# 페이지 인디케이터
def show_step_indicator(current_step, total_steps):
    html = '<div class="step-indicator">'
    for i in range(1, total_steps + 1):
        if i == current_step:
            html += '<div class="step active-step"></div>'
        else:
            html += '<div class="step"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# 이미지에서 텍스트 추출
def extract_text_from_image(image):
    try:
        # 실제 환경에서는 pytesseract 사용
        text = pytesseract.image_to_string(image, lang='kor+eng')
        return text
    except Exception as e:
        # 개발 환경 테스트용
        st.info("테스트 환경에서는 샘플 텍스트를 사용합니다.")
        sample_texts = [
            "오늘 뭐해? 저녁에 시간 있으면 만날래? ㅋㅋㅋ",
            "축하해!! 결혼 소식 들었어 너무 좋겠다 🎉🎉",
            "요즘 뭐하고 지내? 얼굴 본지 진짜 오래됐네 ㅠㅠ",
            "내일 모임에서 보자! 오랜만에 얼굴 보네 ㅎㅎ"
        ]
        return random.choice(sample_texts)

# 대화 분석 함수
def analyze_conversation(conversation, event_type, relationship):
    # 분석 로직
    
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
        special_factors.append("웃음이 많은 대화를 나누는 사이네요! (+2,000원)")
        final_amount += 2000
    
    if "선물" in conversation or "케이크" in conversation or "꽃다발" in conversation:
        special_factors.append("선물 챙겨주는 센스가 있으시네요! (+7,000원)")
        final_amount += 7000
    
    # 재미있는 팁 생성
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
            "이모지 사용": f"{emoji_count}개 ({emoji_factor}점)",
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
    st.markdown('<h1 class="main-title">축의금 분석기</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">말투 분석으로 알아보는 최적의 축의금 금액</p>', unsafe_allow_html=True)
    
    # 페이지 인디케이터
    show_step_indicator(st.session_state.page, 3)
    
    # 페이지 분기
    if st.session_state.page == 1:
        show_welcome_page()
    elif st.session_state.page == 2:
        show_input_page()
    elif st.session_state.page == 3:
        show_result_page()
    
    # 푸터
    st.markdown('<div class="footer">© 2025 축의금 분석기 | 모든 분석 결과는 재미로만 봐주세요</div>', unsafe_allow_html=True)

# 시작 페이지
def show_welcome_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 이모지 아이콘
    st.markdown('<span class="emoji-icon">💌</span>', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">축의금, 얼마를 내야 할지 고민이신가요?</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <p class="result-text">
    생각보다 어려운 축의금 금액 결정, 이제 AI의 도움을 받아보세요.<br><br>
    축의금 분석기는 상대방과의 대화 내용을 분석해 친밀도와 관계를 파악하고,<br>
    최적의 축의금 금액을 추천해드립니다.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p class="result-text">
    <b>이렇게 사용해보세요:</b><br>
    1. 상대방과의 대화 내용을 복사해서 입력하거나 캡처 이미지를 업로드합니다<br>
    2. 행사 유형과 관계를 선택합니다<br>
    3. AI가 분석한 맞춤형 축의금을 확인합니다
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tip-box">
    <p class="result-text">💡 93%의 사용자들이 "이 금액이면 적절하네!"라고 평가했습니다<br>
    (완전히 신뢰할 수 없는 재미있는 통계)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 시작 버튼
    if st.button('분석 시작하기', key='start_btn'):
        next_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 입력 페이지
def show_input_page():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-title">기본 정보</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="label">행사 유형</p>', unsafe_allow_html=True)
        event_type = st.selectbox(
            "",
            ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"],
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<p class="label">상대방과의 관계</p>', unsafe_allow_html=True)
        relationship = st.selectbox(
            "",
            ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"],
            label_visibility="collapsed"
        )
    
    st.markdown('<h2 class="section-title">대화 분석</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["💬 텍스트 입력", "📷 이미지 업로드"])
    
    conversation = ""
    
    with tab1:
        st.markdown('<p class="label">대화 내용을 붙여넣으세요</p>', unsafe_allow_html=True)
        conversation_text = st.text_area(
            "",
            height=180,
            placeholder="카카오톡, 메시지, SNS 등의 대화 내용을 복사해서 붙여넣으세요...",
            label_visibility="collapsed"
        )
        if conversation_text:
            conversation = conversation_text
    
    with tab2:
        st.markdown('<p class="label">대화 캡처 이미지를 업로드하세요</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_column_width=True)
            
            if st.button("이미지에서 텍스트 추출"):
                with st.spinner("텍스트 추출 중..."):
                    time.sleep(1)  # 시각적 효과를 위한 지연
                    conversation = extract_text_from_image(image)
                    st.success("텍스트 추출 완료!")
                    st.text_area("추출된 텍스트", conversation, height=100)
    
    # 버튼
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
                with st.spinner("분석 중..."):
                    # 시각적 효과
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
    
    # 이벤트 정보
    st.markdown(f'<p class="highlight-text" style="display: inline-block">{st.session_state.event_type}</p> <span style="margin: 0 8px; color: #9CA3AF;">|</span> <p class="highlight-text" style="display: inline-block">{st.session_state.relationship}</p>', unsafe_allow_html=True)
    
    # 결과 금액
    st.markdown(f'<div class="result-amount">{results["amount"]:,}원</div>', unsafe_allow_html=True)
    
    # 친밀도 점수
    st.markdown(f'<p style="text-align: center; color: #6B7280; margin-bottom: 4px;">친밀도 점수: {results["intimacy_score"]}/100</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.progress(results["intimacy_score"]/100)
    
    # 분석 세부 정보
    st.markdown('<h3 class="section-title" style="margin-top: 24px;">분석 세부 정보</h3>', unsafe_allow_html=True)
    
    # 2단 컬럼으로 표시
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in list(results["analysis_details"].items())[:3]:
            st.markdown(f'<p class="result-text">• {key}: {value}</p>', unsafe_allow_html=True)
    
    with col2:
        for key, value in list(results["analysis_details"].items())[3:]:
            st.markdown(f'<p class="result-text">• {key}: {value}</p>', unsafe_allow_html=True)
    
    # 특별 요인
    if results["special_factors"]:
        st.markdown('<div class="factors-box">', unsafe_allow_html=True)
        st.markdown('<p style="color: #0369A1; font-weight: 500; margin-bottom: 12px;">✨ 특별 가산 요인</p>', unsafe_allow_html=True)
        for factor in results["special_factors"]:
            st.markdown(f'<p class="result-text">• {factor}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 팁 박스
    st.markdown('<div class="tip-box">', unsafe_allow_html=True)
    st.markdown(f'<p class="result-text">💡 {results["funny_tip"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 결과 해석
    st.markdown('<h3 class="section-title" style="margin-top: 24px;">결과 해석</h3>', unsafe_allow_html=True)
    
    # 친밀도에 따른 메시지
    if results["intimacy_score"] < 30:
        st.markdown('<p class="result-text">친밀도가 <span style="color: #EF4444; font-weight: 500;">낮은 편</span>이네요. 형식적인 관계로 보이며, 최소한의 예의를 갖춘 금액을 추천해드립니다.</p>', unsafe_allow_html=True)
    elif results["intimacy_score"] < 60:
        st.markdown('<p class="result-text">친밀도가 <span style="color: #F59E0B; font-weight: 500;">보통</span>이네요. 무난하게 체면을 지킬 수 있는 금액을 추천해드립니다.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="result-text">친밀도가 <span style="color: #10B981; font-weight: 500;">높은 편</span>이네요! 각별한 사이로 보이며, 정성이 느껴지는 금액을 추천해드립니다.</p>', unsafe_allow_html=True)
    
    # 재미있는 코멘트
    funny_comments = [
        "이 금액이면 '고마워~' 한 마디는 들을 수 있어요!",
        "이 정도면 다음에 만났을 때 커피는 사줄 거에요!",
        "축의금 봉투만 보고도 환하게 웃을 확률 높음!",
        "이 금액이면 다음에 연락했을 때 읽씹 당할 확률 낮음!"
    ]
    st.markdown(f'<p class="result-text" style="margin-top: 12px;">💌 {random.choice(funny_comments)}</p>', unsafe_allow_html=True)
    
    # 면책 문구
    st.markdown('<p style="color: #9CA3AF; font-size: 0.8rem; text-align: center; margin-top: 16px;">⚠️ 이 결과는 100% 재미로만 제공되는 것입니다. 실제 금액은 본인의 상황과 판단에 따라 결정하세요.</p>', unsafe_allow_html=True)
    
    # 다시 분석하기 버튼
    if st.button("← 다시 분석하기", key="prev_btn_result"):
        st.session_state.page = 2
    
    st.markdown('</div>', unsafe_allow_html=True)

# 메인 실행
if __name__ == "__main__":
    main()
