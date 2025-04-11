import streamlit as st
from openai import OpenAI
import pytesseract
from PIL import Image

st.set_page_config(page_title="그래서... 얼마면 돼?", page_icon="💸", layout="centered")

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

# STEP 1: API 키 입력
if st.session_state.step == 1:
    st.title("그래서... 얼마면 돼? 💸")
    st.caption("GPT가 당신과 상대방의 대화를 분석해 웃긴 축의금을 정해드립니다.")
    st.session_state.api_key = st.text_input("🔐 OpenAI API 키 입력", type="password")
    if st.button("축의금 결정하기", disabled=not st.session_state.api_key.strip()):
        st.session_state.step = 2

# STEP 2: 이름 + 대화 입력
elif st.session_state.step == 2:
    st.header("👤 상대방 정보를 입력해주세요")
    st.session_state.name = st.text_input("상대방 이름", placeholder="예: 지현")

    input_method = st.radio("대화 입력 방식", ["텍스트 직접 입력", "카톡 이미지 업로드"])

    if input_method == "텍스트 직접 입력":
        st.session_state.dialogue = st.text_area("💬 대화 내용", height=200,
            placeholder="예: 나: 야 결혼해? / 친구: ㅋㅋ 갑자기 하게 됐어 / 나: 대박 축하해~")
    else:
        uploaded = st.file_uploader("🖼️ 이미지 업로드", type=["png", "jpg", "jpeg"])
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="업로드한 대화 이미지", use_column_width=True)
            st.session_state.dialogue = pytesseract.image_to_string(image, lang="kor")
            st.text_area("📜 추출된 텍스트", value=st.session_state.dialogue, height=180)

    if st.button("🎯 분석 시작", disabled=not (st.session_state.name and st.session_state.dialogue and st.session_state.api_key)):
        try:
            client = OpenAI(api_key=st.session_state.api_key)
            with st.spinner("AI가 사회적 거리와 진심을 분석 중입니다... 🤖"):
                prompt = f"""
너는 사람들 사이의 관계를 분석해서 웃기고 현실적인 축의금 금액을 추천해주는 AI야.
분석 대상: {st.session_state.name}
대화 내용: {st.session_state.dialogue}

다음과 같이 분석해줘:
- 감정, 거리감, 사회적 체면
- 추천 축의금 (또는 빈봉투/가족 3인 밥 먹기 등 웃긴 옵션도 허용)
- 공감 가는 멘트, 사회생활 TMI까지!
"""

                res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "너는 인간관계를 축의금으로 풀어내는 유쾌한 AI야. 분석은 웃기고 설득력 있어야 해."},
                        {"role": "user", "content": prompt}
                    ]
                )
                st.session_state.result = res.choices[0].message.content
                st.session_state.step = 3
        except Exception as e:
            st.error(f"에러 발생: {e}")

# STEP 3: 결과 출력
elif st.session_state.step == 3:
    st.subheader("🎉 AI 축의금 분석 결과")
    st.success(st.session_state.result)
    if st.button("🔁 다시 하기"):
        st.session_state.step = 1
        st.session_state.api_key = ''
        st.session_state.name = ''
        st.session_state.dialogue = ''
        st.session_state.result = None
