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

# CSS 스타일
def set_custom_style():
    st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }
    
    /* 배경색 */
    .stApp {
        background: linear-gradient(135deg, #FFEBB3, #F7D358);
    }
    
    /* 카드 스타일 */
    .card {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        margin-bottom: 20px;
    }
    
    /* 헤더 스타일 */
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 30px;
    }
    
    /* 타이틀 스타일 */
    .title {
        color: #452c22;
        font-size: 36px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .subtitle {
        color: #452c22;
        font-size: 40px;
        font-weight: 600;
        text-align: center;
        margin: 20px 0;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* 라벨 스타일 */
    .label {
        color: #452c22;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
        margin-top: 20px;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #E8A02F;
        color: white;
        font-weight: 600;
        border-radius: 30px;
        padding: 12px 24px;
        border: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #D4901A;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    /* 두 번째 버튼 스타일 (회색) */
    .secondary-button > button {
        background-color: #F0F0F0;
        color: #666666;
        border: 1px solid #E0E0E0;
        box-shadow: none;
    }
    
    .secondary-button > button:hover {
        background-color: #E8E8E8;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* 인풋 스타일 */
    .stSelectbox > div[data-baseweb="select"] > div {
        background-color: #F9F9F9;
        border-radius: 10px;
        border-color: #E0E0E0;
        padding: 5px;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #F9F9F9;
        border-radius: 10px;
        border-color: #E0E0E0;
        padding: 15px;
    }
    
    /* 결과 금액 스타일 */
    .result-amount {
        font-size: 64px;
        font-weight: 700;
        color: #E8A02F;
        text-align: center;
        margin: 30px 0;
    }
    
    /* 특별 요인 카드 */
    .factor-card {
        background-color: #FFF8E1;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 팁 카드 */
    .tip-card {
        background-color: #F5F5F5;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 페이지 인디케이터 */
    .page-indicator {
        display: flex;
        justify-content: center;
        margin: 30px 0;
    }
    
    .indicator-dot {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        background-color: rgba(232, 160, 47, 0.5);
        margin: 0 10px;
        display: inline-block;
    }
    
    .active-dot {
        background-color: #E8A02F;
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        color: #6D4C41;
        font-size: 16px;
        opacity: 0.7;
        margin-top: 50px;
        padding-bottom: 20px;
    }
    
    /* 태그 스타일 */
    .tag {
        display: inline-block;
        background-color: #F5F5F5;
        color: #666666;
        border-radius: 20px;
        padding: 5px 15px;
        margin-right: 10px;
        font-size: 16px;
        font-weight: 500;
    }
    
    /* 카드 헤더 */
    .card-header {
        background-color: #FFF8E1;
        border-radius: 20px 20px 0 0;
        padding: 30px 40px;
        margin: -40px -40px 30px -40px;
    }
    
    /* 중앙 정렬 컨테이너 */
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        text-align: center;
        margin: 30px 0;
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

# SVG 이미지 렌더링 함수
def render_svg(svg_code):
    b64 = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" style="max-width: 100%;">'
    return html

# 봉투 + 하트 SVG 코드
def get_envelope_svg(width=300, height=180):
    svg = f"""
    <svg width="{width}" height="{height}" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
      <rect x="0" y="0" width="300" height="180" rx="10" ry="10" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="3" />
      <path d="M0,0 L150,75 L300,0" fill="none" stroke="#EEEEEE" stroke-width="3" />
      <path d="M150,105 C150,80 135,70 125,70 C110,70 102,90 102,105 C102,120 115,135 150,155 C185,135 198,120 198,105 C198,90 190,70 175,70 C165,70 150,80 150,105 Z" fill="url(#heartGradient)" />
      
      <defs>
        <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FF6B6B" />
          <stop offset="100%" stop-color="#FF8E8E" />
        </linearGradient>
      </defs>
    </svg>
    """
    return svg

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
        col1, col2 = st.columns([1, 5])
        with col1:
            envelope_svg = get_envelope_svg(width=60, height=36)
            st.markdown(render_svg(envelope_svg), unsafe_allow_html=True)
        with col2:
            st.markdown('<h2 style="color: #452c22; font-size: 28px; font-weight: 600; margin-top: 0;">축의금 책정기</h2>', unsafe_allow_html=True)
        st.markdown('<hr style="margin-top: 0; margin-bottom: 30px; border-color: #F0F0F0;">', unsafe_allow_html=True)
    
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
    # 중앙 정렬을 위한 컨테이너
    st.markdown('<div class="center-container">', unsafe_allow_html=True)
    
    # 봉투 아이콘
    envelope_svg = get_envelope_svg(width=500, height=300)
    st.markdown(render_svg(envelope_svg), unsafe_allow_html=True)
    
    # 서브타이틀
    st.markdown('<p class="subtitle">당신의 마음을 금액으로 표현해드립니다</p>', unsafe_allow_html=True)
    
    # 버튼 공간 확보
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    # 시작하기 버튼
    if st.button('축의금 책정하기', key='start_btn'):
        next_page()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 입력 페이지
def show_input_page():
    # 카드 시작
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 타이틀
    st.markdown('<h2 class="title">정보 입력</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #666666; margin-bottom: 30px;">축의금 분석을 위한 정보를 입력해주세요</p>', unsafe_allow_html=True)
    
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
    
    # 카드 시작
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # 카드 헤더
    st.markdown('<div class="card-header">', unsafe_allow_html=True)
    st.markdown('<h2 class="title">분석 결과</h2>', unsafe_allow_html=True)
    
    # 태그 표시
    col1, col2, col3 = st.columns([5, 1, 1])
    with col2:
        st.markdown(f'<span class="tag">{st.session_state.event_type}</span>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<span class="tag">{st.session_state.relationship}</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 결과 표시 영역
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 봉투 아이콘
        envelope_svg = get_envelope_svg(width=150, height=90)
        st.markdown(render_svg(envelope_svg), unsafe_allow_html=True)
    
    with col2:
        # 결과 금액
        st.markdown(f'<div class="result-amount">{results["amount"]:,}원</div>', unsafe_allow_html=True)
    
    # 친밀도 점수
    st.markdown(f'<p style="color: #452c22; font-size: 20px; font-weight: 600; margin-top: 20px;">친밀도 점수: {results["intimacy_score"]}/100</p>', unsafe_allow_html=True)
    progress = results["intimacy_score"] / 100
    st.progress(progress)
    
    # 분석 세부 정보
    st.markdown('<h3 style="color: #452c22; font-size: 24px; font-weight: 600; margin-top: 30px; margin-bottom: 20px;">분석 세부 정보</h3>', unsafe_allow_html=True)
    
    # 2단 컬럼으로 표시
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in list(results["analysis_details"].items())[:3]:
            st.markdown(f'<p style="color: #666666; font-size: 18px; margin-bottom: 10px;">• {key}: {value}</p>', unsafe_allow_html=True)
    
    with col2:
        for key, value in list(results["analysis_details"].items())[3:]:
            st.markdown(f'<p style="color: #666666; font-size: 18px; margin-bottom: 10px;">• {key}: {value}</p>', unsafe_allow_html=True)
    
    # 특별 요인
    if results["special_factors"]:
        st.markdown('<div class="factor-card">', unsafe_allow_html=True)
        st.markdown('<p style="color: #D4A017; font-size: 20px; font-weight: 600; margin-bottom: 10px;">✨ 특별 가산 요인</p>', unsafe_allow_html=True)
        for factor in results["special_factors"]:
            st.markdown(f'<p style="color: #666666; font-size: 18px; margin-bottom: 5px;">• {factor}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 팁 박스
    st.markdown('<div class="tip-card">', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #666666; font-size: 18px;">💡 {results["funny_tip"]}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 버튼 영역 - 중앙 정렬
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        button_col1, button_col2 = st.columns(2)
        
        with button_col1:
            st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
            if st.button("← 다시 분석", key="prev_btn_result"):
                prev_page()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with button_col2:
            if st.button("저장하기", key="save_btn"):
                st.success("결과가 저장되었습니다!")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
