import streamlit as st
import os
import pandas as pd
from streamlit_option_menu import option_menu

def run_eda():
    # 페이지 설정
    st.set_page_config(page_title="🚗 현대자동차 고객 분석 대시보드", layout="wide")
    
    # 추가 CSS 디자인: 구글 폰트, 애니메이션, 배경 그라데이션, 컨테이너, 탭 콘텐츠, 분석 카드 등
    st.markdown(
        """
        <style>
        /* 구글 폰트 로드 */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        
        /* 전체 body 스타일 및 애니메이션 적용 배경 */
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #e0f7fa, #e8f5e9);
            animation: bgAnimation 10s infinite alternate;
        }
        @keyframes bgAnimation {
            0% { background: linear-gradient(135deg, #e0f7fa, #e8f5e9); }
            100% { background: linear-gradient(135deg, #fffde7, #ffe0b2); }
        }
        
        /* Streamlit 기본 배경 제거 */
        .css-18e3th9, .css-1d391kg {
            background: none;
        }
        
        /* 메인 컨테이너 스타일 */
        .reportview-container .main {
            background-color: rgba(255,255,255,0.9);
            padding: 30px 50px;
            border-radius: 20px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        
        /* 헤더 스타일 */
        h1 {
            font-size: 2.8em;
            font-weight: 700;
            text-align: center;
            color: #2E86C1;
            text-shadow: 2px 2px 10px rgba(46, 134, 193, 0.3);
            margin-bottom: 10px;
        }
        h4 {
            text-align: center;
            color: #555;
            margin-bottom: 20px;
        }
        hr {
            border: 1px solid #bbb;
            margin: 20px 0;
        }
        
        /* 옵션 메뉴 스타일 강화 */
        .nav-link {
            transition: background-color 0.3s ease, transform 0.3s ease;
            border-radius: 10px;
        }
        .nav-link:hover {
            background-color: #AED6F1 !important;
            transform: scale(1.05);
        }
        
        /* 탭 콘텐츠 카드 스타일 + 마우스 오버 애니메이션 */
        .tab-content {
            background-color: #fefefe;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .tab-content:hover {
            transform: scale(1.02);
        }
        
        /* 이미지 스타일 */
        img {
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        
        /* 콘텐츠 페이드인 애니메이션 */
        .fade-in {
            animation: fadeInAnimation 1s ease-in;
        }
        @keyframes fadeInAnimation {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* 분석 텍스트 카드 스타일 */
        .analysis-text {
            background-color: #ffffff;
            border-left: 4px solid #2E86C1;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            font-size: 1.1em;
            color: #333;
            line-height: 1.5;
            transition: background-color 0.3s ease;
        }
        .analysis-text:hover {
            background-color: #f7f9fa;
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
    
    # 옵션 메뉴 추가
    selected = option_menu(
        menu_title=None,  # 상단 제목 없음
        options=["📊 가입 연도 분석", "💰 거래 금액 분석", "🛒 구매 빈도 분석", "📈 클러스터링 분석"],
        icons=["calendar", "cash", "cart", "graph-up"],
        menu_icon="cast",  # 메뉴 아이콘 설정
        default_index=0,  # 기본 선택 탭
        orientation="horizontal",  # 가로형 메뉴
        styles={
            "container": {"padding": "0!important", "background-color": "#f9f9f9"},
            "icon": {"color": "#2E86C1", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "padding": "10px"},
            "nav-link-selected": {"background-color": "#2E86C1", "color": "white"},
        }
    )
    
    # 📊 가입 연도 분석 탭
    if selected == "📊 가입 연도 분석":
        st.markdown("<div class='tab-content fade-in'>", unsafe_allow_html=True)
        st.subheader("📊 가입 연도와 고객 세그먼트 관계")
        st.markdown("""
        가입 연도별 고객 세그먼트 변화 양상을 분석하여 **고객 유지 및 이탈 패턴**을 파악할 수 있습니다.
        - 특정 연도에 가입한 고객이 주로 어떤 세그먼트에 속하는지 시각화하여 확인합니다.
        - 연도별 고객 유입 트렌드를 분석함으로써 **마케팅 전략 수립**에 도움을 줄 수 있습니다.
        """)
        image_path = "C:/customer_mini/cluster_analysis/image/가입연도와 고객 세그먼트 관계.png"
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
            st.markdown("""
            <div class='analysis-text'>
            **🔍 분석 내용:**
            - 2023년과 2024년에 일반 고객의 유입이 급증했으며, 이는 해당 연도에 효과적인 마케팅 캠페인이 진행되었음을 의미할 수 있습니다.
            - 신규 고객의 비율이 일정하게 유지되나, 이탈 가능 고객 비율이 증가하는 점을 고려하여 **재구매율을 높이기 위한 전략이 필요**합니다.
            - VIP 고객 비율이 시간이 지나면서 점진적으로 증가하는 경향이 나타나며, 이는 **브랜드 충성도가 증가**함을 시사합니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 💰 거래 금액 분석 탭
    if selected == "💰 거래 금액 분석":
        st.markdown("<div class='tab-content fade-in'>", unsafe_allow_html=True)
        st.subheader("💰 고객 세그먼트별 거래 금액 분포")
        st.markdown("""
        고객 세그먼트별 평균 거래 금액을 분석하여, **VIP 고객과 일반 고객의 소비 패턴**을 확인합니다.
        - VIP 고객군과 일반 고객군의 소비 차이를 분석하여 **차별화된 마케팅 전략**을 수립할 수 있습니다.
        - 특정 세그먼트에서 거래 금액이 급격히 증가하는 시점을 파악하여 **프로모션 효과성 분석**이 가능합니다.
        """)
        image_path = "C:/customer_mini/customer_segment/고객 세그먼트별 거래 금액 분포.png"
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
            st.markdown("""
            <div class='analysis-text'>
            **🔍 분석 내용:**
            - 일반 고객, VIP 고객, 신규 고객, 이탈 가능 고객의 거래 금액 분포를 비교한 결과, 전반적으로 VIP 고객의 중앙값이 가장 높아 **VIP 고객의 평균 소비 금액이 높음을 확인**할 수 있습니다.
            - 박스플롯을 보면 일부 이상치(Outliers)가 존재하는데, 이는 특정 고객이 비정상적으로 높은 금액을 결제한 경우일 가능성이 큽니다.
            - 이탈 가능 고객의 거래 금액 분포가 비교적 넓게 퍼져 있어 **일부 고객군의 높은 소비 패턴이 존재하지만, 전체적으로는 낮은 소비 성향을 보임**을 알 수 있습니다.
            - VIP 고객과 신규 고객의 소비 패턴이 비슷한 경향을 보이며, 신규 고객을 VIP 고객으로 전환시키는 전략이 효과적일 수 있습니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 🛒 구매 빈도 분석 탭
    if selected == "🛒 구매 빈도 분석":
        st.markdown("<div class='tab-content fade-in'>", unsafe_allow_html=True)
        st.subheader("🛒 구매 빈도와 고객 세그먼트 관계")
        st.markdown("""
        고객의 평균 구매 빈도를 분석하여, **반복 구매를 유도할 전략**을 마련할 수 있습니다.
        - VIP 고객은 평균적으로 몇 회 구매하는지 파악하여 **로열티 프로그램 설계**에 도움을 줍니다.
        - 구매 빈도가 낮은 세그먼트를 대상으로 **재구매율을 높이기 위한 마케팅 전략**을 수립할 수 있습니다.
        """)
        image_path = "C:/customer_mini/customer_segment/구매빈도와 고객 세그먼트 관계.png"
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
            st.markdown("""
            <div class='analysis-text'>
            **🔍 분석 내용:**
            - 구매 빈도 1회 고객이 일반 고객군에서 압도적으로 많고, 이탈 가능 고객군에서도 적지 않은 점을 분석했습니다.
            - VIP 고객의 구매 빈도가 상대적으로 높은 경향을 강조하면서, 구매 빈도 증가를 유도할 전략을 제안드립니다.
            - 신규 고객군의 경우 구매 빈도 2~3회에서 증가하는 패턴을 보여 VIP 전환 가능성이 있다는 점도 추가했습니다.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 📈 클러스터링 분석 탭
    if selected == "📈 클러스터링 분석":
        st.markdown("<div class='tab-content fade-in'>", unsafe_allow_html=True)
        st.subheader("📈 클러스터별 고객 세그먼트 분석")
        image_path = "C:/customer_mini/cluster_analysis/image/클러스터별 고객 세그먼트 분포.png"
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.error(f"⚠️ 이미지 파일이 존재하지 않습니다: {image_path}")
        
        st.markdown("""
        <div class='analysis-text'>
        **🔍 클러스터별 분석 내용:**
        - **2번 유형**: 일반 고객이 압도적으로 많으며, 특정 마케팅 캠페인의 효과일 가능성이 있음. **맞춤형 혜택 제공 필요**
        - **5번 유형**: VIP 고객과 이탈 가능 고객이 상대적으로 많으며, **로열티 프로그램**이나 **개인 맞춤형 프로모션** 적용 필요
        - **0, 1, 3, 4번 유형**: 고객 세그먼트가 고르게 분포되어 있으며, 신규 고객이 일부 클러스터에서 다수 존재 → **VIP 전환 가능성 고려**
        
        **📢 결론:**
        - 일반 고객이 많은 클러스터에는 **구매 빈도 증가 전략** 적용
        - VIP 고객 비중이 높은 클러스터에는 **프리미엄 혜택 강화**
        - 이탈 가능 고객이 많은 클러스터에는 **맞춤형 리텐션 캠페인 진행**
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    run_eda()
