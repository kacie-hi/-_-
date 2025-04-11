import streamlit as st
import random
import time
import base64
from PIL import Image
import io

# 페이지 설정
st.set_page_config(
    page_title="그래서..얼마면 돼? - 축의금 결정기",
    page_icon="💸",
    layout="centered"
)

# CSS 스타일 적용
st.markdown("""
<style>
    /* 기본 색상 정의 */
    :root {
        --primary: #1e3a8a;
        --primary-light: #3b82f6;
        --primary-dark: #172554;
        --secondary: #e0f2fe;
        --accent: #f59e0b;
        --accent-light: #fde68a;
        --text: #0f172a;
        --text-light: #475569;
        --white: #ffffff;
    }

    /* 기본 스타일 */
    body {
        font-family: 'Noto Sans KR', sans-serif;
        color: var(--text);
        background-color: #f8fafc;
    }
    
    h1, h2, h3 {
        color: var(--primary);
        font-weight: bold;
    }
    
    h1 {
        font-size: 2.5rem;
    }
    
    .accent-text {
        color: var(--accent) !important;
        font-weight: bold;
    }
    
    /* 카드 스타일 */
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1);
        margin-bottom: 1.5rem;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 2rem;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(30, 58, 138, 0.2);
    }
    
    /* 결과 스타일 */
    .result-amount {
        font-size: 3rem;
        font-weight: 900;
        color: var(--accent);
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .result-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .result-title {
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 0.3rem;
    }
    
    .fun-fact {
        background-color: var(--secondary);
        padding: 1rem;
        border-radius: 0.5rem;
        font-style: italic;
        margin: 1.5rem 0;
    }
    
    .highlight-box {
        background-color: var(--accent-light);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid var(--accent);
        margin: 1.5rem 0;
    }
    
    /* 로딩 애니메이션 */
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
    
    .stTextInput>div>div>input {
        border: 2px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    .stTextArea>div>div>textarea {
        border: 2px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    /* 프로그레스 바 커스텀 */
    .stProgress > div > div > div > div {
        background-color: var(--primary-light);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# 재미있는 로딩 메시지
funny_quotes = [
    "인공지능이 여러분의 우정을 수치화하고 있습니다...",
    "축의금 데이터베이스를 검색 중... 왜 이렇게 인색하죠?",
    "이모티콘 사용 빈도 분석 중... 🤔💼🎉",
    "흠... 정말 이 사람 친구 맞나요?",
    "여러분의 대화 내용이 AI를 당황시키고 있습니다",
    "답장 시간을 계산 중... 3시간은 좀 너무하지 않나요?",
    "축의금 공식: (친밀도 × 0.3) + (만난 횟수 × 0.2) - (인색함 × 0.5)",
    "대화 분석 결과 '형식적 안부 묻기' 패턴 발견...",
    "'안 와도 돼~'라는 메시지는 보통 '와도 좋고 안 와도 좋아'라는 의미입니다",
    "재미있는 사실: 평균적인 축의금은 매년 인플레이션보다 빠르게 오르고 있습니다",
    "상대방의 경제 상황을 분석 중... 음, 어렵네요."
]

# 결과 데이터
result_variations = {
    "amounts": ["3만원", "5만원", "7만원", "10만원", "30만원", "500원(!)"],
    "intimacy": [
        "형식적인 동료 수준이네요. 이름 말고 뭐 아는 게 있나요?",
        "지인 정도? 애매한 사이입니다. 이모티콘도 없고 대화가 딱딱해요.",
        "겉으로는 친한 척하는 미묘한 관계군요.",
        "진짜 친한 것 같긴 한데... 축의금은 적당히!",
        "와... 완전 절친이네요! 대화가 너무 찐해요."
    ],
    "response_time": [
        "평균 5분 이내로 답장하다니, 진짜 한시도 떨어질 수 없는 사이군요!",
        "1시간 내로 답하는 걸 보니 꽤 신경쓰는 관계네요.",
        "평균 3시간... 음, 바쁜 일 있나봐요? 아니면 그냥 귀찮은 건가...",
        "하루 뒤에 답장하다니... 읽씹의 달인이시네요.",
        "일주일 뒤 답장은... 솔직히 기억도 안 날 것 같은데요?"
    ],
    "funny_comments": [
        "이 대화는 재미 지수 10%로 영화 엔딩 크레딧보다 지루합니다.",
        "재미 지수 35%... 지하철 안내방송보다 약간만 재미있네요.",
        "재미 지수 58%로 평범한 직장 회식 수준입니다.",
        "재미 지수 73%로 초등학교 개그 수준! 나쁘지 않아요!",
        "재미 지수 92%! 거의 전문 코미디언 수준이시네요!"
    ]
}

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

if 'chat_content' not in st.session_state:
    st.session_state.chat_content = ''

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {
        'amount': '',
        'intimacy': '',
        'response_time': '',
        'hidden_message': '',
        'special_finding': '',
        'funny_score': 0,
        'funny_comment': ''
    }

# 페이지 전환 함수
def change_page(page):
    st.session_state.page = page

# 분석 시작 함수
def start_analysis():
    if not st.session_state.chat_content:
        st.error('대화 내용을 입력해주세요!')
        return
    
    if not st.session_state.api_key:
        st.error('API 키를 입력해주세요! (실제 키가 아니어도 괜찮아요)')
        return
    
    change_page('loading')

# 분석 수행 (가상의 분석)
def perform_analysis():
    # 임의의 결과 생성
    st.session_state.analysis_results = {
        'amount': random.choice(result_variations['amounts']),
        'intimacy': random.choice(result_variations['intimacy']),
        'response_time': random.choice(result_variations['response_time']),
        'hidden_message': '"바쁘면 안 와도 돼~"라는 메시지 발견! 번역: "와도 되고 안 와도 됨 ㅇㅇ" → 이건 -1만원 감점 요소입니다.',
        'special_finding': '작년에 생일선물 준 적 있다는 이야기가 있네요! 이건 축의금 +1만원 보너스 요소입니다. (정확한 선물 가격은 알 수 없음)',
        'funny_score': random.randint(50, 95),
        'funny_comment': random.choice(result_variations['funny_comments'])
    }
    change_page('result')

# 결과 복사 함수
def copy_result():
    result_text = f"""[그래서..얼마면 돼?] AI 분석 결과

적정 축의금: {st.session_state.analysis_results['amount']}

친밀도 분석: {st.session_state.analysis_results['intimacy']}
응답 시간: {st.session_state.analysis_results['response_time']}
숨겨진 메시지: {st.session_state.analysis_results['hidden_message']}
특별 발견: {st.session_state.analysis_results['special_finding']}

웃음 지수: {st.session_state.analysis_results['funny_score']}%
{st.session_state.analysis_results['funny_comment']}

* 이 결과는 100% 진지한 분석 결과입니다. (농담입니다 😉)
"""
    # 클립보드에 직접 복사는 불가능하므로 텍스트를 보여줍니다
    st.code(result_text)
    st.success('위 텍스트를 복사하여 사용하세요!')

# 예시 대화 설정
example_chat = """나: 야 너 결혼한다면서? 축하해!!!
친구: 응 고마워 ㅎㅎ 5월 20일이야!
나: 오 멋지다~ 청첩장은 언제 보내줄거야?
친구: 다음 주쯤? 근데 너무 부담 갖지 마~ 바쁘면 안 와도 돼!
나: 아니야 당연히 가야지!! 작년에 내 생일 챙겨줬는데 ㅋㅋ"""

# 예시 대화 적용
def use_example():
    st.session_state.chat_content = example_chat
    st.experimental_rerun()

# 인트로 페이지
if st.session_state.page == 'intro':
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 4rem;'>💸</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>축의금 결정기</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>대화 내용만 넣으면 AI가 <span class='accent-text'>까칠하게 분석</span>해서 적정 축의금을 알려드립니다.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>\"이 정도 친구한테 <strong>얼마</strong>나 줘야 돼?\"<br>더 이상 고민하지 마세요!</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='highlight-box'><p style='text-align: center;'>✓ 완전히 재미용입니다! 진짜로 믿으시면 안 됩니다! 😉</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("시작하기", key="start_btn"):
            change_page('input')
    
    st.markdown("<div class='fun-fact'>약 42.7%의 사람들이 축의금 금액 결정에 30분 이상 고민합니다. (완전히 만들어낸 통계)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 입력 페이지
elif st.session_state.page == 'input':
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2>✉️ 대화 내용을 붙여넣으세요</h2>", unsafe_allow_html=True)
    st.markdown("<p>카톡, 메시지 대화 내용을 복사해서 아래에 붙여넣으세요.<br>대화 내용이 많을수록 더 재미있는(?) 분석이 가능합니다!</p>", unsafe_allow_html=True)
    
    st.text_input("API 키", placeholder="AI API 키를 입력하세요", type="password", key="api_key")
    st.caption("* API 키는 로컬에서만 사용되며 어디에도 저장되지 않습니다")
    
    st.text_area("대화 내용", placeholder="여기에 카톡 대화 내용을 붙여넣으세요...", height=200, key="chat_content")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("이전", key="back_to_intro"):
            change_page('intro')
    with col2:
        if st.button("분석 시작!", key="analyze_btn"):
            start_analysis()
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<h3>예시로 시작해보기</h3>", unsafe_allow_html=True)
    
    st.markdown("<div style='background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)
    st.code(example_chat)
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("이 예시로 분석하기"):
        use_example()
    
    st.markdown("</div>", unsafe_allow_html=True)

# 로딩 페이지
elif st.session_state.page == 'loading':
    st.markdown("<div class='card loading-spinner'>", unsafe_allow_html=True)
    
    progress_text = "분석 중입니다..."
    progress_bar = st.progress(0)
    
    # 로딩 중 메시지 표시
    message_placeholder = st.empty()
    
    for i in range(100):
        # 진행 상태 업데이트
        progress_bar.progress(i + 1)
        
        # 10% 단위로 메시지 변경
        if i % 10 == 0:
            message_placeholder.markdown(f"<p style='text-align: center;'>{random.choice(funny_quotes)}</p>", unsafe_allow_html=True)
        
        time.sleep(0.05)
    
    # 분석 수행 및 결과 페이지로 이동
    perform_analysis()
    
    st.markdown("</div>", unsafe_allow_html=True)

# 결과 페이지
elif st.session_state.page == 'result':
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🎉 분석 완료!</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center;'>여러가지 <span class='accent-text'>과학적인 요소</span>를 고려한 결과...</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='result-amount'>{st.session_state.analysis_results['amount']}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>이 금액이면 적절해 보이네요!<br>(농담이에요, 진지하게 받아들이지 마세요 😉)</p>", unsafe_allow_html=True)
    
    # 분석 상세 결과
    st.markdown("<div style='background-color: #e0f2fe; padding: 1.5rem; border-radius: 1rem; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='margin-bottom: 1rem;'>
        <div class='result-icon'>💔</div>
        <div class='result-title'>친밀도 분석</div>
        <div>{st.session_state.analysis_results['intimacy']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='margin-bottom: 1rem;'>
        <div class='result-icon'>⏰</div>
        <div class='result-title'>응답 시간</div>
        <div>{st.session_state.analysis_results['response_time']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='margin-bottom: 1rem;'>
        <div class='result-icon'>🔍</div>
        <div class='result-title'>숨겨진 메시지</div>
        <div>{st.session_state.analysis_results['hidden_message']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div>
        <div class='result-icon'>🎁</div>
        <div class='result-title'>특별 발견</div>
        <div>{st.session_state.analysis_results['special_finding']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 웃음 지수
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-weight: 700; color: #1e3a8a; margin-bottom: 0.5rem; font-size: 1.2rem;'>🤣 웃음 지수</div>", unsafe_allow_html=True)
    
    st.progress(st.session_state.analysis_results['funny_score'] / 100)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        st.markdown("<span style='color: #475569; font-size: 0.8rem;'>심각</span>", unsafe_allow_html=True)
    with col2:
        st.markdown("<span style='color: #475569; font-size: 0.8rem; display: block; text-align: center;'>보통</span>", unsafe_allow_html=True)
    with col3:
        st.markdown("<span style='color: #475569; font-size: 0.8rem; float: right;'>웃김</span>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='font-style: italic; color: #1e3a8a; margin-top: 0.5rem;'>{st.session_state.analysis_results['funny_comment']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # QR 코드 섹션
    st.markdown("<div style='background-color: #e0f2fe; padding: 1.5rem; border-radius: 1rem; margin: 2rem 0; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-weight: 700; color: #1e3a8a; margin-bottom: 0.5rem;'>💰 축의금 송금용 QR코드</div>", unsafe_allow_html=True)
    st.markdown("<p>농담입니다! 진짜 QR은 없어요 😅</p>", unsafe_allow_html=True)
    
    qr_placeholder = st.empty()
    qr_placeholder.markdown("""
    <div style='display: inline-block; background-color: white; padding: 0.5rem; border-radius: 0.5rem; margin-top: 0.5rem;'>
        <div style='width: 150px; height: 150px; background-color: #f8fafc; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; color: #475569; border: 1px dashed #e2e8f0;'>
            여기에 QR 코드가<br>있었으면 좋았을텐데...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 공유 버튼들
    col1, col2 = st.columns(2)
    with col1:
        if st.button("결과 복사"):
            copy_result()
    with col2:
        if st.button("카톡 공유"):
            st.info("카카오톡 공유 기능은 Streamlit에서 직접 지원하지 않습니다. 결과를 복사해서 공유해주세요!")
    
    # 네비게이션 버튼
    col1, col2 = st.columns(2)
    with col1:
        if st.button("다시 분석하기", key="back_to_input_btn"):
            change_page('input')
    with col2:
        if st.button("축의금 내리기", key="confetti_btn"):
            st.balloons()
    
    st.markdown("</div>", unsafe_allow_html=True)

# 푸터
st.markdown("<div style='text-align: center; padding: 1rem 0; color: #475569; font-size: 0.8rem; margin-top: 2rem;'>© 2025 그래서..얼마면 돼? | 100% 재미용이니 진지하게 받아들이지 마세요!</div>", unsafe_allow_html=True)
