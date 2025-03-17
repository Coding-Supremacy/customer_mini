

import pandas as pd
import streamlit as st
import plotly.express as px

def run_description():
    st.title('Description')

    
    st.subheader('원본 데이터 확인')
    df = pd.read_csv('data/고객db_확장본3.csv')
    st.dataframe(df.head())
    st.write(df.columns)

    st.subheader('이상 데이터 처리 - 같은 차종, 다른 차량구분 🚗')
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
                    해당 샘플 데이터에서는 같은 구매한 제품도 다른 차량구분으로 처리되었습니다.  
                    """)
        vehicle_types = df.loc[df["구매한 제품 (Purchased Product)"] == "G80 (RG3)", ["구매한 제품 (Purchased Product)", "차량구분(vehicle types)"]]
        st.write(vehicle_types)
    with col2:
        st.markdown("""
                    고객 선호차종은 차량구분을 중심으로 작업하되,    
                    구매한 제품을 토대로 해당 차량의 최초 모델 출시년월 컬럼을 추가하였습니다.  
                    향후 고객 구매 트렌드 예측 및 맞춤형 서비스 제공을 위한 기반 자료로 활용할 수 있습니다.  
                    """)
        st.code("""# 모델과 출시 년월 데이터
launch_dates = {
    'G70 (IK)': '2017-09',
    'Santa-Fe ™': '2018-01',
    'NEXO (FE)': '2018-01',
    'Avante (CN7 N)': '2020-05',
    'G80 (RG3)': '2020-03',
    'Grandeur (GN7 HEV)': '2022-01',
    'IONIQ (AE EV)': '2016-01',
    'i30 (PD)': '2017-03',
    'Palisade (LX2)': '2018-12',
    'Tucson (NX4 PHEV)': '2021-05',
    'Avante (CN7 HEV)': '2020-07',
    'IONIQ 6 (CE)': '2022-06',
    'G90 (HI)': '2022-03',
    'Santa-Fe (MX5 PHEV)': '2022-06',
    'G90 (RS4)': '2022-03'
}""")
        

    st.subheader('이상 데이터 처리 - 고객 세그먼트 수정 🙆')
    st.markdown("""
                해당 샘플 데이터에서는 고객 세그먼트 분류가 타당하지 않았습니다.  
                하지만 클라이언트가 **VIP, 이탈가능 세그먼트를 부여한 이유가 있을거라 판단**되어,  
                고민끝에 해당 세그먼트는 유지하고, 신규, 일반 세그먼트 위주로 수정하였습니다.  
                """)
    
    col3, col4 = st.columns(2)

    with col3:
        # 1. 제품 구매 빈도와 고객 세그먼트 관계 시각화
        fig1 = px.histogram(df, 
                        x="제품 구매 빈도 (Purchase Frequency)", 
                        color="고객 세그먼트 (Customer Segment)", 
                        title="구매빈도와 고객 세그먼트 관계",
                        labels={"제품 구매 빈도 (Purchase Frequency)": "구매빈도", 
                                "count": "가입 수", 
                                "고객 세그먼트 (Customer Segment)": "고객 세그먼트"},
                        barmode="stack")

        fig1.update_layout(
            xaxis_title="구매빈도",
            yaxis_title="가입 수",
            legend_title="고객 세그먼트"
        )

        # Streamlit에서 Plotly 차트 출력
        st.plotly_chart(fig1)

    with col4:
        # 2. 고객 세그먼트별 거래 금액 분포 시각화
        fig2 = px.box(df, 
                    x="고객 세그먼트 (Customer Segment)", 
                    y="거래 금액 (Transaction Amount)", 
                    title="고객 세그먼트별 거래 금액 분포",
                    labels={"고객 세그먼트 (Customer Segment)": "고객 세그먼트", 
                            "거래 금액 (Transaction Amount)": "거래 금액"})

        fig2.update_layout(
            xaxis_title="고객 세그먼트",
            yaxis_title="거래 금액"
        )

        # Streamlit에서 Plotly 차트 출력
        st.plotly_chart(fig2)

    # 가입연도와 고객 세그먼트 관계 시각화
    df1= pd.read_csv('클러스터링고객데이터_2.csv')
    fig = px.histogram(df1, 
                    x="가입연도", 
                    color="고객 세그먼트 (Customer Segment)", 
                    title="가입연도와 고객 세그먼트 관계",
                    labels={"가입연도": "가입연도", 
                            "count": "가입 수", 
                            "고객 세그먼트 (Customer Segment)": "고객 세그먼트"},
                    barmode="stack")

    fig.update_layout(
        xaxis_title="가입연도",
        yaxis_title="가입 수",
        legend_title="고객 세그먼트"
    )

    # Streamlit에서 Plotly 차트 출력
    st.plotly_chart(fig)

        