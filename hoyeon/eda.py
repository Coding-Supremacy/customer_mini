import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import shutil

# Hugging Face API 토큰 직접 입력
HF_API_TOKEN = ""  # 여기에 본인의 Hugging Face 토큰 입력

# Gemma 모델 사용
model_name = "google/gemma-2-9b-it"

# 저장 공간 확보 (캐시 정리 및 최소한의 캐시 유지)
def clear_cache():
    cache_dir = os.path.expanduser("~/.cache/huggingface")
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        os.makedirs(cache_dir)

clear_cache()

# GPU 사용 가능 여부 확인
device = "cuda" if torch.cuda.is_available() else "cpu"

# 모델 다운로드 속도 향상 (압축된 형태로 다운로드 & 캐시 활용)
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HF_API_TOKEN, cache_dir="./hf_cache", revision="main")
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HF_API_TOKEN, cache_dir="./hf_cache", device_map="auto", revision="main", )

# 텍스트 생성 파이프라인 설정
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

# Streamlit 앱 구성
st.title("CSV 데이터 분석 및 시각화")

# CSV 파일 직접 사용
csv_file_path = "C:/customer_mini/hoyeon/고객데이터(시구).csv"

# CSV 데이터 로드
df = pd.read_csv(csv_file_path)
st.write("### 데이터 미리보기:")
st.write(df.head())

# 유저가 선택한 컬럼 2개 및 타겟 컬럼 선택
columns = df.columns.tolist()
x_col = st.selectbox("X축 컬럼 선택", columns)
y_col = st.selectbox("Y축 컬럼 선택", columns)
target_col = st.selectbox("타겟 컬럼 선택", columns)

# 그래프 3개 생성
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# 산점도
ax[0].scatter(df[x_col], df[y_col], alpha=0.5)
ax[0].set_title(f"{x_col} vs {y_col} (산점도)")
ax[0].set_xlabel(x_col)
ax[0].set_ylabel(y_col)

# 히스토그램
ax[1].hist(df[target_col], bins=20, alpha=0.7, color='g')
ax[1].set_title(f"{target_col} 분포 (히스토그램)")
ax[1].set_xlabel(target_col)

# 박스플롯
ax[2].boxplot(pd.to_numeric(df[target_col].dropna(), errors='coerce').dropna())
ax[2].set_title(f"{target_col} 분포 (박스플롯)")
ax[2].set_xlabel(target_col)

st.pyplot(fig)

# AI 분석 요청
data_description = df[[x_col, y_col, target_col]].to_string(index=False)

prompt = f"""
아래 데이터의 관계성을 분석하고 설명하세요:
{data_description}

[출력 형식]
- 데이터 분석:
- 관계성 설명:
- 인사이트 및 시사점:
"""

result = pipe(prompt, max_length=1024, temperature=0.7, do_sample=True)
response_text = result[0]['generated_text']

st.write("### AI 분석 결과:")
st.write(response_text)
