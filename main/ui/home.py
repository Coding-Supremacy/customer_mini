import streamlit as st

def run_home():
    
    

    st.markdown("<h1 style='text-align: center;'>🚗 고객 클러스터링 & 맞춤형 프로모션 시스템</h1>", unsafe_allow_html=True)

    st.divider()

    # 📌 간단한 앱 소개
    st.write("이 앱은 고객 데이터를 분석하여 클러스터링을 수행하고, 맞춤형 프로모션을 제공합니다.")

    

    st.image('../img/home.png', width=1000)

    # 📦 3개의 카드 형태로 주요 기능 소개
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("#### 📊 고객 분석")
        st.info("데이터를 기반으로 고객을 분석하고 인사이트를 제공합니다.")

    with col2:
        st.write("#### 🤖  예측")
        st.success("머신러닝 모델을 활용하여 고객 행동을 예측합니다.")

    with col3:
        st.write("#### ✉️ 프로모션 발송")
        st.warning("분석된 결과를 바탕으로 맞춤형 이메일을 자동 발송합니다.")