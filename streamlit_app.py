import streamlit as st
import re
import random
import base64

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

# CSS 스타일 정의
def set_custom_style():
    st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 페이지 스타일 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* 배경색 통일 */
    .stApp {
        background: #F7D358;
    }
    
    /* 카드 스타일 - 더 명확한 그림자와 여백 */
    .card-container {
        background-color: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        margin: 20px 0;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* 헤더 영역 */
    .header {
        display: flex;
        align-items: center;
        padding: 15px 0;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        color: #452c22;
        text-align: center;
        margin: 20px 0;
        line-height: 1.3;
    }
    
    .subtitle {
        font-size: 20px;
        font-weight: 500;
        color: #452c22;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* 버튼 스타일 강화 */
    .stButton > button {
        background-color: #E8A02F;
        color: white;
        font-family: 'Pretendard', sans-serif;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 30px;
        border: none;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #D4901A;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* 이전 버튼 스타일 */
    .secondary-button > button {
        background-color: #F0F0F0;
        color: #666666;
        border: 1px solid #E0E0E0;
        box-shadow: none;
    }
    
    .secondary-button > button:hover {
        background-color: #E0E0E0;
    }
    
    /* 선택박스 스타일 개선 */
    .stSelectbox {
        margin-bottom: 25px;
    }
    
    .stSelectbox > div > div > div {
        background-color: white;
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 5px;
    }
    
    /* 텍스트 영역 스타일 개선 */
    .stTextArea > div > div > textarea {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Pretendard', sans-serif;
        font-size: 16px;
    }
    
    /* 결과 금액 강조 스타일 */
    .result-amount {
        font-size: 54px;
        font-weight: 700;
        color: #E8A02F;
        text-align: center;
        margin: 30px 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* 분석 결과 섹션 */
    .analysis-section {
        background-color: #FFF8E1;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 팁 섹션 */
    .tip-section {
        background-color: #F0F0F0;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 태그 스타일 */
    .tag {
        display: inline-block;
        background-color: #F0F0F0;
        color: #666666;
        padding: 5px 15px;
        border-radius: 20px;
        margin-right: 10px;
        font-weight: 500;
        font-size: 14px;
    }
    
    /* 페이지 인디케이터 */
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
    
    /* 푸터 */
    .footer {
        text-align: center;
        padding: 20px 0;
        color: #6D4C41;
        opacity: 0.8;
        font-size: 14px;
        margin-top: 40px;
    }
    
    /* 보더박스 */
    .content-section {
        border: 1px solid #E0E0E0;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 섹션 타이틀 */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #452c22;
        margin-bottom: 20px;
    }
    
    /* 인풋 레이블 */
    .input-label {
        font-size: 18px;
        font-weight: 600;
        color: #452c22;
        margin-bottom: 10px;
    }
    
    /* 프로그레스 바 색상 */
    .stProgress > div > div > div > div {
        background-color: #E8A02F;
    }
    
    /* 중앙 정렬 컨테이너 */
    .center-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 50px 20px;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* 봉투 이미지 컨테이너 */
    .envelope-container {
        text-align: center;
        margin: 40px 0;
    }
    
    /* 버튼 컨테이너 */
    .button-container {
        max-width: 300px;
        margin: 30px auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 페이지 인디케이터
def show_page_indicator(current_page, total_pages=3):
    html = '<div class="page-indicator">'
    for i in range(1, total_pages + 1):
        if i == current_page:
            html += '<div class="indicator-dot active-dot"></div>'
        else:
            html += '<div class="indicator-dot"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# 봉투 + 하트 SVG
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

# 봉투 이미지 표시
def show_envelope(width=300, height=180):
    envelope_svg = get_envelope_svg(width, height)
    st.markdown(f'<div class="envelope-container">{envelope_svg}</div>', unsafe_allow_html=True)

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
    
    # 헤더 (2, 3페이지에만 표시)
    if st.session_state.page > 1:
        st.markdown('<div class="header">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 9])
        with col1:
            st.markdown(get_envelope_svg(width=40, height=24), unsafe_allow_html=True)
        with col2:
            st.markdown('<span style="font-size: 22px; font-weight: 600; color: #452c22;">축의금 책정기</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 페이지 인디케이터
    show_page_indicator(st.session_state.page)
    
    # 페이지별 내용 표시
    if st.session_state.page == 1:
        show_start_page()
    elif st.session_state.page == 2:
        show_input_page()
    elif st.session_state.page == 3:
        show_result_page()
    
    # 푸터
    st.markdown('<div class="footer">© 2025 축의금 책정기</div>', unsafe_allow_html=True)

# 시작 페이지
def show_start_page():
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    # 봉투 이미지
    show_envelope(width=300, height=180)
    
    # 서브타이틀
    st.markdown('<p class="subtitle">당신의 마음을 금액으로 표현해드립니다</p>', unsafe_allow_html=True)
    
    # 버튼 공간 확보
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button('축의금 책정하기', key='start_btn'):
        next_page()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 입력 페이지
def show_input_page():
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    # 타이틀
    st.markdown('<h2 class="section-title">정보 입력</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666666; margin-bottom: 30px;">축의금 분석을 위한 정보를 입력해주세요</p>', unsafe_allow_html=True)
    
    # 행사 유형
    st.markdown('<p class="input-label">행사 유형</p>', unsafe_allow_html=True)
    event_type = st.selectbox(
        "",
        ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"],
        label_visibility="collapsed"
    )
    
    # 관계
    st.markdown('<p class="input-label">상대방과의 관계</p>', unsafe_allow_html=True)
    relationship = st.selectbox(
        "",
        ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"],
        label_visibility="collapsed"
    )
    
    # 대화 내용
    st.markdown('<p class="input-label">대화 내용</p>', unsafe_allow_html=True)
    conversation = st.text_area(
        "",
        height=200,
        placeholder="카카오톡, 메시지 등의 대화 내용을 복사해서 붙여넣으세요...",
        label_visibility="collapsed"
    )
    
    # 버튼 영역
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        if st.button("← 이전", key="prev_btn_input"):
            prev_page()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("분석하기 →", key="next_btn_input"):
            if not conversation:
                st.error("대화 내용을 입력해주세요.")
            else:
                # 세션 상태에 저장
                st.session_state.event_type = event_type
                st.session_state.relationship = relationship
                st.session_state.conversation = conversation
                
                # 분석 실행
                with st.spinner("분석 중..."):
                    st.session_state.analysis_results = analyze_conversation(conversation, event_type, relationship)
                    next_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 결과 페이지
def show_result_page():
    if not st.session_state.analysis_results:
        st.error("분석 결과가 없습니다. 처음부터 다시 시작해주세요.")
        if st.button("처음으로 돌아가기"):
            go_to_page(1)
        return
    
    results = st.session_state.analysis_results
    
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    
    # 카드 헤더
    st.markdown('<div class="analysis-section" style="margin-top:0;">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">분석 결과</h2>', unsafe_allow_html=True)
    
    # 태그 표시
    st.markdown(
        f'<span class="tag">{st.session_state.event_type}</span><span class="tag">{st.session_state.relationship}</span>', 
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 결과 표시 영역
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # 봉투 아이콘
        show_envelope(width=120, height=72)
    
    with col2:
        # 결과 금액
        st.markdown(f'<div class="result-amount">{results["amount"]:,}원</div>', unsafe_allow_html=True)
    
    # 친밀도 점수
    st.markdown(f'<p style="color: #452c22; font-size: 18px; font-weight: 600; margin-top: 30px;">친밀도 점수: {results["intimacy_score"]}/100</p>', unsafe_allow_html=True)
    progress = results["intimacy_score"] / 100
    st.progress(progress)
    
    # 분석 세부 정보
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">분석 세부 정보</h3>', unsafe_allow_html=True)
    
    # 2단 컬럼으로 표시
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in list(results["analysis_details"].items())[:3]:
            st.markdown(f'<p style="color: #666666; font-size: 16px; margin-bottom: 10px;">• {key}: {value}</p>', unsafe_allow_html=True)
    
    with col2:
        for key, value in list(results["analysis_details"].items())[3:]:
            st.markdown(f'<p style="color: #666666; font-size: 16px; margin-bottom: 10px;">• {key}: {value}</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 특별 요인
    if results["special_factors"]:
        st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #D4A017; font-size: 18px; font-weight: 600; margin-bottom: 15px;">✨ 특별 가산 요인</h3>', unsafe_allow_html=True)
        for factor in results["special_factors"]:
            st.markdown(f'<p style="color: #666666; font-size: 16px; margin-bottom: 8px;">• {factor}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 팁 박스
    st.markdown('<div class="tip-section">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #666666; font-size: 16px;">💡 {results["funny_tip"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 버튼 영역
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
            if st.button("← 다시 분석", key="prev_btn_result"):
                prev_page()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with button_col2:
            if st.button("결과 저장", key="save_btn"):
                st.success("결과가 저장되었습니다!")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
