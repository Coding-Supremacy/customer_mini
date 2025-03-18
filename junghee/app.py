import streamlit as st
import pandas as pd
import numpy as np
import joblib 
from streamlit_option_menu import option_menu

from ui.home import run_home
from ui.input_new_customer_info2 import run_input_customer_info




def run_app():

    st.title('미니프로젝트')

    menu = ['홈', '고객정보 입력', 'EDA', 'Predict', 'About']

    with st.sidebar:
        selected = option_menu("메뉴", menu, 
            icons=['house'], menu_icon="cast", default_index=1)
        
    if selected == '홈':
        run_home()
       
    if selected == '고객정보 입력':
        run_input_customer_info() 
        
        
        

    
    
    
    st.sidebar.markdown('---')  # 구분선
    st.sidebar.markdown("## 📚 Information")
    st.sidebar.info("이 앱은 고객 데이터를 활용하여 고객 클러스터링을 수행하고, 고객의 세분화된 정보를 제공합니다.")
    st.sidebar.info("왼쪽의 메뉴에서 선택해주세요.")
    

if __name__ == "__main__":
    run_app()