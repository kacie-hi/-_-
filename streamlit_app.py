import streamlit as st
import random
import time
import openai
from PIL import Image
from io import BytesIO
import base64
import os

# 페이지 기본 설정
st.set_page_config(
    page_title="초유쾌 축의금 분석기",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 적용
def load_css():
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Noto Sans KR', sans-serif;
        }
        
        .main-title {
            background: linear-gradient(90deg, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .subtitle {
            font-size: 1.2rem;
            color: #6b7280;
            margin-bottom: 2rem;
        }
        
        .card {
            background-color: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.5rem;
        }
        
        .gradient-header {
            background: linear-gradient(90deg, #8b5cf6, #ec4899);
            height: 0.5rem;
            border-radius: 1rem 1rem 0 0;
            margin: -1.5rem -1.5rem 1rem -1.5rem;
        }
        
        .emoji-icon {
            font-size: 2rem;
            margin-right: 0.5rem;
            vertical-align: middle;
        }
        
        .result-amount {
            font-size: 2.5rem;
            font-weight: 900;
            color: #7c3aed;
            text-align: center;
            margin: 1rem 0;
        }
        
        .analysis-point {
            background-color: #f3f4f6;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        
        .summary-box {
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            border-radius: 0 0.75rem 0.75rem 0;
            padding: 1rem;
            margin: 1.5rem 0;
        }
        
        .tip-box {
            background-color: #ede9fe;
            border-radius: 0.75rem;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        .footer-text {
            text-align: center;
            color: #9ca3af;
            font-size: 0.75rem;
            margin-top: 1.5rem;
        }
        
        .btn-primary {
            background: linear-gradient(90deg, #8b5cf6, #ec4899);
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: opacity 0.2s;
        }
        
        .btn-primary:hover {
            opacity: 0.9;
        }
        
        .btn-secondary {
            background-color: white;
            color: #6b7280;
            border: 2px solid #d1d5db;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.2s;
        }
        
        .btn-secondary:hover {
            background-color: #f9fafb;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
    
if 'dialogue' not in st.session_state:
    st.session_state.dialogue = ""
    
if 'result' not in st.session_state:
    st.session_state.result = None

# 예시 대화 설정
EXAMPLE_DIALOGUE = """야 결혼한다면서? 축하해! 잘됐네
응 고마워! 다음달 12일이야 시간되면 와줘
그래? 축하해 시간되면 가볼게~ 어디서 해?
강남에서 해! 청첩장은 다음주에 보낼게
알겠어 기대할게!"""

# 대체 분석 결과 데이터 (API 오류 시 사용)
FALLBACK_RESULTS = [
    {
        "amount": "3만원",
        "points": [
            "대화 중 '그래서 언제였더라?' 물음 횟수가 3회. 관심도 21% 감지됨",
            "이모티콘 대신 'ㅋㅋ'만 사용하는 '귀차니즘 레벨 4' 감지",
            "주로 밤 10시 이후에만 답장하는 '최소한의 예의파' 판정"
        ],
        "summary": "진심 지수: 22%, 체면 지수: 78%, 인생은 줄다리기다. 당겨야 할 때를 알자.",
        "emoji": "😐",
        "funTip": "아껴둔 술 한 잔을 결혼식에서 건네면 인간관계 점수 +10"
    },
    {
        "amount": "5만원",
        "points": [
            "대화 중 '축하해' 사용 횟수 4회. 허나 느낌표(!) 0회. 형식적 축하 패턴",
            "7일 내 답장 평균시간 3시간 27분. '잊을만하면 생각나는 사이'",
            "서로의 개인사 공유율 35%. '적당히 알고 지내는 사이' 등급"
        ],
        "summary": "친밀도: 중하, 경제적 부담 감수 의향: 중. 내 통장에도 구멍이 나겠군요.",
        "emoji": "🙂",
        "funTip": "축의금과 함께 어색한 하이파이브 선물 증정 시 존재감 +15% 상승"
    },
    {
        "amount": "10만원",
        "points": [
            "'우리 언제 한번 만나야 되는데' 멘트 횟수 5회, 실제 만남 0회. '약속의 신' 등급",
            "대화 중 상대방 근황 질문 11회. '은근히 챙겨주는 타입'",
            "대화 시작 시간대가 주로 점심시간. '밥이나 한번 먹자' 클래스"
        ],
        "summary": "정 많은 척 지수: 89%, 실제 정 지수: 62%, 인생은 연기다. 그럴싸하게 포장하자.",
        "emoji": "😊",
        "funTip": "결혼식장에서 '옛날에 우리 참 재밌었는데'라는 멘트 사용 시 호감도 급상승"
    }
]

# 화면 이동 함수
def go_to_step(step):
    st.session_state.step = step
    
def reset_app():
    st.session_state.step = 1
    st.session_state.dialogue = ""
    st.session_state.result = None

# OpenAI를 사용한 대화 분석 함수
def analyze_with_openai(dialogue):
    try:
        # API 키 가져오기 (Streamlit Secrets 또는 환경 변수에서)
        api_key = st.secrets.get("openai_api_key", os.environ.get("OPENAI_API_KEY"))
        
        if not api_key:
            st.warning("OpenAI API 키가 설정되지 않았습니다. 대체 결과를 사용합니다.")
            return get_fallback_result()
        
        client = openai.OpenAI(api_key=api_key)
        
        # 대화 내용 분석 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4" (비용이 더 높지만 더 좋은 결과)
            messages=[
                {"role": "system", "content": """당신은 대화 내용을 분석하여 사람들 간의 친밀도와 적절한 축의금 액수를 추천하는 AI입니다. 
                재미있고 유쾌하게 분석해주세요. 다음 형식으로 정확히 대답해주세요:

                축의금: [금액]원
                
                분석포인트:
                - [재미있는 분석 포인트 1]
                - [재미있는 분석 포인트 2]
                - [재미있는 분석 포인트 3]
                
                요약: [관계 분석 유머러스한 요약]
                
                감정: [이모지 하나만 - 😊, 🙂, 😐 중 하나]
                
                조언: [재미있는 인간관계 팁]
                """},
                {"role": "user", "content": f"다음 대화를 분석해주세요:\n\n{dialogue}"}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # 응답 파싱
        analysis_text = response.choices[0].message.content
        
        # 구조화된 결과 생성
        result = {
            "amount": "분석 결과를 가져올 수 없습니다",
            "points": ["대화 분석 중 오류가 발생했습니다"],
            "summary": "다시 시도해 주세요",
            "emoji": "😕",
            "funTip": "다시 시도해 주세요"
        }
        
        # 응답 파싱
        lines = analysis_text.split('\n')
        points = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("축의금:"):
                result["amount"] = line[4:].strip()
            elif line.startswith("-"):
                points.append(line[1:].strip())
            elif line.startswith("요약:"):
                result["summary"] = line[3:].strip()
            elif line.startswith("감정:"):
                result["emoji"] = line[3:].strip()
            elif line.startswith("조언:"):
                result["funTip"] = line[3:].strip()
        
        if points:
            result["points"] = points
            
        return result
    
    except Exception as e:
        st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
        return get_fallback_result()

# 대체 결과 가져오기 (API 오류 시)
def get_fallback_result():
    result_index = random.randint(0, len(FALLBACK_RESULTS) - 1)
    return FALLBACK_RESULTS[result_index]

# 분석 처리 함수
def analyze_dialogue():
    with st.spinner('대화 내용을 분석하는 중...'):
        # AI 분석 시간 시뮬레이션 (사용자 경험을 위한 지연)
        time.sleep(2)
        
        # OpenAI로 분석 시도
        result = analyze_with_openai(st.session_state.dialogue)
        
        st.session_state.result = result
        st.session_state.step = 3

# UI 구현
def main():
    load_css()
    
    # 상단 그라데이션 바
    st.markdown('<div style="background: linear-gradient(90deg, #8b5cf6, #ec4899); height: 0.5rem; margin: -1rem -5rem 1rem -5rem;"></div>', unsafe_allow_html=True)
    
    # 단계별 UI
    if st.session_state.step == 1:
        show_intro_page()
    elif st.session_state.step == 2:
        show_input_page()
    elif st.session_state.step == 3:
        show_result_page()
    
    # 푸터
    st.markdown('<div class="footer-text">이 서비스는 100% 재미 목적으로 제공됩니다 (진지하게 받아들이지 마세요!)<br>© 2025 초유쾌 축의금 분석기 - 인간관계 지갑 열어젖히기 프로젝트</div>', unsafe_allow_html=True)

# 첫 화면 (소개 페이지)
def show_intro_page():
    st.markdown('<h1 class="main-title">초유쾌 축의금 분석기</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">당신의 카톡을 AI가 분석해서 친밀도와 적정 축의금을 알려드립니다!</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background-color: #ede9fe; border-radius: 0.75rem; padding: 1rem; height: 100%;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">😊</div>
            <h3 style="font-weight: 700; color: #6d28d9; margin-bottom: 0.5rem;">웃음 보장</h3>
            <p style="font-size: 0.9rem; color: #4b5563;">당신의 인간관계를 재미있게 분석해드립니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background-color: #fcE7f3; border-radius: 0.75rem; padding: 1rem; height: 100%;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💬</div>
            <h3 style="font-weight: 700; color: #db2777; margin-bottom: 0.5rem;">대화 분석</h3>
            <p style="font-size: 0.9rem; color: #4b5563;">카톡 내용을 붙여넣으면 AI가 관계 패턴을 파악합니다</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background-color: #e0f2fe; border-radius: 0.75rem; padding: 1rem; height: 100%;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">💸</div>
            <h3 style="font-weight: 700; color: #0369a1; margin-bottom: 0.5rem;">축의금 추천</h3>
            <p style="font-size: 0.9rem; color: #4b5563;">관계 분석 결과를 바탕으로 재치있는 조언까지!</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("시작하기", key="start_btn", type="primary"):
        go_to_step(2)

# 입력 페이지
def show_input_page():
    st.markdown('<h1 style="font-size: 1.8rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">대화 내용 입력</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6b7280; margin-bottom: 1.5rem;">카톡이나 문자 내용을 붙여넣으세요</p>', unsafe_allow_html=True)
    
    # 대화 입력 영역
    st.session_state.dialogue = st.text_area(
        "대화 내용",
        value=st.session_state.dialogue,
        height=200,
        placeholder="예시) 야 결혼한다면서? 축하해! 언제 하는데? / 응 고마워! 다음달 12일이야. 시간 되면 와줘!",
        label_visibility="collapsed"
    )
    
    # 입력 컨트롤
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("예시 넣기", key="example_btn"):
            st.session_state.dialogue = EXAMPLE_DIALOGUE
            st.rerun()
    
    with col2:
        if st.button("지우기", key="clear_btn"):
            st.session_state.dialogue = ""
            st.rerun()
    
    # 이미지 업로드 영역
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div style="background-color: #fce7f3; border-radius: 0.75rem; padding: 1rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 0.75rem;">📷</div>
                <div>
                    <h3 style="font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">이미지로도 분석할 수 있어요!</h3>
                    <p style="font-size: 0.9rem; color: #4b5563; margin-bottom: 0.5rem;">카카오톡 캡처 이미지도 분석 가능합니다</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
            st.markdown('<p style="color: #d1d5db; font-size: 0.8rem; text-align: center; margin-top: 0.5rem;">* 이미지 분석 기능은 개발 중입니다</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p style="color: #d1d5db; font-size: 0.8rem; text-align: center; margin-top: 0.5rem;">* 이미지 분석 기능은 개발 중입니다</p>', unsafe_allow_html=True)
    
    # 버튼 영역
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("이전", key="back_btn"):
            go_to_step(1)
    
    with col2:
        analyze_btn = st.button("분석하기", key="analyze_btn", type="primary", disabled=len(st.session_state.dialogue) < 10)
        
        if analyze_btn and len(st.session_state.dialogue) >= 10:
            analyze_dialogue()

# 결과 페이지
def show_result_page():
    result = st.session_state.result
    
    st.markdown('<h1 style="font-size: 1.8rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">분석 결과</h1>', unsafe_allow_html=True)
    
    # 추천 축의금 금액
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #8b5cf6, #ec4899); border-radius: 0.75rem; padding: 1.5rem; color: white; margin-bottom: 1.5rem; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -2rem; right: -2rem; width: 8rem; height: 8rem; background-color: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        <div style="position: absolute; bottom: -2rem; left: -2rem; width: 6rem; height: 6rem; background-color: rgba(255,255,255,0.1); border-radius: 50%;"></div>
        <div style="display: flex; align-items: center; margin-bottom: 0.75rem;">
            <div style="background-color: rgba(255,255,255,0.2); width: 3rem; height: 3rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem;">
                <span style="font-size: 1.5rem;">💸</span>
            </div>
            <div>
                <h2 style="font-size: 1.2rem; font-weight: 500; opacity: 0.9; margin: 0;">AI 추천 축의금</h2>
                <div style="display: flex; align-items: baseline; margin-top: 0.25rem;">
                    <span style="font-size: 2rem; font-weight: 800; margin-right: 0.5rem;">{result['amount']}</span>
                    <div style="background-color: rgba(255,255,255,0.3); border-radius: 9999px; padding: 0.25rem 0.5rem; font-size: 0.75rem;">
                        재미로 봐주세요!
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI 분석 결과
    emoji = result.get('emoji', '😊')
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center;">
                <span style="color: #eab308; margin-right: 0.5rem;">⚡</span>
                <h2 style="font-weight: 700; color: #1f2937; margin: 0;">AI 분석 결과</h2>
            </div>
            <div style="display: flex; align-items: center;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">{emoji}</span>
                <span style="background-color: #ede9fe; color: #6d28d9; font-size: 0.75rem; padding: 0.125rem 0.5rem; border-radius: 9999px;">친밀도 지수</span>
            </div>
        </div>
        
        <div style="margin-bottom: 1.25rem;">
    """, unsafe_allow_html=True)
    
    # 분석 포인트들
    for i, point in enumerate(result['points']):
        st.markdown(f"""
        <div style="background-color: #f3f4f6; border-radius: 0.75rem; padding: 0.75rem; margin-bottom: 0.75rem; display: flex; align-items: flex-start;">
            <div style="background: linear-gradient(135deg, #8b5cf6, #ec4899); color: white; width: 1.5rem; height: 1.5rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-right: 0.75rem; margin-top: 0.125rem; font-size: 0.75rem; font-weight: 600;">
                {i+1}
            </div>
            <p style="margin: 0; color: #4b5563;">{point}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 요약 및 팁
    st.markdown(f"""
        </div>
        
        <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 0 0.75rem 0.75rem 0; padding: 1rem; margin-bottom: 1.5rem;">
            <p style="margin: 0; color: #1f2937; font-weight: 500;">{result['summary']}</p>
        </div>
        
        <div style="background-color: #fcE7f3; border-radius: 0.75rem; padding: 1rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: #db2777; margin-right: 0.5rem;">⭐</span>
                <h3 style="font-weight: 500; color: #1f2937; margin: 0;">AI의 유쾌한 조언</h3>
            </div>
            <p style="margin: 0; color: #be185d; font-style: italic;">"{result['funTip']}"</p>
        </div>
        
        <div style="background-color: #ede9fe; border-radius: 0.75rem; padding: 1rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="color: #7c3aed; margin-right: 0.5rem;">🏆</span>
                <h3 style="font-weight: 500; color: #1f2937; margin: 0;">인간관계 개선 팁</h3>
            </div>
            <p style="margin: 0; color: #6d28d9;">이 상대방에게 축의금만 주고 끝내지 마세요! 결혼식에서 "내가 축의금 진짜 많이 줬어"라고 귓속말을 한다면 친밀도가 급상승합니다.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 하단 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("다시 분석하기", key="reset_btn"):
            reset_app()
    
    with col2:
        if st.button("결과 공유하기", key="share_btn", type="primary"):
            st.success("친구들에게 공유되었습니다! (가상)")

    # 추천 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        if st.button("이 서비스 추천하기", key="recommend_btn"):
            st.balloons()
            st.success("♥ 우리 서비스가 마음에 드셨다면 친구들에게 공유해주세요!")

if __name__ == "__main__":
    main()
