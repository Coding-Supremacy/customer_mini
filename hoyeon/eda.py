import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.colors as pc
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 10초마다 자동 새로고침 (10000 밀리초)
st_autorefresh(interval=10000, limit=None, key="fizzbuzz")

# 인포 메시지를 세밀하게 표시하는 함수
def custom_info(message, bg_color, text_color="black"):
    st.markdown(
        f'<div style="background-color: {bg_color}; color: {text_color}; padding: 10px; border-radius: 4px; margin-bottom: 10px;">{message}</div>',
        unsafe_allow_html=True
    )

# 기본 스타일 설정


# 메뉴 생성 (분석 종류 선택)
selected = option_menu(
    menu_title=None,
    options=[
        "📊 가입 연도 분석",
        "💰 거래 금액 분석",
        "🛒 구매 빈도 분석",
        "📈 클러스터링 분석",
        "🌎 지역별 구매 분석"
    ],
    icons=["calendar", "cash", "cart", "graph-up", "globe"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f9f9f9"},
        "icon": {"color": "#2E86C1", "font-size": "20px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "padding": "10px"},
        "nav-link-selected": {"background-color": "#2E86C1", "color": "white"},
    }
)

pastel_colors = pc.qualitative.Pastel

# CSV 파일 경로 (각 섹션에서 사용하는 CSV 파일 경로, 필요에 따라 수정)
csv_path = r"D:\customer_mini\data\클러스터링고객데이터_5.csv"

# 1) 가입 연도 분석
if selected == "📊 가입 연도 분석":
    st.subheader("📊 가입 연도와 고객 세그먼트")
    st.markdown("""
    가입일 데이터를 이용해 연도를 추출하면, 각 연도에 몇 명의 고객이 유입되었는지, 그리고 그 고객들이 어떤 유형(예: 일반, VIP, 이탈 가능 등)인지 확인할 수 있습니다. 
    X축은 가입 연도, Y축은 해당 연도에 가입한 고객 수를 나타내며, 각 막대는 고객 유형별로 색상으로 구분되어 있어, 연도별 고객 유입 패턴과 특성을 한눈에 파악할 수 있습니다.
    """, unsafe_allow_html=True)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if '가입일' in df.columns and '고객 세그먼트' in df.columns:
            df['가입일'] = pd.to_datetime(df['가입일'], errors='coerce')
            df['가입 연도'] = df['가입일'].dt.year
            df_grouped = df.groupby(['가입 연도', '고객 세그먼트']).size().reset_index(name='고객 수')
            bar_fig = px.bar(
                df_grouped,
                x='가입 연도',
                y='고객 수',
                color='고객 세그먼트',
                title='가입 연도별 고객 세그먼트 변화',
                labels={'가입 연도': '연도', '고객 수': '가입 고객 수', '고객 세그먼트': '고객 유형'},
                color_discrete_sequence=pastel_colors
            )
            bar_fig.update_layout(
                title={'text': '가입 연도별 고객 세그먼트 변화', 'x': 0.5, 'font': {'size': 20}},
                xaxis=dict(title='가입 연도', tickformat='%Y'),
                yaxis=dict(title='가입 고객 수'),
                margin=dict(l=40, r=40, t=40, b=80),
                plot_bgcolor='#f4f4f9', paper_bgcolor='#ffffff', font=dict(size=12)
            )
            st.plotly_chart(bar_fig)
            custom_info(
                "<strong> 그래프 설명:</strong><br> 이 그래프는 고객 가입 연도별 유입 고객 수와 유형을 시각화합니다. "
                "각 막대는 특정 연도에 가입한 고객 수를 나타내며, 색상은 각 고객의 유형을 구분하여 보여줍니다. 이 정보를 통해 특정 시기에 마케팅 전략을 강화할 필요가 있는지 판단할 수 있습니다.",
                "#d1ecf1", "black"
            )
            total_customers = df_grouped['고객 수'].sum()
            if total_customers >= 2000:
                custom_info("프로모션 제안: 고객수가 매우 많습니다. → 대규모 할인 행사, 프리미엄 멤버십 리뉴얼, VIP 전용 개인화 서비스 강화.", "#d1e7dd", "darkgreen")
            elif total_customers >= 1500:
                custom_info("프로모션 제안: 고객수가 양호합니다. → 신규 고객 혜택 강화, 추천인 보상 프로그램 도입 등을 고려하세요.", "#fff3cd", "darkorange")
            elif total_customers >= 1000:
                custom_info("프로모션 제안: 고객수가 보통입니다. → 소규모 이벤트와 온라인 프로모션을 통한 추가 고객 유입을 촉진하세요.", "#f8d7da", "darkred")
            elif total_customers >= 500:
                custom_info("프로모션 제안: 고객수가 낮습니다. → 온라인 광고, SNS 마케팅, 지역 이벤트 등을 통해 신규 고객 확보에 주력하세요.", "#f8d7da", "darkred")
            else:
                custom_info("프로모션 제안: 고객수가 매우 적습니다. → 전면적인 마케팅 전략 재검토 및 고객 피드백 수집 후 개선 방안을 마련하세요.", "#f5c6cb", "darkred")
        else:
            st.error("필요한 컬럼('가입일', '고객 세그먼트')이 CSV 파일에 없습니다.")
    else:
        st.error(f"⚠️ CSV 파일이 존재하지 않습니다: {csv_path}")

# 2) 거래 금액 분석
elif selected == "💰 거래 금액 분석":
    st.subheader("💰 고객 세그먼트별 거래 금액")
    st.markdown("""
    이 박스플롯은 고객 유형별 거래 금액의 분포를 보여줍니다. 
    중앙값, 사분위 범위, 이상치를 통해 각 고객군의 소비 성향과 지출 패턴을 명확하게 파악할 수 있으며, 이를 바탕으로 프리미엄 전략이나 할인 정책 등 마케팅 전략을 수립할 수 있습니다.
    """, unsafe_allow_html=True)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if {'고객 세그먼트', '거래 금액'}.issubset(df.columns):
            box_fig = px.box(
                df,
                x="고객 세그먼트",
                y="거래 금액",
                title="세그먼트별 거래 금액 분포",
                labels={'고객 세그먼트': '고객 유형', '거래 금액': '거래 금액(원)'},
                color="고객 세그먼트",
                color_discrete_sequence=pastel_colors
            )
            box_fig.update_layout(
                title={'text': '세그먼트별 거래 금액 분포', 'x': 0.5, 'font': {'size': 20}},
                xaxis=dict(title='고객 유형'),
                yaxis=dict(title='거래 금액(원)'),
                margin=dict(l=40, r=40, t=40, b=80),
                plot_bgcolor='#f4f4f9', paper_bgcolor='#ffffff', font=dict(size=12)
            )
            st.plotly_chart(box_fig)
            custom_info(
                "<strong>그래프 설명:</strong><br> 박스플롯은 각 고객 유형의 거래 금액 중앙값과 분포(상자), 그리고 이상치(개별 점)를 보여줍니다. 이 정보를 통해 소비 패턴을 분석하고, 고가 상품이나 할인 전략 등 마케팅 방향을 결정할 수 있습니다.",
                "#d1ecf1", "black"
            )
            avg_transaction = df['거래 금액'].mean()
            if avg_transaction >= 10000:
                custom_info("프로모션 제안: 거래 금액이 매우 높습니다. → 초고가 상품 및 맞춤형 컨시어지 서비스, VIP 전담 이벤트 강화.", "#d1e7dd", "darkgreen")
            elif avg_transaction >= 8000:
                custom_info("프로모션 제안: 거래 금액이 높습니다. → 프리미엄 멤버십 확대, VIP 특별 초청 행사, 맞춤형 상품 추천.", "#cce5ff", "darkblue")
            elif avg_transaction >= 5000:
                custom_info("프로모션 제안: 거래 금액이 양호합니다. → VIP 추가 할인 및 업셀링, 맞춤 마케팅 컨설팅 제공.", "#d4edda", "darkgreen")
            elif avg_transaction >= 3000:
                custom_info("프로모션 제안: 거래 금액이 보통 이상입니다. → 할인 쿠폰, 포인트 적립, 단골 고객 전용 이벤트 진행.", "#fff3cd", "darkorange")
            elif avg_transaction >= 2000:
                custom_info("프로모션 제안: 거래 금액이 보통입니다. → 소액 구매 고객 대상으로 업셀링 및 크로스셀링 프로모션 적용.", "#ffeeba", "darkorange")
            elif avg_transaction >= 1000:
                custom_info("프로모션 제안: 거래 금액이 낮습니다. → 재구매 할인 쿠폰, 적립 이벤트, 타겟 마케팅을 통한 충성도 향상.", "#f8d7da", "darkred")
            elif avg_transaction >= 500:
                custom_info("프로모션 제안: 거래 금액이 매우 낮습니다. → 가격 경쟁력 강화, 소액 구매 프로모션 및 신규 고객 확보 전략 집중.", "#f5c6cb", "darkred")
            else:
                custom_info("프로모션 제안: 거래 금액이 극히 낮습니다. → 전면적인 가격 정책 재검토 및 마케팅 전략 전환이 필요합니다.", "#f5c6cb", "darkred")
        else:
            st.error("필요한 컬럼('고객 세그먼트', '거래 금액')이 CSV 파일에 없습니다.")
    else:
        st.error(f"⚠️ CSV 파일이 존재하지 않습니다: {csv_path}")

# 3) 구매 빈도 분석
elif selected == "🛒 구매 빈도 분석":
    st.subheader("🛒 고객 세그먼트별 구매 빈도")
    st.markdown("""
    이 바 차트는 각 고객 유형별 평균 구매 횟수를 시각화합니다. 
    X축은 고객 유형, Y축은 해당 그룹의 평균 구매 횟수를 나타내며, 이를 통해 고객의 재구매 성향 및 소비 패턴을 심도 있게 분석할 수 있습니다.
    """, unsafe_allow_html=True)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if {'고객 세그먼트', '제품 구매 빈도'}.issubset(df.columns):
            freq_df = df.groupby('고객 세그먼트')['제품 구매 빈도'].mean().reset_index()
            freq_df.rename(columns={'제품 구매 빈도': '평균 구매 횟수'}, inplace=True)
            bar_fig = px.bar(
                freq_df,
                x="고객 세그먼트",
                y="평균 구매 횟수",
                title="세그먼트별 평균 구매 빈도",
                labels={'고객 세그먼트': '고객 유형', '평균 구매 횟수': '평균 구매 횟수'},
                color="고객 세그먼트",
                color_discrete_sequence=pastel_colors
            )
            bar_fig.update_layout(
                title={'text': '세그먼트별 평균 구매 빈도', 'x': 0.5, 'font': {'size': 20}},
                xaxis=dict(title='고객 유형'),
                yaxis=dict(title='평균 구매 횟수'),
                margin=dict(l=40, r=40, t=40, b=80),
                plot_bgcolor='#f4f4f9', paper_bgcolor='#ffffff', font=dict(size=12)
            )
            st.plotly_chart(bar_fig)
            custom_info(
                "<strong> 그래프 설명:</strong><br> 이 차트는 각 고객 유형별 평균 구매 횟수를 보여주어, 재구매 경향과 소비 패턴을 파악하는 데 도움을 줍니다. 이를 통해 고객 충성도 강화 및 재구매 촉진 전략을 수립할 수 있습니다.",
                "#d1ecf1", "black"
            )
            avg_purchase = freq_df['평균 구매 횟수'].mean()
            if avg_purchase >= 10:
                custom_info("프로모션 제안: 구매 빈도가 매우 높습니다. → VIP 보상 프로그램, 맞춤 할인, 전담 컨설팅 강화.", "#d1e7dd", "darkgreen")
            elif avg_purchase >= 8:
                custom_info("프로모션 제안: 구매 빈도가 높습니다. → 고객 보상 이벤트, 추가 포인트 적립, 맞춤 쿠폰 제공 고려.", "#cce5ff", "darkblue")
            elif avg_purchase >= 5:
                custom_info("프로모션 제안: 구매 빈도가 양호합니다. → 단골 고객 전환을 위한 보상 프로그램과 업그레이드 혜택 제공.", "#d4edda", "darkgreen")
            elif avg_purchase >= 3:
                custom_info("프로모션 제안: 구매 빈도가 보통입니다. → 재구매 할인, 포인트 2배 적립 행사 등으로 구매 촉진 시도.", "#fff3cd", "darkorange")
            elif avg_purchase >= 2:
                custom_info("프로모션 제안: 구매 빈도가 낮습니다. → 타겟 마케팅, 즉시 구매 혜택 제공을 통해 재구매 유도.", "#ffeeba", "darkorange")
            elif avg_purchase >= 1:
                custom_info("프로모션 제안: 구매 빈도가 매우 낮습니다. → 신규 고객 확보 및 재구매 촉진을 위한 강력한 할인 및 프로모션 전략 필요.", "#f8d7da", "darkred")
            elif avg_purchase == 0:
                custom_info("프로모션 제안: 구매 데이터가 0입니다. → 데이터 점검 후, 신규 이벤트 및 시스템 오류 수정이 필요합니다.", "#f5c6cb", "darkred")
            else:
                custom_info("프로모션 제안: 구매 데이터 오류 발생. → 데이터 정합성 재확인 및 마케팅 전략 수정 필요.", "#f5c6cb", "darkred")
        else:
            st.error("필요한 컬럼('고객 세그먼트', '제품 구매 빈도')이 CSV 파일에 없습니다.")
    else:
        st.error(f"⚠️ CSV 파일이 존재하지 않습니다: {csv_path}")

# 4) 클러스터링 분석
elif selected == "📈 클러스터링 분석":
    st.subheader("📈 클러스터별 고객 세그먼트")
    st.markdown("""
    아래 표와 그래프는 고객 데이터를 클러스터링 알고리즘을 통해 그룹화한 결과를 보여줍니다. 
    각 클러스터는 평균 연령, 거래 금액, 친환경차 선호도 등 주요 지표를 종합하여 고객 특성을 집약한 결과로, 
    이를 통해 클러스터별 고객의 소비 성향과 선호도를 파악할 수 있으며, 맞춤형 마케팅 및 차량 추천 전략 수립에 활용됩니다.
    """, unsafe_allow_html=True)
    # 클러스터 요약 데이터 (인덱스 제거)
    cluster_data = {
        "유형": [1, 2, 3, 4, 5, 6, 7, 8],
        "평균 연령대": [34.65, 51.35, 60.00, 34.51, 38.55, 61.95, 33.52, 44.94],
        "거래 금액": ["높음", "높음", "적음", "적당", "낮음", "낮음", "낮음", "매우 높음"],
        "친환경차 비율": ["13.04%", "9.30%", "0%", "20.51%", "39.39%", "13.95%", "0%", "100%"]
    }
    df_summary = pd.DataFrame(cluster_data)
    st.markdown(df_summary.to_html(index=False), unsafe_allow_html=True)
    
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if {'Cluster', '고객 세그먼트'}.issubset(df.columns):
            df_grouped = df.groupby(['Cluster', '고객 세그먼트']).size().reset_index(name='고객 수')
            bar_fig = px.bar(
                df_grouped,
                x='Cluster',
                y='고객 수',
                color='고객 세그먼트',
                title='클러스터별 고객 세그먼트 분포',
                labels={'Cluster': '클러스터', '고객 수': '고객 수', '고객 세그먼트': '고객 유형'},
                color_discrete_sequence=pastel_colors,
                barmode="stack"
            )
            bar_fig.update_layout(
                title={'text': '클러스터별 고객 세그먼트 분포', 'x': 0.5, 'font': {'size': 20}},
                xaxis=dict(title='클러스터'),
                yaxis=dict(title='고객 수'),
                margin=dict(l=40, r=40, t=40, b=80),
                plot_bgcolor='#f4f4f9', paper_bgcolor='#ffffff', font=dict(size=12)
            )
            st.plotly_chart(bar_fig)
            custom_info(
                "<strong>그래프 설명:</strong><br> 이 그래프는 고객 데이터를 클러스터별로 그룹화하여, 각 클러스터 내 고객 유형별 분포를 시각화합니다. "
                "X축은 클러스터 번호, Y축은 해당 클러스터의 고객 총수를 나타내며, 색상은 고객 유형(예: 일반, VIP, 이탈 가능 등)을 구분합니다. "
                "이 정보를 통해 각 클러스터의 특성을 명확히 파악하고, 맞춤형 마케팅 전략을 수립할 수 있습니다.",
                "#d1ecf1", "black"
            )
        else:
            st.error("필요한 컬럼('Cluster', '고객 세그먼트')이 CSV 파일에 없습니다.")
    else:
        st.error(f"⚠️ CSV 파일이 존재하지 않습니다: {csv_path}")

# 5) 지역별 구매 분석
elif selected == "🌎 지역별 구매 분석":
    st.subheader("🌎 지역별 구매한 제품 수")
    st.markdown("""
    이 분석은 각 지역별 고객이 구매한 제품의 총 '구매 건수'를 시각화합니다.
    X축은 지역, Y축은 해당 지역의 총 구매 건수를 나타내며, 막대의 색상은 지역별 판매된 제품군을 구분합니다.
    또한, 파이차트를 통해 선택한 지역 내 각 제품의 구매 비율을 상세히 파악할 수 있습니다.
    """, unsafe_allow_html=True)
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if {'시구', '구매한 제품', '제품 구매 빈도'}.issubset(df.columns):
            df = df.copy()
            df.rename(columns={'제품 구매 빈도': '구매 건수'}, inplace=True)
            purchase_count_by_region = df.groupby(['시구', '구매한 제품'])['구매 건수'].sum().reset_index()
            bar_fig = px.bar(
                purchase_count_by_region, 
                x='시구', 
                y='구매 건수', 
                color='구매한 제품', 
                title='지역별 구매 제품 건수',
                labels={'시구': '지역', '구매 건수': '총 구매 건수', '구매한 제품': '제품'},
                color_discrete_sequence=pastel_colors
            )
            bar_fig.update_layout(
                title={'text': '지역별 구매 제품 건수', 'x': 0.5, 'font': {'size': 20}},
                xaxis=dict(title='지역', tickangle=45),
                yaxis=dict(title='총 구매 건수'),
                margin=dict(l=40, r=40, t=40, b=80),
                plot_bgcolor='#f4f4f9', paper_bgcolor='#ffffff', font=dict(size=12),
                showlegend=True
            )
            st.plotly_chart(bar_fig)
            custom_info(
                "<strong> 그래프 설명:</strong><br> X축은 각 지역(예: 서울, 부산 등), Y축은 해당 지역의 총 구매 건수를 나타내며, "
                "막대의 색상은 각 지역에서 판매된 제품군을 구분합니다. 이를 통해 지역별 고객 선호도와 구매 패턴을 심도 있게 분석할 수 있습니다.",
                "#d1ecf1", "black"
            )
            region_selected = st.selectbox("지역 선택", df['시구'].unique())
            region_data = df[df['시구'] == region_selected]
            product_count_by_region = region_data.groupby('구매한 제품')['구매 건수'].sum().reset_index()
            pie_chart_fig = px.pie(
                product_count_by_region,
                names='구매한 제품',
                values='구매 건수',
                title=f"{region_selected} 지역의 제품 구매 비율",
                color_discrete_sequence=pastel_colors
            )
            st.plotly_chart(pie_chart_fig)
            custom_info(
                f"<strong> 파이차트 설명:</strong><br> 파이차트는 {region_selected} 지역 내 각 제품의 구매 건수 비율을 시각적으로 표현하여, "
                "인기 제품과 마케팅 포인트를 명확하게 파악할 수 있도록 돕습니다.",
                "#d1ecf1", "black"
            )
            total_region = product_count_by_region['구매 건수'].sum()
            if total_region >= 150:
                custom_info("프로모션 제안: 해당 지역의 구매 건수가 매우 높습니다. → 대형 이벤트, 지역 맞춤 플래그십 스토어 운영, 시승행사 등 강력한 오프라인 마케팅 전략을 추진하세요.",
                           "#d1e7dd", "darkgreen")
            elif total_region >= 120:
                custom_info("프로모션 제안: 구매 건수가 높습니다. → 지역 페스티벌, 시승행사, 특별 할인 및 VIP 혜택 확대를 고려하세요.",
                           "#cce5ff", "darkblue")
            elif total_region >= 100:
                custom_info("프로모션 제안: 구매 건수가 양호합니다. → 지역 맞춤 할인 쿠폰, 멤버십 이벤트, 고객 리워드 프로그램 등을 통해 추가 매출 증대를 도모하세요.",
                           "#d4edda", "darkgreen")
            elif total_region >= 80:
                custom_info("프로모션 제안: 구매 건수가 보통 이상입니다. → 오프라인 체험 행사, 지역 광고 및 SNS 마케팅 강화로 브랜드 인지도 상승을 노려보세요.",
                           "#fff3cd", "darkorange")
            elif total_region >= 60:
                custom_info("프로모션 제안: 구매 건수가 보통입니다. → 소규모 이벤트, 온라인 마케팅, 고객 피드백 기반 프로모션 전략을 적용하세요.",
                           "#ffeeba", "darkorange")
            elif total_region >= 40:
                custom_info("프로모션 제안: 구매 건수가 다소 낮습니다. → 타겟 마케팅, 지역 맞춤 할인, 현지 딜러 협업을 통해 구매 활성화를 도모하세요.",
                           "#f8d7da", "darkred")
            elif total_region >= 20:
                custom_info("프로모션 제안: 구매 건수가 낮습니다. → 집중 온라인 광고, 신규 고객 프로모션, 현지 시장 재분석을 통한 전략 수정이 필요합니다.",
                           "#f5c6cb", "darkred")
            elif total_region >= 10:
                custom_info("프로모션 제안: 구매 건수가 매우 낮습니다. → 신규 시장 테스트, 강력한 온라인 캠페인, 프로모션 재설계를 고려하세요.",
                           "#f5c6cb", "darkred")
            elif total_region >= 1:
                custom_info("프로모션 제안: 구매 건수가 극히 적습니다. → 전면적인 시장 재분석 후, 집중 타겟 마케팅 및 신규 전략 수립이 필수적입니다.",
                           "#f5c6cb", "darkred")
            else:
                custom_info("프로모션 제안: 이 지역에서는 구매가 전혀 이루어지지 않았습니다. → 전략적 철수 또는 신규 시장 개척을 신중히 검토하세요.",
                           "#f5c6cb", "darkred")
            st.markdown(
                """
                ---<br>
                <strong>추가 설명:</strong><br>
                - 데이터는 실제 상황과 다를 수 있으며, 지역별 특성에 따라 마케팅 효과가 달라집니다.<br>
                - 다양한 시나리오와 A/B 테스트를 통해 최적의 마케팅 전략을 도출하시기 바랍니다.
                """, unsafe_allow_html=True
            )
        else:
            st.error("필요한 컬럼('시구', '구매한 제품', '제품 구매 빈도')이 CSV 파일에 없습니다.")
    else:
        st.error(f"⚠️ CSV 파일이 존재하지 않습니다: {csv_path}")

