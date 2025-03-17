import streamlit as st
import pandas as pd
import numpy as np


from ui.description import run_description
from ui.home import run_home
from ui.input_new_customer_info2 import run_input_customer_info 



def run_app():
    st.set_page_config(page_title="My Streamlit App", layout="wide")

    menu = ['Home', 'Description', 'EDA', 'New Customer Info']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Home':
        run_home()
    elif choice == 'Description':
        run_description()

    elif choice == 'EDA':
        run_eda()
    elif choice == 'New Customer Info':
        run_input_customer_info()


if __name__ == "__main__":
    run_app()