import pandas as pd
import streamlit as st
import plotly.express as px

def run_description():
    
    st.title('데이터 전처리')
    df = pd.read_csv('data/고객db_확장본3.csv')  # 원본 데이터
    df1 = pd.read_csv('data/description1.csv')  # 전처리 데이터
    df2 = pd.read_csv("data/description2.csv")  # 전처리 완료 데이터 = 클러스터링고객데이터_4.csv
    st.subheader('원본 데이터 확인')
    st.dataframe(df.head(),hide_index=True)

    st.markdown("")
    st.markdown("---")

    st.subheader('같은 차종, 다른 차량구분 🚗')
    col1, col2 = st.columns(2)
    with col1:
        vehicle_types = df.loc[df["구매한 제품 (Purchased Product)"] == "Avante (CN7 N)", ["구매한 제품 (Purchased Product)", "차량구분(vehicle types)"]]
        st.dataframe(vehicle_types,hide_index=True)
    with col2:
        st.markdown("""<br><br><br><br>
                    샘플 데이터에서는 동일한 제품이라도 차량 구분이 다른 경우가 있었습니다.<br>
                    이를 확인하기 위해 실제로 제품 네이밍을 공유하는 모델들 중 차량 구분이 다를 수 있을지 살펴보았습니다.<br>
                    디자인별, 구동방식(전기차, 하이브리드 등)별로 같은 네이밍 내 여러 바리에이션이 있긴 했으나 차량 구분자체는 구분이 없었습니다.<br>
                    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
        st.markdown("""<br><br><br><br><br><br>
                    따라서 고객 선호차종을 분석할 때는 차량 구분을 중심으로 작업을 진행했습니다.    
                    그리고 구매한 제품의 최초 모델 출시년월 컬럼을 추가하여
                    향후 고객 구매 트렌드 예측 및 맞춤형 서비스 제공을 위한 기반 자료로 활용하고자 하였습니다.
                    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("---")
    st.subheader("🌳 친환경차 모델 확인")
    col1, col2 = st.columns(2)
    with col1:
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
        st.dataframe(eco_friendly_df,hide_index=True)
    with col2:
        df_ecoproduct = df2[['구매한 제품', '친환경차']]
        st.dataframe(df_ecoproduct,hide_index=True)
    st.markdown("""
구매 모델 중 **FCEV, HEV, EV, PHEV 모델**은 친환경차로 분류하여 **친환경차를 선호하는 고객군**을 파악하고자 하였습니다.
                    """)

    st.markdown("---")   

    st.subheader('고객 세그먼트 수정 🙆')
    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
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

    col1, col2 = st.columns(2)

    with col1:
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

    with col2:
        st.markdown("""
        <br><br><br><br><br><br>
        <span style="color:red;">2022, 2023, 2024년 가입자도 신규로 처리</span>된 경우가 많았습니다.<br>
        클라이언트측에서 업데이트를 처리하지 않은것으로 판단하고,<br>2025년 가입자만 신규 세그먼트로<br>
        그 외 신규세그먼트는 일반으로 변경 하였습니다.
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    category_order = ['신규', '일반', 'vip', '이탈가능', '총 인원']

    with col1:
        # '고객 세그먼트 (Customer Segment)'의 value_counts 결과를 순서대로 맞추기
        segment_counts1 = df1['고객 세그먼트 (Customer Segment)'].value_counts().reindex(category_order).fillna(0).astype(int)
        # 총 인원 수를 계산하여 '총 인원' 추가
        total_count1 = segment_counts1.sum()
        segment_counts1['총 인원'] = total_count1
        st.write(segment_counts1)
        st.markdown("""
        변경 전 고객 세그먼트 분포  
        """)

    with col2:
        # '고객 세그먼트 (Customer Segment)'의 value_counts 결과를 순서대로 맞추기
        segment_counts2 = df2['고객 세그먼트'].value_counts().reindex(category_order).fillna(0).astype(int)

        # 총 인원 수를 계산하여 '총 인원'
        total_count2 = segment_counts2.sum()
        segment_counts2['총 인원'] = total_count2

        st.write(segment_counts2)
        st.markdown("""
        변경 후 고객 세그먼트 분포  
        """)
    st.markdown("**고객 정보 입력**시 기본값은 신규로, 하지만 클라이언트가 세그먼트를 변경할 수 있도록 하였습니다.")

    st.subheader('👵 연령 변환')
    st.markdown("""고객 생년월일 데이터를 25년 3월 기준 연령으로 변환 하였습니다.""")
    merged_df = pd.concat([df['생년월일 (Date of Birth)'], df2['연령']], axis=1)
    merged_df.columns = ['원본파일의 생년월일 (Date of Birth)', '변환 후 연령']
    st.dataframe(merged_df,hide_index=True)

    st.subheader('전처리 후 고객정보 데이터셋 📊')
    df2['휴대폰번호'] = df2['휴대폰번호'].astype(str).apply(lambda x: '0' + x)
    st.dataframe(df2.head())

    st.markdown("---")
    st.title("KMeans 클러스터링 진행")
    st.subheader('클러스터링을 위한 X 데이터 선정')
    st.markdown("""
위의 가공 데이터를 바탕으로 클러스터링을 위한 X 데이터를 선정하였습니다.
- 연령 (Age)
- 거래 금액 (Transaction Amount)
- 제품 구매 빈도 (Purchase Frequency)
- 성별 (Gender),차량구분(vehicle types)
- 거래 방식 (Transaction Method)
- 제품 출시년월 (Launch Date)
- 제품 구매 날짜 (Purchase Date)
- 고객 세그먼트 (Customer Segment)
- 친환경차 (Eco-friendly Product)    
    """)

    st.markdown("""<b>고객 세그먼트 (Customer Segment)를 클러스터링 결과로 보지 않고 X 값으로 활용한 이유:</b><br>
    세그먼트는 클라이언트의 전략적 판단에 따라 고객의 특성을 기반으로 나눈 값으로 보았습니다.<br>
                클러스터링을 통해 고객을 더 세밀하게 분류한 후, 이를 기존 세그먼트와 결합하면, 비즈니스 전략에 더 유용한 인사이트를 제공할 수 있습니다.<br>
                """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image('img/elbow.png', use_container_width=200)
    with col2:
        st.markdown("""<br><br><br><br><br><br>
엘보우 기법 분석 결과 클러스터 수를 8개로 선정하여 KMeans 클러스터링을 진행하였습니다.<br>
                    클러스터링 결과는 EDA페이지에서 확인할 수 있습니다.<br>
                    """, unsafe_allow_html=True)
        
    st.markdown("---")

    st.subheader("SVC 모델을 활용한 신규 고객 클러스터링 분류")

    col1, col2 = st.columns(2)
    with col1:
        st.image('img/sc3.png')
    with col2:
        st.markdown("""
파이프라인을 구축하여 새 고객 데이터가 입력되면 카테고리컬 데이터는 인코딩, 수치형 데이터는 스케일링이 자동으로 수행과, SVC 모델을 통해 클러스터링 및 분류가 이루어지도록 설계하였습니다.
                """)
    col1, col2 = st.columns(2)
    with col1:
        st.code("""
# 새로운 고객 데이터 생성
new_customer_data = {
    "성별": ["남성"],
    "차량구분": ["대형 세단"],
    "거래 방식": ["현금"],
    "제품 출시년월": ["2023-01"],
    "제품 구매 날짜": ["2025-03-15"],
    "고객 세그먼트": ["신규"],
    "친환경차": ["부"],
    "연령": [21],
    "거래 금액": [90000000],
    "제품 구매 빈도": [2]
}""")
    with col2:
        st.image('img/sc4.png', use_container_width=True)

    st.markdown("---")


    st.subheader("고객 세그먼트별 프로모션 이메일 발송")
    st.markdown("""
분석 결과를 토대로 고객 클러스터링별 프로모션 이메일이 발송되도록 설정하였습니다.

""")
    col1, col2 = st.columns(2)
    with col1:
        st.image('img/sc1.png', use_container_width=True)
        st.markdown("""
      0번 클러스터 프로모션 메일 예시

""")
    with col2:
        st.image('img/sc2.png', use_container_width=True)
        st.markdown("""
      1번 클러스터 프로모션 메일 예시
        """)
        
