import streamlit as st
import openai
import pytesseract
from PIL import Image

st.set_page_config(page_title='그래서… 얼마면 돼?', page_icon='💸', layout='centered')

# 상태 저장
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'dialogue' not in st.session_state:
    st.session_state.dialogue = ''
if 'result' not in st.session_state:
    st.session_state.result = None

# 스타일
st.markdown("""<style>
    .big-title { font-size: 36px; font-weight: 700; text-align: center; margin-bottom: 1rem; }
    .center { text-align: center; }
</style>""", unsafe_allow_html=True)

# Step 1: API 키 입력
if st.session_state.step == 1:
    st.markdown('<div class="big-title">그래서... 얼마면 돼?</div>', unsafe_allow_html=True)
    st.write("GPT가 너와 상대의 대화를 분석해서 웃기고 사회적인 축의금 금액을 추천해줍니다 💌")
    st.session_state.api_key = st.text_input("🔐 OpenAI API 키를 입력해주세요", type="password")
    if st.button("축의금 결정하기", disabled=not st.session_state.api_key.strip()):
        st.session_state.step = 2

# Step 2: 상대 정보 & 대화
elif st.session_state.step == 2:
    st.markdown('<div class="big-title">상대방 정보를 입력해주세요</div>', unsafe_allow_html=True)
    st.session_state.name = st.text_input("👤 상대방 이름", placeholder="예: 지현")
    input_method = st.radio("대화 입력 방식", ["텍스트 직접 입력", "카톡 이미지 업로드"])
    
    if input_method == "텍스트 직접 입력":
        st.session_state.dialogue = st.text_area("💬 대화 내용", height=180,
            placeholder="예: 나: 야 결혼해? / 친구: ㅋㅋ 갑자기 하게 됐어 / 나: 대박 축하해~")
    else:
        uploaded = st.file_uploader("🖼️ 대화 이미지 업로드", type=["png", "jpg", "jpeg"])
        if uploaded:
            img = Image.open(uploaded)
            st.image(img, caption="업로드한 대화 이미지", use_column_width=True)
            st.session_state.dialogue = pytesseract.image_to_string(img, lang='kor')
            st.text_area("📜 추출된 텍스트", value=st.session_state.dialogue, height=150)

    if st.button("🎯 분석 시작", disabled=not (st.session_state.api_key.strip() and st.session_state.dialogue.strip() and st.session_state.name.strip())):
        openai.api_key = st.session_state.api_key
        with st.spinner("AI가 사회적 거리와 감정을 분석 중입니다... 🤖💭"):
            prompt = f"""
너는 인간관계를 분석해 축의금을 추천해주는 유쾌한 AI야.
상대 이름은 '{st.session_state.name}'이고, 아래 대화 내용을 보고
- 감정 / 친밀도 분석
- 추천 축의금 금액 또는 빈봉투 옵션
- 빵 터지는 웃긴 코멘트
- 사회생활 TMI까지 넣어줘

대화:
{st.session_state.dialogue}
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "너는 웃기고 현실적인 축의금 분석기야. 결과는 아주 재밌게!"},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.session_state.result = response.choices[0].message.content
                st.session_state.step = 3
            except Exception as e:
                st.error(f"에러 발생: {e}")

# Step 3: 결과 화면
elif st.session_state.step == 3:
    st.markdown('<div class="big-title">💸 AI 축의금 분석 결과</div>', unsafe_allow_html=True)
    st.success(st.session_state.result)
    if st.button("🔄 다시 하기"):
        st.session_state.step = 1
        st.session_state.dialogue = ''
        st.session_state.name = ''
        st.session_state.result = None
