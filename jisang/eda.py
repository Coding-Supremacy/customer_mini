import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.io as pio
import plotly.colors as pc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 페이지 설정 (가장 먼저 호출되어야 함)
st.set_page_config(page_title="🚗 현대자동차 고객 분석 대시보드", layout="wide")

# 추가 CSS 디자인: 구글 폰트, 애니메이션, 배경 그라데이션, 컨테이너, 탭 콘텐츠, 분석 카드 등
st.markdown(
    """
    <style>
    /* 구글 폰트 로드 */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    /* 전체 body 스타일 */
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #f0f4f8, #e8f5e9);
        padding: 20px;
    }

    /* Streamlit 기본 배경 제거 */
    .css-18e3th9, .css-1d391kg {
        background: none;
    }
    
    /* 메인 컨테이너 스타일 */
    .reportview-container .main {
        background-color: rgba(255,255,255,0.9);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }

    /* 헤더 스타일 */
    h1 {
        font-size: 2.5em;
        font-weight: 700;
        text-align: center;
        color: #2E86C1;
        margin-bottom: 10px;
    }

    h4 {
        text-align: center;
        color: #555;
        margin-bottom: 30px;
        font-size: 1.1em;
    }
    
    hr {
        border: 1px solid #bbb;
        margin: 20px 0;
    }
    
    /* 옵션 메뉴 스타일 */
    .nav-link {
        transition: background-color 0.3s ease, transform 0.3s ease;
        border-radius: 10px;
    }

    .nav-link:hover {
        background-color: #AED6F1 !important;
        transform: scale(1.05);
    }
    
    /* 분석 텍스트 카드 스타일 */
    .analysis-text {
        background-color: #ffffff;
        border-left: 4px solid #2E86C1;
        padding: 20px;
        margin: 30px 0;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        font-size: 1.1em;
        color: #333;
        line-height: 1.5;
    }
    
    .analysis-text:hover {
        background-color: #f7f9fa;
    }

    /* 탭 콘텐츠 스타일 */
    .tab-content {
        background-color: #fefefe;
        padding: 30px;
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    /* 이미지 스타일 */
    img {
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        max-width: 100%;
    }

    /* 옵션 메뉴 스타일 */
    .option-menu .nav-link-selected {
        background-color: #2E86C1;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)

# 메인 헤더
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>🚗 현대자동차 고객 분석 대시보드</h1>
<h4 style='text-align: center;'>고객 데이터를 기반으로 한 맞춤형 마케팅 전략</h4>
<hr>
""", unsafe_allow_html=True)

