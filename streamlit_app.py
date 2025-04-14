import streamlit as st
import pandas as pd
import numpy as np
import re
import random
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from io import BytesIO
import base64
import altair as alt
from datetime import datetime, timedelta
import time

# 페이지 설정 및 스타일링
st.set_page_config(
    page_title="AIxivity - 축의금 분석기",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 커스터마이징
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF5757;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #5E17EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-text {
        font-size: 1rem;
        color: #666;
    }
    .highlight {
        background-color: #F0F2F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .result-card {
        background-color: #FFF0F0;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #FF5757;
        margin-top: 2rem;
    }
    .result-title {
        font-size: 1.5rem;
        color: #FF5757;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .emoji-text {
        font-size: 1.2rem;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #888;
        font-size: 0.8rem;
    }
    .stButton>button {
        background-color: #FF5757;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
        margin-top: 1rem;
        width: 100%;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #DDD;
        text-align: center;
    }
    .progress-container {
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    .sidebar-content {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.image("https://i.imgur.com/8NtZ5R5.png", width=200)  # 대체할 로고 URL
    st.markdown("## 👋 안녕하세요!")
    st.markdown("AIxivity는 친구와의 대화와 관계를 분석하여 재미있는 축의금 제안을 해드립니다.")
    st.markdown("### 🔍 사용 방법")
    st.markdown("1. 대화 내용을 입력하거나 파일을 업로드하세요")
    st.markdown("2. 관계 정보와 세부 설정을 입력하세요")
    st.markdown("3. 분석 버튼을 누르고 결과를 확인하세요!")
    
    # 세부 설정
    st.markdown("### ⚙️ 분석 모드 설정")
    analysis_mode = st.radio(
        "분석 모드를 선택하세요:",
        ["재미 위주 🎭", "현실 반영 💼", "완전 랜덤 🎲"]
    )
    
    # 고급 설정
    st.markdown("### 🔧 고급 설정")
    with st.expander("고급 설정 보기"):
        detailed_analysis = st.toggle("상세 분석 결과 보기", value=True)
        visualization_type = st.selectbox(
            "시각화 타입",
            ["기본", "상세", "미니멀"]
        )
        animation_speed = st.slider("애니메이션 속도", 1, 10, 5)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 푸터
    st.markdown("<div class='footer'>AIxivity © 2025 | 비개발자 AI 크리에이터 프로젝트</div>", unsafe_allow_html=True)

# 메인 헤더
st.markdown("<h1 class='main-header'>💰 AIxivity - 축의금 분석기 💰</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>친구와의 대화와 관계를 분석하여 재미있고 신선한 축의금 금액을 제안해드립니다!</p>", unsafe_allow_html=True)

# 탭 설정
tab1, tab2, tab3 = st.tabs(["🔍 대화 분석기", "📊 관계 분석 결과", "💡 축의금 제안"])

# 첫 번째 탭: 입력 섹션
with tab1:
    st.markdown("<h2 class='sub-header'>🔍 대화 정보 입력</h2>", unsafe_allow_html=True)
    
    # 대화 입력 방식
    input_method = st.radio(
        "대화 입력 방식을 선택하세요:",
        ["텍스트 직접 입력", "파일 업로드"]
    )
    
    conversation_text = ""
    
    if input_method == "텍스트 직접 입력":
        conversation_text = st.text_area(
            "친구와의 대화 내용을 붙여넣기 해주세요 (카카오톡 내보내기 형식 권장)",
            height=200,
            placeholder="2023년 4월 1일 오후 2:23, 친구: 오랜만이야! 잘 지냈어?\n2023년 4월 1일 오후 2:25, 나: 응 잘 지내고 있어! 너는 어때?\n..."
        )
    else:
        uploaded_file = st.file_uploader("대화 파일을 업로드하세요 (.txt)", type=["txt"])
        if uploaded_file is not None:
            try:
                conversation_text = uploaded_file.getvalue().decode("utf-8")
                st.success("파일 업로드 성공! 대화 내용이 로드되었습니다.")
                with st.expander("대화 내용 미리보기"):
                    st.text(conversation_text[:500] + "..." if len(conversation_text) > 500 else conversation_text)
            except Exception as e:
                st.error(f"파일 로드 중 오류가 발생했습니다: {e}")
    
    # 구분선
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # 관계 정보 입력
    st.markdown("<h2 class='sub-header'>👥 관계 정보 입력</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        relationship_type = st.selectbox(
            "관계 유형",
            ["친구", "직장 동료", "학교 선후배", "가족/친척", "연인/배우자", "소모임/동호회", "기타"]
        )
        
        relationship_duration = st.slider(
            "알고 지낸 기간 (년)",
            0, 30, 5
        )
        
        meeting_frequency = st.select_slider(
            "만남 빈도",
            options=["거의 없음", "연 1-2회", "월 1-2회", "주 1회 이상", "거의 매일"]
        )
    
    with col2:
        emotional_closeness = st.slider(
            "감정적 친밀도 (1-10)",
            1, 10, 7
        )
        
        has_helped = st.checkbox("과거에 도움을 주고받은 적이 있나요?")
        
        additional_context = st.text_area(
            "추가 맥락 정보 (선택사항)",
            placeholder="예: 최근에 있었던 중요한 일, 특별한 기념일 등"
        )
    
    # 이벤트 정보
    st.markdown("<h2 class='sub-header'>🎉 이벤트 정보</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        event_type = st.selectbox(
            "축하 이벤트 유형",
            ["결혼식", "돌잔치", "생일", "집들이", "승진", "개업/창업", "기타"]
        )
    
    with col2:
        if event_type == "결혼식":
            is_remarriage = st.checkbox("재혼인가요?")
            wedding_scale = st.select_slider(
                "결혼식 규모",
                options=["소규모 (50명 이하)", "중간 (50-200명)", "대규모 (200명 이상)"]
            )
        elif event_type == "돌잔치":
            is_first_child = st.checkbox("첫 아이인가요?")
        elif event_type == "개업/창업":
            business_type = st.text_input("사업 종류")
    
    with col3:
        your_budget = st.number_input(
            "예상 예산 범위 (만원)",
            min_value=0,
            max_value=100,
            value=10
        )
        
        is_attending = st.checkbox("이벤트에 참석할 예정인가요?", value=True)
    
    # 분석 버튼
    analyze_btn = st.button("대화 및 관계 분석하기", type="primary")
    
    # 로딩 상태 표시
    if analyze_btn and conversation_text:
        with st.spinner("AI가 대화를 분석하고 있습니다... 잠시만 기다려주세요! 🔍"):
            progress_bar = st.progress(0)
            for i in range(100):
                # 실제 처리 대신 시각적 효과
                time.sleep(0.03)
                progress_bar.progress(i + 1)
            
            # 분석 완료 후 두 번째 탭으로 이동
            st.success("분석이 완료되었습니다! '관계 분석 결과' 탭에서 결과를 확인하세요.")
            time.sleep(1)
            st.experimental_rerun()
    elif analyze_btn and not conversation_text:
        st.warning("대화 내용을 입력하거나 파일을 업로드해주세요!")

# 두 번째 탭: 분석 결과
with tab2:
    # 분석이 실행되지 않았을 때 표시할 메시지
    if not analyze_btn and not st.session_state.get('analysis_complete', False):
        st.info("대화 분석을 먼저 실행해주세요!")
    else:
        # 세션 상태에 분석 완료 표시
        st.session_state.analysis_complete = True
        
        st.markdown("<h2 class='sub-header'>📊 대화 패턴 분석</h2>", unsafe_allow_html=True)
        
        # 샘플 데이터 생성 (실제로는 대화 분석 로직 구현)
        if 'conversation_text' in locals() and conversation_text:
            # 간단한 대화 분석 로직 구현
            total_messages = len(re.findall(r'\n', conversation_text)) + 1
            user_messages = random.randint(total_messages // 3, total_messages // 2)
            friend_messages = total_messages - user_messages
            
            # 응답 시간 계산 (랜덤 샘플)
            response_times = []
            for i in range(50):
                response_times.append(random.randint(1, 300))  # 1~300분 사이 응답 시간
            
            avg_response_time = sum(response_times) // len(response_times)
            
            # 대화 키워드 분석 (샘플)
            keywords = {
                "만나자": random.randint(5, 15),
                "밥": random.randint(8, 20),
                "ㅋㅋㅋ": random.randint(20, 50),
                "굿": random.randint(3, 10),
                "화이팅": random.randint(2, 8),
                "취업": random.randint(1, 7),
                "여행": random.randint(3, 12),
                "축하": random.randint(2, 9),
                "고마워": random.randint(5, 15),
                "사랑": random.randint(0, 5),
                "돈": random.randint(1, 8),
                "술": random.randint(10, 25),
                "영화": random.randint(3, 10),
                "주말": random.randint(5, 15),
                "오랜만": random.randint(3, 10)
            }
            
            # 이모티콘 사용 빈도
            emoji_count = random.randint(total_messages // 5, total_messages // 2)
            emoji_ratio = emoji_count / total_messages
            
            # 메시지 길이 분석
            message_lengths = []
            for i in range(total_messages):
                message_lengths.append(random.randint(5, 100))
            
            avg_message_length = sum(message_lengths) // len(message_lengths)
            
            # 시각화: 메시지 비율
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("총 메시지 수", f"{total_messages}개")
                
                # Plotly를 사용한 파이 차트
                fig = go.Figure(data=[go.Pie(
                    labels=['나', '친구'],
                    values=[user_messages, friend_messages],
                    hole=.3,
                    marker_colors=['#FF5757', '#5E17EB']
                )])
                
                fig.update_layout(
                    title="메시지 비율",
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("평균 응답 시간", f"{avg_response_time}분")
                
                # 응답 시간 히스토그램
                fig = px.histogram(
                    x=response_times, 
                    nbins=20, 
                    labels={'x':'응답 시간 (분)'}, 
                    title="응답 시간 분포",
                    color_discrete_sequence=['#5E17EB']
                )
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 키워드 분석
            st.markdown("<h3 class='sub-header'>🔑 키워드 분석</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                # 워드클라우드 생성
                wc = WordCloud(
                    background_color='white',
                    width=500,
                    height=300,
                    max_words=100,
                    colormap='viridis'
                ).generate_from_frequencies(keywords)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                
                st.pyplot(fig)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                # 키워드 빈도 막대 그래프
                top_keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:8])
                
                fig = px.bar(
                    x=list(top_keywords.keys()),
                    y=list(top_keywords.values()),
                    labels={'x': '키워드', 'y': '빈도'},
                    title="상위 키워드 빈도",
                    color_discrete_sequence=['#FF5757']
                )
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 대화 패턴 분석
            st.markdown("<h3 class='sub-header'>📱 대화 패턴 분석</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("평균 메시지 길이", f"{avg_message_length}자")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric("이모티콘 사용 비율", f"{emoji_ratio:.1%}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                conversation_activity = random.choice(["아침형", "저녁형", "주말형", "평일형", "불규칙형"])
                st.metric("대화 활동 패턴", conversation_activity)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # 관계 분석
            st.markdown("<h3 class='sub-header'>👫 관계 분석</h3>", unsafe_allow_html=True)
            
            # 관계 점수 계산 (샘플)
            conversation_score = random.randint(1, 100)
            relationship_score = random.randint(1, 100)
            emotional_score = random.randint(1, 100)
            overall_score = (conversation_score + relationship_score + emotional_score) // 3
            
            relationship_types = {
                "소통 지수": conversation_score,
                "친밀도 지수": relationship_score,
                "정서적 연결": emotional_score,
                "전체 관계 점수": overall_score
            }
            
            # 레이더 차트
            categories = list(relationship_types.keys())
            values = list(relationship_types.values())
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='관계 점수',
                marker_color='#FF5757'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title="관계 분석 점수",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 재미있는 관계 유형 정의
            relationship_archetypes = [
                {
                    "name": "영혼의 단짝",
                    "description": "말이 필요 없는 깊은 우정. 눈빛만으로도 서로를 이해합니다.",
                    "score": random.randint(80, 100),
                    "emoji": "✨"
                },
                {
                    "name": "밥약 전문가",
                    "description": "주로 먹을 때만 만나지만, 그 시간은 항상 즐겁습니다.",
                    "score": random.randint(60, 85),
                    "emoji": "🍽️"
                },
                {
                    "name": "열정의 토론가",
                    "description": "어떤 주제든 깊은 대화로 발전시키는 지적 파트너십.",
                    "score": random.randint(70, 90),
                    "emoji": "🔥"
                },
                {
                    "name": "감정의 서포터",
                    "description": "힘든 시간을 함께 견뎌주는 정서적 지지자.",
                    "score": random.randint(75, 95),
                    "emoji": "🤗"
                },
                {
                    "name": "온라인 친밀러",
                    "description": "실제 만남은 드물지만 온라인에서는 항상 연결되어 있는 관계.",
                    "score": random.randint(50, 80),
                    "emoji": "💻"
                },
                {
                    "name": "추억의 보관자",
                    "description": "과거의 좋은 시간을 함께한, 역사가 깊은 관계.",
                    "score": random.randint(65, 85),
                    "emoji": "🕰️"
                },
                {
                    "name": "공백기 마스터",
                    "description": "오랜 시간 연락이 없어도 만나면 예전과 같은 특별한 관계.",
                    "score": random.randint(40, 70),
                    "emoji": "⏳"
                },
                {
                    "name": "이모티콘 폭격기",
                    "description": "문자보다 이모티콘으로 더 많은 대화를 나누는 관계.",
                    "score": random.randint(60, 80),
                    "emoji": "😂"
                }
            ]
            
            # 점수에 따라 관계 유형 선택
            selected_archetype = random.choice(relationship_archetypes)
            
            st.markdown("<div class='highlight'>", unsafe_allow_html=True)
            st.markdown(f"### {selected_archetype['emoji']} 당신의 관계 유형: {selected_archetype['name']}")
            st.markdown(f"**{selected_archetype['description']}**")
            st.markdown(f"관계 점수: {selected_archetype['score']}/100")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 특별한 인사이트
            interesting_insights = [
                f"당신은 친구보다 평균 {random.randint(5, 30)}분 더 빨리 응답하는 경향이 있습니다.",
                f"대화 중 '{random.choice(list(keywords.keys()))}' 단어를 가장 많이 사용하셨습니다.",
                f"당신들의 대화는 주로 {random.choice(['저녁', '늦은 밤', '아침', '주말'])}에 이루어집니다.",
                f"약속을 잡는 대화가 전체의 {random.randint(10, 40)}%를 차지합니다.",
                f"실제 만남으로 이어진 대화는 약 {random.randint(5, 25)}%에 불과합니다.",
                f"{random.choice(['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'])}에 가장 활발하게 대화하는 경향이 있습니다."
            ]
            
            st.markdown("<h3 class='sub-header'>💡 흥미로운 인사이트</h3>", unsafe_allow_html=True)
            
            for i, insight in enumerate(random.sample(interesting_insights, 3)):
                st.markdown(f"**{i+1}. {insight}**")
        else:
            st.warning("대화 내용이 없습니다. 분석을 위해 대화 내용을 입력해주세요.")

# 세 번째 탭: 축의금 제안
with tab3:
    # 분석이 실행되지 않았을 때 표시할 메시지
    if not st.session_state.get('analysis_complete', False):
        st.info("대화 분석을 먼저 실행해주세요!")
    else:
        st.markdown("<h2 class='sub-header'>💰 AI 축의금 제안</h2>", unsafe_allow_html=True)
        
        # 이전 탭에서 선택된 관계 유형과 점수
        if 'selected_archetype' in locals():
            archetype_name = selected_archetype['name']
            archetype_score = selected_archetype['score']
        else:
            archetype_name = random.choice(["영혼의 단짝", "밥약 전문가", "온라인 친밀러", "공백기 마스터"])
            archetype_score = random.randint(40, 100)
        
        # 축의금 계산 요인 설명
        st.markdown("### 🧮 축의금 계산 요인")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='highlight'>", unsafe_allow_html=True)
            st.markdown("#### 관계 요인")
            st.markdown("- 관계 유형: " + relationship_type)
            st.markdown(f"- 알고 지낸 기간: {relationship_duration}년")
            st.markdown("- 만남 빈도: " + meeting_frequency)
            st.markdown(f"- 감정적 친밀도: {emotional_closeness}/10")
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='highlight'>", unsafe_allow_html=True)
            st.markdown("#### 대화 패턴 요인")
            if 'conversation_score' in locals():
                st.markdown(f"- 소통 지수: {conversation_score}/100")
            else:
                st.markdown(f"- 소통 지수: {random.randint(40, 90)}/100")
            
            if 'emoji_ratio' in locals():
                st.markdown(f"- 이모티콘 사용 비율: {emoji_ratio:.1%}")
            else:
                st.markdown(f"- 이모티콘 사용 비율: {random.randint(10, 50)}%")
            
            if 'avg_response_time' in locals():
                st.markdown(f"- 평균 응답 시간: {avg_response_time}분")
            else:
                st.markdown(f"- 평균 응답 시간: {random.randint(5, 120)}분")
            
            st.markdown(f"- 관계 유형: {archetype_name}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 이벤트 정보 요약
        st.markdown("### 🎉 이벤트 요약")
        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
        st.markdown(f"- 이벤트 유형: {event_type}")
        
        if 'is_attending' in locals():
            attendance_status = "참석 예정" if is_attending else "불참 예정"
            st.markdown(f"- 참석 여부: {attendance_status}")
        
        if 'wedding_scale' in locals() and event_type == "결혼식":
            st.markdown(f"- 결혼식 규모: {wedding_scale}")
            if 'is_remarriage' in locals():
                remarriage_status = "재혼" if is_remarriage else "초혼"
                st.markdown(f"- 결혼 유형: {remarriage_status}")
        
        if 'is_first_child' in locals() and event_type == "돌잔치":
            child_status = "첫 아이" if is_first_child else "둘째 이상"
            st.markdown(f"- 자녀 순서: {child_status}")
        
        if 'business_type' in locals() and event_type == "개업/창업":
            st.markdown(f"- 사업 종류: {business_type}")
        
        if 'your_budget' in locals():
            st.markdown(f"- 예상 예산: {your_budget}만원")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 로딩 애니메이션
        st.markdown("### 💰 AI가 제안하는 축의금")
        
        with st.spinner("AI가 최적의 축의금을 계산하고 있습니다..."):
            # 진행 상태 바 - 시각적 효과
            if "progress_bar_run" not in st.session_state:
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)
                st.session_state.progress_bar_run = True
        
        # 분석 모드에 따른 결과 생성
        if 'analysis_mode' in locals():
            mode = analysis_mode
        else:
            mode = random.choice(["재미 위주 🎭", "현실 반영 💼", "완전 랜덤 🎲"])
        
        # 축의금 금액 및 설명 생성
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
                    "description": "현금과 선물의 조합. 당신의 관계 유형인 '공백기 마스터'에게는 존재감을 확실히 각인시킬 수 있는 방법입니다.",
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
            duration_adjust = min(relationship_duration / 10, 2)
            
            # 감정적 친밀도에 따른 조정
            closeness_adjust = emotional_closeness / 5
            
            # 최종 금액 계산
            if 'relationship_type' in locals() and 'event_type' in locals():
                amount = base_amount * relation_adjust.get(relationship_type, 1) * event_adjust.get(event_type, 1) * duration_adjust * closeness_adjust
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
                        "description": f"당신의 관계와 상황을 분석했을 때, 현실적으로 적절한 금액입니다. {relationship_type}이고 {relationship_duration}년간 알아온 관계를 고려했습니다.",
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
            else:
                # 기본 현실적 옵션
                gift_options = [
                    {
                        "amount": "5만원",
                        "description": "가장 무난한 금액입니다. 대부분의 경우에 적합합니다.",
                        "emoji": "💵",
                        "details": "기본적인 예의를 갖춘 금액입니다."
                    },
                    {
                        "amount": "10만원",
                        "description": "조금 더 특별한 관계에 적합한 금액입니다.",
                        "emoji": "💰",
                        "details": "더 의미 있는 관계임을 표현합니다."
                    },
                    {
                        "amount": "3만원",
                        "description": "부담 없는 금액으로, 친밀도가 높지 않은 경우에 적합합니다.",
                        "emoji": "💴",
                        "details": "최소한의 예의를 갖춘 금액입니다."
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
        
        # 최종 추천 결과 표시
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='result-title'>🎁 AI의 최종 축의금 추천</h2>", unsafe_allow_html=True)
        
        # 메인 추천
        main_option = random.choice(gift_options)
        
        st.markdown(f"## {main_option['emoji']} 추천 축의금: {main_option['amount']}")
        st.markdown(f"**{main_option['description']}**")
        st.markdown(f"*{main_option['details']}*")
        
        # 버튼 - 다른 옵션 보기
        if st.button("다른 추천 옵션 보기"):
            # 나머지 옵션들
            other_options = [opt for opt in gift_options if opt != main_option]
            
            for i, option in enumerate(other_options):
                st.markdown(f"### 대안 {i+1}: {option['emoji']} {option['amount']}")
                st.markdown(f"**{option['description']}**")
                st.markdown(f"*{option['details']}*")
        
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
        
        # 공유 및 저장 옵션
        st.markdown("### 🔄 분석 결과 공유하기")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("결과 이미지로 저장"):
                st.info("분석 결과를 이미지로 저장하는 기능은 개발 중입니다.")
        
        with col2:
            if st.button("결과 링크 복사하기"):
                st.success("결과 링크가 클립보드에 복사되었습니다! (데모용)")
                st.code("https://aixivity.app/results/a1b2c3d4")
        
        # 사용자 피드백
        st.markdown("### 💬 이 결과가 도움이 되었나요?")
        
        feedback = st.radio(
            "분석 결과에 대한 만족도를 선택해주세요:",
            ["매우 만족", "만족", "보통", "불만족", "매우 불만족"],
            horizontal=True
        )
        
        feedback_text = st.text_area("추가 의견이 있다면 알려주세요:", placeholder="의견을 입력해주세요...")
        
        if st.button("피드백 제출하기"):
            st.success("피드백을 제출해주셔서 감사합니다! 더 나은 서비스를 위해 노력하겠습니다.")
            
# 푸터
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; padding: 1rem;'>"
    "© 2025 AIxivity | 비개발자 AI 크리에이터 프로젝트 | 문의: aixivity@example.com"
    "</div>",
    unsafe_allow_html=True
)
