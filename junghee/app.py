import threading
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

import promo_email

# 페이지 설정
st.set_page_config(page_title="🚗 고객 클러스터링 & 맞춤형 프로모션 시스템", layout="wide")


st.markdown(
    """
    <style>
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
                background-color: #ffffff; 
                box-shadow: 2px 2px 10px rgba(0,0,0,0.2); /* 살짝 그림자 효과 */
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

        
    

    menu = ['홈', '개발 과정', '고객정보 입력', 'EDA', 'Predict', 'About']

    with st.sidebar:
        selected = option_menu("메뉴", menu, 
            icons=['house'], menu_icon="cast", default_index=0)
        
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
    # 🟢 백그라운드에서 이메일 스케줄 실행
    scheduler_thread = threading.Thread(target=promo_email.schedule_worker, daemon=True)
    scheduler_thread.start()

    run_app()