import streamlit as st
from openai import OpenAI
import pytz
from PIL import Image
import random
import re
import json
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="그래서..얼마면 돼? - 축의금 결정기",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS 스타일 적용
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    
    :root {
        --navy-950: #0a192f;
        --navy-900: #112240;
        --navy-800: #1a2e52;
        --navy-700: #223b69;
        --navy-600: #2a4780;
        --cyan-400: #22d3ee;
        --purple-500: #a855f7;
        --yellow-400: #facc15;
    }
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .main {
        background-color: var(--navy-950);
    }
    
    .stApp {
        background-color: var(--navy-950);
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #22d3ee, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }
    
    .navy-card {
        background-color: var(--navy-900);
        border: 1px solid var(--navy-800);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    .event-button {
        background-color: var(--navy-800);
        border: 1px solid var(--navy-700);
        border-radius: 12px;
        padding: 15px;
        transition: all 0.3s;
        text-align: center;
        height: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .event-button:hover {
        background-color: var(--navy-700);
    }
    
    .event-button.selected {
        background: linear-gradient(135deg, #9333ea, #7e22ce);
        border: 2px solid #a855f7;
    }
    
    .relationship-button {
        background-color: var(--navy-800);
        border: 1px solid var(--navy-700);
        border-radius: 8px;
        padding: 10px 15px;
        transition: all 0.3s;
        text-align: center;
        margin: 5px;
    }
    
    .relationship-button:hover {
        background-color: var(--navy-700);
    }
    
    .relationship-button.selected {
        background: linear-gradient(135deg, #0891b2, #0e7490);
        border: 2px solid #22d3ee;
    }
    
    .gradient-button {
        background: linear-gradient(90deg, #22d3ee, #a855f7);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .gradient-button:hover {
        opacity: 0.9;
    }
    
    .progress-container {
        background-color: var(--navy-700);
        border-radius: 10px;
        height: 10px;
        margin-bottom: 20px;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #22d3ee, #a855f7);
        border-radius: 10px;
        height: 10px;
        transition: width 0.5s ease-out;
    }
    
    .result-amount {
        font-size: 48px;
        font-weight: bold;
        color: var(--yellow-400);
        text-align: center;
        margin: 20px 0;
    }
    
    .gauge-container {
        background-color: var(--navy-800);
        border-radius: 10px;
        height: 12px;
        margin: 10px 0;
    }
    
    .gauge-bar {
        border-radius: 10px;
        height: 12px;
    }
    
    .funny-comment {
        background-color: var(--navy-800);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .special-note {
        background-color: var(--navy-800);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .footer {
        text-align: center;
        font-size: 12px;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 50px;
    }
    
    /* 화면 전환 애니메이션 */
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* 로딩 애니메이션 */
    .loading-spinner {
        width: 80px;
        height: 80px;
        margin: 0 auto;
        border-radius: 50%;
        border: 6px solid #22d3ee;
        border-top-color: #a855f7;
        animation: spin 1.5s linear infinite;
    }
    
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* 금액 버튼 */
    .amount-button {
        background-color: var(--navy-800);
        border: 1px solid var(--navy-700);
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px;
        transition: all 0.3s;
        font-weight: bold;
    }
    
    .amount-button:hover {
        background-color: var(--navy-700);
    }
    
    /* 자동 높이 조절 텍스트 영역 */
    textarea {
        background-color: var(--navy-800) !important;
        border: 1px solid var(--navy-700) !important;
        border-radius: 8px !important;
        color: white !important;
        min-height: 150px;
    }
    
    /* 버튼 스타일 재정의 */
    .stButton > button {
        background-color: var(--navy-800);
        color: white;
        border: 1px solid var(--navy-700);
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: var(--navy-700);
    }
</style>
""", unsafe_allow_html=True)

# 초기 세션 상태 설정
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'event_type' not in st.session_state:
    st.session_state.event_type = None
if 'relationship' not in st.session_state:
    st.session_state.relationship = None
if 'attendees' not in st.session_state:
    st.session_state.attendees = 1
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = ""
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

# 헤더 표시
st.markdown('<div class="navy-card fade-in">', unsafe_allow_html=True)
st.markdown('<h1><span class="gradient-text">그래서..얼마면 돼?</span> <small style="font-size: 16px; color: rgba(255, 255, 255, 0.6);">축의금 결정기</small></h1>', unsafe_allow_html=True)
st.markdown('<p style="color: rgba(255, 255, 255, 0.7);">대화 내용을 AI가 분석하여 센스있는 축의금 액수를 추천해드립니다.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 프로그레스 바 (현재 단계 표시)
progress_value = ((st.session_state.step - 1) / 3) * 100
st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {progress_value}%;"></div></div>', unsafe_allow_html=True)

# 스텝 1: 이벤트 유형 선택
if st.session_state.step == 1:
    st.markdown('<div class="navy-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 class="gradient-text">어떤 자리에 가시나요?</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 20px;">축의금을 낼 행사 유형을 선택해주세요</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        wedding_selected = "selected" if st.session_state.event_type == "wedding" else ""
        st.markdown(f'<div class="event-button {wedding_selected}" id="wedding-button"><div style="font-size: 32px;">💍</div><div>결혼식</div></div>', unsafe_allow_html=True)
        if st.button("결혼식 선택", key="wedding_btn"):
            st.session_state.event_type = "wedding"
            st.experimental_rerun()
    
    with col2:
        funeral_selected = "selected" if st.session_state.event_type == "funeral" else ""
        st.markdown(f'<div class="event-button {funeral_selected}" id="funeral-button"><div style="font-size: 32px;">🕯️</div><div>장례식</div></div>', unsafe_allow_html=True)
        if st.button("장례식 선택", key="funeral_btn"):
            st.session_state.event_type = "funeral"
            st.experimental_rerun()
    
    with col3:
        party_selected = "selected" if st.session_state.event_type == "party" else ""
        st.markdown(f'<div class="event-button {party_selected}" id="party-button"><div style="font-size: 32px;">🎂</div><div>생일/파티</div></div>', unsafe_allow_html=True)
        if st.button("생일/파티 선택", key="party_btn"):
            st.session_state.event_type = "party"
            st.experimental_rerun()
    
    st.markdown('<div style="margin-top: 30px; text-align: right;">', unsafe_allow_html=True)
    if st.session_state.event_type is not None:
        if st.button("다음 단계 →", key="next_to_step2"):
            st.session_state.step = 2
            st.experimental_rerun()
    else:
        st.markdown('<p style="color: rgba(255, 255, 255, 0.5); font-size: 14px; text-align: center;">행사 유형을 선택해주세요!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 스텝 2: 관계 및 참석자 수 선택
elif st.session_state.step == 2:
    st.markdown('<div class="navy-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 class="gradient-text">상대방과 어떤 관계인가요?</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 20px;">관계 유형을 선택해주세요</p>', unsafe_allow_html=True)
    
    # 관계 유형 버튼
    relationships = {
        "friend": "친구/지인", 
        "colleague": "직장동료", 
        "family": "가족/친척", 
        "boss": "상사/선배"
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        for key, value in list(relationships.items())[:2]:
            selected = "selected" if st.session_state.relationship == key else ""
            st.markdown(f'<div class="relationship-button {selected}">{value}</div>', unsafe_allow_html=True)
            if st.button(f"{value} 선택", key=f"{key}_btn"):
                st.session_state.relationship = key
                st.experimental_rerun()
    
    with col2:
        for key, value in list(relationships.items())[2:]:
            selected = "selected" if st.session_state.relationship == key else ""
            st.markdown(f'<div class="relationship-button {selected}">{value}</div>', unsafe_allow_html=True)
            if st.button(f"{value} 선택", key=f"{key}_btn"):
                st.session_state.relationship = key
                st.experimental_rerun()
    
    # 참석자 수 선택
    st.markdown('<h3 style="margin-top: 30px; margin-bottom: 15px; color: rgba(255, 255, 255, 0.9);">함께 참석하는 인원</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("➖", key="decrease_attendees"):
            if st.session_state.attendees > 1:
                st.session_state.attendees -= 1
                st.experimental_rerun()
    
    with col2:
        st.markdown(f'<div style="background-color: var(--navy-800); border-radius: 8px; padding: 10px; text-align: center;"><span style="font-size: 20px; font-weight: bold;">{st.session_state.attendees}명</span> <span style="color: rgba(255, 255, 255, 0.6); font-size: 14px;">{" (본인만)" if st.session_state.attendees == 1 else f" (본인 포함 {st.session_state.attendees}명)"}</span></div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("➕", key="increase_attendees"):
            st.session_state.attendees += 1
            st.experimental_rerun()
    
    # 이전/다음 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← 이전", key="back_to_step1"):
            st.session_state.step = 1
            st.experimental_rerun()
    
    with col2:
        if st.session_state.relationship is not None:
            if st.button("다음 단계 →", key="next_to_step3"):
                st.session_state.step = 3
                st.experimental_rerun()
        else:
            st.markdown('<p style="color: rgba(255, 255, 255, 0.5); font-size: 14px; text-align: center;">관계 유형을 선택해주세요!</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 스텝 3: 대화 입력 및 분석
elif st.session_state.step == 3:
    st.markdown('<div class="navy-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 class="gradient-text">대화 내용을 분석해 드릴게요</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 20px;">최근 나눈 대화를 붙여넣어 주세요. (카톡, 문자, 이메일 등)</p>', unsafe_allow_html=True)
    
    # API 키 입력 (처음 사용하는 경우)
    if not st.session_state.api_key:
        api_key = st.text_input("OpenAI API 키를 입력해주세요 (분석에 필요합니다)", type="password")
        if api_key:
            st.session_state.api_key = api_key
    
    # 대화 입력
    conversation = st.text_area("대화 내용", value=st.session_state.conversation, 
                              placeholder="예:\n상대방: 다음 주에 결혼식인데 와줄 수 있어?\n나: 물론이지! 축하해 정말 기쁘다~\n상대방: 고마워 ^^ 너무 부담 갖지 말고 편하게 와~",
                              height=200)
    
    # 도움말 박스
    st.markdown('<div class="special-note">', unsafe_allow_html=True)
    st.markdown('💡 **팁**: 대화가 많을수록 더 정확한 분석이 가능해요. 실제 대화를 복사해서 붙여넣어 주세요!', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 이전/분석 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← 이전", key="back_to_step2"):
            st.session_state.conversation = conversation
            st.session_state.step = 2
            st.experimental_rerun()
    
    with col2:
        if st.button("분석하기", key="analyze", disabled=(not conversation.strip() or not st.session_state.api_key)):
            st.session_state.conversation = conversation
            
            # 로딩 화면 표시
            with st.spinner("AI가 대화를 분석 중입니다..."):
                # AI 분석 로직 (OpenAI API 호출)
                try:
                    client = OpenAI(api_key=st.session_state.api_key)
                    analysis_result = analyze_conversation(client, conversation, st.session_state.relationship, 
                                                         st.session_state.event_type, st.session_state.attendees)
                    st.session_state.analysis_result = analysis_result
                    st.session_state.step = 4
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"분석 중 오류가 발생했습니다: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 스텝 4: 결과 표시
elif st.session_state.step == 4 and st.session_state.analysis_result:
    result = st.session_state.analysis_result
    
    st.markdown('<div class="navy-card fade-in">', unsafe_allow_html=True)
    st.markdown('<h2 class="gradient-text">분석 완료!</h2>', unsafe_allow_html=True)
    
    # 추천 축의금 액수
    st.markdown('<div style="background-color: var(--navy-800); border-radius: 12px; padding: 20px; text-align: center; margin: 20px 0;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: white; margin-bottom: 10px;">추천 축의금은...</h3>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-amount">{result["amount"]:,}원</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.6); font-size: 14px;">*AI의 추천일 뿐, 최종 결정은 본인의 판단에 따라주세요!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 친밀도 게이지
    st.markdown('<h3 style="margin: 20px 0 10px 0;">친밀도</h3>', unsafe_allow_html=True)
    st.markdown(f'<div style="display: flex; justify-content: space-between;"><span style="color: rgba(255, 255, 255, 0.7);">친밀도</span><span style="color: var(--cyan-400);">{result["closeness"]}%</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="gauge-container"><div class="gauge-bar" style="width: {result["closeness"]}%; background: linear-gradient(90deg, #22d3ee, #06b6d4);"></div></div>', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255, 255, 255, 0.5);"><span>남남</span><span>찐친</span></div>', unsafe_allow_html=True)
    
    # 유머 지수 게이지
    st.markdown('<h3 style="margin: 20px 0 10px 0;">유머 지수</h3>', unsafe_allow_html=True)
    st.markdown(f'<div style="display: flex; justify-content: space-between;"><span style="color: rgba(255, 255, 255, 0.7);">유머 지수</span><span style="color: var(--yellow-400);">{result["humor"]}%</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="gauge-container"><div class="gauge-bar" style="width: {result["humor"]}%; background: linear-gradient(90deg, #facc15, #eab308);"></div></div>', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; justify-content: space-between; font-size: 12px; color: rgba(255, 255, 255, 0.5);"><span>사무적</span><span>개그맨</span></div>', unsafe_allow_html=True)
    
    # AI의 한마디
    st.markdown('<h3 style="margin: 25px 0 15px 0;">AI의 한마디</h3>', unsafe_allow_html=True)
    for comment in result["funny_comments"]:
        st.markdown(f'<div class="funny-comment"><span style="color: var(--yellow-400); margin-right: 8px;">👉</span> {comment}</div>', unsafe_allow_html=True)
    
    # 특별 노트
    if result["special_notes"]:
        st.markdown('<h3 style="margin: 25px 0 15px 0;">축의금 꿀팁</h3>', unsafe_allow_html=True)
        for note in result["special_notes"]:
            st.markdown(f'<div class="special-note"><span style="font-weight: bold; color: var(--cyan-400);">{note["title"]}</span><p style="margin-top: 5px;">{note["content"]}</p></div>', unsafe_allow_html=True)
    
    # 다시하기 및 공유 버튼
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 다시 분석하기", key="restart"):
            st.session_state.step = 1
            st.session_state.event_type = None
            st.session_state.relationship = None
            st.session_state.attendees = 1
            st.session_state.conversation = ""
            st.session_state.analysis_result = None
            st.experimental_rerun()
    
    with col2:
        # 공유 버튼 - 실제 구현에서는 URL 생성 또는 결과 저장 로직 추가
        if st.button("📤 결과 공유하기", key="share"):
            st.info("공유 기능은 현재 개발 중입니다. 곧 이용하실 수 있습니다!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# 푸터
st.markdown('<div class="footer">© 2025 그래서..얼마면 돼? | 축의금 결정기</div>', unsafe_allow_html=True)

# AI 대화 분석 함수
def analyze_conversation(client, conversation, relationship, event_type, attendees):
    # 관계 유형 한글 변환
    relationship_map = {
        "friend": "친구/지인", 
        "colleague": "직장동료", 
        "family": "가족/친척", 
        "boss": "상사/선배"
    }
    
    # 이벤트 유형 한글 변환
    event_map = {
        "wedding": "결혼식",
        "funeral": "장례식",
        "party": "생일/파티"
    }
    
    # OpenAI API 요청 메시지 구성
    messages = [
        {"role": "system", "content": """당신은 대화 내용을 분석하여 축의금을 추천하는 AI입니다. 
         사용자가 제공한 대화 내용, 관계 유형, 이벤트 유형, 참석자 수를 바탕으로 재미있고 센스있는 분석을 제공해야 합니다.
         분석 결과는 다음 요소를 포함해야 합니다:
         1. 친밀도 점수 (0-100%)
         2. 유머 지수 점수 (0-100%)
         3. 추천 축의금 액수 (원 단위)
         4. 재미있는 코멘트 3-4개
         5. 특별 팁이나 노트 2-3개
         응답은 반드시 JSON 형식으로 제공하세요."""},
        {"role": "user", "content": f"""다음 정보를 바탕으로 축의금을 분석해주세요:
         
         이벤트 유형: {event_map.get(event_type, event_type)}
         관계 유형: {relationship_map.get(relationship, relationship)}
         참석자 수: {attendees}명
         
         대화 내용:
         {conversation}
         
         분석 결과를 JSON 형식으로 제공해주세요. 특히 축의금 금액은 정확한 숫자로, 친밀도와 유머 지수는 백분율로, 코멘트는 재미있고 유머러스하게 작성해주세요.
         관계와 대화 내용에 따라 현실적인 축의금 액수를 추천해주세요.
         특히, 재미있는 코멘트와 특별 노트는 정말 유머스럽고 센스있게 작성해주세요."""}
    ]
    
    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # 또는 사용 가능한 최신 모델
        messages=messages,
        temperature=0.8,
        max_tokens=1000
    )
    
    # API 응답 파싱
    result_text = response.choices[0].message.content
    
    # JSON 응답 추출
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', result_text)
    if json_match:
        result_json = json_match.group(1)
    else:
        result_json = result_text
    
    try:
        result = json.loads(result_json)
    except json.JSONDecodeError:
        # JSON 파싱 실패 시 기본값 제공
        result = {
            "closeness": random.randint(50, 90),
            "humor": random.randint(40, 95),
            "amount": get_default_amount(relationship, event_type, attendees),
            "funny_comments": [
                "대화 분석에 실패했지만, 이 정도면 '나 결혼했어' 문자에 '누구랑?' 대답하는 사이는 아닌 것 같네요!",
                "문자 톤이 왜인지 슬로우 모션으로 들리는 사이... 축의금은 빠르게 건네주세요!",
                f"분석이 어려울 정도로 복잡한 관계네요! {get_default_amount(relationship, event_type, attendees):,}원으로 무난하게 갑시다."
            ],
            "special_notes": [
                {
                    "title": "축의금 대신 할 수 있는 것",
                    "content": "현금이 부담스럽다면 재능기부도 좋아요! 사진사, DJ, 축가... 뭐든 가능!"
                },
                {
                    "title": "전달 꿀팁",
                    "content": "봉투에 이름 쓸 때 오타 조심! 축의금보다 더 기억에 남습니다."
                }
            ]
        }
    
    return result

# 기본 축의금 추천 함수
def get_default_amount(relationship, event_type, attendees):
    # 기본 금액 설정
    base_amount = 50000
    
    # 관계 유형에 따른 조정
    if relationship == "friend":
        base_amount = 50000
    elif relationship == "colleague":
        base_amount = 70000
    elif relationship == "family":
        base_amount = 100000
    elif relationship == "boss":
        base_amount = 100000
    
    # 이벤트 유형에 따른 조정
    if event_type == "funeral":
        base_amount = int(base_amount * 1.1)
    elif event_type == "party":
        base_amount = int(base_amount * 0.7)
    
    # 참석자 수에 따른 조정
    if attendees > 1:
        base_amount = int(base_amount * (1 + (attendees - 1) * 0.5))
    
    # 만원 단위로 반올림
    return round(base_amount / 10000) * 10000

# 현재 한국 시간 가져오기
def get_korea_time():
    korea_tz = pytz.timezone('Asia/Seoul')
    korea_time = datetime.now(korea_tz)
    return korea_time.strftime("%Y-%m-%d %H:%M:%S")

# 재미 요소: 5% 확률로 특이한 금액 추천 (실제 분석에서도 사용될 수 있음)
def add_funny_amount(amount):
    if random.random() < 0.05:  # 5% 확률
        funny_amounts = [31415, 42000, 69000, 87654, 123456]
        return random.choice(funny_amounts)
    return amount
