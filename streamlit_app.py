python
import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import json

# 페이지 설정
st.set_page_config(
    page_title="CSV 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

# OpenAI API 키 설정
openai_api_key = st.sidebar.text_input("OpenAI API 키", type="password")

# 제목 표시
st.title("📊 CSV 데이터 분석 대시보드")
st.markdown("CSV 파일을 업로드하면 AI가 자동으로 데이터를 분석해줍니다.")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 선택하세요", type="csv")
python
# 함수: OpenAI API를 사용한 데이터 분석
def analyze_data_with_ai(df_info):
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
        
        이 데이터에 대한 분석을 다음 형식의 JSON으로 제공해주세요:
        1. "insights": 데이터에서 발견된 주요 인사이트(최소 3개)
        2. "recommendations": 이 데이터를 바탕으로 한 추천 사항(최소 2개)
        3. "visualizations": 만들면 좋을 시각화 종류와 이유
        
        JSON 형식으로만 응답해주세요.
        """
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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
            return {"insights": ["API 응답을 파싱하는데 문제가 발생했습니다."], "recommendations": [], "visualizations": []}
        
    except Exception as e:
        st.error(f"OpenAI API 호출 중 오류가 발생했습니다: {str(e)}")
        return None
      python
# 데이터가 업로드되면 실행
if uploaded_file is not None:
    # 데이터 로드
    df = pd.read_csv(uploaded_file)
    
    # 데이터 기본 정보
    st.subheader("📋 데이터 미리보기")
    st.dataframe(df.head(10))
    
    # 데이터 기본 정보 수집
    df_info = {
        "columns": list(df.columns),
        "dtypes": str(df.dtypes),
        "describe": str(df.describe()),
        "shape": df.shape
    }
    
    # 기본 통계 정보
    st.subheader("📊 데이터 기본 통계")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"👉 행(Rows): {df.shape[0]}, 열(Columns): {df.shape[1]}")
        st.info(f"👉 결측치(Missing Values): {df.isna().sum().sum()}")
    
    with col2:
        # 수치형 열만 선택
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        if numeric_cols:
            st.info(f"👉 수치형 열(Numeric Columns): {len(numeric_cols)}개")
            # 첫번째 수치형 열의 평균, 최소, 최대값 표시
            col_name = numeric_cols[0]
            st.info(f"👉 {col_name}의 평균: {df[col_name].mean():.2f}, 최소: {df[col_name].min()}, 최대: {df[col_name].max()}")
    
    # AI 분석 실행
    with st.spinner("AI가 데이터를 분석 중입니다..."):
        analysis_result = analyze_data_with_ai(df_info)
    
    # AI 분석 결과 표시
    if analysis_result:
        st.subheader("🤖 AI 분석 인사이트")
        
        # 인사이트 표시
        st.markdown("### 주요 인사이트")
        for i, insight in enumerate(analysis_result.get("insights", [])):
            st.markdown(f"**{i+1}.** {insight}")
        
        # 추천사항 표시
        if analysis_result.get("recommendations"):
            st.markdown("### 추천 사항")
            for i, rec in enumerate(analysis_result.get("recommendations", [])):
                st.markdown(f"**{i+1}.** {rec}")
    
    # 자동 시각화
    st.subheader("📈 데이터 시각화")
    
    # 수치형 열만 선택
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    if len(numeric_cols) >= 1:
        # 히스토그램
        st.markdown("### 히스토그램")
        col_for_hist = st.selectbox("히스토그램을 표시할 열을 선택하세요:", numeric_cols)
        fig = px.histogram(df, x=col_for_hist, title=f"{col_for_hist} 분포")
        st.plotly_chart(fig, use_container_width=True)
        
        # 산점도
        if len(numeric_cols) >= 2:
            st.markdown("### 산점도")
            col_x = st.selectbox("X축 열을 선택하세요:", numeric_cols, key="scatter_x")
            col_y = st.selectbox("Y축 열을 선택하세요:", numeric_cols, key="scatter_y", index=min(1, len(numeric_cols)-1))
            fig = px.scatter(df, x=col_x, y=col_y, title=f"{col_x} vs {col_y}")
            st.plotly_chart(fig, use_container_width=True)
        
        # 상관관계 히트맵
        if len(numeric_cols) >= 2:
            st.markdown("### 상관관계 히트맵")
            corr = df[numeric_cols].corr()
            fig = px.imshow(corr, text_auto=True, title="변수 간 상관관계")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("수치형 데이터가 없어 차트를 표시할 수 없습니다.")
    
    # 다운로드 버튼
    csv = df.to_csv(index=False)
    st.download_button(
        label="분석 데이터 다운로드",
        data=csv,
        file_name="analyzed_data.csv",
        mime="text/csv",
    )
else:
    # 파일이 업로드되지 않았을 때 표시할 내용
    st.info("👆 CSV 파일을 업로드하면 자동으로 분석이 시작됩니다.")
    
    # 예시 이미지 또는 설명
    st.markdown("""
    ### 사용 방법
    1. 왼쪽 사이드바에 OpenAI API 키를 입력하세요
    2. CSV 파일을 업로드하세요
    3. AI가 자동으로 데이터를 분석하고 인사이트를 제공합니다
    4. 다양한 시각화를 통해 데이터를 탐색해보세요
    """)
