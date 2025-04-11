import streamlit as st
import openai
import pytesseract
from PIL import Image

st.set_page_config(page_title='그래서… 얼마면 돼?', layout='centered')
st.title("그래서… 얼마면 돼?")
st.write("AI가 너랑 상대의 대화를 분석해서 적절한 축의금을 알려줄게! 텍스트 입력 or 카톡 이미지 올려도 돼 🤖")

api_key = st.text_input("🔐 OpenAI API 키를 입력해주세요", type="password")

option = st.radio("입력 방식 선택", ["텍스트 직접 입력", "카톡 대화 이미지 업로드"])
tone = st.radio("🎭 분석 결과 스타일 선택", ["웃긴 톤", "감동 톤", "진지한 톤"])

dialogue = ""

if option == "텍스트 직접 입력":
    dialogue = st.text_area("📥 대화 내용을 입력해주세요", height=200,
                            placeholder="예: 나: 야 결혼해? / 친구: ㅋㅋ 갑자기 하게 됐어 / 나: 대박 축하해~")
else:
    uploaded_file = st.file_uploader("🖼️ 카톡 대화 캡처 이미지를 업로드해주세요", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='업로드한 이미지', use_column_width=True)
        dialogue = pytesseract.image_to_string(image, lang='kor')
        st.text_area("📝 추출된 텍스트", value=dialogue, height=150)

tone_prompts = {
    "웃긴 톤": "너는 인간관계를 분석해서 적절한 축의금을 추천해주는 AI야. 결과를 유쾌하고 웃기게 말해줘. 빈봉투, 가족 데려가기 같은 기발한 옵션도 제안해.",
    "감동 톤": "너는 인간관계를 분석해서 적절한 축의금을 추천해주는 AI야. 따뜻하고 감동적인 톤으로 조언해줘. 축복의 메시지도 넣어줘.",
    "진지한 톤": "너는 인간관계를 분석해서 적절한 축의금을 추천해주는 AI야. 진지하고 공손하게 사회적 예의에 따라 금액을 안내해줘."
}

if st.button("분석하기", disabled=not (dialogue.strip() and api_key.strip())):
    openai.api_key = api_key
    with st.spinner("AI가 사회생활을 계산 중입니다... 🤖💭"):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": tone_prompts[tone]},
                    {"role": "user", "content": f"다음 대화를 분석해서 축의금 금액을 추천해줘:\\n{dialogue}"}
                ]
            )
            analysis = response.choices[0].message.content
            st.subheader("💸 AI 축의금 분석 결과")
            st.markdown(analysis)
        except Exception as e:
            st.error(f"에러 발생: {e}")

st.markdown(\"\"\"---  
예시 톤:
- 웃긴 톤: 빈봉투 + 혼밥 추천  
- 감동 톤: "행복한 인생의 출발을 응원합니다."  
- 진지한 톤: "사회 통념상 최소 5만원 이상을 권장합니다."  
\"\"\")
