import streamlit as st
import pandas as pd
import numpy as np
import joblib 



def run_app():

    st.title('미니프로젝트')

    # 모델 로드
    model = joblib.load("model.pkl")

    # 입력 폼 생성
    st.header("데이터 입력")

    # 사용자 입력 받기
    연령대 = st.number_input("연령대 입력", min_value=10, max_value=100, step=1)
    거래금액 = st.number_input("거래 금액 입력", min_value=0, step=1000000)
    구매빈도 = st.number_input("제품 구매 빈도 입력", min_value=0, step=1)
    성별 = st.selectbox("성별 선택", ["남", "여"])
    차량구분 = st.selectbox("차량 구분 선택", ["준중형 세단", "중형 세단", "대형 세단", "SUV", "픽업트럭"])
    거래방식 = st.selectbox("거래 방식 선택", ["카드", "현금", "계좌이체"])
    제품출시년월 = st.text_input("제품 출시 년월 입력 (예: 2023-03)")
    제품구매날짜 = st.text_input("제품 구매 날짜 입력 (예: 2025-03-04)")

    # 입력값을 데이터프레임으로 변환
    if st.button("예측하기"):
        input_data = pd.DataFrame([[연령대, 거래금액, 구매빈도, 성별, 차량구분, 거래방식, 제품출시년월, 제품구매날짜]],
                                columns=["연령대", "거래 금액 (Transaction Amount)", "제품 구매 빈도 (Purchase Frequency)",
                                        "성별 (Gender)", "차량구분(vehicle types)", "거래 방식 (Transaction Method)",
                                        "제품 출시년월 (Launch Date)", "제품 구매 날짜 (Purchase Date)"])
        
        # 예측 실행
        prediction = model.predict(input_data)
        
        # 결과 출력
        st.write(f"예측된 클러스터: {prediction[0]}")

if __name__ == "__main__":
    run_app()