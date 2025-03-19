import streamlit as st
import pandas as pd
import numpy as np
import joblib 
from streamlit_option_menu import option_menu


from home import run_home
from input_new_customer_info import run_input_customer_info
import os

from description import run_description
from eda import run_eda


st.set_page_config(page_title="Dog Info App", layout="wide")
    
st.markdown(
    """
    <style>
    /* 버튼 기본 스타일 */
        div.stButton > button {
            background-color: #FFCC80; /* 파스텔톤 주황 */
            color: #5A3E36; /* 부드러운 갈색 (텍스트) */
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px 24px;
            border: none;
            transition: all 0.3s ease-in-out;
        }

        /* 버튼 마우스 호버 효과 */
        div.stButton > button:hover {
            background-color: #FFB74D; /* 살짝 진한 주황 */
            transform: scale(1.05);
            box-shadow: 0px 4px 10px rgba(255, 179, 71, 0.3);
        }

        /* 버튼 클릭 효과 */
        div.stButton > button:active {
            background-color: #FFA726; /* 더 진한 주황 */
            transform: scale(0.98);
        }
        /* 배경색 설정 */
        .stApp {
            background-color: #ffffff; 
        }
        /* 컨텐츠 정렬 */
        .block-container {
            max-width: 1100px; /* 중앙 정렬을 위한 최대 너비 */
            margin: auto;
            padding: 2rem;
            border-radius: 10px;
            background-color: #F8F9FA; /* 컨텐츠 부분만 흰색 */
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1); /* 살짝 그림자 효과 */
        }

        /* 제목 스타일 */
        h1, h2, h3 {
            color: #343a40; /* 다크 그레이 */
        }
    </style>
    """,
    unsafe_allow_html=True
)
def run_app():

    

    # 📌 CSS 적용하여 좌우 여백 추가 (최대 너비 조정)
    

    menu = ['홈', '개발 과정', '고객정보 입력', 'EDA', 'Predict', 'About']

    with st.sidebar:
        selected = option_menu("메뉴", menu, 
            icons=['house'], menu_icon="cast", default_index=1)
        
    if selected == '홈' :
        run_home()

    if selected == '개발 과정' :
        run_description()
       
    if selected == '고객정보 입력' :
        run_input_customer_info() 
    
    if selected == 'EDA' :
        run_eda()
     
    
        

    
    
    
    st.sidebar.markdown('---')  # 구분선
    st.sidebar.markdown("## 📚 정보")
    st.sidebar.info("이 앱은 고객 데이터를 활용하여 고객 클러스터링을 수행하고, 고객의 세분화된 정보를 제공합니다.")
    st.sidebar.info("왼쪽의 메뉴에서 선택해주세요.")
    

if __name__ == "__main__":
    run_app()