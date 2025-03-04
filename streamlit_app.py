import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import json
import openai
import os
import re
from io import StringIO
import time
import altair as alt
import uuid
from PIL import Image
from streamlit_option_menu import option_menu

# 페이지 설정
st.set_page_config(
    page_title="CSV 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
st.markdown("""
<style>
    /* 전체 폰트 및 색상 */
    .main {
        font-family: 'Arial', sans-serif;
        color: #505050;
    }
    
    /* 헤더 스타일 */
    .title-container {
        background-color: #1a3a5f;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    /* 카드 스타일 */
    .card {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        padding: 1rem;
        margin-bottom: 20px;
    }
    
    .card-header {
        border-top: 8px solid #1a3a5f;
        border-radius: 5px 5px 0 0;
    }
    
    .card-warning-header {
        border-top: 8px solid #f0ad4e;
        border-radius: 5px 5px 0 0;
    }
    
    /* 인사이트 상자 스타일 */
    .insight-box {
        background-color: #f1f5f9;
        border-radius: 5px;
        padding: 0.8rem;
        margin-top: 10px;
        border-left: 4px solid #1a3a5f;
    }
    
    .warning-insight {
        border-left: 4px solid #f0ad4e;
    }
    
    /* 지표 스타일 */
    .metric-container {
        text-align: center;
        padding: 1rem;
        border-radius: 5px;
        background-color: white;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        min-height: 150px;
    }
    
    .metric-title {
        font-size: 1rem;
        color: #505050;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1a3a5f;
        margin-bottom: 0.5rem;
    }
    
    .metric-change {
        font-size: 0.9rem;
        color: #28a745;
    }
    
    .metric-change-negative {
        color: #dc3545;
    }
    
    /* 팝업 스타일 */
    .popup-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
        padding: 20px;
        z-index: 1000;
        max-width: 90%;
        max-height: 90%;
        overflow-y: auto;
        display: none;
    }
    
    .popup-header {
        background-color: #1a3a5f;
        color: white;
        padding: 1rem;
        border-radius: 5px 5px 0 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .close-btn {
        cursor: pointer;
        font-size: 1.5rem;
        color: white;
    }
    
    /* 필터 컨테이너 */
    .filter-container {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        padding: 0.5rem;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
    }
    
    .filter-item {
        background-color: #f1f5f9;
        border-radius: 3px;
        border: 1px solid #d0d0d0;
        padding: 5px 10px;
        margin: 5px;
        font-size: 0.8rem;
    }
    
    /* 섹션 스타일 */
    .section-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1a3a5f;
        margin-bottom: 1rem;
    }
    
    /* 인사이트 점 스타일 */
    .insight-dot {
        width: 4px;
        height: 15px;
        background-color: #1a3a5f;
        margin-right: 10px;
        display: inline-block;
    }
    
    .warning-dot {
        background-color: #f0ad4e;
    }
    
    /* 로딩 스타일 */
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    /* 테이블 스타일 */
    .styled-table {
        border-collapse: collapse;
        width: 100%;
        border-radius: 5px;
        overflow: hidden;
    }
    
    .styled-table th {
        background-color: #1a3a5f;
        color: white;
        padding: 10px;
        text-align: left;
    }
    
    .styled-table td {
        padding: 10px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .styled-table tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    /* 팝업 스타일 JS */
    .stButton>button {
        width: 100%;
    }
    
    /* 세그먼트 카드 스타일 */
    .segment-card {
        background-color: #f1f5f9;
        border-radius: 5px;
        border: 1px solid #d0d0d0;
        min-height: 150px;
    }
    
    .segment-header {
        border-radius: 5px 5px 0 0;
        padding: 0.5rem;
        text-align: center;
        color: white;
        font-weight: bold;
    }
    
    .segment-body {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)
# 세션 상태 초기화
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4"
if 'data' not in st.session_state:
    st.session_state.data = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'insights' not in st.session_state:
    st.session_state.insights = None
if 'charts' not in st.session_state:
    st.session_state.charts = None
if 'popup_content' not in st.session_state:
    st.session_state.popup_content = {}
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
if 'show_popup' not in st.session_state:
    st.session_state.show_popup = False
if 'popup_title' not in st.session_state:
    st.session_state.popup_title = ""
if 'popup_content_html' not in st.session_state:
    st.session_state.popup_content_html = ""

# 헤더 표시
st.markdown("""
<div class="title-container">
    <h2>CSV 데이터 분석 대시보드</h2>
    <span>최종 업데이트: {}</span>
</div>
""".format(st.session_state.last_updated), unsafe_allow_html=True)
# 사이드바 설정
with st.sidebar:
    st.header("설정")
    
    # API 키 입력
    api_key = st.text_input("OpenAI API 키", value=st.session_state.api_key, type="password")
    if api_key:
        st.session_state.api_key = api_key
    
    # 모델 선택
    model_options = {
        "GPT-4": "gpt-4",
        "GPT-3.5 Turbo": "gpt-3.5-turbo",
        "GPT-3.5": "gpt-3.5-turbo-instruct"
    }
    
    selected_model = st.selectbox(
        "OpenAI 모델 선택",
        options=list(model_options.keys()),
        index=0
    )
    st.session_state.model = model_options[selected_model]
    
    st.markdown("---")
    
    # 파일 업로드
    uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # 데이터 로드
            data = pd.read_csv(uploaded_file)
            st.session_state.data = data
            st.success(f"파일 '{uploaded_file.name}'이 업로드되었습니다!")
            st.write(f"열 {len(data.columns)}개, 행 {len(data)}개")
            
            # 간단한 데이터 프리뷰
            st.write("데이터 미리보기:")
            st.dataframe(data.head(5))
            
            # 분석 시작 버튼
            if st.button("데이터 분석 시작", key="start_analysis"):
                if not st.session_state.api_key:
                    st.error("OpenAI API 키를 입력해주세요!")
                else:
                    with st.spinner("데이터를 분석 중입니다... 잠시만 기다려주세요."):
                        # API 키 설정
                        openai.api_key = st.session_state.api_key
                        
                        # 분석 시작
                        st.session_state.summary = analyze_data_summary(data)
                        st.session_state.insights = analyze_data_insights(data)
                        st.session_state.charts = analyze_data_charts(data)
                        
                        # 팝업 콘텐츠 생성
                        create_popup_contents(data)
                        
                        # 분석 완료 표시
                        st.session_state.analysis_complete = True
                        st.session_state.last_updated = datetime.datetime.now().strftime("%Y-%m-%d")
                        
                        st.success("데이터 분석이 완료되었습니다!")
                        st.rerun()
        
        except Exception as e:
            st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
# 메인 페이지 컨텐츠
if st.session_state.data is not None and st.session_state.analysis_complete:
    # 필터 섹션
    st.markdown("""
    <div class="filter-container">
        <span style='margin-right: 10px; font-weight: bold;'>필터:</span>
        <div class="filter-item">날짜: 최근 30일</div>
        <div class="filter-item">카테고리: 전체</div>
        <div class="filter-item">지역: 전체</div>
        <div class="filter-item">고객군: 전체</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 전체 분석 요약 카드
    st.markdown("""
    <div class="card">
        <h3 class="section-title">데이터 분석 종합 요약</h3>
        <div>
    """, unsafe_allow_html=True)
    
    if st.session_state.summary:
        for i, insight in enumerate(st.session_state.summary["insights"]):
            warning_class = "warning-insight" if insight.get("is_warning", False) else ""
            dot_class = "warning-dot" if insight.get("is_warning", False) else ""
            
            st.markdown(f"""
            <div class="insight-box {warning_class}">
                <div class="insight-dot {dot_class}"></div>
                {insight["text"]}
            </div>
            """, unsafe_allow_html=True)
        
        # 우측 통계 블록
        st.markdown("""
        <div style="background-color: #f1f5f9; border-radius: 3px; border: 1px solid #d0d0d0; padding: 15px; margin-top: 15px;">
            <h4 style="font-weight: bold; color: #1a3a5f; margin-bottom: 10px;">주요 통계 지표</h4>
        """, unsafe_allow_html=True)
        
        for stat in st.session_state.summary["statistics"]:
            st.markdown(f"""
            <p style="margin-bottom: 5px;">{stat["name"]}: {stat["value"]} | {stat.get("additional", "")}</p>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 차트 인사이트 팝업 버튼
    if st.button("차트 인사이트 보기", key="show_summary_insights"):
        st.session_state.show_popup = True
        st.session_state.popup_title = "데이터 분석 종합 요약 상세 보기"
        st.session_state.popup_content_html = get_popup_content("summary")
        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # 주요 지표 섹션
    st.markdown("<h3 class='section-title'>주요 지표</h3>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 주요 지표 카드 표시
    if st.session_state.summary and "metrics" in st.session_state.summary:
        metrics = st.session_state.summary["metrics"]
        
        for i, (col, metric) in enumerate(zip([col1, col2, col3, col4], metrics)):
            with col:
                change_class = "metric-change-negative" if metric.get("change_value", 0) < 0 else "metric-change"
                change_icon = "↓" if metric.get("change_value", 0) < 0 else "↑"
                
                header_class = "card-warning-header" if i == 3 else "card-header"
                
                st.markdown(f"""
                <div class="metric-container {header_class}">
                    <div class="metric-title">{metric["title"]}</div>
                    <div class="metric-value">{metric["value"]}</div>
                    <div class="metric-change {change_class}">{change_icon} {abs(metric["change_value"])}%</div>
                </div>
                """, unsafe_allow_html=True)
                
                # 팝업 버튼
                if st.button("상세 보기", key=f"metric_{i}"):
                    st.session_state.show_popup = True
                    st.session_state.popup_title = f"{metric['title']} 상세 분석"
                    st.session_state.popup_content_html = get_popup_content(f"metric_{i}")
                    st.rerun()
# 차트 섹션 1: 매출 추이
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>월별 매출 및 성장률 추이</h3>", unsafe_allow_html=True)
    
    if st.session_state.charts and "time_series" in st.session_state.charts:
        time_series_data = st.session_state.charts["time_series"]
        
        # 차트 설명 표시
        st.markdown(f"""
        <p style="margin-bottom: 15px;">{time_series_data["description"]}</p>
        """, unsafe_allow_html=True)
        
        # 차트 표시
        fig = create_time_series_chart(time_series_data)
        st.plotly_chart(fig, use_container_width=True)
        
        # 차트 인사이트 팝업 버튼
        if st.button("차트 인사이트 보기", key="show_time_series_insights"):
            st.session_state.show_popup = True
            st.session_state.popup_title = "월별 매출 추이 분석"
            st.session_state.popup_content_html = get_popup_content("time_series")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 텍스트 섹션: 주요 인사이트
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>주요 비즈니스 인사이트</h3>", unsafe_allow_html=True)
    
    if st.session_state.insights:
        for i, insight in enumerate(st.session_state.insights["business_insights"]):
            warning_class = "warning-insight" if insight.get("is_warning", False) else ""
            dot_class = "warning-dot" if insight.get("is_warning", False) else ""
            
            st.markdown(f"""
            <div class="insight-box {warning_class}">
                <div class="insight-dot {dot_class}"></div>
                {insight["text"]}
            </div>
            """, unsafe_allow_html=True)
        
        # 차트 인사이트 팝업 버튼
        if st.button("상세 인사이트 보기", key="show_business_insights"):
            st.session_state.show_popup = True
            st.session_state.popup_title = "비즈니스 인사이트 상세 분석"
            st.session_state.popup_content_html = get_popup_content("business_insights")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
# 차트 섹션 2: 두 개의 작은 차트
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-title'>제품 카테고리별 매출 비중</h3>", unsafe_allow_html=True)
        
        if st.session_state.charts and "category_distribution" in st.session_state.charts:
            category_data = st.session_state.charts["category_distribution"]
            
            # 도넛 차트 표시
            fig = create_category_chart(category_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # 차트 인사이트 팝업 버튼
            if st.button("카테고리 분석 보기", key="show_category_insights"):
                st.session_state.show_popup = True
                st.session_state.popup_title = "제품 카테고리 분석"
                st.session_state.popup_content_html = get_popup_content("category_distribution")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h3 class='section-title'>지역별 판매 분포</h3>", unsafe_allow_html=True)
        
        if st.session_state.charts and "region_distribution" in st.session_state.charts:
            region_data = st.session_state.charts["region_distribution"]
            
            # 바 차트 표시
            fig = create_region_chart(region_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # 분석 텍스트
            if "analysis" in region_data:
                st.markdown(f"""
                <p style="margin-top: 10px;">{region_data["analysis"]}</p>
                """, unsafe_allow_html=True)
            
            # 차트 인사이트 팝업 버튼
            if st.button("지역 분석 보기", key="show_region_insights"):
                st.session_state.show_popup = True
                st.session_state.popup_title = "지역별 판매 분석"
                st.session_state.popup_content_html = get_popup_content("region_distribution")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
# 고객 세그먼트 분석
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>고객 세그먼트 분석</h3>", unsafe_allow_html=True)
    
    if st.session_state.insights and "customer_segments" in st.session_state.insights:
        segments = st.session_state.insights["customer_segments"]
        
        # 설명 텍스트
        st.markdown(f"""
        <p style="margin-bottom: 15px;">{segments["description"]}</p>
        """, unsafe_allow_html=True)
        
        # 세그먼트 카드 표시
        segment_cols = st.columns(len(segments["segments"]))
        
        for i, (col, segment) in enumerate(zip(segment_cols, segments["segments"])):
            with col:
                # 색상 선택
                colors = ["#1a3a5f", "#2c5282", "#3c7cb0", "#f0ad4e"]
                color = colors[i % len(colors)]
                
                st.markdown(f"""
                <div class="segment-card">
                    <div class="segment-header" style="background-color: {color};">
                        {segment["name"]}
                    </div>
                    <div class="segment-body">
                        <p><strong>비율:</strong> {segment["percentage"]}</p>
                        <p><strong>구매 빈도:</strong> {segment["purchase_frequency"]}</p>
                        <p><strong>평균 지출:</strong> {segment["avg_spending"]}</p>
                        <p><strong>특징:</strong> {segment["characteristics"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 차트 인사이트 팝업 버튼
        if st.button("세그먼트 분석 상세 보기", key="show_segment_insights"):
            st.session_state.show_popup = True
            st.session_state.popup_title = "고객 세그먼트 상세 분석"
            st.session_state.popup_content_html = get_popup_content("customer_segments")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 시계열 패턴 분석
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>시계열 패턴 분석</h3>", unsafe_allow_html=True)
    
    if st.session_state.insights and "time_patterns" in st.session_state.insights:
        time_patterns = st.session_state.insights["time_patterns"]
        
        # 설명 텍스트
        st.markdown(f"""
        <p style="margin-bottom: 15px;">{time_patterns["description"]}</p>
        """, unsafe_allow_html=True)
        
        # 테이블 헤더
        st.markdown("""
        <table class="styled-table">
            <thead>
                <tr>
                    <th>패턴 유형</th>
                    <th>발견 사항</th>
                    <th>영향도</th>
                    <th>신뢰도</th>
                </tr>
            </thead>
            <tbody>
        """, unsafe_allow_html=True)
        
        # 테이블 행
        for pattern in time_patterns["patterns"]:
            st.markdown(f"""
            <tr>
                <td>{pattern["type"]}</td>
                <td>{pattern["finding"]}</td>
                <td>{pattern["impact"]}</td>
                <td>{pattern["confidence"]}</td>
            </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        # 차트 인사이트 팝업 버튼
        if st.button("시계열 패턴 상세 분석", key="show_time_patterns"):
            st.session_state.show_popup = True
            st.session_state.popup_title = "시계열 패턴 상세 분석"
            st.session_state.popup_content_html = get_popup_content("time_patterns")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
# 팝업 표시
    if st.session_state.show_popup:
        st.markdown(f"""
        <div id="popup" class="popup-container" style="display: block;">
            <div class="popup-header">
                <h3>{st.session_state.popup_title}</h3>
                <div class="close-btn" onclick="document.getElementById('popup').style.display='none';">×</div>
            </div>
            <div style="padding: 20px;">
                {st.session_state.popup_content_html}
            </div>
        </div>
        
        <script>
            // 팝업 닫기 기능
            const closeBtn = document.querySelector('.close-btn');
            if (closeBtn) {{
                closeBtn.addEventListener('click', function() {{
                    document.getElementById('popup').style.display = 'none';
                }});
            }}
        </script>
        """, unsafe_allow_html=True)
        
        if st.button("팝업 닫기"):
            st.session_state.show_popup = False
            st.rerun()

elif st.session_state.data is not None and not st.session_state.analysis_complete:
    st.info("왼쪽 사이드바에서 '데이터 분석 시작' 버튼을 클릭하여 분석을 시작하세요.")
else:
    # 처음 방문 시 안내 메시지
    st.markdown("""
    <div class="card">
        <h3 class="section-title">CSV 데이터 분석 대시보드에 오신 것을 환영합니다!</h3>
        <p>이 대시보드는 CSV 파일을 업로드하면 OpenAI GPT 모델을 활용하여 자동으로 데이터를 분석하고 시각화합니다.</p>
        <br>
        <p><b>시작하려면:</b></p>
        <ol>
            <li>왼쪽 사이드바에 OpenAI API 키를 입력하세요</li>
            <li>사용할 모델을 선택하세요 (기본값: GPT-4)</li>
            <li>분석할 CSV 파일을 업로드하세요</li>
            <li>'데이터 분석 시작' 버튼을 클릭하여 분석을 시작하세요</li>
        </ol>
        <br>
        <p>분석이 완료되면 다양한 차트와 인사이트를 확인할 수 있습니다.</p>
    </div>
    """, unsafe_allow_html=True)
# ----- 함수 정의 -----

def analyze_data_summary(data):
    """OpenAI API를 사용하여 데이터 요약 정보 생성"""
    try:
        # 데이터 기본 정보 수집
        total_records = len(data)
        valid_records = data.dropna().shape[0]
        missing_records = total_records - valid_records
        missing_percentage = round((missing_records / total_records) * 100, 1) if total_records > 0 else 0
        
        # OpenAI API를 사용하여 요약 분석
        prompt = f"""
        다음 데이터에 대한 종합 요약 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {total_records}
        - 유효 데이터: {valid_records}개 ({100 - missing_percentage}%)
        - 누락 데이터: {missing_records}개 ({missing_percentage}%)
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        처음 5개 행:
        {data.head(5).to_string()}
        
        요약 통계:
        {data.describe().to_string()}
        
        다음 형식으로 JSON 응답을 제공해주세요:
        {
            "insights": [
                {"text": "주요 인사이트 1", "is_warning": false},
                {"text": "주요 인사이트 2", "is_warning": false},
                {"text": "주의가 필요한 인사이트", "is_warning": true}
            ],
            "statistics": [
                {"name": "중앙값", "value": "값", "additional": "추가 정보"},
                {"name": "표준편차", "value": "값", "additional": "추가 정보"},
                {"name": "자기상관계수", "value": "값", "additional": "추가 정보"}
            ],
            "metrics": [
                {"title": "총 레코드 수", "value": "15,240", "change_value": 12.3},
                {"title": "평균 매출", "value": "₩5.28M", "change_value": 8.7},
                {"title": "평균 수익률", "value": "38.2%", "change_value": 5.1},
                {"title": "신규 고객", "value": "1,845", "change_value": 23.4}
            ]
        }
        
        각 필드에 대한 설명:
        - insights: 데이터에서 발견된 주요 인사이트 (3-4개). is_warning이 true인 경우 주의가 필요한 인사이트
        - statistics: 주요 통계 지표 (3-4개)
        - metrics: 주요 KPI 지표 (4개)
        
        지표는 데이터의 특성에 맞게 적절히 선택하고, 값과 변화율을 포함해주세요.
        """
        
        response = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        # JSON 응답 파싱
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        st.error(f"데이터 요약 분석 중 오류가 발생했습니다: {e}")
        return {
            "insights": [
                {"text": "데이터 분석 중 오류가 발생했습니다. 다시 시도해주세요.", "is_warning": True}
            ],
            "statistics": [
                {"name": "오류", "value": "분석 실패", "additional": ""}
            ],
            "metrics": [
                {"title": "총 레코드 수", "value": f"{total_records}", "change_value": 0},
                {"title": "유효 데이터", "value": f"{valid_records}", "change_value": 0},
                {"title": "누락 데이터", "value": f"{missing_records}", "change_value": 0},
                {"title": "데이터 완전성", "value": f"{100 - missing_percentage}%", "change_value": 0}
            ]
        }

def analyze_data_insights(data):
    """OpenAI API를 사용하여 비즈니스 인사이트 및 고객 세그먼트 생성"""
    try:
        # OpenAI API를 사용하여 인사이트 분석
        prompt = f"""
        다음 데이터에 대한 비즈니스 인사이트와 고객 세그먼트 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        처음 5개 행:
        {data.head(5).to_string()}
        
        요약 통계:
        {data.describe().to_string()}
        
        다음 형식으로 JSON 응답을 제공해주세요:
        {
            "business_insights": [
                {"text": "비즈니스 인사이트 1", "is_warning": false},
                {"text": "비즈니스 인사이트 2", "is_warning": false},
                {"text": "주의가 필요한 인사이트", "is_warning": true}
            ],
            "customer_segments": {
                "description": "고객 세그먼트 분석에 대한 설명",
                "segments": [
                    {
                        "name": "충성 고객",
                        "percentage": "15%",
                        "purchase_frequency": "높음",
                        "avg_spending": "₩850K",
                        "characteristics": "정기적 방문"
                    },
                    {
                        "name": "잠재 고객",
                        "percentage": "25%",
                        "purchase_frequency": "중간",
                        "avg_spending": "₩520K",
                        "characteristics": "할인 민감"
                    }
                ]
            },
            "time_patterns": {
                "description": "시계열 패턴 분석에 대한 설명",
                "patterns": [
                    {
                        "type": "계절성",
                        "finding": "분기별 주기가 뚜렷함",
                        "impact": "높음",
                        "confidence": "높음"
                    },
                    {
                        "type": "추세",
                        "finding": "상승 추세",
                        "impact": "중간",
                        "confidence": "높음"
                    }
                ]
            }
        }
        
        각 필드에 대한 설명:
        - business_insights: 비즈니스에 관련된 주요 인사이트 (3개). is_warning이 true인 경우 주의가 필요한 인사이트
        - customer_segments: 고객 세그먼트 분석
        - time_patterns: 시계열 패턴 분석
        
        데이터의 특성에 맞게 적절히 분석해주세요. 예시 데이터는 참고용이며, 실제 데이터를 기반으로 분석해주세요.
        """
        
        response = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        # JSON 응답 파싱
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        st.error(f"비즈니스 인사이트 분석 중 오류가 발생했습니다: {e}")
        return {
            "business_insights": [
                {"text": "데이터 분석 중 오류가 발생했습니다. 다시 시도해주세요.", "is_warning": True}
            ],
            "customer_segments": {
                "description": "세그먼트 분석을 실행할 수 없습니다.",
                "segments": [
                    {
                        "name": "오류",
                        "percentage": "N/A",
                        "purchase_frequency": "N/A",
                        "avg_spending": "N/A",
                        "characteristics": "분석 실패"
                    }
                ]
            },
            "time_patterns": {
                "description": "시계열 패턴 분석을 실행할 수 없습니다.",
                "patterns": [
                    {
                        "type": "오류",
                        "finding": "분석 실패",
                        "impact": "N/A",
                        "confidence": "N/A"
                    }
                ]
            }
        }
def analyze_data_charts(data):
    """OpenAI API를 사용하여 차트 데이터 생성"""
    try:
        # OpenAI API를 사용하여 차트 데이터 분석
        prompt = f"""
        다음 데이터에 대한 차트 데이터를 생성해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        처음 5개 행:
        {data.head(5).to_string()}
        
        요약 통계:
        {data.describe().to_string()}
        
        다음 형식으로 JSON 응답을 제공해주세요:
        {
            "time_series": {
                "description": "최근 8개월간의 매출 추이와 월별 성장률을 보여줍니다.",
                "labels": ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월"],
                "values": [100, 120, 115, 130, 135, 150, 160, 175],
                "growth_rates": [0, 20, -4.2, 13, 3.8, 11.1, 6.7, 9.4]
            },
            "category_distribution": {
                "description": "제품 카테고리별 매출 비중을 보여줍니다.",
                "categories": ["제품 A", "제품 B", "제품 C", "제품 D"],
                "values": [35, 25, 20, 20],
                "colors": ["#1a3a5f", "#2c5282", "#3c7cb0", "#f0ad4e"]
            },
            "region_distribution": {
                "description": "지역별 판매 분포를 보여줍니다.",
                "regions": ["서울", "경기", "부산", "기타"],
                "values": [45, 30, 15, 10],
                "analysis": "서울 지역이 전체 매출의 45%를 차지하며, 경기 지역이 30%로 그 뒤를 잇습니다. 수도권 집중도가 75%로 매우 높게 나타납니다."
            }
        }
        
        각 필드에 대한 설명:
        - time_series: 시계열 차트 데이터
        - category_distribution: 카테고리 분포 차트 데이터
        - region_distribution: 지역 분포 차트 데이터
        
        데이터의 특성에 맞게 적절한 차트 데이터를 생성해주세요. 예시 데이터는 참고용이며, 실제 데이터를 기반으로 분석해주세요.
        날짜/시간 열이 있으면 time_series 데이터에 활용하고, 카테고리나 지역 관련 열이 있으면 해당 차트에 활용해주세요.
        """
        
        response = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        # JSON 응답 파싱
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        st.error(f"차트 데이터 생성 중 오류가 발생했습니다: {e}")
        return {
            "time_series": {
                "description": "시계열 차트를 생성할 수 없습니다.",
                "labels": ["오류"],
                "values": [0],
                "growth_rates": [0]
            },
            "category_distribution": {
                "description": "카테고리 분포 차트를 생성할 수 없습니다.",
                "categories": ["오류"],
                "values": [100],
                "colors": ["#cccccc"]
            },
            "region_distribution": {
                "description": "지역 분포 차트를 생성할 수 없습니다.",
                "regions": ["오류"],
                "values": [100],
                "analysis": "분석을 실행할 수 없습니다."
            }
        }

def create_popup_contents(data):
    """각 섹션에 대한 팝업 콘텐츠 생성"""
    try:
        # 요약 팝업 콘텐츠
        prompt_summary = f"""
        다음 데이터에 대한 상세 분석 인사이트를 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        처음 5개 행:
        {data.head(5).to_string()}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 주요 발견점 (bullet points)
        2. 이상값 분석
        3. 상관관계 분석
        4. 개선 기회
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_summary = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_summary}],
            temperature=0.2
        )
        
        st.session_state.popup_content["summary"] = response_summary.choices[0].message.content
        
        # 메트릭 팝업 콘텐츠
        for i in range(4):
            prompt_metric = f"""
            다음 데이터의 지표 {i+1}에 대한 상세 분석을 제공해주세요:
            
            데이터 정보:
            - 총 레코드 수: {len(data)}
            
            열 목록:
            {', '.join(data.columns.tolist())}
            
            요약 통계:
            {data.describe().to_string()}
            
            HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
            1. 지표 정의 및 중요성
            2. 추세 분석
            3. 상세 통계
            4. 개선 추천사항
            
            간결하면서도 통찰력 있는 분석을 제공해주세요.
            """
            
            response_metric = openai.ChatCompletion.create(
                model=st.session_state.model,
                messages=[{"role": "user", "content": prompt_metric}],
                temperature=0.3
            )
            
            st.session_state.popup_content[f"metric_{i}"] = response_metric.choices[0].message.content
        
        # 차트 팝업 콘텐츠 (시계열)
        prompt_time_series = f"""
        다음 데이터의 시계열 분석에 대한 상세 인사이트를 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 주요 발견점 (bullet points)
        2. 계절성 패턴
        3. 추세 분석
        4. 이상점 분석
        5. 예측 및 전망
        6. 개선 기회
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_time_series = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_time_series}],
            temperature=0.3
        )
        
        st.session_state.popup_content["time_series"] = response_time_series.choices[0].message.content
        
        # 비즈니스 인사이트 팝업 콘텐츠
        prompt_business = f"""
        다음 데이터의 비즈니스 인사이트에 대한 상세 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 주요 비즈니스 성과
        2. 문제점 및 위험 요소
        3. 기회 영역
        4. 추천 액션 플랜
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_business = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_business}],
            temperature=0.3
        )
        
        st.session_state.popup_content["business_insights"] = response_business.choices[0].message.content
        
        # 카테고리 분포 팝업 콘텐츠
        prompt_category = f"""
        다음 데이터의 카테고리 분포에 대한 상세 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 각 카테고리 세부 분석
        2. 상위 카테고리 성과 요인
        3. 하위 카테고리 개선점
        4. 카테고리 최적화 전략
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_category = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_category}],
            temperature=0.3
        )
        
        st.session_state.popup_content["category_distribution"] = response_category.choices[0].message.content
        
        # 지역 분포 팝업 콘텐츠
        prompt_region = f"""
        다음 데이터의 지역 분포에 대한 상세 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 각 지역 세부 분석
        2. 지역별 성과 차이 요인
        3. 지역별 최적화 전략
        4. 지역 확장 기회
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_region = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_region}],
            temperature=0.3
        )
        
        st.session_state.popup_content["region_distribution"] = response_region.choices[0].message.content
        
        # 고객 세그먼트 팝업 콘텐츠
        prompt_segment = f"""
        다음 데이터의 고객 세그먼트에 대한 상세 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 각 세그먼트 상세 프로필
        2. 세그먼트별 행동 패턴
        3. 타겟 마케팅 전략
        4. 세그먼트 성장 기회
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_segment = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_segment}],
            temperature=0.3
        )
        
        st.session_state.popup_content["customer_segments"] = response_segment.choices[0].message.content
        
        # 시계열 패턴 팝업 콘텐츠
        prompt_time_pattern = f"""
        다음 데이터의 시계열 패턴에 대한 상세 분석을 제공해주세요:
        
        데이터 정보:
        - 총 레코드 수: {len(data)}
        
        열 목록:
        {', '.join(data.columns.tolist())}
        
        요약 통계:
        {data.describe().to_string()}
        
        HTML 형식으로 응답해주세요. 다음 내용을 포함해주세요:
        1. 시계열 패턴 상세 분석
        2. 계절성 특성
        3. 추세 특성
        4. 이상점 분석
        5. 예측 모델 제안
        
        간결하면서도 통찰력 있는 분석을 제공해주세요.
        """
        
        response_time_pattern = openai.ChatCompletion.create(
            model=st.session_state.model,
            messages=[{"role": "user", "content": prompt_time_pattern}],
            temperature=0.3
        )
        
        st.session_state.popup_content["time_patterns"] = response_time_pattern.choices[0].message.content
    
    except Exception as e:
        st.error(f"팝업 콘텐츠 생성 중 오류가 발생했습니다: {e}")
        for key in ["summary", "time_series", "business_insights", "category_distribution", 
                   "region_distribution", "customer_segments", "time_patterns"] + [f"metric_{i}" for i in range(4)]:
            if key not in st.session_state.popup_content:
                st.session_state.popup_content[key] = "<p>상세 내용을 불러올 수 없습니다.</p>"

def get_popup_content(section_key):
    """팝업 콘텐츠 가져오기"""
    if section_key in st.session_state.popup_content:
        return st.session_state.popup_content[section_key]
    else:
        return "<p>상세 내용을 불러올 수 없습니다.</p>"

def create_time_series_chart(data):
    """시계열 차트 생성"""
    months = data["labels"]
    values = data["values"]
    growth_rates = data["growth_rates"]
    
    # 서브플롯 생성
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 라인 차트 추가
    fig.add_trace(
        go.Scatter(
            x=months,
            y=values,
            name="매출",
            line=dict(color="#1a3a5f", width=3),
            mode="lines+markers"
        ),
        secondary_y=False
    )
    
    # 막대 차트 추가
    fig.add_trace(
        go.Bar(
            x=months,
            y=growth_rates,
            name="성장률 (%)",
            marker_color=["#f0ad4e" if x >= 0 else "#dc3545" for x in growth_rates]
        ),
        secondary_y=True
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title=None,
        xaxis_title="월",
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=400
    )
    
    # Y축 설정
    fig.update_yaxes(title_text="매출", secondary_y=False)
    fig.update_yaxes(title_text="성장률 (%)", secondary_y=True)
    
    return fig

def create_category_chart(data):
    """카테고리 차트 생성"""
    categories = data["categories"]
    values = data["values"]
    colors = data["colors"]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=categories,
            values=values,
            hole=0.5,
            marker_colors=colors
        )
    ])
    
    fig.update_layout(
        title=None,
        margin=dict(l=0, r=0, t=30, b=0),
        height=300,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1)
    )
    
    return fig

def create_region_chart(data):
    """지역 차트 생성"""
    regions = data["regions"]
    values = data["values"]
    
    colors = ["#1a3a5f", "#2c5282", "#3c7cb0", "#f0ad4e"]
    if len(regions) > len(colors):
        colors = colors * (len(regions) // len(colors) + 1)
    
    fig = go.Figure(data=[
        go.Bar(
            x=regions,
            y=values,
            marker_color=colors[:len(regions)]
        )
    ])
    
    fig.update_layout(
        title=None,
        xaxis_title="지역",
        yaxis_title="비율 (%)",
        margin=dict(l=0, r=0, t=30, b=0),
        height=300
    )
    
    return fig
