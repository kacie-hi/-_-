import streamlit as st
import random
import time
import re

# 페이지 설정 및 스타일링
st.set_page_config(
    page_title="AIxivity - 축의금 분석기",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 커스터마이징
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #FF5757, #5E17EB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        padding: 20px;
    }
    
    .sub-header {
        font-size: 2rem;
        color: #5E17EB;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .intro-text {
        font-size: 1.2rem;
        color: #444;
        margin-bottom: 2rem;
        line-height: 1.6;
        text-align: center;
    }
    
    .highlight {
        background-color: #F0F2F6;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .result-card {
        background-color: #FFF0F0;
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid #FF5757;
        margin-top: 2rem;
        box-shadow: 0 10px 20px rgba(255,87,87,0.1);
    }
    
    .result-title {
        font-size: 1.8rem;
        color: #FF5757;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #FF5757, #FF8C8C);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.8rem 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1.5rem;
        width: 100%;
        box-shadow: 0 4px 10px rgba(255,87,87,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(255,87,87,0.4);
    }
    
    .step-container {
        background-color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2.5rem;
        border: 1px solid #e0e0e0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .progress-label {
        text-align: center;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        color: #666;
    }
    
    .step-nav {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }
    
    .emoji-big {
        font-size: 3rem;
        margin-bottom: 1rem;
        text-align: center;
        display: block;
    }
    
    .card-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-align: center;
        display: block;
    }
    
    .feature-title {
        font-size: 1.3rem;
        color: #333;
        margin-bottom: 0.5rem;
        font-weight: 600;
        text-align: center;
    }
    
    .feature-text {
        color: #666;
        text-align: center;
        font-size: 1rem;
    }
    
    /* 버튼 큰 버전 */
    .big-button {
        text-align: center;
        padding: 20px 0;
    }
    
    .big-button .stButton>button {
        max-width: 300px;
        height: 60px;
        font-size: 1.4rem;
    }
    
    /* 진행 상황 표시 */
    .progress-bar-container {
        margin: 40px 0;
    }
    
    .progress-step {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    
    .progress-step-item {
        text-align: center;
        width: 25%;
        position: relative;
    }
    
    .progress-step-item.active .step-number {
        background-color: #FF5757;
        color: white;
    }
    
    .progress-step-item.completed .step-number {
        background-color: #5E17EB;
        color: white;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px;
        font-weight: bold;
        border: 2px solid #ddd;
    }
    
    .step-name {
        font-size: 0.9rem;
        color: #666;
    }
    
    .progress-line {
        height: 4px;
        background-color: #f0f0f0;
        position: relative;
    }
    
    .progress-line-fill {
        height: 100%;
        background: linear-gradient(90deg, #FF5757, #5E17EB);
        position: absolute;
        top: 0;
        left: 0;
        transition: width 0.5s;
    }
    
    /* 폼 스타일링 */
    .form-label {
        font-weight: 600;
        color: #333;
        margin-bottom: 0.5rem;
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[role="radiogroup"] > label {
        background-color: #f8f9fa;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        transition: all 0.2s;
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[role="radiogroup"] > label:hover {
        background-color: #e9ecef;
    }
    
    /* 특별 디자인 요소 */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #ddd, transparent);
        margin: 2rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = "intro"  # 초기 페이지: intro, step1, step2, step3, result
if 'conversation_text' not in st.session_state:
    st.session_state.conversation_text = ""
if 'relationship_type' not in st.session_state:
    st.session_state.relationship_type = "친구"
if 'relationship_duration' not in st.session_state:
    st.session_state.relationship_duration = 5
if 'meeting_frequency' not in st.session_state:
    st.session_state.meeting_frequency = "월 1-2회"
if 'emotional_closeness' not in st.session_state:
    st.session_state.emotional_closeness = 7
if 'has_helped' not in st.session_state:
    st.session_state.has_helped = False
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = "재미 위주 🎭"
if 'event_type' not in st.session_state:
    st.session_state.event_type = "결혼식"
if 'your_budget' not in st.session_state:
    st.session_state.your_budget = 10
if 'is_attending' not in st.session_state:
    st.session_state.is_attending = True
if 'analysis_results' not in st.session_state:
    # 랜덤 분석 결과 미리 생성
    st.session_state.analysis_results = {
        "conversation_score": random.randint(40, 100),
        "relationship_score": random.randint(40, 100),
        "emotional_score": random.randint(40, 100),
        "selected_archetype": {
            "name": random.choice(["영혼의 단짝", "밥약 전문가", "온라인 친밀러", "공백기 마스터"]),
            "score": random.randint(40, 100),
            "emoji": random.choice(["✨", "🍽️", "💻", "⏳"]),
            "description": "매우 특별한 관계입니다."
        }
    }

# 페이지 네비게이션 함수
def set_page(page_name):
    st.session_state.page = page_name
    # 더 이상 st.experimental_rerun() 사용하지 않음

# 진행 상황 표시 함수
def show_progress_bar(current_step):
    progress_percentages = {
        "intro": 0,
        "step1": 33,
        "step2": 66,
        "step3": 100,
        "result": 100
    }
    
    current_percentage = progress_percentages.get(current_step, 0)
    
    st.markdown("""
    <div class="progress-bar-container">
        <div class="progress-step">
            <div class="progress-step-item {0}">
                <div class="step-number">1</div>
                <div class="step-name">시작하기</div>
            </div>
            <div class="progress-step-item {1}">
                <div class="step-number">2</div>
                <div class="step-name">관계 정보</div>
            </div>
            <div class="progress-step-item {2}">
                <div class="step-number">3</div>
                <div class="step-name">대화 분석</div>
            </div>
            <div class="progress-step-item {3}">
                <div class="step-number">4</div>
                <div class="step-name">결과</div>
            </div>
        </div>
        <div class="progress-line">
            <div class="progress-line-fill" style="width: {4}%;"></div>
        </div>
    </div>
    """.format(
        "active" if current_step == "intro" else ("completed" if current_percentage > 0 else ""),
        "active" if current_step == "step1" else ("completed" if current_percentage > 33 else ""),
        "active" if current_step == "step2" else ("completed" if current_percentage > 66 else ""),
        "active" if current_step in ["step3", "result"] else ("completed" if current_percentage == 100 else ""),
        current_percentage
    ), unsafe_allow_html=True)

# 헤더 표시
st.markdown("<h1 class='main-header'>💰 AIxivity - 축의금 분석기 💰</h1>", unsafe_allow_html=True)

# 현재 페이지에 따라 컨텐츠 표시
if st.session_state.page == "intro":
    # 시작 페이지
    show_progress_bar("intro")
    
    st.markdown("<p class='intro-text'>친구와의 대화와 관계를 AI가 분석하여<br>재미있고 신선한 축의금 금액을 제안해드립니다!</p>", unsafe_allow_html=True)
    
    # 특징 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🔍</span>
            <h3 class="feature-title">대화 패턴 분석</h3>
            <p class="feature-text">카카오톡 대화를 AI가 분석해 숨겨진 관계 패턴을 발견합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💝</span>
            <h3 class="feature-title">관계 유형 파악</h3>
            <p class="feature-text">여러분의 특별한 관계 유형을 재미있게 정의합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💰</span>
            <h3 class="feature-title">맞춤형 축의금 추천</h3>
            <p class="feature-text">관계와 대화 패턴에 기반한 특별한 축의금을 추천합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 모드 선택
    st.markdown("<h2 class='sub-header'>분석 모드 선택</h2>", unsafe_allow_html=True)
    
    analysis_mode = st.radio(
        "어떤 스타일의 결과를 원하시나요?",
        options=["재미 위주 🎭", "현실 반영 💼", "완전 랜덤 🎲"],
        index=["재미 위주 🎭", "현실 반영 💼", "완전 랜덤 🎲"].index(st.session_state.analysis_mode),
        horizontal=True
    )
    st.session_state.analysis_mode = analysis_mode
    
    # 모드 설명
    if analysis_mode == "재미 위주 🎭":
        st.markdown("""
        <div class="highlight">
            <h4>재미 위주 모드 💯</h4>
            <p>유쾌하고 기발한 축의금 제안을 받아보세요! 일반적인 금액부터 '빈 봉투 + 진심 어린 편지'나 '3만원 + 가족 식사 초대권'까지 재미있는 아이디어가 가득합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    elif analysis_mode == "현실 반영 💼":
        st.markdown("""
        <div class="highlight">
            <h4>현실 반영 모드 📊</h4>
            <p>관계 유형, 알고 지낸 기간, 이벤트 종류 등 실제 요소를 고려한 현실적인 축의금 제안을 받아보세요. 사회적 관례와 개인 관계를 모두 고려합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="highlight">
            <h4>완전 랜덤 모드 🎲</h4>
            <p>운명에 맡겨보세요! 완전히 무작위로 선택된 금액이나 아이디어가 제안됩니다. 예상치 못한 재미있는 결과를 경험해보세요.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 시작 버튼
    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button("시작하기", key="start_btn"):
        set_page("step1")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 사용 방법
    with st.expander("사용 방법"):
        st.markdown("""
        1. **관계 정보 입력**: 친구와의 관계 유형, 알고 지낸 기간, 친밀도 등을 입력합니다.
        2. **대화 내용 입력**: 카카오톡 대화 내용을 복사하여 붙여넣거나 파일로 업로드합니다.
        3. **분석 과정**: AI가 대화와 관계를 분석하여 패턴을 찾아냅니다.
        4. **결과 확인**: 관계 유형과 맞춤형 축의금 추천을 확인하세요!
        """)

elif st.session_state.page == "step1":
    # 1단계: 관계 정보 입력
    show_progress_bar("step1")
    
    st.markdown("<h2 class='sub-header'>👥 관계 정보 입력</h2>", unsafe_allow_html=True)
    st.markdown("축의금을 보낼 상대방과의 관계에 대한 정보를 알려주세요.", unsafe_allow_html=True)
    
    st.markdown("<div class='step-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        relationship_type = st.selectbox(
            "관계 유형",
            ["친구", "직장 동료", "학교 선후배", "가족/친척", "연인/배우자", "소모임/동호회", "기타"],
            index=["친구", "직장 동료", "학교 선후배", "가족/친척", "연인/배우자", "소모임/동호회", "기타"].index(st.session_state.relationship_type)
        )
        st.session_state.relationship_type = relationship_type
        
        relationship_duration = st.slider(
            "알고 지낸 기간 (년)",
            0, 30, st.session_state.relationship_duration
        )
        st.session_state.relationship_duration = relationship_duration
        
        meeting_frequency = st.select_slider(
            "만남 빈도",
            options=["거의 없음", "연 1-2회", "월 1-2회", "주 1회 이상", "거의 매일"],
            value=st.session_state.meeting_frequency
        )
        st.session_state.meeting_frequency = meeting_frequency
    
    with col2:
        emotional_closeness = st.slider(
            "감정적 친밀도 (1-10)",
            1, 10, st.session_state.emotional_closeness
        )
        st.session_state.emotional_closeness = emotional_closeness
        
        has_helped = st.checkbox("과거에 도움을 주고받은 적이 있나요?", value=st.session_state.has_helped)
        st.session_state.has_helped = has_helped
    
    # 이벤트 정보
    st.markdown("<h3>🎉 이벤트 정보</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        event_type = st.selectbox(
            "축하 이벤트 유형",
            ["결혼식", "돌잔치", "생일", "집들이", "승진", "개업/창업", "기타"],
            index=["결혼식", "돌잔치", "생일", "집들이", "승진", "개업/창업", "기타"].index(st.session_state.event_type)
        )
        st.session_state.event_type = event_type
    
    with col2:
        your_budget = st.number_input(
            "예상 예산 범위 (만원)",
            min_value=0,
            max_value=100,
            value=st.session_state.your_budget
        )
        st.session_state.your_budget = your_budget
        
        is_attending = st.checkbox("이벤트에 참석할 예정인가요?", value=st.session_state.is_attending)
        st.session_state.is_attending = is_attending
    
    # 버튼 영역
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("이전으로", key="prev_step1"):
            set_page("intro")
    
    with col2:
        if st.button("다음으로", key="next_step1"):
            set_page("step2")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "step2":
    # 2단계: 대화 내용 입력
    show_progress_bar("step2")
    
    st.markdown("<h2 class='sub-header'>💬 대화 내용 입력</h2>", unsafe_allow_html=True)
    st.markdown("더 정확한 분석을 위해 카카오톡 대화 내용을 입력해주세요.", unsafe_allow_html=True)
    
    st.markdown("<div class='step-container'>", unsafe_allow_html=True)
    
    # 대화 입력 방식
    input_method = st.radio(
        "대화 입력 방식을 선택하세요:",
        ["텍스트 직접 입력", "파일 업로드"],
        horizontal=True
    )
    
    if input_method == "텍스트 직접 입력":
        conversation_text = st.text_area(
            "친구와의 대화 내용을 붙여넣기 해주세요 (카카오톡 내보내기 형식 권장)",
            height=250,
            value=st.session_state.conversation_text,
            placeholder="2023년 4월 1일 오후 2:23, 친구: 오랜만이야! 잘 지냈어?\n2023년 4월 1일 오후 2:25, 나: 응 잘 지내고 있어! 너는 어때?\n..."
        )
        st.session_state.conversation_text = conversation_text
    else:
        uploaded_file = st.file_uploader("대화 파일을 업로드하세요 (.txt)", type=["txt"])
        if uploaded_file is not None:
            try:
                conversation_text = uploaded_file.getvalue().decode("utf-8")
                st.session_state.conversation_text = conversation_text
                st.success("파일 업로드 성공! 대화 내용이 로드되었습니다.")
                with st.expander("대화 내용 미리보기"):
                    st.text(conversation_text[:500] + "..." if len(conversation_text) > 500 else conversation_text)
            except Exception as e:
                st.error(f"파일 로드 중 오류가 발생했습니다: {e}")
    
    # 대화가 없을 경우 샘플 데이터 제공
    if not st.session_state.conversation_text:
        with st.expander("샘플 대화 사용하기"):
            st.info("실제 대화가 없으신가요? 아래 샘플 대화를 사용해보세요.")
            sample_conv = """2023년 4월 1일 오후 2:23, 친구: 오랜만이야! 잘 지냈어?
2023년 4월 1일 오후 2:25, 나: 응 잘 지내고 있어! 너는 어때?
2023년 4월 1일 오후 2:26, 친구: 나도 잘 지내! 그런데 좋은 소식이 있어
2023년 4월 1일 오후 2:27, 나: 오 무슨 소식??
2023년 4월 1일 오후 2:30, 친구: 다음 달에 결혼해! 초대장 보낼게 ㅎㅎ
2023년 4월 1일 오후 2:31, 나: 와 축하해!!! 정말 기쁜 소식이네!
2023년 4월 1일 오후 2:32, 친구: 고마워 ㅎㅎ 꼭 와줘~
2023년 4월 1일 오후 2:33, 나: 당연하지! 빠질 수 없지 ㅎㅎ
2023년 5월 10일 오후 1:15, 나: 결혼식 준비 잘 돼가?
2023년 5월 10일 오후 3:42, 친구: 응! 좀 바쁘긴 한데 재밌어
2023년 5월 10일 오후 3:45, 나: 도움 필요하면 말해~
2023년 5월 10일 오후 4:01, 친구: 고마워 😊 신경써줘서 감동이야
2023년 6월 5일 오후 2:10, 친구: 이번주 토요일에 시간 돼?
2023년 6월 5일 오후 2:15, 나: 응 왜?
2023년 6월 5일 오후 2:17, 친구: 결혼 전에 한번 만나서 밥이나 먹으려고!
2023년 6월 5일 오후 2:20, 나: 좋아! 어디서 만날까?
2023년 6월 5일 오후 2:25, 친구: 강남역 어때? 6시쯤?
2023년 6월 5일 오후 2:26, 나: 좋아 거기서 보자!"""
            if st.button("이 샘플 사용하기"):
                st.session_state.conversation_text = sample_conv
                st.success("샘플 대화가 입력되었습니다!")
    
    # 버튼 영역
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("이전으로", key="prev_step2"):
            set_page("step1")
    
    with col2:
        if st.button("분석 시작하기", key="next_step2"):
            # 대화가 없어도 진행 가능하게 함
            if not st.session_state.conversation_text:
                st.session_state.conversation_text = "샘플 대화"
            set_page("step3")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "step3":
    # 3단계: 분석 중 & 결과
    show_progress_bar("step3")
    
    st.markdown("<h2 class='sub-header'>🔍 대화 및 관계 분석 중...</h2>", unsafe_allow_html=True)

    # 로딩 애니메이션 표시
    with st.spinner("AI가 대화와 관계를 분석하고 있습니다..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.03)
            progress_bar.progress(i + 1)
        
        # 기본 분석 결과 (실제로는 랜덤 생성)
        total_messages = 0
        if st.session_state.conversation_text:
            total_messages = len(re.findall(r'\n', st.session_state.conversation_text)) + 1
        
        if total_messages < 5:  # 입력이 적거나 없는 경우
            total_messages = random.randint(15, 50)
        
        user_messages = random.randint(total_messages // 3, total_messages // 2)
        friend_messages = total_messages - user_messages
        
        # 분석 결과 업데이트
        st.session_state.analysis_results["total_messages"] = total_messages
        st.session_state.analysis_results["user_messages"] = user_messages
        st.session_state.analysis_results["friend_messages"] = friend_messages
        st.session_state.analysis_results["avg_response_time"] = random.randint(10, 180)
        st.session_state.analysis_results["most_used_word"] = random.choice(['ㅋㅋㅋ', '응', '그래', '좋아', '알겠어', '언제', '어디서', '밥', '술'])
    
    st.success("분석이 완료되었습니다!")
    
    # 분석 결과 표시
    st.markdown("<div class='step-container'>", unsafe_allow_html=True)
    
    # 대화 패턴 분석 결과
    st.markdown("<h3>📊 대화 패턴 분석</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown(f"**총 메시지 수:** {st.session_state.analysis_results['total_messages']}개")
        st.markdown(f"**내가 보낸 메시지:** {st.session_state.analysis_results['user_messages']}개 ({st.session_state.analysis_results['user_messages']/st.session_state.analysis_results['total_messages']:.0%})")
        st.markdown(f"**친구가 보낸 메시지:** {st.session_state.analysis_results['friend_messages']}개 ({st.session_state.analysis_results['friend_messages']/st.session_state.analysis_results['total_messages']:.0%})")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown(f"**평균 응답 시간:** {st.session_state.analysis_results['avg_response_time']}분")
        st.markdown(f"**가장 많이 사용한 단어:** '{st.session_state.analysis_results['most_used_word']}'")
        conversation_activity = random.choice(["아침형", "저녁형", "주말형", "평일형", "불규칙형"])
        st.markdown(f"**대화 활동 패턴:** {conversation_activity}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 관계 분석 결과
    st.markdown("<h3>👫 관계 분석</h3>", unsafe_allow_html=True)
    
    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
    st.markdown(f"**소통 지수:** {st.session_state.analysis_results['conversation_score']}/100")
    st.markdown(f"**친밀도 지수:** {st.session_state.analysis_results['relationship_score']}/100")
    st.markdown(f"**정서적 연결:** {st.session_state.analysis_results['emotional_score']}/100")
    overall_score = (st.session_state.analysis_results['conversation_score'] + st.session_state.analysis_results['relationship_score'] + st.session_state.analysis_results['emotional_score']) // 3
    st.markdown(f"**전체 관계 점수:** {overall_score}/100")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 관계 유형 분석
    st.markdown("<h3>🔍 당신의 관계 유형</h3>", unsafe_allow_html=True)
    
    selected_archetype = st.session_state.analysis_results["selected_archetype"]
    
    st.markdown("<div class='highlight'>", unsafe_allow_html=True)
    st.markdown(f"### {selected_archetype['emoji']} 관계 유형: {selected_archetype['name']}")
    st.markdown(f"**{selected_archetype['description']}**")
    st.markdown(f"관계 점수: {selected_archetype['score']}/100")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 특별한 인사이트
    st.markdown("<h3>💡 흥미로운 인사이트</h3>", unsafe_allow_html=True)
    
    interesting_insights = [
        f"당신은 친구보다 평균 {random.randint(5, 30)}분 더 빨리 응답하는 경향이 있습니다.",
        f"당신들의 대화는 주로 {random.choice(['저녁', '늦은 밤', '아침', '주말'])}에 이루어집니다.",
        f"약속을 잡는 대화가 전체의 {random.randint(10, 40)}%를 차지합니다.",
        f"실제 만남으로 이어진 대화는 약 {random.randint(5, 25)}%에 불과합니다.",
        f"{random.choice(['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'])}에 가장 활발하게 대화하는 경향이 있습니다.",
        f"당신은 이모티콘을 친구보다 {random.randint(10, 50)}% 더 많이 사용합니다.",
        f"대화 중 '{random.choice(['밥', '술', '영화', '언제', '만나'])}'에 관한 내용이 가장 많습니다."
    ]
    
    for i, insight in enumerate(random.sample(interesting_insights, 3)):
        st.markdown(f"**{i+1}. {insight}**")
    
    # 버튼 영역
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("이전으로", key="prev_step3"):
            set_page("step2")
    
    with col2:
        if st.button("축의금 추천 받기", key="next_step3"):
            set_page("result")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.page == "result":
    # 결과 페이지: 축의금 추천
    show_progress_bar("result")
    
    st.markdown("<h2 class='sub-header'>💰 AI 축의금 추천 결과</h2>", unsafe_allow_html=True)
    
    # 로딩 효과
    with st.spinner("AI가 최적의 축의금을 계산하고 있습니다..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)
    
    # 축의금 추천 결과 카드
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    st.markdown("<h2 class='result-title'>🎁 AI의 최종 축의금 추천</h2>", unsafe_allow_html=True)
    
    # 선택된 모드에 따른 추천 생성
    mode = st.session_state.analysis_mode
    gift_options = []
    
    if mode == "재미 위주 🎭":
        # 재미있는 축의금 옵션들
        joke_options = [
            {
                "amount": "빈 봉투 + 진심 어린 편지",
                "description": "가끔은 진심 어린 마음이 돈보다 값진 법이죠. 특히 당신의 경우, 평소 감정적 표현이 부족한 것으로 분석되어 이런 방식이 더 인상적일 수 있습니다.",
                "emoji": "💌",
                "details": "봉투에 '마음만은 천만원'이라고 써서 드리세요."
            },
            {
                "amount": "3만원 + 가족 2명 데리고 식사",
                "description": "당신들의 대화에서 '밥 먹자'는 말이 자주 등장하지만 실제로 만난 횟수는 적습니다. 이번 기회에 진짜로 만나서 먹어보는 건 어떨까요?",
                "emoji": "🍽️",
                "details": "식사 후 영수증을 봉투에 같이 넣어드리면 더 재밌는 선물이 될 수 있어요."
            },
            {
                "amount": "7만 4천 2백 33원",
                "description": "특별한 의미가 담긴 금액은 아니지만, 이렇게 디테일한 금액은 친구에게 강한 인상을 남길 수 있습니다. 상대방이 왜 이런 금액인지 평생 궁금해할 거예요.",
                "emoji": "🔢",
                "details": "봉투에 '이 금액의 의미를 알아내면 추가 선물 증정'이라고 써보세요."
            },
            {
                "amount": "10만원 + 3만원 상당 선물",
                "description": f"현금과 선물의 조합. 당신의 관계 유형인 '{st.session_state.analysis_results['selected_archetype']['name']}'에게는 존재감을 확실히 각인시킬 수 있는 방법입니다.",
                "emoji": "🎁",
                "details": "선물은 상대방이 대화에서 자주 언급한 관심사와 관련된 것이 좋습니다."
            },
            {
                "amount": "랜덤 금액 봉투 3개 (총 10만원)",
                "description": "각각 다른 금액이 들어있는 봉투 3개를 준비해서 하나를 선택하게 하는 방식. 당신들의 대화에서 '선택장애'가 자주 언급되었기에 재미있는 요소가 될 수 있습니다.",
                "emoji": "🎲",
                "details": "예: 3만원, 5만원, 2만원 봉투를 준비하고 랜덤으로 선택하게 합니다."
            }
        ]
        
        # 랜덤하게 3개 선택
        gift_options = random.sample(joke_options, 3)
    
    elif mode == "현실 반영 💼":
        # 현실적인 축의금 계산
        base_amount = 5  # 5만원 기본
        
        # 관계 유형에 따른 조정
        relation_adjust = {
            "친구": 2,
            "직장 동료": 1,
            "학교 선후배": 1.5,
            "가족/친척": 3,
            "연인/배우자": 3,
            "소모임/동호회": 1,
            "기타": 1
        }
        
        # 이벤트 유형에 따른 조정
        event_adjust = {
            "결혼식": 1.5,
            "돌잔치": 1,
            "생일": 0.6,
            "집들이": 0.8,
            "승진": 1,
            "개업/창업": 1.2,
            "기타": 1
        }
        
        # 알고 지낸 기간에 따른 조정 (최대 2배)
        duration_adjust = min(st.session_state.relationship_duration / 10, 2)
        
        # 감정적 친밀도에 따른 조정
        closeness_adjust = st.session_state.emotional_closeness / 5
        
        # 최종 금액 계산
        amount = base_amount * relation_adjust.get(st.session_state.relationship_type, 1) * event_adjust.get(st.session_state.event_type, 1) * duration_adjust * closeness_adjust
        amount = round(amount)  # 반올림
        
        # 적절한 단위로 반올림 (1, 3, 5, 10만원 단위)
        if amount <= 3:
            amount = 3
        elif amount <= 5:
            amount = 5
        elif amount <= 10:
            amount = 10
        else:
            amount = round(amount / 5) * 5  # 5만원 단위로 반올림
        
        gift_options = [
            {
                "amount": f"{amount}만원",
                "description": f"당신의 관계와 상황을 분석했을 때, 현실적으로 적절한 금액입니다. {st.session_state.relationship_type}이고 {st.session_state.relationship_duration}년간 알아온 관계를 고려했습니다.",
                "emoji": "💸",
                "details": "일반적인 사회적 관례와 개인적 관계를 모두 고려한 금액입니다."
            },
            {
                "amount": f"{amount-2}만원",
                "description": "조금 더 경제적인 옵션입니다. 현재 경제 상황이 부담스럽다면 이 정도도 무난합니다.",
                "emoji": "💰",
                "details": "조금 적더라도 정성스러운 카드를 함께 준비하면 좋습니다."
            },
            {
                "amount": f"{amount+3}만원",
                "description": "조금 더 넉넉한 옵션입니다. 특별히 친밀한 관계이거나 경제적으로 여유가 있다면 고려해보세요.",
                "emoji": "💎",
                "details": "향후 관계 발전을 위한 투자로 생각해도 좋습니다."
            }
        ]
    
    else:  # 완전 랜덤
        random_options = [
            {
                "amount": f"{random.choice([1, 2, 3, 5, 7, 9, 10, 15, 20, 30, 50])}만원",
                "description": "AI가 완전히 랜덤하게 선택한 금액입니다. 운명에 맡겨보세요!",
                "emoji": "🎯",
                "details": "랜덤이지만 어쩌면 이게 가장 적절한 금액일지도..."
            },
            {
                "amount": "커피 쿠폰 10장",
                "description": "현금 대신 실용적인 선물을 해보는 것은 어떨까요?",
                "emoji": "☕",
                "details": "현금보다 더 오래 기억에 남을 수 있는 선물입니다."
            },
            {
                "amount": "축하 영상 + 5만원",
                "description": "특별한 축하 영상과 함께 적당한 금액을 준비해보세요.",
                "emoji": "🎬",
                "details": "영상은 30초~1분 정도면 충분합니다. 진심이 담긴 메시지가 중요해요."
            },
            {
                "amount": "비밀 봉투 게임",
                "description": "1만원~20만원 사이의 금액이 랜덤하게 들어있는 봉투를 3개 준비해서 하나를 고르게 하세요.",
                "emoji": "🎮",
                "details": "게임의 재미와 설렘이 더해져 특별한 축하가 됩니다."
            },
            {
                "amount": "분할 지급 약속 (총 10만원)",
                "description": "지금 5만원, 6개월 후에 5만원을 약속하는 재미있는 방식입니다.",
                "emoji": "⏳",
                "details": "장기적인 관계를 유지하겠다는 의미 있는 제스처가 될 수 있습니다."
            }
        ]
        
        # 랜덤하게 3개 선택
        gift_options = random.sample(random_options, 3)
    
    # 메인 추천 표시
    main_option = random.choice(gift_options)
    
    st.markdown(f"<span class='emoji-big'>{main_option['emoji']}</span>", unsafe_allow_html=True)
    st.markdown(f"## 추천 축의금: {main_option['amount']}")
    st.markdown(f"**{main_option['description']}**")
    st.markdown(f"*{main_option['details']}*")
    
    # 다른 추천 옵션 보기
    other_options = [opt for opt in gift_options if opt != main_option]
    
    if st.button("다른 추천 옵션 보기"):
        st.markdown("<div class='card-container'>", unsafe_allow_html=True)
        
        for i, option in enumerate(other_options):
            st.markdown(f"""
            <div class="feature-card">
                <span class="feature-icon">{option['emoji']}</span>
                <h3 class="feature-title">{option['amount']}</h3>
                <p><strong>{option['description']}</strong></p>
                <p><em>{option['details']}</em></p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 관계 및 이벤트 요약
    st.markdown("<h3>🔍 분석 요약</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown(f"**관계 유형:** {st.session_state.relationship_type}")
        st.markdown(f"**알고 지낸 기간:** {st.session_state.relationship_duration}년")
        st.markdown(f"**만남 빈도:** {st.session_state.meeting_frequency}")
        st.markdown(f"**감정적 친밀도:** {st.session_state.emotional_closeness}/10")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown(f"**이벤트 유형:** {st.session_state.event_type}")
        attendance_status = "참석 예정" if st.session_state.is_attending else "불참 예정"
        st.markdown(f"**참석 여부:** {attendance_status}")
        st.markdown(f"**예산 범위:** {st.session_state.your_budget}만원")
        st.markdown(f"**관계 점수:** {overall_score}/100")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 특별 메시지
    special_messages = [
        "절대 정답은 없습니다! 당신의 상황과 관계에 맞게 조정하세요.",
        "축의금보다 마음이 더 중요해요. 진심 어린 축하의 말 한마디가 큰 선물이 됩니다.",
        "금액에 집착하지 마세요. 관계의 질과 상황에 맞게 결정하는 것이 좋습니다.",
        "재미있는 요소를 더하면 금액과 상관없이 기억에 남는 선물이 됩니다.",
        "이 추천은 참고용입니다. 최종 결정은 당신의 판단에 맡깁니다!"
    ]
    
    st.markdown("---")
    st.markdown(f"*💡 {random.choice(special_messages)}*")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 처음으로 / 다시하기 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("분석 결과로 돌아가기", key="back_to_analysis"):
            set_page("step3")
    
    with col2:
        if st.button("처음부터 다시하기", key="restart"):
            st.session_state.page = "intro"
    
    # 피드백 섹션
    st.markdown("<h3>💬 이 결과가 도움이 되었나요?</h3>", unsafe_allow_html=True)
    
    feedback = st.radio(
        "분석 결과에 대한 만족도를 선택해주세요:",
        ["매우 만족", "만족", "보통", "불만족", "매우 불만족"],
        horizontal=True
    )
    
    feedback_text = st.text_area("추가 의견이 있다면 알려주세요:", placeholder="의견을 입력해주세요...")
    
    if st.button("피드백 제출하기"):
        st.success("피드백을 제출해주셔서 감사합니다! 더 나은 서비스를 위해 노력하겠습니다.")

# 푸터
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown(
    "<div class='footer'>"
    "© 2025 AIxivity | 비개발자 AI 크리에이터 프로젝트<br>"
    "축의금 분석기는 재미 목적으로 제작되었으며, 실제 금액은 개인의 판단에 따라 결정하세요.<br>"
    "문의: aixivity@example.com"
    "</div>",
    unsafe_allow_html=True
)