def run_eda():
    # 옵션 메뉴 추가
    selected = option_menu(
        menu_title=None,  
        options=["📊 가입 연도 분석", "💰 거래 금액 분석", "🛒 구매 빈도 분석", "📈 클러스터링 분석", "🌎 지역별 구매 분석"],
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

    # 📊 가입 연도 분석 탭
    if selected == "📊 가입 연도 분석":
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.subheader("📊 가입 연도와 고객 세그먼트 관계")
        st.markdown("""
        이 분석은 가입 연도별 고객 세그먼트 변화 양상을 시각화하여, 고객 유지 및 이탈 패턴을 분석합니다. 특정 연도에 가입한 고객들이 주로 속한 세그먼트를 살펴봄으로써 마케팅 전략을 수립할 수 있습니다.
        
        - 특정 연도에 가입한 고객들이 어떤 세그먼트에 속하는지 파악하여 타겟 마케팅을 설계할 수 있습니다.
        - 또한, 연도별 고객 유입 트렌드를 분석하여 향후 고객 이탈을 방지하는 전략을 개발하는 데 도움을 줍니다.
        """)
        image_path = "../customer_segment/가입연도와 고객 세그먼트 관계.png"
        if os.path.exists(image_path):
            st.image(image_path)
            st.markdown("""
            <div class='analysis-text'>
            **🔍 분석 내용:**
            - 2023년과 2024년에 일반 고객의 유입이 급증했으며, 이는 해당 연도에 효과적인 마케팅 캠페인이 진행되었음을 의미할 수 있습니다.
            - 신규 고객의 비율은 일정하지만, 이탈 가능 고객 비율이 증가하고 있어 재구매율을 높이기 위한 전략이 필요합니다.
            - VIP 고객 비율이 점차 증가하는 추세로, 브랜드 충성도 증가를 시사합니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 💰 거래 금액 분석 탭
    if selected == "💰 거래 금액 분석":
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.subheader("💰 고객 세그먼트별 거래 금액 분포")
        st.markdown("""
        고객 세그먼트별 평균 거래 금액을 분석하여, VIP 고객과 일반 고객의 소비 패턴을 비교합니다. 이를 통해 각 고객 군에 맞는 마케팅 전략을 수립할 수 있습니다.
        
        - VIP 고객과 일반 고객군의 소비 차이를 파악하여 차별화된 전략을 설계합니다.
        - 특정 세그먼트에서 거래 금액이 급격히 증가하는 시점을 파악하여 프로모션 효과성 분석을 할 수 있습니다.
        """)
        image_path = "../customer_segment/고객 세그먼트별 거래 금액 분포.png"
        if os.path.exists(image_path):
            st.image(image_path)
            st.markdown("""
            <div class='analysis-text'>
            **🔍 분석 내용:**
            - VIP 고객의 거래 금액 중앙값이 가장 높아, VIP 고객군이 가장 높은 소비를 하고 있음을 확인할 수 있습니다.
            - 박스플롯에서 이상치가 존재하는데, 이는 일부 고객이 비정상적으로 높은 금액을 결제한 경우일 수 있습니다.
            - 이탈 가능 고객의 거래 금액 분포가 넓게 퍼져 있어, 일부 고객군은 높은 소비를 하지만 전체적으로는 낮은 소비 성향을 보임을 알 수 있습니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 🛒 구매 빈도 분석 탭
    if selected == "🛒 구매 빈도 분석":
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.subheader("🛒 구매 빈도와 고객 세그먼트 관계")
        st.markdown("""
        고객의 평균 구매 빈도를 분석하여 반복 구매를 유도할 전략을 마련합니다. 특히 VIP 고객의 평균 구매 빈도를 파악하여 로열티 프로그램 설계에 도움을 줍니다.
        
        - 구매 빈도가 낮은 고객을 대상으로 재구매율을 높이기 위한 마케팅 전략을 수립합니다.
        - 또한, 구매 빈도가 높은 고객을 분석하여 더 많은 혜택을 제공할 수 있습니다.
        """)
        image_path = "../customer_segment/구매빈도와 고객 세그먼트 관계.png"
        if os.path.exists(image_path):
            st.image(image_path)
            st.markdown("""
            <div class='analysis-text'>
            **🔍 분석 내용:**
            - 구매 빈도 1회 고객이 일반 고객군에서 압도적으로 많고, 이탈 가능 고객군에서도 적지 않은 점을 분석했습니다.
            - VIP 고객의 구매 빈도가 상대적으로 높은 경향을 강조하며, 반복 구매를 유도할 전략이 필요합니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 📈 클러스터링 분석 탭
    if selected == "📈 클러스터링 분석":
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.subheader("📈 클러스터별 고객 세그먼트 분석")
        image_path = "../image/클러스터별 고객 세그먼트 분포.png"
        if os.path.exists(image_path):
            st.image(image_path)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        
        st.markdown("""
        <div class='analysis-text'>
        **🔍 클러스터별 분석 내용:**
        - **2번 유형**: 일반 고객이 많으며, 맞춤형 혜택 제공 필요.
        - **5번 유형**: VIP 고객과 이탈 가능 고객이 많아 로열티 프로그램 필요.
        - **0, 1, 3, 4번 유형**: 고객 세그먼트가 고르게 분포되어 있으며, 신규 고객 전환 가능성이 있음.
        
        **📢 결론:**
        - 일반 고객이 많은 클러스터에는 구매 빈도 증가 전략 적용.
        - VIP 고객 비중이 높은 클러스터에는 프리미엄 혜택 강화.
        - 이탈 가능 고객이 많은 클러스터에는 맞춤형 리텐션 캠페인 진행.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

            # 🌎 지역별 구매 분석 탭 (실시간 그래프)
    if selected == "🌎 지역별 구매 분석":
        st.markdown("<div class='tab-content'>", unsafe_allow_html=True)
        st.subheader("🌎 지역별 구매한 제품 수")
        st.markdown("""
        이 분석은 지역별로 고객들이 구매한 제품의 수를 시각화합니다. 이를 통해 특정 지역의 제품 선호도를 분석하고, 지역 기반 마케팅 전략을 수립할 수 있습니다.
        
        - 인기모델, 지역별 선호 제품 파악을 통해 제품 라인업을 최적화하여 선재고 확보후 마케팅 전략 수립.
        """)

        # 고객 데이터 (CSV 파일 불러오기)
        file_path = "../data/클러스터링고객데이터_5.csv"  # 절대 경로로 수정

        # 데이터 로딩 함수
        def load_data(file_path):
            return pd.read_csv(file_path)

       # 파일 변경 감지 및 데이터 업데이트
        class FileChangeHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if event.src_path == file_path:
                    st.session_state.data_updated = True

        # 파일 감지 함수
        def watch_file_changes():
            event_handler = FileChangeHandler()
            observer = Observer()
            observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
            observer.start()
            return observer

        # 파일 변경 감지를 위한 Observer 시작
        if 'observer' not in st.session_state:
            st.session_state.observer = watch_file_changes()

        # 데이터를 로드하고 캐시를 사용하여 자동으로 업데이트
        @st.cache_data(ttl=60)  # TTL을 설정하여 캐시된 데이터를 일정 시간 동안 유지
        def get_data():
            if os.path.exists(file_path):
                return load_data(file_path)
            else:
                st.error(f"⚠️ CSV 파일이 존재하지 않습니다: {file_path}")
                return pd.DataFrame()

        # 데이터 로드
        df = get_data()

        # 데이터가 업데이트되었는지 확인
        if 'data_updated' in st.session_state and st.session_state.data_updated:
            df = get_data()  # 데이터 새로고침
            st.session_state.data_updated = False

            # 데이터에서 시구와 구매한 제품 및 구매수 컬럼 추출
        if '시구' in df.columns and '구매한 제품' in df.columns and '제품 구매 빈도' in df.columns:
            # 지역별 구매한 제품 수 시각화
            product_count_by_region = df.groupby(['시구', '구매한 제품']).sum().reset_index()

            pastel_colors = pc.qualitative.Pastel

            # Plotly를 사용한 바 차트 생성 (전체 지역의 제품 구매 빈도)
            bar_fig = px.bar(product_count_by_region, 
                            x='시구', 
                            y='제품 구매 빈도', 
                            color='구매한 제품', 
                            title='지역별 구매한 제품 수',
                            labels={'시구': '지역', '제품 구매 빈도': '구매 빈도', '구매한 제품': '제품'},
                            color_discrete_sequence=pastel_colors)  # 색상 팔레트 지정

            # 그래프 꾸미기
            bar_fig.update_layout(
                title={'text': '지역별 구매한 제품 수', 'x': 0.5, 'xanchor': 'center', 'font': {'size': 20, 'family': 'Nanum Gothic', 'color': '#333'}},
                xaxis=dict(title='지역', tickangle=45),
                yaxis=dict(title='제품 구매 빈도'),
                margin=dict(l=40, r=40, t=40, b=80),
                plot_bgcolor='#f4f4f9',
                paper_bgcolor='#ffffff',
                font=dict(family='Nanum Gothic', size=12, color='#333'),
                showlegend=True,
            )

            # 그래프 시각화
            st.plotly_chart(bar_fig)

            # 지역 선택 (selectbox)
            region_selected = st.selectbox("지역을 선택하세요:", df['시구'].unique())

            # 선택한 지역의 데이터 필터링
            region_data = df[df['시구'] == region_selected]

            # 선택한 지역에 대한 구매한 제품별 총 갯수
            product_count_by_selected_region = region_data.groupby('구매한 제품')['제품 구매 빈도'].sum().reset_index()

            # 지역에 맞는 제품 구매 빈도를 파이 차트로 시각화
            pie_chart_fig = px.pie(product_count_by_selected_region,
                                    names='구매한 제품',
                                    values='제품 구매 빈도',
                                    title=f'{region_selected} 지역별 제품 구매 비율',
                                    color_discrete_sequence=pastel_colors)

            # 파이 차트 그래프 시각화
            st.plotly_chart(pie_chart_fig)
                
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run_eda()
