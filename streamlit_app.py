import streamlit as st
import re
import random
import base64

# 페이지 설정
st.set_page_config(
    page_title="축의금 책정기",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'event_type' not in st.session_state:
    st.session_state.event_type = "결혼식"
if 'relationship' not in st.session_state:
    st.session_state.relationship = "친구"
if 'conversation' not in st.session_state:
    st.session_state.conversation = ""

# 페이지 이동 함수
def next_page():
    st.session_state.page += 1
    st.experimental_rerun()

def prev_page():
    st.session_state.page -= 1
    st.experimental_rerun()

def go_to_page(page_num):
    st.session_state.page = page_num
    st.experimental_rerun()

# HTML을 직접 렌더링하는 함수
def render_html(html_content):
    st.markdown(html_content, unsafe_allow_html=True)

# 페이지 전체 HTML 템플릿 (배경, 스타일 등 포함)
def get_page_template():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
            
            body {
                font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 0;
                padding: 0;
                width: 100vw;
                height: 100vh;
                background: linear-gradient(135deg, #FFEBB3, #F7D358);
            }
            
            .content-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            
            .page-indicator {
                display: flex;
                justify-content: center;
                margin: 20px 0;
            }
            
            .indicator-dot {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: rgba(232, 160, 47, 0.3);
                margin: 0 8px;
            }
            
            .active-dot {
                background-color: #E8A02F;
            }
            
            .footer {
                text-align: center;
                padding: 1rem;
                color: #6D4C41;
                opacity: 0.7;
                font-size: 14px;
                margin-top: 2rem;
            }
        </style>
    </head>
    <body>
        <div class="content-container">
            {content}
        </div>
        <div class="footer">
            © 2025 축의금 책정기
        </div>
    </body>
    </html>
    """

# 페이지 인디케이터 HTML
def get_page_indicator_html(current_page, total_pages=3):
    html = '<div class="page-indicator">'
    for i in range(1, total_pages + 1):
        if i == current_page:
            html += '<div class="indicator-dot active-dot"></div>'
        else:
            html += '<div class="indicator-dot"></div>'
    html += '</div>'
    return html

# 시작 페이지 HTML
def get_start_page_html():
    html = """
    <style>
        .start-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 80vh;
            text-align: center;
        }
        
        .envelope-container {
            margin-bottom: 2rem;
        }
        
        .subtitle {
            color: #452c22;
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 3rem;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        }
    </style>
    
    <div class="start-container">
        <div class="envelope-container">
            <svg width="500" height="300" viewBox="0 0 500 300" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                        <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.15"/>
                    </filter>
                    <linearGradient id="heartGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#FF6B6B" />
                        <stop offset="100%" stop-color="#FF8E8E" />
                    </linearGradient>
                </defs>
                <rect x="0" y="0" width="500" height="300" rx="15" ry="15" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="2" filter="url(#shadow)" />
                <path d="M0,0 L250,130 L500,0" fill="none" stroke="#EEEEEE" stroke-width="2" />
                <path d="M250,175 C250,140 230,125 215,125 C195,125 185,150 185,170 C185,190 205,215 250,245 C295,215 315,190 315,170 C315,150 305,125 285,125 C270,125 250,140 250,175 Z" fill="url(#heartGradient)" />
            </svg>
        </div>
        
        <p class="subtitle">당신의 마음을 금액으로 표현해드립니다</p>
    </div>
    """
    return html

# 입력 페이지 HTML 템플릿
def get_input_page_html():
    html = """
    <style>
        .header {
            display: flex;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }
        
        .header-title {
            font-size: 28px;
            font-weight: 600;
            color: #452c22;
            margin-left: 1rem;
        }
        
        .card {
            background-color: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            margin: 0 auto;
            max-width: 900px;
        }
        
        .section-title {
            font-size: 36px;
            font-weight: 600;
            color: #452c22;
            margin-bottom: 1rem;
        }
        
        .section-subtitle {
            color: #666666;
            font-size: 18px;
            margin-bottom: 2rem;
        }
        
        .input-section {
            margin-bottom: 2rem;
        }
        
        .input-label {
            font-size: 24px;
            font-weight: 600;
            color: #452c22;
            margin-bottom: 1rem;
        }
    </style>
    
    <div class="header">
        <svg width="40" height="24" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="300" height="180" rx="10" ry="10" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="3" />
            <path d="M0,0 L150,75 L300,0" fill="none" stroke="#EEEEEE" stroke-width="3" />
            <path d="M150,105 C150,80 135,70 125,70 C110,70 102,90 102,105 C102,120 115,135 150,155 C185,135 198,120 198,105 C198,90 190,70 175,70 C165,70 150,80 150,105 Z" fill="#FF6B6B" />
        </svg>
        <span class="header-title">축의금 책정기</span>
    </div>
    
    <div class="card">
        <h2 class="section-title">정보 입력</h2>
        <p class="section-subtitle">축의금 분석을 위한 정보를 입력해주세요</p>
        
        <div class="input-section">
            <p class="input-label">행사 유형</p>
            <!-- Streamlit will replace this -->
            <div id="event-type-select"></div>
        </div>
        
        <div class="input-section">
            <p class="input-label">상대방과의 관계</p>
            <!-- Streamlit will replace this -->
            <div id="relationship-select"></div>
        </div>
        
        <div class="input-section">
            <p class="input-label">대화 내용</p>
            <!-- Streamlit will replace this -->
            <div id="conversation-input"></div>
        </div>
        
        <!-- Streamlit will replace these -->
        <div id="button-container" style="display: flex; justify-content: space-between; margin-top: 3rem;">
            <div id="prev-button" style="width: 48%;"></div>
            <div id="next-button" style="width: 48%;"></div>
        </div>
    </div>
    """
    return html

# 결과 페이지 HTML 템플릿
def get_result_page_html(results):
    html = f"""
    <style>
        .header {{
            display: flex;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
        }}
        
        .header-title {{
            font-size: 28px;
            font-weight: 600;
            color: #452c22;
            margin-left: 1rem;
        }}
        
        .card {{
            background-color: white;
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            margin: 0 auto;
            max-width: 900px;
        }}
        
        .card-header {{
            background-color: #FFF8E1;
            border-radius: 20px 20px 0 0;
            padding: 2rem;
            margin: -3rem -3rem 2rem -3rem;
        }}
        
        .section-title {{
            font-size: 36px;
            font-weight: 600;
            color: #452c22;
            margin-bottom: 1rem;
        }}
        
        .tag {{
            display: inline-block;
            background-color: #F5F5F5;
            color: #666666;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            margin-right: 0.5rem;
            font-weight: 500;
            font-size: 16px;
        }}
        
        .result-container {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 2rem 0;
        }}
        
        .envelope-container {{
            margin-right: 2rem;
        }}
        
        .result-amount {{
            font-size: 64px;
            font-weight: 700;
            color: #E8A02F;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        .intimacy-section {{
            margin: 2rem 0;
        }}
        
        .details-section {{
            background-color: #F9F9F9;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
        }}
        
        .details-title {{
            font-size: 24px;
            font-weight: 600;
            color: #452c22;
            margin-bottom: 1.5rem;
        }}
        
        .details-item {{
            font-size: 18px;
            color: #666666;
            margin-bottom: 0.5rem;
        }}
        
        .factors-section {{
            background-color: #FFF8E1;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
        }}
        
        .factors-title {{
            font-size: 20px;
            font-weight: 600;
            color: #D4A017;
            margin-bottom: 1rem;
        }}
        
        .tip-section {{
            background-color: #F0F0F0;
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
        }}
        
        .columns {{
            display: flex;
            justify-content: space-between;
        }}
        
        .column {{
            width: 48%;
        }}
    </style>
    
    <div class="header">
        <svg width="40" height="24" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="300" height="180" rx="10" ry="10" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="3" />
            <path d="M0,0 L150,75 L300,0" fill="none" stroke="#EEEEEE" stroke-width="3" />
            <path d="M150,105 C150,80 135,70 125,70 C110,70 102,90 102,105 C102,120 115,135 150,155 C185,135 198,120 198,105 C198,90 190,70 175,70 C165,70 150,80 150,105 Z" fill="#FF6B6B" />
        </svg>
        <span class="header-title">축의금 책정기</span>
    </div>
    
    <div class="card">
        <div class="card-header">
            <h2 class="section-title">분석 결과</h2>
            <span class="tag">{st.session_state.event_type}</span>
            <span class="tag">{st.session_state.relationship}</span>
        </div>
        
        <div class="result-container">
            <div class="envelope-container">
                <svg width="150" height="90" viewBox="0 0 300 180" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="0" width="300" height="180" rx="10" ry="10" fill="#FFFFFF" stroke="#EEEEEE" stroke-width="3" />
                    <path d="M0,0 L150,75 L300,0" fill="none" stroke="#EEEEEE" stroke-width="3" />
                    <path d="M150,105 C150,80 135,70 125,70 C110,70 102,90 102,105 C102,120 115,135 150,155 C185,135 198,120 198,105 C198,90 190,70 175,70 C165,70 150,80 150,105 Z" fill="#FF6B6B" />
                </svg>
            </div>
            
            <div class="result-amount">{results["amount"]:,}원</div>
        </div>
        
        <div class="intimacy-section">
            <p style="font-size: 20px; font-weight: 600; color: #452c22; margin-bottom: 0.5rem;">친밀도 점수: {results["intimacy_score"]}/100</p>
            <!-- Streamlit will replace this -->
            <div id="progress-bar"></div>
        </div>
        
        <div class="details-section">
            <h3 class="details-title">분석 세부 정보</h3>
            
            <div class="columns">
                <div class="column">
                    {
                        ''.join([f'<p class="details-item">• {key}: {value}</p>' 
                                 for key, value in list(results["analysis_details"].items())[:3]])
                    }
                </div>
                
                <div class="column">
                    {
                        ''.join([f'<p class="details-item">• {key}: {value}</p>' 
                                 for key, value in list(results["analysis_details"].items())[3:]])
                    }
                </div>
            </div>
        </div>
        
        {
            f'''
            <div class="factors-section">
                <h3 class="factors-title">✨ 특별 가산 요인</h3>
                {"".join([f'<p class="details-item">• {factor}</p>' for factor in results["special_factors"]])}
            </div>
            ''' if results["special_factors"] else ''
        }
        
        <div class="tip-section">
            <p class="details-item">💡 {results["funny_tip"]}</p>
        </div>
        
        <!-- Streamlit will replace these -->
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 3rem;">
            <div id="prev-button" style="width: 200px;"></div>
            <div id="save-button" style="width: 200px;"></div>
        </div>
    </div>
    """
    return html

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
    # 컨텐츠 컨테이너 열기
    _, center_col, _ = st.columns([1, 10, 1])  # 좌우 여백을 위한 열 추가
    
    with center_col:
        if st.session_state.page == 1:
            # 시작 페이지
            start_page_html = get_start_page_html()
            st.markdown(get_page_template().format(content=start_page_html + get_page_indicator_html(1)), unsafe_allow_html=True)
            
            # 버튼을 HTML 아래에 배치
            col1, col2, col3 = st.columns([2, 6, 2])
            with col2:
                if st.button("축의금 책정하기", key="start_btn", use_container_width=True):
                    next_page()
        
        elif st.session_state.page == 2:
            # 입력 페이지 HTML 템플릿
            input_page_html = get_input_page_html()
            
            # 페이지 인디케이터 추가
            page_with_indicator = input_page_html + get_page_indicator_html(2)
            
            # 전체 페이지 템플릿 적용
            st.markdown(get_page_template().format(content=page_with_indicator), unsafe_allow_html=True)
            
            # 입력 요소들 (HTML 플레이스홀더 대체)
            st.markdown("<style>.stSelectbox {margin-bottom: 40px;}</style>", unsafe_allow_html=True)
            
            event_type = st.selectbox(
                "행사 유형",
                ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"],
                key="event_type_select",
                index=0 if st.session_state.event_type == "결혼식" else ["결혼식", "돌잔치", "백일", "집들이", "생일", "승진", "개업", "출산"].index(st.session_state.event_type)
            )
            
            relationship = st.selectbox(
                "상대방과의 관계",
                ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"],
                key="relationship_select",
                index=0 if st.session_state.relationship == "친구" else ["친구", "회사동료", "선후배", "가족/친척", "지인", "SNS친구"].index(st.session_state.relationship)
            )
            
            conversation = st.text_area(
                "대화 내용",
                value=st.session_state.conversation,
                height=200,
                placeholder="카카오톡, 메시지 등의 대화 내용을 복사해서 붙여넣으세요...",
                key="conversation_input"
            )
            
            # 버튼 영역
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("← 이전", key="prev_btn", use_container_width=True):
                    prev_page()
            
            with col2:
                if st.button("분석하기 →", key="analyze_btn", use_container_width=True):
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
        
        elif st.session_state.page == 3:
            # 결과가 없으면 오류 표시
            if not st.session_state.analysis_results:
                st.error("분석 결과가 없습니다. 처음부터 다시 시작해주세요.")
                if st.button("처음으로 돌아가기", key="go_home_btn"):
                    go_to_page(1)
                return
            
            # 결과 페이지 HTML 생성
            results = st.session_state.analysis_results
            result_page_html = get_result_page_html(results)
            
            # 페이지 인디케이터 추가
            page_with_indicator = result_page_html + get_page_indicator_html(3)
            
            # 전체 페이지 템플릿 적용
            st.markdown(get_page_template().format(content=page_with_indicator), unsafe_allow_html=True)
            
            # 프로그레스 바 추가 (HTML에서 대체할 수 없음)
            progress = results["intimacy_score"] / 100
            st.progress(progress)
            
            # 버튼 영역
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("← 다시 분석", key="retry_btn", use_container_width=True):
                    prev_page()
            
            with col2:
                if st.button("결과 저장", key="save_btn", use_container_width=True):
                    st.success("결과가 저장되었습니다!")

if __name__ == "__main__":
    main()
