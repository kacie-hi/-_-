import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import openai
import json
import numpy as np
from datetime import datetime

# 페이지 설정 및 스타일 적용
st.set_page_config(
    page_title="고급 CSV 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

# 커스텀 CSS 적용
st.markdown("""
<style>
    .card {
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        border-radius: 10px;
        padding: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
    }
    .st-emotion-cache-16txtl3 h1 {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .insight-card {
        border-left: 4px solid #4e8df5;
        padding: 10px 15px;
        margin-bottom: 10px;
        background-color: #f8f9fa;
    }
    .chart-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f2f6;
    }
    .st-tabs {
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #4e8df5;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #3a7bd5;
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 설정
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2621/2621303.png", width=80)
    st.title("분석 설정")
    openai_api_key = st.text_input("OpenAI API 키", type="password")
    
    st.markdown("---")
    
    model_option = st.selectbox(
        "OpenAI 모델 선택",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0
    )
    
    st.markdown("---")
    
    st.markdown("### 🎨 대시보드 테마")
    color_theme = st.selectbox(
        "색상 테마",
        ["파랑 계열", "초록 계열", "보라 계열", "주황 계열"],
        index=0
    )
    
    # 색상 테마 설정
    if color_theme == "파랑 계열":
        primary_color = "#4e8df5"
        secondary_color = "#2c58a0"
        chart_colors = px.colors.sequential.Blues
    elif color_theme == "초록 계열":
        primary_color = "#36b37e"
        secondary_color = "#1a7f5a"
        chart_colors = px.colors.sequential.Greens
    elif color_theme == "보라 계열":
        primary_color = "#a259ff"
        secondary_color = "#7b3fd1"
        chart_colors = px.colors.sequential.Purples
    else:
        primary_color = "#ff9900"
        secondary_color = "#d97b00"
        chart_colors = px.colors.sequential.Oranges
    
    st.markdown("---")
    
    st.markdown("### 📊 만든이 정보")
    st.markdown("Made with ❤️ by AI 기반 데이터 분석팀")
    st.markdown("© 2025 CSV Analyzer Pro")

# 메인 헤더
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 20px; margin-bottom: 20px;">
    <div style="font-size: 2.5rem; background: linear-gradient(90deg, {primary_color}, {secondary_color}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;">
        고급 데이터 분석 대시보드
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("CSV 파일을 업로드하면 AI가 자동으로 데이터를 분석하고 인사이트를 제공합니다.")

# 함수: CSV 데이터 자동 분석
def analyze_csv_structure(df):
    """CSV 파일의 구조를 분석하여 적합한 시각화 방법 추천"""
    analysis = {
        "numeric_cols": df.select_dtypes(include=['int64', 'float64']).columns.tolist(),
        "categorical_cols": df.select_dtypes(include=['object', 'category']).columns.tolist(),
        "datetime_cols": [],
        "recommended_charts": [],
        "has_time_series": False,
        "correlation_candidates": []
    }
    
    # 날짜 열 탐지
    for col in analysis["categorical_cols"]:
        try:
            # 첫 5개 행으로 날짜 열인지 확인
            sample = df[col].dropna().head(5)
            if len(sample) > 0:
                pd.to_datetime(sample.iloc[0])
                # 성공하면 날짜 열로 간주
                analysis["datetime_cols"].append(col)
                analysis["has_time_series"] = True
        except:
            pass
    
    # 날짜 열을 카테고리 열에서 제거
    for col in analysis["datetime_cols"]:
        if col in analysis["categorical_cols"]:
            analysis["categorical_cols"].remove(col)
    
    # 추천 차트 결정
    if analysis["has_time_series"] and len(analysis["numeric_cols"]) > 0:
        analysis["recommended_charts"].append({
            "type": "line", 
            "title": f"{analysis['datetime_cols'][0]} 기준 시계열 분석", 
            "x": analysis["datetime_cols"][0],
            "y": analysis["numeric_cols"][0]
        })
    
    # 수치형 열이 2개 이상이면 산점도 추천
    if len(analysis["numeric_cols"]) >= 2:
        analysis["recommended_charts"].append({
            "type": "scatter", 
            "title": f"{analysis['numeric_cols'][0]} vs {analysis['numeric_cols'][1]} 관계", 
            "x": analysis["numeric_cols"][0],
            "y": analysis["numeric_cols"][1]
        })
        
        # 상관관계 후보 설정
        analysis["correlation_candidates"] = analysis["numeric_cols"]
    
    # 카테고리 + 수치 조합이 있으면 바 차트 추천
    if len(analysis["categorical_cols"]) > 0 and len(analysis["numeric_cols"]) > 0:
        analysis["recommended_charts"].append({
            "type": "bar", 
            "title": f"{analysis['categorical_cols'][0]} 별 {analysis['numeric_cols'][0]} 분포", 
            "x": analysis["categorical_cols"][0],
            "y": analysis["numeric_cols"][0]
        })
    
    # 수치형 열에 대한 히스토그램 추천
    if len(analysis["numeric_cols"]) > 0:
        analysis["recommended_charts"].append({
            "type": "histogram", 
            "title": f"{analysis['numeric_cols'][0]} 분포", 
            "x": analysis["numeric_cols"][0]
        })
    
    # 파이 차트 (카테고리 열이 있고 카디널리티가 적절한 경우)
    if len(analysis["categorical_cols"]) > 0:
        # 카테고리 수 확인
        for col in analysis["categorical_cols"]:
            if 2 <= df[col].nunique() <= 10 and len(analysis["numeric_cols"]) > 0:
                analysis["recommended_charts"].append({
                    "type": "pie", 
                    "title": f"{col} 구성 비율", 
                    "names": col,
                    "values": analysis["numeric_cols"][0]
                })
                break
    
    return analysis

# 함수: OpenAI API를 사용한 데이터 분석
def analyze_data_with_ai(df_info, df_structure):
    if not openai_api_key:
        st.error("OpenAI API 키를 입력해주세요.")
        return None
    
    try:
        openai.api_key = openai_api_key
        prompt = f"""
        다음은 CSV 데이터 파일에 대한 정보입니다:
        
        컬럼 목록: {df_info['columns']}
        데이터 타입: {df_info['dtypes']}
        요약 통계: {df_info['describe']}
        데이터 구조 분석: {df_structure}
        
        최대한 구체적으로 이 데이터에 대한 분석을 다음 형식의 JSON으로 제공해주세요:
        1. "key_metrics": 5개 이하의 핵심 지표로, 각각 "metric_name", "value", "description", "trend" 필드를 포함 (value는 숫자, trend는 "상승", "하락", "유지" 중 하나)
        2. "insights": 데이터에서 발견된 주요 인사이트 (최소 4개)
        3. "recommendations": 이 데이터를 바탕으로 한 실행 가능한 추천 사항 (최소 3개)
        4. "chart_insights": 각 차트 유형별 인사이트 (시계열, 히스토그램, 산점도, 바 차트, 파이 차트에 대한 코멘트)
        
        JSON 형식으로만 응답해주세요. 예시 형식:
        {
          "key_metrics": [
            {"metric_name": "평균 매출", "value": 5000, "description": "전체 기간 평균 매출액", "trend": "상승"},
            ...
          ],
          "insights": ["주요 인사이트 1", "주요 인사이트 2", ...],
          "recommendations": ["추천 사항 1", "추천 사항 2", ...],
          "chart_insights": {
            "time_series": "시계열 차트에서 관찰된 인사이트...",
            "histogram": "히스토그램에서 관찰된 인사이트...",
            "scatter": "산점도에서 관찰된 인사이트...",
            "bar": "바 차트에서 관찰된 인사이트...",
            "pie": "파이 차트에서 관찰된 인사이트..."
          }
        }
        """
        
        response = openai.chat.completions.create(
            model=model_option,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        
        result = response.choices[0].message.content
        # JSON 부분만 추출
        try:
            json_start = result.find('{')
            json_end = result.rfind('}') + 1
            if json_start >= 0 and json_end > 0:
                result = result[json_start:json_end]
            return json.loads(result)
        except:
            st.error("API 응답을 JSON으로 파싱하는데 문제가 발생했습니다.")
            return {
                "key_metrics": [{"metric_name": "오류", "value": 0, "description": "API 응답 파싱 실패", "trend": "유지"}],
                "insights": ["API 응답을 파싱하는데 문제가 발생했습니다."],
                "recommendations": ["다시 시도해보세요."],
                "chart_insights": {
                    "time_series": "",
                    "histogram": "",
                    "scatter": "",
                    "bar": "",
                    "pie": ""
                }
            }
        
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {str(e)}")
        return None

# 차트 생성 함수
def create_chart(df, chart_type, x=None, y=None, names=None, values=None, title=""):
    fig = None
    
    if chart_type == "line":
        if x and y:
            fig = px.line(df, x=x, y=y, title=title)
    
    elif chart_type == "bar":
        if x and y:
            fig = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=[primary_color])
    
    elif chart_type == "histogram":
        if x:
            fig = px.histogram(df, x=x, title=title, color_discrete_sequence=[primary_color])
    
    elif chart_type == "scatter":
        if x and y:
            fig = px.scatter(df, x=x, y=y, title=title, color_discrete_sequence=[primary_color])
    
    elif chart_type == "pie":
        if names and values:
            fig = px.pie(df, names=names, values=values, title=title)
    
    elif chart_type == "heatmap":
        # 상관관계 히트맵 특별 처리
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, text_auto=True, title=title)
    
    if fig:
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font=dict(size=16, color='#333', family="Arial, sans-serif"),
            font=dict(family="Arial, sans-serif"),
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0'),
            margin=dict(l=40, r=40, t=60, b=40),
            height=450
        )
    
    return fig

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type="csv")

# 데이터가 업로드되면 실행
if uploaded_file is not None:
    # 탭 생성
    tabs = st.tabs(["📊 대시보드", "🔍 심층 분석", "📈 시각화 도구", "📋 데이터 탐색"])
    
    # 데이터 로드
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"CSV 파일을 로드하는 중 오류가 발생했습니다: {str(e)}")
        st.stop()
    
    # 데이터 구조 분석
    df_structure = analyze_csv_structure(df)
    
    # 데이터 기본 정보 수집
    df_info = {
        "columns": list(df.columns),
        "dtypes": str(df.dtypes),
        "describe": str(df.describe()),
        "shape": df.shape
    }
    
    # AI 분석 실행
    with st.spinner("AI가 데이터를 분석 중입니다..."):
        if openai_api_key:
            analysis_result = analyze_data_with_ai(df_info, df_structure)
        else:
            st.warning("OpenAI API 키가 입력되지 않았습니다. 데이터 시각화만 제공됩니다.")
            analysis_result = None
    
    # 대시보드 탭
    with tabs[0]:
        st.markdown(f"<h2 class='section-title'>📊 데이터 요약</h2>", unsafe_allow_html=True)
        
        # 기본 데이터 정보 (상단 핵심 지표)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 5px solid {primary_color}">
                <div class="metric-label">총 레코드</div>
                <div class="metric-value">{df.shape[0]:,}</div>
                <div>행 수</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 5px solid {primary_color}">
                <div class="metric-label">변수 수</div>
                <div class="metric-value">{df.shape[1]}</div>
                <div>열 수</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            missing_values = df.isna().sum().sum()
            st.markdown(f"""
            <div class="metric-card" style="border-top: 5px solid {primary_color}">
                <div class="metric-label">결측치</div>
                <div class="metric-value">{missing_values:,}</div>
                <div>전체 데이터의 {missing_values / (df.shape[0] * df.shape[1]) * 100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # 수치형 열이 있는 경우 평균값을 표시
            if len(df_structure["numeric_cols"]) > 0:
                col_name = df_structure["numeric_cols"][0]
                col_mean = df[col_name].mean()
                st.markdown(f"""
                <div class="metric-card" style="border-top: 5px solid {primary_color}">
                    <div class="metric-label">{col_name} 평균</div>
                    <div class="metric-value">{col_mean:.2f}</div>
                    <div>주요 변수 평균값</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="metric-card" style="border-top: 5px solid {primary_color}">
                    <div class="metric-label">카테고리 수</div>
                    <div class="metric-value">{len(df_structure["categorical_cols"])}</div>
                    <div>범주형 변수 수</div>
                </div>
                """, unsafe_allow_html=True)
        
        # AI 분석 결과가 있는 경우 핵심 지표 표시
        if analysis_result and 'key_metrics' in analysis_result:
            st.markdown(f"<h2 class='section-title'>📈 AI 분석 핵심 지표</h2>", unsafe_allow_html=True)
            
            metrics = analysis_result['key_metrics']
            if metrics:
                cols = st.columns(min(len(metrics), 5))  # 최대 5개까지 표시
                
                for i, metric in enumerate(metrics[:5]):  # 최대 5개까지 표시
                    name = metric.get('metric_name', '지표')
                    value = metric.get('value', 0)
                    desc = metric.get('description', '')
                    trend = metric.get('trend', '유지')
                    
                    # 트렌드에 따른 색상 및 아이콘 설정
                    if trend == '상승':
                        trend_color = '#36b37e'  # 초록색
                        trend_icon = '↑'
                    elif trend == '하락':
                        trend_color = '#ff5630'  # 빨간색
                        trend_icon = '↓'
                    else:
                        trend_color = '#6554c0'  # 보라색
                        trend_icon = '→'
                    
                    with cols[i]:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-label">{name}</div>
                            <div class="metric-value">{value:,}</div>
                            <div>{desc}</div>
                            <div style="color: {trend_color}; font-weight: bold;">{trend_icon} {trend}</div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # AI 인사이트 섹션
        if analysis_result and 'insights' in analysis_result:
            st.markdown(f"<h2 class='section-title'>🔍 AI 분석 인사이트</h2>", unsafe_allow_html=True)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            insights = analysis_result['insights']
            for i, insight in enumerate(insights):
                st.markdown(f"""
                <div class="insight-card">
                    <strong>인사이트 {i+1}:</strong> {insight}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 추천 차트 섹션
        st.markdown(f"<h2 class='section-title'>📊 데이터 시각화</h2>", unsafe_allow_html=True)
        
        # 시각화 행 1
        if len(df_structure["recommended_charts"]) > 0:
            # 차트를 2열로 배치
            chart_cols = 2
            charts_per_row = min(chart_cols, len(df_structure["recommended_charts"]))
            
            # 첫 번째 행
            cols = st.columns(charts_per_row)
            
            for i, chart_info in enumerate(df_structure["recommended_charts"][:charts_per_row]):
                with cols[i % charts_per_row]:
                    st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
                    st.subheader(chart_info["title"])
                    
                    # 차트 생성
                    if chart_info["type"] == "pie":
                        fig = create_chart(
                            df, "pie", 
                            names=chart_info["names"], 
                            values=chart_info["values"], 
                            title=chart_info["title"]
                        )
                    else:
                        fig = create_chart(
                            df, chart_info["type"], 
                            x=chart_info.get("x"), 
                            y=chart_info.get("y"), 
                            title=chart_info["title"]
                        )
                    
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # 차트 인사이트 (AI 분석 결과가 있는 경우)
                        if analysis_result and 'chart_insights' in analysis_result:
                            insights = analysis_result['chart_insights']
                            if chart_info["type"] in insights:
                                with st.expander("📝 차트 인사이트 보기"):
                                    st.markdown(insights[chart_info["type"]])
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # 두 번째 행 (있는 경우)
            if len(df_structure["recommended_charts"]) > charts_per_row:
                cols = st.columns(charts_per_row)
                
                for i, chart_info in enumerate(df_structure["recommended_charts"][charts_per_row:charts_per_row*2]):
                    with cols[i % charts_per_row]:
                        st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
                        st.subheader(chart_info["title"])
                        
                        # 차트 생성
                        if chart_info["type"] == "pie":
                            fig = create_chart(
                                df, "pie", 
                                names=chart_info["names"], 
                                values=chart_info["values"], 
                                title=chart_info["title"]
                            )
                        else:
                            fig = create_chart(
                                df, chart_info["type"], 
                                x=chart_info.get("x"), 
                                y=chart_info.get("y"), 
                                title=chart_info["title"]
                            )
                        
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # 차트 인사이트 (AI 분석 결과가 있는 경우)
                            if analysis_result and 'chart_insights' in analysis_result:
                                insights = analysis_result['chart_insights']
                                if chart_info["type"] in insights:
                                    with st.expander("📝 차트 인사이트 보기"):
                                        st.markdown(insights[chart_info["type"]])
                        
                        st.markdown("</div>", unsafe_allow_html=True)
        
        # 상관관계 히트맵 (수치형 열이 2개 이상인 경우)
        if len(df_structure["correlation_candidates"]) >= 2:
            st.markdown(f"<h2 class='section-title'>📊 변수 간 상관관계</h2>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='chart-container'>", unsafe_allow_html=True)
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            corr = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.columns,
                colorscale='Blues',
                zmin=-1, zmax=1,
                text=corr.round(2).values,
                hovertemplate='%{y} - %{x}: %{z:.2f}<extra></extra>',
                texttemplate='%{text:.2f}'
            ))
            
            fig.update_layout(
                title='변수 간 상관관계 히트맵',
                height=500,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=16, color='#333', family="Arial, sans-serif"),
                font=dict(family="Arial, sans-serif"),
                margin=dict(l=40, r=40, t=60, b=40),
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 상관관계 인사이트 (AI 분석 결과가 있는 경우)
            if analysis_result and 'chart_insights' in analysis_result and 'heatmap' in analysis_result['chart_insights']:
                with st.expander("📝 상관관계 인사이트 보기"):
                    st.markdown(analysis_result['chart_insights']['heatmap'])
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 추천 사항 섹션
        if analysis_result and 'recommendations' in analysis_result:
            st.markdown(f"<h2 class='section-title'>💡 추천 사항</h2>", unsafe_allow_html=True)
            
            st.markdown('<div class="card">', unsafe_allow_html=True)
            
            recommendations = analysis_result['recommendations']
            for i, rec in enumerate(recommendations):
                st.markdown(f"""
                <div style="margin-bottom: 15px;">
                    <strong style="color: {primary_color};">추천 {i+1}:</strong> {rec}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 심층 분석 탭
    with tabs[1]:
        st.markdown(f"<h2 class='section-title'>🔍 심층 데이터 분석</h2>", unsafe_allow_html=True)
        
        # 표준 통계 분석
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 기술 통계량")
        
       # 수치형 열 선택
        if df_structure["numeric_cols"]:
            num_stats = df[df_structure["numeric_cols"]].describe().transpose()
            
            # 추가 통계 계산
            num_stats['median'] = df[df_structure["numeric_cols"]].median()
            num_stats['skewness'] = df[df_structure["numeric_cols"]].skew()
            num_stats['kurtosis'] = df[df_structure["numeric_cols"]].kurtosis()
            num_stats['missing'] = df[df_structure["numeric_cols"]].isna().sum()
            num_stats['missing_pct'] = df[df_structure["numeric_cols"]].isna().sum() / len(df) * 100
            
            # 소수점 지정
            st.dataframe(num_stats.style.format("{:.2f}"))
        else:
            st.info("수치형 데이터가 발견되지 않았습니다.")
        
        # 범주형 데이터 분석
        if df_structure["categorical_cols"]:
            st.subheader("📊 범주형 변수 분석")
            
            col1, col2 = st.columns(2)
            
            for i, col in enumerate(df_structure["categorical_cols"]):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"**{col}의 빈도 분석**")
                    value_counts = df[col].value_counts().reset_index()
                    value_counts.columns = [col, '빈도']
                    value_counts['비율 (%)'] = value_counts['빈도'] / value_counts['빈도'].sum() * 100
                    
                    # 상위 10개만 표시
                    if len(value_counts) > 10:
                        st.info(f"상위 10개 결과만 표시합니다 (총 {len(value_counts)}개 중)")
                        value_counts = value_counts.head(10)
                    
                    st.dataframe(value_counts.style.format({'비율 (%)': "{:.2f}"}))
                    
                    # 차트 표시
                    fig = px.bar(
                        value_counts.head(10), 
                        x=col, y='빈도',
                        color='빈도',
                        color_continuous_scale=chart_colors,
                        title=f"{col} 빈도 분포"
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 시계열 분석 (날짜 열이 있는 경우)
        if df_structure["datetime_cols"]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("📅 시계열 분석")
            
            date_col = st.selectbox("날짜 열 선택", df_structure["datetime_cols"])
            metric_col = st.selectbox("측정값 선택", df_structure["numeric_cols"])
            
            # 날짜 형식으로 변환
            try:
                df['temp_date'] = pd.to_datetime(df[date_col])
                
                # 시간 단위 선택
                time_unit = st.radio("시간 단위", ["일", "주", "월", "년"], horizontal=True)
                
                # 선택한 시간 단위로 그룹화
                if time_unit == "일":
                    grouped = df.groupby(df['temp_date'].dt.date)[metric_col].mean().reset_index()
                    x_title = "일자"
                elif time_unit == "주":
                    grouped = df.groupby(df['temp_date'].dt.isocalendar().week)[metric_col].mean().reset_index()
                    x_title = "주차"
                elif time_unit == "월":
                    grouped = df.groupby(df['temp_date'].dt.month)[metric_col].mean().reset_index()
                    x_title = "월"
                else:  # 년
                    grouped = df.groupby(df['temp_date'].dt.year)[metric_col].mean().reset_index()
                    x_title = "년도"
                
                # 시계열 차트
                fig = px.line(
                    grouped, 
                    x='temp_date', y=metric_col,
                    markers=True,
                    title=f"{date_col} 기준 {metric_col} 추세",
                    labels={'temp_date': x_title, metric_col: metric_col}
                )
                fig.update_traces(line_color=primary_color)
                st.plotly_chart(fig, use_container_width=True)
                
                # 이동 평균 추가
                if len(grouped) > 5:
                    st.subheader("추세 분석 (이동 평균)")
                    window_size = st.slider("이동 평균 기간", min_value=2, max_value=min(10, len(grouped)-1), value=3)
                    
                    grouped['이동평균'] = grouped[metric_col].rolling(window=window_size).mean()
                    
                    fig = px.line(
                        grouped, 
                        x='temp_date', 
                        y=[metric_col, '이동평균'],
                        title=f"{date_col} 기준 {metric_col} 추세 및 {window_size}기간 이동평균",
                        labels={'temp_date': x_title, 'value': metric_col}
                    )
                    fig.update_layout(legend_title_text='')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 성장률 계산
                    if len(grouped) > 1:
                        grouped['성장률'] = grouped[metric_col].pct_change() * 100
                        
                        fig = px.bar(
                            grouped.dropna(), 
                            x='temp_date', y='성장률',
                            title=f"{date_col} 기준 {metric_col} 성장률 (%)",
                            labels={'temp_date': x_title, '성장률': '성장률 (%)'}
                        )
                        fig.update_traces(marker_color=primary_color)
                        st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"시계열 분석 중 오류가 발생했습니다: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # 이상치 분석
        if df_structure["numeric_cols"]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🔍 이상치 탐지")
            
            col_for_outlier = st.selectbox("이상치 분석할 열 선택", df_structure["numeric_cols"])
            
            # 박스플롯
            fig = px.box(df, y=col_for_outlier, title=f"{col_for_outlier} 박스플롯")
            fig.update_traces(marker_color=primary_color)
            st.plotly_chart(fig, use_container_width=True)
            
            # IQR 방식으로 이상치 계산
            Q1 = df[col_for_outlier].quantile(0.25)
            Q3 = df[col_for_outlier].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col_for_outlier] < lower_bound) | (df[col_for_outlier] > upper_bound)]
            
            st.markdown(f"""
            **이상치 범위 기준**:
            - 1사분위수(Q1): {Q1:.2f}
            - 3사분위수(Q3): {Q3:.2f}
            - IQR(Q3-Q1): {IQR:.2f}
            - 하한 경계값: {lower_bound:.2f}
            - 상한 경계값: {upper_bound:.2f}
            - 발견된 이상치 수: {len(outliers)} (전체 데이터의 {len(outliers)/len(df)*100:.2f}%)
            """)
            
            if not outliers.empty:
                with st.expander("이상치 데이터 보기"):
                    st.dataframe(outliers)
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # 시각화 도구 탭
    with tabs[2]:
        st.markdown(f"<h2 class='section-title'>📈 맞춤형 시각화 도구</h2>", unsafe_allow_html=True)
        
        # 시각화 종류 선택
        chart_types = {
            "bar": "막대 차트",
            "line": "선 그래프",
            "scatter": "산점도",
            "histogram": "히스토그램",
            "pie": "파이 차트",
            "heatmap": "히트맵"
        }
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        selected_chart = st.selectbox("차트 종류 선택", list(chart_types.values()))
        
        # 선택된 차트 유형에 따라 필요한 입력 요청
        chart_type_key = list(chart_types.keys())[list(chart_types.values()).index(selected_chart)]
        
        if chart_type_key == "bar":
            x_col = st.selectbox("X축 (범주형)", df.columns)
            y_col = st.selectbox("Y축 (수치형)", df_structure["numeric_cols"] if df_structure["numeric_cols"] else df.columns)
            
            # 추가 옵션
            col1, col2 = st.columns(2)
            with col1:
                bar_mode = st.radio("차트 모드", ["수직 막대", "수평 막대"], horizontal=True)
            with col2:
                sort_values = st.checkbox("값으로 정렬", value=True)
            
            if bar_mode == "수직 막대":
                if sort_values:
                    # 값으로 정렬
                    temp_df = df.groupby(x_col)[y_col].mean().reset_index()
                    temp_df = temp_df.sort_values(y_col, ascending=False)
                    fig = px.bar(temp_df, x=x_col, y=y_col, title=f"{x_col} 별 {y_col}")
                else:
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col} 별 {y_col}")
            else:
                if sort_values:
                    # 값으로 정렬
                    temp_df = df.groupby(x_col)[y_col].mean().reset_index()
                    temp_df = temp_df.sort_values(y_col, ascending=True)
                    fig = px.bar(temp_df, y=x_col, x=y_col, title=f"{x_col} 별 {y_col}", orientation='h')
                else:
                    fig = px.bar(df, y=x_col, x=y_col, title=f"{x_col} 별 {y_col}", orientation='h')
            
            fig.update_traces(marker_color=primary_color)
        
        elif chart_type_key == "line":
            x_col = st.selectbox("X축", df.columns)
            y_col = st.selectbox("Y축", df_structure["numeric_cols"] if df_structure["numeric_cols"] else df.columns)
            
            # 날짜 열인 경우 날짜로 변환
            if x_col in df_structure["datetime_cols"]:
                temp_df = df.copy()
                temp_df['temp_date'] = pd.to_datetime(temp_df[x_col])
                fig = px.line(temp_df.sort_values('temp_date'), x='temp_date', y=y_col, markers=True, title=f"{x_col} vs {y_col}")
            else:
                fig = px.line(df, x=x_col, y=y_col, markers=True, title=f"{x_col} vs {y_col}")
            
            fig.update_traces(line_color=primary_color)
        
        elif chart_type_key == "scatter":
            x_col = st.selectbox("X축", df_structure["numeric_cols"] if df_structure["numeric_cols"] else df.columns)
            y_col = st.selectbox("Y축", [col for col in df_structure["numeric_cols"] if col != x_col] if len(df_structure["numeric_cols"]) > 1 else df_structure["numeric_cols"])
            
            # 추가 옵션
            color_col = st.selectbox("색상 구분 (선택사항)", ["없음"] + list(df.columns))
            
            if color_col != "없음":
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{x_col} vs {y_col}")
            else:
                fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
                fig.update_traces(marker_color=primary_color)
            
            # 추세선 추가 옵션
            add_trendline = st.checkbox("추세선 추가")
            if add_trendline:
                fig.update_layout(
                    shapes=[
                        dict(
                            type='line',
                            yref='paper', y0=0, y1=1,
                            xref='paper', x0=0, x1=1,
                            line=dict(color=secondary_color, width=2, dash='dash')
                        )
                    ]
                )
                
                # 선형 회귀선 추가
                x = df[x_col].values
                y = df[y_col].values
                mask = ~np.isnan(x) & ~np.isnan(y)
                if np.sum(mask) > 1:  # 최소 2개 이상의 유효한 점이 필요
                    x = x[mask]
                    y = y[mask]
                    slope, intercept = np.polyfit(x, y, 1)
                    fig.add_trace(go.Scatter(
                        x=df[x_col],
                        y=slope * df[x_col] + intercept,
                        mode='lines',
                        name=f'추세선 (y = {slope:.2f}x + {intercept:.2f})',
                        line=dict(color=secondary_color, width=2, dash='dash')
                    ))
        
        elif chart_type_key == "histogram":
            x_col = st.selectbox("값", df_structure["numeric_cols"] if df_structure["numeric_cols"] else df.columns)
            
            # 추가 옵션
            col1, col2 = st.columns(2)
            with col1:
                bins = st.slider("구간 수", min_value=5, max_value=50, value=20)
            with col2:
                kde = st.checkbox("밀도 커브 추가", value=True)
            
            fig = px.histogram(df, x=x_col, nbins=bins, title=f"{x_col} 분포")
            fig.update_traces(marker_color=primary_color)
            
            if kde:
                # KDE 추가 (밀도 커브)
                kde_vals = df[x_col].dropna()
                if len(kde_vals) > 1:
                    hist_vals, bin_edges = np.histogram(kde_vals, bins=bins, density=True)
                    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
                    
                    from scipy.stats import gaussian_kde
                    kde = gaussian_kde(kde_vals)
                    
                    x_kde = np.linspace(min(kde_vals), max(kde_vals), 1000)
                    y_kde = kde(x_kde)
                    
                    # 밀도 곡선 추가
                    fig.add_trace(go.Scatter(
                        x=x_kde,
                        y=y_kde,
                        mode='lines',
                        name='밀도 커브',
                        line=dict(color=secondary_color, width=2)
                    ))
        
        elif chart_type_key == "pie":
            names_col = st.selectbox("라벨 (범주형)", df_structure["categorical_cols"] if df_structure["categorical_cols"] else df.columns)
            values_col = st.selectbox("값 (수치형)", df_structure["numeric_cols"] if df_structure["numeric_cols"] else df.columns)
            
            # 추가 옵션
            col1, col2 = st.columns(2)
            with col1:
                max_categories = st.slider("최대 카테고리 수", min_value=3, max_value=15, value=8)
            with col2:
                show_values = st.radio("표시 값", ["비율", "값"], horizontal=True)
            
            # 데이터 집계
            pie_data = df.groupby(names_col)[values_col].sum().reset_index()
            
            # 카테고리 제한
            if len(pie_data) > max_categories:
                top_categories = pie_data.nlargest(max_categories-1, values_col)
                other_sum = pie_data.nsmallest(len(pie_data) - (max_categories-1), values_col)[values_col].sum()
                other_row = pd.DataFrame({names_col: ['기타'], values_col: [other_sum]})
                pie_data = pd.concat([top_categories, other_row])
            
            if show_values == "비율":
                fig = px.pie(pie_data, names=names_col, values=values_col, title=f"{names_col} 구성 비율", 
                        hover_data=[values_col], labels={values_col: values_col})
            else:
                fig = px.pie(pie_data, names=names_col, values=values_col, title=f"{names_col} 구성 비율", 
                        hover_data=[values_col], labels={values_col: values_col})
                fig.update_traces(textinfo='value+label')
        
        elif chart_type_key == "heatmap":
            # 상관관계 히트맵
            if len(df_structure["numeric_cols"]) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    selected_columns = st.multiselect(
                        "열 선택 (수치형)", 
                        df_structure["numeric_cols"],
                        default=df_structure["numeric_cols"][:min(5, len(df_structure["numeric_cols"]))]
                    )
                with col2:
                    color_scale = st.selectbox(
                        "색상 스케일", 
                        ["Blues", "Reds", "Greens", "Purples", "Oranges"]
                    )
                
                if selected_columns:
                    corr = df[selected_columns].corr()
                    
                    fig = go.Figure(data=go.Heatmap(
                        z=corr.values,
                        x=corr.columns,
                        y=corr.columns,
                        colorscale=color_scale,
                        zmin=-1, zmax=1,
                        text=corr.round(2).values,
                        hovertemplate='%{y} - %{x}: %{z:.2f}<extra></extra>',
                        texttemplate='%{text:.2f}'
                    ))
                    
                    fig.update_layout(
                        title='변수 간 상관관계 히트맵',
                        height=500
                    )
                else:
                    st.warning("분석할 열을 선택해주세요.")
                    fig = None
            else:
                st.warning("히트맵을 생성하기 위해서는 최소 2개 이상의 수치형 열이 필요합니다.")
                fig = None
        
        # 차트 표시
        if fig:
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font=dict(size=16, color='#333', family="Arial, sans-serif"),
                font=dict(family="Arial, sans-serif"),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 차트 다운로드 버튼
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("💡 **TIP**: 차트 위에서 마우스 우클릭하면 이미지로 저장할 수 있습니다.")
            with col2:
                st.download_button(
                    label="데이터 CSV 다운로드",
                    data=df.to_csv(index=False),
                    file_name="chart_data.csv",
                    mime="text/csv",
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 측정 지표 계산기
        st.markdown(f"<h2 class='section-title'>🧮 측정 지표 계산기</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        metric_type = st.selectbox(
            "계산할 측정 지표 선택", 
            ["기본 통계", "상관관계 분석", "시계열 분석", "범주형 변수 분석"]
        )
        
        if metric_type == "기본 통계":
            col1, col2 = st.columns(2)
            
            with col1:
                metric_col = st.selectbox("분석할 열 선택", df_structure["numeric_cols"] if df_structure["numeric_cols"] else df.columns)
            
            with col2:
                filter_col = st.selectbox("필터 열 (선택사항)", ["없음"] + list(df.columns))
            
            if filter_col != "없음":
                filter_values = st.multiselect(
                    "필터 값 선택", 
                    df[filter_col].unique(),
                    default=df[filter_col].unique()[0] if len(df[filter_col].unique()) > 0 else None
                )
                
                if filter_values:
                    filtered_df = df[df[filter_col].isin(filter_values)]
                    if len(filtered_df) > 0:
                        st.markdown(f"**'{filter_col}' = {', '.join([str(v) for v in filter_values])}인 경우의 '{metric_col}' 통계**")
                        stats = filtered_df[metric_col].describe()
                    else:
                        st.warning("선택한 필터 조건에 맞는 데이터가 없습니다.")
                        stats = None
                else:
                    st.warning("필터 값을 선택해주세요.")
                    stats = None
            else:
                filtered_df = df
                stats = df[metric_col].describe()
            
            if stats is not None:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("평균", f"{stats['mean']:.2f}")
                    st.metric("표준편차", f"{stats['std']:.2f}")
                    st.metric("최소값", f"{stats['min']:.2f}")
                
                with col2:
                    st.metric("중앙값", f"{stats['50%']:.2f}")
                    st.metric("최대값", f"{stats['max']:.2f}")
                    st.metric("데이터 수", f"{stats['count']:.0f}")
                
                # 히스토그램 표시
                fig = px.histogram(
                    filtered_df, 
                    x=metric_col,
                    title=f"{metric_col} 분포",
                    nbins=20,
                    histnorm='probability density'
                )
                fig.add_vline(
                    x=stats['mean'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text="평균"
                )
                fig.add_vline(
                    x=stats['50%'],
                    line_dash="dash",
                    line_color="green",
                    annotation_text="중앙값"
                )
                fig.update_layout(height=300)
                fig.update_traces(marker_color=primary_color)
                
                st.plotly_chart(fig, use_container_width=True)
        
        elif metric_type == "상관관계 분석":
            if len(df_structure["numeric_cols"]) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X축 변수", df_structure["numeric_cols"])
                
                with col2:
                    y_col = st.selectbox(
                        "Y축 변수", 
                        [col for col in df_structure["numeric_cols"] if col != x_col]
                    )
                
                # 상관계수 계산
                pearson_corr = df[[x_col, y_col]].corr().iloc[0, 1]
                
                # 상관관계 강도 해석
                if abs(pearson_corr) < 0.3:
                    corr_strength = "약한"
                    corr_color = "#ffc107"  # 노란색
                elif abs(pearson_corr) < 0.7:
                    corr_strength = "중간 정도의"
                    corr_color = "#fd7e14"  # 주황색
                else:
                    corr_strength = "강한"
                    corr_color = "#dc3545"  # 빨간색
                
                # 상관관계 방향
                if pearson_corr > 0:
                    corr_direction = "양의"
                else:
                    corr_direction = "음의"
                
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h3 style="margin-bottom: 10px;">상관계수 (Pearson)</h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: {corr_color};">{pearson_corr:.4f}</div>
                    <p>{x_col}와(과) {y_col} 사이에는 <span style="color: {corr_color}; font-weight: bold;">{corr_strength} {corr_direction}</span> 상관관계가 있습니다.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 산점도 및 추세선
                fig = px.scatter(
                    df, 
                    x=x_col, 
                    y=y_col,
                    trendline="ols",
                    title=f"{x_col} vs {y_col} 산점도와 추세선"
                )
                fig.update_layout(height=400)
                fig.update_traces(marker=dict(color=primary_color), selector=dict(mode='markers'))
                fig.update_traces(line=dict(color=secondary_color), selector=dict(mode='lines'))
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 회귀식 계산
                import statsmodels.api as sm
                
                # 결측치 제거
                valid_data = df[[x_col, y_col]].dropna()
                
                if len(valid_data) > 1:  # 최소 2개 이상의 유효한 점이 필요
                    X = valid_data[x_col]
                    X = sm.add_constant(X)  # 상수항 추가
                    model = sm.OLS(valid_data[y_col], X).fit()
                    
                    st.markdown(f"""
                    **회귀 모델 정보**:
                    - 회귀식: {y_col} = {model.params[1]:.4f} × {x_col} + {model.params[0]:.4f}
                    - R² (결정계수): {model.rsquared:.4f}
                    - p-값: {model.pvalues[1]:.4f}
                    
                    **해석**:
                    - {x_col}가 1단위 증가할 때마다 {y_col}는 평균적으로 {model.params[1]:.4f}만큼 변화합니다.
                    - 이 모델은 {y_col} 변동의 {model.rsquared*100:.1f}%를 설명합니다.
                    - p-값이 0.05 미만이면 통계적으로 유의미한 관계입니다 {'(유의미함)' if model.pvalues[1] < 0.05 else '(유의미하지 않음)'}.
                    """)
            else:
                st.warning("상관관계 분석을 위해서는 최소 2개 이상의 수치형 변수가 필요합니다.")
        
        elif metric_type == "시계열 분석":
            if df_structure["datetime_cols"]:
col1, col2 = st.columns(2)
                
                with col1:
                    date_col = st.selectbox("날짜 열", df_structure["datetime_cols"])
                
                with col2:
                    value_col = st.selectbox("값 열", df_structure["numeric_cols"])
                
                # 날짜 변환
                try:
                    temp_df = df.copy()
                    temp_df['temp_date'] = pd.to_datetime(temp_df[date_col])
                    
                    # 시간 단위 선택
                    time_unit = st.radio("시간 단위", ["일", "주", "월", "년"], horizontal=True)
                    
                    # 선택한 시간 단위로 그룹화
                    if time_unit == "일":
                        grouped = temp_df.groupby(temp_df['temp_date'].dt.date)[value_col].mean().reset_index()
                        x_title = "일자"
                    elif time_unit == "주":
                        grouped = temp_df.groupby(temp_df['temp_date'].dt.isocalendar().week)[value_col].mean().reset_index()
                        x_title = "주차"
                    elif time_unit == "월":
                        grouped = temp_df.groupby(temp_df['temp_date'].dt.month)[value_col].mean().reset_index()
                        x_title = "월"
                    else:  # 년
                        grouped = temp_df.groupby(temp_df['temp_date'].dt.year)[value_col].mean().reset_index()
                        x_title = "년도"
                    
                    # 시계열 차트
                    fig = px.line(
                        grouped, 
                        x='temp_date', y=value_col,
                        markers=True,
                        title=f"{date_col} 기준 {value_col} 추세",
                        labels={'temp_date': x_title, value_col: value_col}
                    )
                    fig.update_traces(line_color=primary_color)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 기본 통계
                    st.markdown(f"""
                    **시계열 데이터 기본 통계**:
                    - 평균: {grouped[value_col].mean():.2f}
                    - 최소값: {grouped[value_col].min():.2f}
                    - 최대값: {grouped[value_col].max():.2f}
                    - 변동 범위: {grouped[value_col].max() - grouped[value_col].min():.2f}
                    """)
                    
                    # 추세 및 계절성 분석 섹션
                    st.subheader("추세 분석")
                    
                    if len(grouped) > 2:
                        # 단순 추세선 (선형 회귀)
                        x = np.arange(len(grouped))
                        y = grouped[value_col].values
                        slope, intercept = np.polyfit(x, y, 1)
                        
                        trend_direction = "증가" if slope > 0 else "감소"
                        
                        st.markdown(f"""
                        **선형 추세 분석**:
                        - 추세 방향: {trend_direction}
                        - 기울기: {slope:.4f} / 기간
                        - 해석: 각 {time_unit}마다 평균적으로 {abs(slope):.4f}씩 {trend_direction}하는 추세를 보입니다.
                        """)
                        
                        # 추세선이 있는 차트
                        grouped['추세선'] = intercept + slope * x
                        
                        fig = px.line(
                            grouped, 
                            x='temp_date', 
                            y=[value_col, '추세선'],
                            title=f"{date_col} 기준 {value_col} 추세 및 선형 추세선",
                            labels={'temp_date': x_title, 'value': value_col}
                        )
                        fig.update_layout(legend_title_text='')
                        st.plotly_chart(fig, use_container_width=True)
                
                except Exception as e:
                    st.error(f"시계열 분석 중 오류가 발생했습니다: {str(e)}")
            else:
                st.warning("시계열 분석을 위해서는 날짜 형식의 열이 필요합니다.")
        
        elif metric_type == "범주형 변수 분석":
            if df_structure["categorical_cols"]:
                col1, col2 = st.columns(2)
                
                with col1:
                    cat_col = st.selectbox("범주형 변수", df_structure["categorical_cols"])
                
                with col2:
                    if df_structure["numeric_cols"]:
                        num_col = st.selectbox("수치형 변수 (선택사항)", ["없음"] + df_structure["numeric_cols"])
                    else:
                        num_col = "없음"
                        st.info("수치형 변수가 없습니다.")
                
                # 범주별 빈도 분석
                value_counts = df[cat_col].value_counts().reset_index()
                value_counts.columns = [cat_col, '빈도']
                value_counts['비율 (%)'] = value_counts['빈도'] / value_counts['빈도'].sum() * 100
                
                # 상위 10개만 표시
                show_top = st.slider("표시할 범주 수", min_value=5, max_value=min(20, len(value_counts)), value=min(10, len(value_counts)))
                
                if len(value_counts) > show_top:
                    st.warning(f"상위 {show_top}개 결과만 표시합니다 (총 {len(value_counts)}개 중)")
                    display_counts = value_counts.head(show_top)
                else:
                    display_counts = value_counts
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 파이 차트
                    fig = px.pie(
                        display_counts, 
                        names=cat_col, 
                        values='빈도',
                        title=f"{cat_col} 범주별 구성 비율"
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # 데이터 테이블
                    st.dataframe(display_counts.style.format({'비율 (%)': "{:.2f}"}), height=400)
                
                # 범주형 + 수치형 분석 (수치형 변수가 선택된 경우)
                if num_col != "없음":
                    st.subheader(f"{cat_col} 범주별 {num_col} 분석")
                    
                    # 범주별 기술 통계량
                    group_stats = df.groupby(cat_col)[num_col].agg(['mean', 'median', 'std', 'min', 'max', 'count']).reset_index()
                    
                    # 정렬 방식
                    sort_by = st.radio("정렬 기준", ["범주명", "평균값"], horizontal=True)
                    
                    if sort_by == "범주명":
                        group_stats = group_stats.sort_values(cat_col)
                    else:
                        group_stats = group_stats.sort_values('mean', ascending=False)
                    
                    st.dataframe(group_stats.style.format({
                        'mean': "{:.2f}",
                        'median': "{:.2f}",
                        'std': "{:.2f}",
                        'min': "{:.2f}",
                        'max': "{:.2f}",
                        'count': "{:.0f}"
                    }))
                    
                    # 막대 차트
                    fig = px.bar(
                        group_stats,
                        x=cat_col,
                        y='mean',
                        error_y='std',
                        labels={cat_col: cat_col, 'mean': f'{num_col} 평균'},
                        title=f"{cat_col} 범주별 {num_col} 평균 (± 표준편차)"
                    )
                    fig.update_traces(marker_color=primary_color)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # ANOVA 분석 (범주가 3개 이상인 경우)
                    if len(group_stats) >= 3:
                        st.subheader("ANOVA 분석 (범주 간 평균 차이 검정)")
                        
                        from scipy import stats
                        
                        # 각 그룹의 데이터 추출
                        groups = []
                        group_names = []
                        
                        for category in group_stats[cat_col]:
                            group_data = df[df[cat_col] == category][num_col].dropna()
                            if len(group_data) > 0:
                                groups.append(group_data)
                                group_names.append(category)
                        
                        if len(groups) >= 2:
                            # ANOVA 실행
                            f_stat, p_value = stats.f_oneway(*groups)
                            
                            st.markdown(f"""
                            **ANOVA 결과**:
                            - F-통계량: {f_stat:.4f}
                            - p-값: {p_value:.4f}
                            - 결론: {cat_col} 범주 간 {num_col}의 평균은 {'통계적으로 유의하게 다릅니다' if p_value < 0.05 else '통계적으로 유의한 차이가 없습니다'} (유의수준 0.05 기준).
                            """)
                            
                            # 상자 그림 (Box Plot)
                            fig = px.box(
                                df,
                                x=cat_col,
                                y=num_col,
                                title=f"{cat_col} 범주별 {num_col} 분포"
                            )
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("범주형 변수 분석을 위해서는 범주형(문자열) 변수가 필요합니다.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 데이터 탐색 탭
    with tabs[3]:
        st.markdown(f"<h2 class='section-title'>📋 데이터 탐색</h2>", unsafe_allow_html=True)
        
        # 데이터 미리보기
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 데이터 미리보기")
        
        # 표시 행 수 선택
        rows_to_show = st.slider("표시할 행 수", min_value=5, max_value=100, value=10)
        
        # 열 선택
        all_columns = list(df.columns)
        selected_columns = st.multiselect("표시할 열 선택", all_columns, default=all_columns)
        
        if selected_columns:
            st.dataframe(df[selected_columns].head(rows_to_show), height=400)
        else:
            st.dataframe(df.head(rows_to_show), height=400)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 데이터 필터링
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔍 데이터 필터링")
        
        # 필터 추가 기능
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_col = st.selectbox("필터 열", all_columns)
        
        # 선택된 열의 데이터 타입에 따라 다른 필터 옵션 제공
        if filter_col in df_structure["numeric_cols"]:
            with col2:
                filter_type = st.selectbox("필터 유형", ["범위", "이상", "이하", "같음"], key="filter_type_num")
            
            with col3:
                if filter_type == "범위":
                    min_val = df[filter_col].min()
                    max_val = df[filter_col].max()
                    filter_range = st.slider(
                        "값 범위", 
                        min_value=float(min_val), 
                        max_value=float(max_val), 
                        value=(float(min_val), float(max_val))
                    )
                    filtered_df = df[(df[filter_col] >= filter_range[0]) & (df[filter_col] <= filter_range[1])]
                
                elif filter_type == "이상":
                    min_val = df[filter_col].min()
                    max_val = df[filter_col].max()
                    filter_value = st.slider(
                        "최소값", 
                        min_value=float(min_val), 
                        max_value=float(max_val), 
                        value=float(min_val)
                    )
                    filtered_df = df[df[filter_col] >= filter_value]
                
                elif filter_type == "이하":
                    min_val = df[filter_col].min()
                    max_val = df[filter_col].max()
                    filter_value = st.slider(
                        "최대값", 
                        min_value=float(min_val), 
                        max_value=float(max_val), 
                        value=float(max_val)
                    )
                    filtered_df = df[df[filter_col] <= filter_value]
                
                else:  # 같음
                    unique_values = df[filter_col].unique()
                    if len(unique_values) > 30:
                        filter_value = st.number_input("값", value=unique_values[0])
                        filtered_df = df[df[filter_col] == filter_value]
                    else:
                        filter_value = st.selectbox("값", unique_values)
                        filtered_df = df[df[filter_col] == filter_value]
        
        else:  # 범주형 변수
            with col2:
                filter_type = st.selectbox("필터 유형", ["포함", "제외", "같음"], key="filter_type_cat")
            
            with col3:
                unique_values = df[filter_col].unique()
                
                if filter_type == "같음":
                    filter_value = st.selectbox("값", unique_values)
                    filtered_df = df[df[filter_col] == filter_value]
                
                elif filter_type == "포함":
                    filter_values = st.multiselect("값", unique_values, default=unique_values[0] if len(unique_values) > 0 else None)
                    if filter_values:
                        filtered_df = df[df[filter_col].isin(filter_values)]
                    else:
                        filtered_df = df
                
                else:  # 제외
                    filter_values = st.multiselect("제외할 값", unique_values)
                    if filter_values:
                        filtered_df = df[~df[filter_col].isin(filter_values)]
                    else:
                        filtered_df = df
        
        # 필터링 결과 표시
        st.markdown(f"**필터링 결과**: {len(filtered_df):,}개 행 (전체의 {len(filtered_df) / len(df) * 100:.1f}%)")
        
        # 필터링된 데이터 표시
        st.dataframe(filtered_df.head(rows_to_show), height=300)
        
        # 필터링된 데이터 다운로드 버튼
        if not filtered_df.empty:
            st.download_button(
                label="필터링된 데이터 다운로드",
                data=filtered_df.to_csv(index=False),
                file_name="filtered_data.csv",
                mime="text/csv",
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 열 정보 탐색
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📝 열 정보 상세 탐색")
        
        col_to_explore = st.selectbox("탐색할 열 선택", all_columns)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**데이터 타입**: {df[col_to_explore].dtype}")
            st.markdown(f"**유니크 값 수**: {df[col_to_explore].nunique():,}")
            st.markdown(f"**결측치 수**: {df[col_to_explore].isna().sum():,} ({df[col_to_explore].isna().sum() / len(df) * 100:.1f}%)")
        
        with col2:
            if df[col_to_explore].dtype in ['int64', 'float64']:
                st.markdown(f"**평균**: {df[col_to_explore].mean():.2f}")
                st.markdown(f"**중앙값**: {df[col_to_explore].median():.2f}")
                st.markdown(f"**최소/최대**: {df[col_to_explore].min():.2f} / {df[col_to_explore].max():.2f}")
            else:
                top_value = df[col_to_explore].value_counts().index[0] if not df[col_to_explore].value_counts().empty else "N/A"
                st.markdown(f"**최빈값**: {top_value}")
                st.markdown(f"**최빈값 빈도**: {df[col_to_explore].value_counts().iloc[0] if not df[col_to_explore].value_counts().empty else 0:,}")
                st.markdown(f"**최빈값 비율**: {df[col_to_explore].value_counts().iloc[0] / len(df) * 100 if not df[col_to_explore].value_counts().empty else 0:.1f}%")
        
        # 열 데이터 시각화
        if df[col_to_explore].dtype in ['int64', 'float64']:
            # 히스토그램 표시
            fig = px.histogram(
                df, 
                x=col_to_explore,
                title=f"{col_to_explore} 분포",
                nbins=30
            )
            fig.update_traces(marker_color=primary_color)
            st.plotly_chart(fig, use_container_width=True)
        else:
            # 상위 15개 값에 대한 바 차트
            value_counts = df[col_to_explore].value_counts().reset_index().head(15)
            if not value_counts.empty:
                value_counts.columns = [col_to_explore, '빈도']
                
                fig = px.bar(
                    value_counts,
                    x=col_to_explore,
                    y='빈도',
                    title=f"{col_to_explore} 상위 값 분포"
                )
                fig.update_traces(marker_color=primary_color)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
else:
    # 시작 화면 (파일 업로드 전)
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 70vh; flex-direction: column; text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/2621/2621303.png" width="100" style="margin-bottom: 20px;">
        <h1 style="font-size: 2rem; margin-bottom: 1rem; background: linear-gradient(90deg, #4e8df5, #2c58a0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            고급 CSV 데이터 분석 도구
        </h1>
        <p style="font-size: 1.2rem; color: #555; max-width: 800px; margin-bottom: 2rem;">
            CSV 파일을 업로드하면 AI가 데이터를 자동으로 분석하고 최적의 시각화와 인사이트를 제공합니다.
            왼쪽 사이드바에 OpenAI API 키를 입력하면 더 풍부한 분석을 받아볼 수 있습니다.
        </p>
        <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-bottom: 2rem;">
            <div style="text-align: center; background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); width: 180px;">
                <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
                <div style="font-weight: bold; margin-bottom: 5px;">자동 시각화</div>
                <div style="font-size: 0.9rem; color: #666;">데이터에 최적화된 차트 자동 생성</div>
            </div>
            <div style="text-align: center; background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); width: 180px;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🤖</div>
                <div style="font-weight: bold; margin-bottom: 5px;">AI 인사이트</div>
                <div style="font-size: 0.9rem; color: #666;">주요 인사이트와 패턴 발견</div>
            </div>
            <div style="text-align: center; background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); width: 180px;">
                <div style="font-size: 2rem; margin-bottom: 10px;">🔍</div>
                <div style="font-weight: bold; margin-bottom: 5px;">심층 분석</div>
                <div style="font-size: 0.9rem; color: #666;">통계 분석 및 데이터 탐색</div>
            </div>
        </div>
        <div style="text-align: center; background-color: #f8f9fa; padding: 15px; border-radius: 10px; max-width: 600px;">
            <p style="font-weight: bold; margin-bottom: 10px;">🚀 시작하기</p>
            <p style="font-size: 0.9rem; color: #666;">
                상단의 "Browse files" 버튼을 클릭하여 CSV 파일을 업로드하세요. 
                최대 200MB 크기의 CSV 파일을 지원합니다.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
