import streamlit as st
import random
import time
import openai
from PIL import Image

# 페이지 기본 설정
st.set_page_config(
    page_title="초유쾌 축의금 분석기",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

# 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1
    
if 'dialogue' not in st.session_state:
    st.session_state.dialogue = ""
    
if 'result' not in st.session_state:
    st.session_state.result = None
    
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

# 화면 이동 함수
def go_to_step(step):
    st.session_state.step = step
    
def reset_app():
    st.session_state.step = 1
    st.session_state.dialogue = ""
    st.session_state.result = None

# OpenAI를 사용한 대화 분석 함수
def analyze_with_openai(dialogue, api_key):
    try:
        if not api_key:
            st.warning("OpenAI API 키가 입력되지 않았습니다. 대체 결과를 사용합니다.")
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
        result = analyze_with_openai(st.session_state.dialogue, st.session_state.api_key)
        
        st.session_state.result = result
        st.session_state.step = 3

# 메인 함수 
def main():
    # API 키 입력 영역 (사이드바)
    with st.sidebar:
        st.header("OpenAI API 설정")
        st.session_state.api_key = st.text_input("API 키를 입력하세요", value=st.session_state.api_key, type="password", help="OpenAI API 키를 입력하세요. 입력한 키는 저장되지 않습니다.")
        st.caption("API 키는 안전하게 처리되며 저장되지 않습니다.")
        
        # API 키 테스트 버튼
        if st.button("API 키 테스트"):
            if st.session_state.api_key:
                try:
                    client = openai.OpenAI(api_key=st.session_state.api_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": "안녕하세요"}],
                        max_tokens=5
                    )
                    st.success("API 키가 유효합니다!")
                except Exception as e:
                    st.error(f"API 키 테스트 실패: {e}")
            else:
                st.warning("API 키를 입력해주세요.")

    # 각 단계별 UI 표시
    if st.session_state.step == 1:
        show_intro_page()
    elif st.session_state.step == 2:
        show_input_page()
    elif st.session_state.step == 3:
        show_result_page()

# 첫 화면 (소개 페이지)
def show_intro_page():
    st.title("초유쾌 축의금 분석기")
    st.subheader("당신의 카톡을 분석해서 친밀도와 적정 축의금을 알려드립니다!")
    
    # API 키 경고
    if not st.session_state.api_key:
        st.warning("OpenAI API 키가 설정되지 않았습니다. 사이드바에서 API 키를 입력하거나, API 키 없이 대체 결과를 볼 수 있습니다.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 😊 웃음 보장")
        st.write("당신의 인간관계를 재미있게 분석해드립니다")
    
    with col2:
        st.markdown("### 💬 대화 분석")
        st.write("카톡 내용을 붙여넣으면 관계 패턴을 파악합니다")
    
    with col3:
        st.markdown("### 💸 축의금 추천")
        st.write("관계 분석 결과를 바탕으로 재치있는 조언까지!")
    
    if st.button("시작하기", type="primary"):
        go_to_step(2)

# 입력 페이지
def show_input_page():
    st.title("대화 내용 입력")
    st.write("카톡이나 문자 내용을 붙여넣으세요")
    
    # API 키 경고
    if not st.session_state.api_key:
        st.warning("OpenAI API 키가 설정되지 않았습니다. 사이드바에서 API 키를 입력하거나, API 키 없이 대체 결과를 볼 수 있습니다.")
    
    # 대화 입력 영역
    st.session_state.dialogue = st.text_area(
        "대화 내용",
        value=st.session_state.dialogue,
        height=200,
        placeholder="예시) 야 결혼한다면서? 축하해! 언제 하는데? / 응 고마워! 다음달 12일이야. 시간 되면 와줘!"
    )
    
    # 입력 컨트롤
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("예시 넣기"):
            st.session_state.dialogue = EXAMPLE_DIALOGUE
            st.rerun()
    
    with col2:
        if st.button("지우기"):
            st.session_state.dialogue = ""
            st.rerun()
    
    # 이미지 업로드 영역
    st.subheader("이미지로도 분석할 수 있어요!")
    st.write("카카오톡 캡처 이미지도 분석 가능합니다")
    
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_column_width=True)
        st.caption("* 이미지 분석 기능은 개발 중입니다")
    
    # 버튼 영역
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("이전"):
            go_to_step(1)
    
    with col2:
        analyze_btn = st.button("분석하기", type="primary", disabled=len(st.session_state.dialogue) < 10)
        
        if analyze_btn and len(st.session_state.dialogue) >= 10:
            analyze_dialogue()

# 결과 페이지
def show_result_page():
    result = st.session_state.result
    
    st.title("분석 결과")
    
    # 추천 축의금 금액
    st.subheader("AI 추천 축의금")
    st.markdown(f"## {result['amount']}")
    st.caption("재미로 봐주세요!")
    
    # API 키가 없는 경우 알림
    if not st.session_state.api_key:
        st.info("OpenAI API 키가 설정되지 않아 예시 분석 결과를 표시합니다. 실제 AI 분석을 위해 사이드바에서 API 키를 설정해주세요.")
    
    # AI 분석 결과
    st.subheader("AI 분석 결과")
    
    # 분석 포인트들
    for i, point in enumerate(result['points']):
        st.markdown(f"**{i+1}.** {point}")
    
    # 요약 및 팁
    st.info(result['summary'])
    
    st.markdown("### AI의 유쾌한 조언")
    st.success(f'"{result["funTip"]}"')
    
    # 하단 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("다시 분석하기"):
            reset_app()
    
    with col2:
        if st.button("결과 공유하기", type="primary"):
            st.success("친구들에게 공유되었습니다! (가상)")

    if st.button("이 서비스 추천하기"):
        st.balloons()
        st.success("♥ 우리 서비스가 마음에 드셨다면 친구들에게 공유해주세요!")

# 앱 실행
if __name__ == "__main__":
    main()
