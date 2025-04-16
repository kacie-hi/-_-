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

# CSS 스타일 - 개선된 버전
def set_custom_style():
    st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #FFF8E1, #FFECB3);
    }
    
    /* 컨테이너 스타일 */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* 카드 스타일 - 더 깔끔하고 일관된 디자인 */
    .card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 32px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }
    
    /* 카드 호버 효과 */
    .card:hover {
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    /* 헤더 스타일 */
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #F0F0F0;
    }
    
    /* 타이틀 스타일 - 더 현대적인 폰트 크기와 가중치 */
    .title {
        color: #333333;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        color: #333333;
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin: 16px 0;
        letter-spacing: -0.02em;
    }
    
    /* 라벨 스타일 */
    .label {
        color: #333333;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
        margin-top: 24px;
    }
    
    /* 버튼 스타일 - 더 현대적인 디자인 */
    .stButton > button {
        background-color: #FF9800;
        color: white;
        font-weight: 600;
        border-radius: 12px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 4px 12px rgba(255, 152, 0, 0.2);
        transition: all 0.2s ease;
        font-size: 16px;
        letter-spacing: -0.01em;
    }
    
    .stButton > button:hover {
        background-color: #F57C00;
        box-shadow: 0 6px 16px rgba(255, 152, 0, 0.3);
        transform: translateY(-2px);
    }
    
    /* 두 번째 버튼 스타일 (회색) */
    .secondary-button > button {
        background-color: #F5F5F5;
        color: #555555;
        border: none;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    .secondary-button > button:hover {
        background-color: #EEEEEE;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
    
    /* 인풋 스타일 - 더 깔끔한 디자인 */
    .stSelectbox > div[data-baseweb="select"] > div {
        background-color: #F9F9F9;
        border-radius: 12px;
        border: 1px solid #EEEEEE;
        padding: 8px 12px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div[data-baseweb="select"] > div:focus-within {
        border-color: #FF9800;
        box-shadow: 0 0 0 2px rgba(255, 152, 0, 0.1);
    }
    
    .stTextArea > div > div > textarea {
        background-color: #F9F9F9;
        border-radius: 12px;
        border: 1px solid #EEEEEE;
        padding: 16px;
        font-size: 16px;
        transition: all 0.2s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #FF9800;
        box-shadow: 0 0 0 2px rgba(255, 152, 0, 0.1);
    }
    
    /* 결과 금액 스타일 - 더 강조된 디자인 */
    .result-amount {
        font-size: 56px;
        font-weight: 800;
        color: #FF9800;
        text-align: center;
        margin: 32px 0;
        letter-spacing: -0.03em;
    }
    
    /* 특별 요인 카드 */
    .factor-card {
        background-color: #FFF8E1;
        border-radius: 12px;
        padding: 24px;
        margin: 24px 0;
        border-left: 4px solid #FFB74D;
    }
    
    /* 팁 카드 */
    .tip-card {
        background-color: #F5F5F5;
        border-radius: 12px;
        padding: 24px;
        margin: 24px 0;
        border-left: 4px solid #BDBDBD;
    }
    
    /* 페이지 인디케이터 - 더 세련된 디자인 */
    .page-indicator {
        display: flex;
        justify-content: center;
        margin: 32px 0;
    }
    
    .indicator-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: rgba(255, 152, 0, 0.3);
        margin: 0 8px;
        display: inline-block;
        transition: all 0.2s ease;
    }
    
    .active-dot {
        background-color: #FF9800;
        transform: scale(1.2);
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        color: #757575;
        font-size: 14px;
        opacity: 0.8;
        margin-top: 48px;
        padding-bottom: 24px;
    }
    
    /* 태그 스타일 */
    .tag {
        display: inline-block;
        background-color: #F5F5F5;
        color: #555555;
        border-radius: 20px;
        padding: 6px 16px;
        margin-right: 8px;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* 카드 헤더 */
    .card-header {
        background-color: #FFF8E1;
        border-radius: 16px 16px 0 0;
        padding: 24px 32px;
        margin: -32px -32px 24px -32px;
        border-bottom: 1px solid #FFE0B2;
    }
    
    /* 중앙 정렬 컨테이너 */
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        margin: 32px 0;
        padding: 0 16px;
    }
    
    /* 진행 표시줄 스타일 개선 */
    .stProgress > div > div {
        background-color: #FFB74D !important;
    }
    
    /* 분석 세부 정보 항목 */
    .analysis-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        background-color: #F9F9F9;
        border-radius: 12px;
        margin-bottom: 8px;
    }
    
    .analysis-item-label {
        font-weight: 600;
        color: #555555;
        margin-right: 8px;
    }
    
    .analysis-item-value {
        color: #333333;
    }
    
    /* 반응형 디자인 개선 */
    @media (max-width: 768px) {
        .card {
            padding: 24px;
        }
        
        .card-header {
            padding: 20px 24px;
            margin: -24px -24px 20px -24px;
        }
        
        .title {
            font-size: 28px;
        }
        
        .subtitle {
            font-size: 28px;
        }
        
        .result-amount {
            font-size: 42px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 개선된 SVG 이미지 렌더링 함수
def render_svg(svg_code):
    b64 = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" style="max-width: 100%;">'
    return html

# 개선된 봉투 + 하트 SVG 코드
def get_envelope_svg(width=300, height=180):
    svg = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
          <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.15"/>
        </filter>
        <linearGradient id="envelopeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FFFFFF" />
          <stop offset="100%" stop-color="#F5F5F5" />
        </linearGradient>
        <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FF7043" />
          <stop offset="100%" stop-color="#FF9800" />
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="300" height="180" rx="16" ry="16" fill="url(#envelopeGradient)" stroke="#EEEEEE" stroke-width="2" filter="url(#shadow)" />
      <path d="M0,0 L150,75 L300,0" fill="none" stroke="#EEEEEE" stroke-width="2" />
      <path d="M150,105 C150,80 135,70 125,70 C110,70 102,90 102,105 C102,120 115,135 150,155 C185,135 198,120 198,105 C198,90 190,70 175,70 C165,70 150,80 150,105 Z" fill="url(#heartGradient)" />
    </svg>
    """
    return svg

# 페이지 인디케이터 - 개선된 버전
def show_page_indicator(current_page, total_pages=3):
    html = '<div class="page-indicator">'
    for i in range(1, total_pages + 1):
        if i == current_page:
            html += '<div class="indicator-dot active-dot"></div>'
        else:
            html += '<div class="indicator-dot"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# 대화 분석 함수 - 로직은 동일하게 유지
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

# 메인 함수 - 개선된 레이아웃
def main():
    # 스타일 적용
    set_custom_style()
    
    # 전체 컨테이너 시작
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # 헤더 (2, 3페이지에만 표시)
    if st.session_state.page > 1:
        st.markdown('<div class="header">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 5])
        with col1:
            envelope_svg = get_envelope_svg(width=60, height=36)
            st.markdown(render_svg(envelope_svg), unsafe_allow_html=True)
        with col2:
            st.markdown('<h2 style="color: #333333; font-size: 24px; font-weight: 700; margin-top: 0;">축의금 책정기</h2>', unsafe_allow_html=True)
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
    
    # 전체 컨테이너 종료
    st.markdown('</div>', unsafe_allow_html=True)

# 시작 페이지 - 개선된 디자인
def show_start_page():
    # 중앙 정렬을 위한 컨테이너
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    # 봉투 아이콘 - 더 세련된 디자인
    envelope_svg = get_envelope_svg(width=280, height=180)
    st.markdown(render_svg(envelope_svg), unsafe_allow_html=True)
    
    # 서브타이틀
    st.markdown('<p class="subtitle">당신의 마음을 금액으로 표현해드립니다</p>', unsafe_allow_html=True)
    
    # 간단한 설명 추가
    st.markdown('<p style="color: #757575; font-size: 18px; text-align: center; margin-bottom: 32px;">대화 내용을 분석하여 최적의 축의금 금액을 추천해드립니다</p>', unsafe_allow_html=True)
    
    # 시작하기 버튼
    if st.button('축의금 책정하기', key='start_btn'):
        next_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 입력 페이지 - 개선된 레이아웃
def show_input_page():
    # 카드 시작
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 카드 헤더
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<h2 class="title">정보 입력</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #757575; font-size: 16px;">축의금 분석을 위한 정보를 입력해주세요</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 행사 유형
    st.markdown('<p class="label">행사 유형</p>', unsafe_allow_html=True)
    event_type = st.selectbox(
        "",
        ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"],
        label_visibility="collapsed"
    )
    
    # 관계
    st.markdown('<p class="label">상대방과의 관계</p>', unsafe_allow_html=True)
    relationship = st.selectbox(
        "",
        ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"],
        label_visibility="collapsed"
    )
    
    # 대화 내용
    st.markdown('<p class="label">대화 내용</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: #757575; font-size: 14px; margin-bottom: 8px;">카카오톡, 메시지 등의 대화 내용을 복사해서 붙여넣으세요</p>', unsafe_allow_html=True)
    conversation = st.text_area(
        "",
        height=200,
        placeholder="여기에 대화 내용을 붙여넣으세요...",
        label_visibility="collapsed"
    )
    
    # 버튼 영역 - 개선된 레이아웃
    st.markdown('<div style="display: flex; gap: 16px; margin-top: 32px;">', unsafe_allow_html=True)
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# 결과 페이지 - 개선된 디자인
def show_result_page():
    if not st.session_state.analysis_results:
        st.error("분석 결과가 없습니다. 처음부터 다시 시작해주세요.")
        if st.button("처음으로 돌아가기"):
            go_to_page(1)
        return
    
    results = st.session_state.analysis_results
    
    # 카드 시작
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 카드 헤더
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<h2 class="title">분석 결과</h2>', unsafe_allow_html=True)
    
    # 태그 표시 - 개선된 레이아웃
    st.markdown(f'<div style="display: flex; gap: 8px; margin-top: 12px;">', unsafe_allow_html=True)
    st.markdown(f'<span class="tag">{st.session_state.event_type}</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="tag">{st.session_state.relationship}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 결과 표시 영역 - 개선된 레이아웃
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 봉투 아이콘 - 더 세련된 디자인
        envelope_svg = get_envelope_svg(width=150, height=90)
        st.markdown(render_svg(envelope_svg), unsafe_allow_html=True)
    
    with col2:
        # 결과 금액 - 더 강조된 디자인
        st.markdown(f'<div class="result-amount">{results["amount"]:,}원</div>', unsafe_allow_html=True)
    
    # 친밀도 점수 - 개선된 디자인
    st.markdown(f'  unsafe_allow_html=True)
    
    # 친밀도 점수 - 개선된 디자인
    st.markdown(f'<p style="color: #333333; font-size: 18px; font-weight: 600; margin-top: 24px; margin-bottom: 8px;">친밀도 점수: {results["intimacy_score"]}/100</p>', unsafe_allow_html=True)
    progress = results["intimacy_score"] / 100
    st.progress(progress)
    
    # 분석 세부 정보 - 개선된 레이아웃
    st.markdown('<h3 style="color: #333333; font-size: 20px; font-weight: 700; margin-top: 32px; margin-bottom: 16px;">분석 세부 정보</h3>', unsafe_allow_html=True)
    
    # 분석 세부 정보를 카드 형태로 표시
    for key, value in results["analysis_details"].items():
        st.markdown(f'''
        <div class="analysis-item">
            <span class="analysis-item-label">{key}:</span>
            <span class="analysis-item-value">{value}</span>
        </div>
        ''', unsafe_allow_html=True)
    
    # 특별 요인 - 개선된 디자인
    if results["special_factors"]:
        st.markdown('<div class="factor-card">', unsafe_allow_html=True)
        st.markdown('<p style="color: #F57C00; font-size: 18px; font-weight: 600; margin-bottom: 16px;">✨ 특별 가산 요인</p>', unsafe_allow_html=True)
        for factor in results["special_factors"]:
            st.markdown(f'<p style="color: #555555; font-size: 16px; margin-bottom: 8px;">• {factor}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 팁 박스 - 개선된 디자인
    st.markdown('<div class="tip-card">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #555555; font-size: 16px;">💡 {results["funny_tip"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 버튼 영역 - 개선된 레이아웃
    st.markdown('<div style="display: flex; justify-content: center; gap: 16px; margin-top: 32px;">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        if st.button("← 다시 분석", key="prev_btn_result"):
            prev_page()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("결과 저장하기", key="save_btn"):
            st.success("결과가 저장되었습니다!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
