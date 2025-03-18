import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 가벼운 모델로 변경하여 빠르게 로딩됨
@st.cache_resource
def load_model():
    model_name = "EleutherAI/polyglot-ko-1.3b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, device_map='auto')
    return tokenizer, model

tokenizer, model = load_model()

# 앱 타이틀
st.title("📊 고객 데이터 클러스터링 분석 AI")

# 데이터 로드 (실제 파일 경로에 맞게 수정)
df = pd.read_csv("hoyeon/클러스터링고객데이터_4.csv")

# 원본 데이터 보기
st.subheader("📌 원본 데이터 미리보기")
st.dataframe(df.head())

# 클러스터링 데이터 요약 (실제 컬럼명 사용)
cluster_summary = df.groupby('고객 세그먼트 (Customer Segment)').agg({
    '연령': 'mean',
    '아이디 (User ID)': 'count'
}).reset_index().rename(columns={
    '연령': '평균 연령',
    '아이디 (User ID)': '고객 수'
})

cluster_summary.rename(columns={'고객 세그먼트 (Customer Segment)': '고객 세그먼트'}, inplace=True)

# 요약 데이터 표시
st.subheader("📈 클러스터링 요약 데이터")
st.dataframe(cluster_summary)

# 클러스터별 고객 수 그래프
fig = px.bar(cluster_summary, x='고객 세그먼트', y='고객 수',
             title='고객 세그먼트별 고객 수', color='고객 세그먼트')
st.plotly_chart(fig, use_container_width=True)

# AI 분석 버튼
if st.button('🤖 AI로 클러스터링 데이터 분석하기'):

    summary_text = ""
    for _, row in cluster_summary.iterrows():
        summary_text += (f"[{row['고객 세그먼트']}] 세그먼트의 평균 연령은 {row['평균 연령']:.1f}세이고, "
                         f"전체 고객 수는 {row['고객 수']}명입니다.\n")

    prompt = f"""
    다음은 고객 데이터를 클러스터링한 결과입니다:

    {summary_text}

    각 고객 세그먼트의 특성을 간략히 분석하고 쉽게 설명해주세요.
    """

    with st.spinner("AI 분석 중입니다..."):
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            inputs,
            max_length=300,
            do_sample=False,
            early_stopping=True
        )
        analysis = tokenizer.decode(outputs[0], skip_special_tokens=True)

    st.subheader("✅ AI 분석 결과")
    st.write(analysis)
