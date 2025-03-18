import pandas as pd
import streamlit as st
import plotly.express as px

def run_description():
    st.title('Description')
    df = pd.read_csv('data/고객db_확장본3.csv')
    df2 = pd.read_csv("yeseul/클러스터링고객데이터_4.csv")
    df1 = pd.read_csv('/Users/marurun66/Documents/GitHub/customer_mini/data/고객데이터_가입연월.csv')
    st.subheader('원본 데이터 확인')

    st.dataframe(df.head())
    st.markdown("")
    st.markdown("---")

    st.subheader('같은 차종, 다른 차량구분 🚗')
    col1, col2 = st.columns(2)
    with col1:
        vehicle_types = df.loc[df["구매한 제품 (Purchased Product)"] == "Avante (CN7 N)", ["구매한 제품 (Purchased Product)", "차량구분(vehicle types)"]]
        st.dataframe(vehicle_types.style.hide(axis="index"))
    with col2:
        st.markdown("""<br><br><br><br>
                    샘플 데이터에서는 동일한 제품이라도 차량 구분이 다른 경우가 있었습니다.<br>
                    이를 확인하기 위해 실제로 제품 네이밍을 공유하는 모델들 중 차량 구분이 다를 수 있을지 살펴보았습니다.<br>
                    디자인별, 구동방식(전기차, 하이브리드 등)별로 같은 네이밍 내 여러 바리에이션이 있긴 했으나 차량 구분자체는 구분이 없었습니다.<br>
                    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col4:
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
    with col3:
        st.markdown("""<br><br><br><br><br><br>
                    제품 네이밍을 공유하는 모델들이 존재했지만, 각 모델의 차량 구분에는 큰 차이가 없었기 때문에, 고객 선호차종을 분석할 때는 차량 구분을 중심으로 작업을 진행했습니다.    
                    구매한 제품을 토대로 해당 차량의 최초 모델 출시년월 컬럼을 추가하여
                    향후 고객 구매 트렌드 예측 및 맞춤형 서비스 제공을 위한 기반 자료로 활용하고자 하였습니다.
                    """, unsafe_allow_html=True)
    st.markdown("")

    st.subheader("🌳 구매한 제품 친환경차 모델 반영")
    col11, col12 = st.columns(2)
    with col11:
        # Create the table data
        eco_friendly_table = [
            {"Model": "NEXO (FE)", "Type": "수소 전기차 (FCEV)"},
            {"Model": "Avante (CN7 HEV)", "Type": "하이브리드 (HEV)"},
            {"Model": "Grandeur (GN7 HEV)", "Type": "하이브리드 (HEV)"},
            {"Model": "IONIQ (AE EV)", "Type": "전기차 (EV)"},
            {"Model": "Tucson (NX4 PHEV)", "Type": "플러그인 하이브리드 (PHEV)"},
            {"Model": "IONIQ 6 (CE)", "Type": "전기차 (EV)"},
            {"Model": "Santa-Fe (MX5 PHEV)", "Type": "플러그인 하이브리드 (PHEV)"}
        ]
        eco_friendly_df = pd.DataFrame(eco_friendly_table)
        st.dataframe(eco_friendly_df.style.hide(axis="index"))  # 인덱스 숨기기
    with col12:
        df2['구매한 제품']
        st.dataframe(df2)

    st.markdown("---")   

    st.subheader('고객 세그먼트 수정 🙆')
    col5, col6 = st.columns(2)

    with col5:
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

    with col6:
        # 2. 고객 세그먼트별 거래 금액 분포 시각화
        fig2 = px.box(df, 
                    x="고객 세그먼트 (Customer Segment)", 
                    y="거래 금액 (Transaction Amount)", 
                    title="고객 세그먼트별 거래 금액 분포",
                    labels={"고객 세그먼트 (Customer Segment)": "고객 세그먼트", 
                            "거래 금액 (Transaction Amount)": "거래 금액"},
                    color="고객 세그먼트 (Customer Segment)",  # 고객 세그먼트별 색상 지정
                    color_discrete_sequence=px.colors.qualitative.Set1)  # 색상 팔레트 지정

        fig2.update_layout(
            xaxis_title="고객 세그먼트",
            yaxis_title="거래 금액"
        )

        # Streamlit에서 Plotly 차트 출력
        st.plotly_chart(fig2)

    st.markdown("""
                📌 구매빈도 횟수와 무관해보이는 세그먼트 구분<br>📌 일반, 신규 거래금액과 크게 차이가 없는 이탈가능 세그먼트의 거래금액 분포<br>
                고객 세그먼트 기준을 모르는 개발팀 입장에서는 어떤 기준으로 VIP, 이탈가능으로 분류했는지 모호합니다. <br>
                하지만 클라이언트 측 고객관리팀에서 **VIP, 이탈가능 세그먼트를 선정한 기준이 있을것으로 판단**하고 세그먼트를 유지하였습니다.  
    """, unsafe_allow_html=True)

    col7, col8 = st.columns(2)

    with col7:
        # 가입연도와 고객 세그먼트 관계 시각화

        df1['가입연도'] = df1['가입연도'].astype(int)
        # 그래프 그리기
        fig = px.histogram(df1, 
                            x="가입연도",  # 연도를 x축에 설정
                            color="고객 세그먼트 (Customer Segment)", 
                            title="가입연도와 고객 세그먼트 관계",
                            labels={"가입연도": "가입연도", 
                                    "count": "가입 수", 
                                    "고객 세그먼트 (Customer Segment)": "고객 세그먼트"},
                            barmode="stack")

        fig.update_layout(
            xaxis_title="가입연도",
            yaxis_title="가입 수",
            legend_title="고객 세그먼트",
            xaxis=dict(tickmode='array', tickvals=[2022, 2023, 2024, 2025], ticktext=['2022', '2023', '2024', '2025'])  # x축 값 설정
        )

        # Streamlit에서 Plotly 차트 출력
        st.plotly_chart(fig)

    with col8:
        st.markdown("""
        <br><br><br><br><br><br>
        <span style="color:red;">2022, 2023, 2024년 가입자도 신규로 처리</span>된 경우가 많았습니다.<br>
        클라이언트측에서 업데이트를 처리하지 않은것으로 판단하고,<br>2025년 가입자만 신규 세그먼트로<br>
        그 외 신규세그먼트는 일반으로 변경 하였습니다.
        """, unsafe_allow_html=True)

    col9, col10 = st.columns(2)
    category_order = ['신규', '일반', 'vip', '이탈가능', '총 인원']

    with col9:
        # '고객 세그먼트 (Customer Segment)'의 value_counts 결과를 순서대로 맞추기
        segment_counts1 = df1['고객 세그먼트 (Customer Segment)'].value_counts().reindex(category_order).fillna(0).astype(int)
        # 총 인원 수를 계산하여 '총 인원' 추가
        total_count1 = segment_counts1.sum()
        segment_counts1['총 인원'] = total_count1
        st.write(segment_counts1)
        st.markdown("""
        변경 전 고객 세그먼트 분포  
        """)

    with col10:
        # '고객 세그먼트 (Customer Segment)'의 value_counts 결과를 순서대로 맞추기
        segment_counts2 = df2['고객 세그먼트 (Customer Segment)'].value_counts().reindex(category_order).fillna(0).astype(int)

        # 총 인원 수를 계산하여 '총 인원' 추가
        total_count2 = segment_counts2.sum()
        segment_counts2['총 인원'] = total_count2

        st.write(segment_counts2)
        st.markdown("""
        변경 후 고객 세그먼트 분포  
        """)
