import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import re

import base64
import requests
import promo_email


# 클러스터 ID에 대한 설명
cluster_description = {
    0: ("30대 중반 고객", "거래 금액 크고, 제품 구매 빈도 높음, 친환경차 비율 낮음"),
    1: ("50대 초반 고객", "거래 금액 크고, 제품 구매 빈도 낮음, 친환경차 비율 높음"),
    2: ("60대 이상 고객", "거래 금액 적당하고 구매 빈도 중간, 친환경차 비율 높음"),
    3: ("30대 중반 고객", "거래 금액 평균적이고, 제품 구매 빈도 중간, 친환경차 비율 낮음"),
    4: ("30대 후반 고객", "거래 금액 적당하고, 제품 구매 빈도 높음, 친환경차 비율 보통"),
    5: ("60대 이상 고객", "거래 금액 크고, 자주 구매하지 않지만 큰 금액 지출, 친환경차 비율 높음"),
    6: ("30대 초반 고객", "거래 금액 적고, 구매 빈도 낮음, 친환경차 비율 높음"),
    7: ("40대 초반 고객", "거래 금액 적당하고 구매 빈도 낮음, 친환경차 비율 높음")
}

# 모델과 출시 년월 데이터
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
}

# 친환경차 모델 목록
eco_friendly_models = [
    'NEXO (FE)', 'Avante (CN7 HEV)', 'Grandeur (GN7 HEV)', 'IONIQ (AE EV)', 
    'Tucson (NX4 PHEV)', 'IONIQ 6 (CE)', 'Santa-Fe (MX5 PHEV)'
]

# 유틸리티 함수 정의
def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def is_eco_friendly(vehicle):
    return "여" if vehicle in eco_friendly_models else "부"

def extract_sigu(address):
    match = re.search(r'([가-힣]+(?:광역시|특별시|도)? [가-힣]+(?:시|구))', address)
    return match.group(0) if match else "시구 없음"

def validate_phone_number(phone):
    phone = re.sub(r'[^0-9]', '', phone)
    return phone if re.fullmatch(r"\d{11}", phone) else None

def validate_email(email):
    return email if "@" in email and "." in email else None

def send_sms(to_number, message_body):
    clicksend_username = st.secrets["CLICKSEND"]["CLICKSEND_USERNAME"]
    clicksend_api_key = st.secrets["CLICKSEND"]["CLICKSEND_API_KEY"]
    auth_header = f"Basic {base64.b64encode(f'{clicksend_username}:{clicksend_api_key}'.encode()).decode()}"
    headers = {"Authorization": auth_header, "Content-Type": "application/json"}
    data = {"messages": [{"source": "sdk", "body": message_body, "to": "+82" + to_number[1:]}]}
    try:
        requests.post("https://rest.clicksend.com/v3/sms/send", headers=headers, json=data)
        return True
    except:
        return False

def run_input_customer_info():
    if "step" not in st.session_state:
        st.session_state["step"] = 1
    steps = {1: run_input_step1, 2: step2_vehicle_selection, 3: step3_customer_data_storage}
    steps.get(st.session_state["step"], run_input_step1)()

def run_input_step1():
    st.title('📋 고객 정보 입력')
    model = joblib.load("model/model4.pkl")
    st.info("고객 정보를 모두 입력하고 예측 버튼을 눌러주세요.")
    with st.form(key="customer_info_form"):
        col1, col2 = st.columns([1, 1])
        with col1:
            성별 = st.selectbox("성별 선택", ["남", "여"])
            생년월일 = st.date_input("생년월일 입력", min_value=datetime(1900, 1, 1), max_value=datetime.today().replace(year=datetime.today().year - 20))
            연령 = calculate_age(생년월일)
            고객세그먼트 = st.selectbox("고객 세그먼트 선택", ["신규", "VIP", "일반", "이탈가능"], index=0)
            거래금액 = st.number_input("고객 예산 입력", min_value=10000000, step=1000000)
            구매빈도 = st.number_input("제품 구매 빈도 입력", min_value=1, step=1, value=1)
        with col2:
            차량구분 = st.selectbox("희망 차량 구분 선택", ["준중형 세단", "중형 세단", "대형 세단", "SUV", "픽업트럭"])
            거래방식 = st.selectbox("거래 방식 선택", ["카드", "현금", "계좌이체"])
            구매경로 = st.selectbox("구매 경로 선택", ["온라인", "오프라인"], index=1)
            구매한제품 = st.selectbox("구입 희망 모델 선택", list(launch_dates.keys()))
            제품구매날짜 = st.date_input("제품 구매 날짜 입력")
        if st.form_submit_button("예측하기"):
            st.session_state.update({
                "성별": 성별, "생년월일": 생년월일, "고객세그먼트": 고객세그먼트,
                "거래금액": 거래금액, "구매빈도": 구매빈도, "차량구분": 차량구분,
                "거래방식": 거래방식, "구매경로": 구매경로, "구매한제품": 구매한제품,
                "제품구매날짜": 제품구매날짜, "연령": 연령, "제품출시년월": launch_dates.get(구매한제품)
            })
            input_data = pd.DataFrame([[연령, 거래금액, 구매빈도, 성별, 차량구분, 거래방식, launch_dates.get(구매한제품), 제품구매날짜, 고객세그먼트, is_eco_friendly(구매한제품)]],
                                      columns=["연령", "거래 금액", "제품 구매 빈도", "성별", "차량구분", "거래 방식", "제품 출시년월", "제품 구매 날짜", "고객 세그먼트", "친환경차"])
            prediction = model.predict(input_data)
            st.session_state.update({"Cluster": prediction[0], "step": 2, "recommended_vehicles": get_recommended_vehicles(prediction[0])})
            st.rerun()




# 차량 추천
def get_recommended_vehicles(cluster_id):
    recommended_vehicles = []

    if cluster_id == 0:
        recommended_vehicles = [
            'Avante (CN7 N)','NEXO (FE)','Santa-Fe ™'
        ]
    elif cluster_id == 1:
        recommended_vehicles = [
            'G80 (RG3)','G90 (HI)','IONIQ 6 (CE)'
        ]
    elif cluster_id == 2:
        recommended_vehicles = [
            'G70 (IK)','i30 (PD)','Avante (CN7 HEV)'
        ]
    elif cluster_id == 3:
        recommended_vehicles = [
            'Avante (CN7 N)','Tucson (NX4 PHEV)','Grandeur (GN7 HEV)'
        ]
    elif cluster_id == 4:
        recommended_vehicles = [
            'IONIQ (AE EV)','NEXO (FE)','Tucson (NX4 PHEV)'
        ]
    elif cluster_id == 5:
        recommended_vehicles = [
            'Santa-Fe ™','G70 (IK)','Grandeur (GN7 HEV)'
        ]
    elif cluster_id == 6:
        recommended_vehicles = [
            'i30 (PD)','Avante (CN7 N)','Avante (CN7 HEV)'
        ]
    elif cluster_id == 7:
        recommended_vehicles = [
            'IONIQ 6 (CE)','NEXO (FE)','G90 (RS4)'
        ]
    return recommended_vehicles



# 2단계: 고객이 모델 선택 후 인적 사항 입력
def step2_vehicle_selection():
    st.title("🚗 추천 차량 선택")

    # 🚗 **차량 정보 딕셔너리** (기본 추천 멘트 포함)
    vehicle_data = {
        "Avante (CN7 N)": {
            "image": "img/Avante (CN7 N).png",
            "link": "https://www.hyundai.com/kr/ko/vehicles/avante",
            "price": "19640000",
            "description": "Avante (CN7 N)은 뛰어난 성능과 스타일을 자랑하는 최신형 세단입니다. 실용성과 세련된 디자인을 갖춘 완벽한 선택입니다."
        },
        "NEXO (FE)": {
            "image": "img/NEXO.png",
            "link": "https://www.hyundai.com/kr/ko/vehicles/nexo",
            "price": "69500000",
            "description": "NEXO는 친환경적인 수소차로, 연료비 절감과 환경을 고려하는 고객에게 적합합니다. 고급스러움과 친환경성을 동시에 제공합니다."
        },
        "Santa-Fe ™": {
            "image": "img/santafe.png",
            "link": "https://www.hyundai.com/kr/ko/e/vehicles/santafe/intro",
            "price": "34920000",
            "description": "넉넉한 공간과 실용성을 갖춘 Santa-Fe, 가족 단위 여행에 적합한 SUV입니다."
        },
        "G80 (RG3)": {
            "image": "img/g80.png",
            "link": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g80-black/highlights.html",
            "price": "82750000",
            "description": "G80은 고급스러운 세단으로 품격 있는 운전 경험을 제공합니다. VIP 고객님에게 어울리는 차량입니다."
        },
        "G90 (HI)": {
            "image": "img/G90.jpg",
            "link": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g90-black/highlights.html",
            "price": "129600000",
            "description": "G90은 프리미엄 세단으로, 고급스러움과 편안함을 제공합니다. 모든 세부 사항이 완벽하게 설계되어 있어 최고의 만족감을 선사합니다."
        },
        "IONIQ 6 (CE)": {
            "image": "img/IONIQ6.png",
            "link": "https://www.hyundai.com/kr/ko/e/vehicles/ioniq6/intro",
            "price": "46950000",
            "description": "IONIQ 6는 첨단 기술과 세련된 디자인을 갖춘 전기차입니다. 친환경적인 드라이빙을 원하시는 고객님께 적합합니다."
        },
        "i30 (PD)": {
            "image": "img/i30.png",
            "link": "https://www.hyundai-n.com/ko/models/n/i30-n.do",
            "price": "25560000",
            "description": "i30은 실용적이고 경제적인 소형차로 유지비가 적은 선택입니다. 특히 첫 차로 적합한 모델입니다."
        },
        "Tucson (NX4 PHEV)": {
            "image": "img/TUCSON.png",
            "link": "https://www.hyundai.com/kr/ko/vehicles/tucson",
            "price": "27290000",
            "description": "Tucson은 플러그인 하이브리드 SUV로, 환경을 고려하면서도 강력한 성능을 제공합니다. 연비 효율성이 뛰어난 차량입니다."
        },
        "Grandeur (GN7 HEV)": {
            "image": "img/Grandeur.png",
            "link": "https://www.hyundai.com/kr/ko/vehicles/grandeur",
            "price": "37110000",
            "description": "Grandeur는 고급스러움과 실용성을 동시에 제공합니다. 하이브리드 모델로 연비가 뛰어나고, 가격 대비 좋은 선택입니다."
        },
        "IONIQ (AE EV)": {
            "image": "img/IONIQ.png",
            "link": "https://www.hyundai.com/kr/ko/e/vehicles/ioniq9/intro",
            "price": "67150000",
            "description": "IONIQ는 전기차로 연료비 절감과 친환경적인 운전이 가능합니다. 가격 대비 성능이 뛰어난 모델입니다."
        },
        "G70 (IK)": {
            "image": "img/g70.png",
            "link": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g70/highlights.html",
            "price": "45240000",
            "description": "G70은 고급 세단으로, 가격대가 적당하면서도 세련된 디자인을 갖춘 차량입니다."
        },
        "Palisade (LX2)": {
            "image": "img/PALISADE.png",
            "link": "https://www.hyundai.com/kr/ko/vehicles/palisade",
            "price": "43830000",
            "description": "Palisade는 넓고 고급스러운 3열 SUV로 대가족이나 넉넉한 공간을 필요로 하는 고객님께 적합합니다."
        },
        "Santa-Fe (MX5 PHEV)": {
            "image": "img/Santa-FePHEV.png",
            "link": "https://www.hyundai.com/kr/ko/e/vehicles/santafe/intro",
            "price": "34920000",
            "description": "Santa-Fe PHEV는 플러그인 하이브리드 SUV로, 친환경을 고려하면서도 넓은 공간과 뛰어난 성능을 자랑하는 선택입니다."
        },
        "G90 (RS4)": {
            "image": "img/G90.jpg",
            "link": "https://www.genesis.com/kr/ko/models/luxury-sedan-genesis/g90-black/highlights.html",
            "price": "135800000",
            "description": "G90 RS4는 프리미엄 브랜드의 대표 모델로, 최고급 세단에 걸맞은 품격과 편안함을 제공합니다. 세부 사항까지 완벽한 선택입니다."
        },
        "Avante (CN7 HEV)": {
            "image": "img/Avante.png",
            "link": "https://www.hyundai.com/kr/ko/e/vehicles/avante-n/intro",
            "price": "33090000",
            "description": "Avante (CN7 HEV)는 친환경차를 선호하는 고객님께 적합한 하이브리드 세단입니다. 뛰어난 연비와 친환경적인 장점이 돋보입니다."
        }
    }

    # 📌 **클러스터별 추천 차량**
    cluster_recommendations = {
        0: ["Avante (CN7 N)", "NEXO (FE)", "Santa-Fe ™"],
        1: ["G80 (RG3)", "G90 (HI)", "IONIQ 6 (CE)"],
        2: ["G70 (IK)", "i30 (PD)", "Avante (CN7 HEV)"],
        3: ["Avante (CN7 N)", "Tucson (NX4 PHEV)", "Grandeur (GN7 HEV)"],
        4: ["IONIQ (AE EV)", "NEXO (FE)", "Tucson (NX4 PHEV)"],
        5: ["Santa-Fe ™", "G70 (IK)", "Grandeur (GN7 HEV)"],
        6: ["i30 (PD)", "Avante (CN7 N)", "Avante (CN7 HEV)"],
        7: ["IONIQ 6 (CE)", "NEXO (FE)", "G90 (RS4)"]
    }

    # 클러스터별 차량 추천 이유 매핑
    vehicle_recommendations = {
        "Avante (CN7 N)": {
            0: "젊은 연령대와 높은 거래 금액을 자랑하는 고객님께 딱 맞는 트렌디한 선택입니다. \n 최신형 세단으로 스타일과 실용성 두 마리 토끼를 잡을 수 있는 완벽한 선택입니다. \n 이 차량으로 한 단계 더 업그레이드된 라이프스타일을 경험해 보세요.",
            1: "VIP 고객님에게 어울리는 고급스러움을 제공하는 차량입니다. \n  고급 세단으로서 품격 있는 스타일을 완성해 드립니다. \n 더욱 럭셔리한 운전을 즐기세요.",
            2: "가격 대비 성능 최고! Avante (CN7 N)은 경제적이면서도 뛰어난 성능을 자랑하는 차량입니다.",
            3: "젊은 고객님, 스타일과 친환경성을 모두 고려한 Avante (CN7 N)!\n  최신 기술과 뛰어난 성능, 이 차량은 바로 고객님의 라이프스타일에 맞는 완벽한 파트너입니다.",
            4: "이 차량은 친환경차 선호도가 높은 고객님께도 안성맞춤!\n  가격 대비 성능이 뛰어나며 실용성도 고려한 Avante (CN7 N)을 추천 드립니다.",
            5: "신뢰할 수 있는 차량, Avante (CN7 N)!\n  현금 거래 비율이 높은 고객님께는 안정감과 실용성까지 제공하는 세련된 선택이 될 거예요.",
            6: "젊은 고객님들에게 더 없이 좋은 가격 대비 성능의 Avante (CN7 N)!\n  실용적이면서도 트렌디한 선택을 원하신다면 이 차가 바로 정답입니다.",
            7: "친환경차를 선호하시는 고객님에게 더할 나위 없이 좋은 전기차 옵션까지 고려한 Avante (CN7 N),\n  이 차와 함께라면 환경을 생각하는 운전이 가능해요."
        },
        "NEXO (FE)": {
            0: "친환경을 중요시하는 고객님께 완벽한 선택, 수소차 NEXO! \n 연령대가 젊고 환경을 생각하는 여러분께 딱 맞는 차량입니다. 지속 가능한 미래를 위한 선택을 하세요.",
            1: "친환경차 선호도가 높은 VIP 고객님께 완벽한 고급스러움과 친환경을 동시에 만족시킬 수 있는 차량, NEXO!\n  고급스러우면서도 환경을 생각하는 똑똑한 선택입니다.",
            4: "친환경차에 대한 관심이 높은 고객님께 맞춤 추천!\n  NEXO는 연료비 절감과 친환경적 요소를 모두 고려한 차량으로, 미래를 향한 현명한 선택입니다.",
            7: "친환경을 생각하는 고객님께 완벽한 선택, 수소차 NEXO!\n  완벽한 친환경차로, 여러분의 선택이 더욱 빛날 것입니다. 고급스러움과 친환경을 동시에 갖춘 NEXO를 만나보세요."
        },
        "Santa-Fe ™": {
            0: "가족 단위 고객님께 완벽한 공간과 실용성을 제공하는 Santa-Fe!\n  넓고 다용도로 사용 가능한 SUV, 장거리 여행에도 완벽한 선택입니다.\n  여러분의 생활을 더욱 편리하고 즐겁게 만들어 드려요!",
            5: "편안한 승차감과 넉넉한 공간을 자랑하는 Santa-Fe!\n  나이가 많고 현금 거래 비율이 높은 고객님께 실용적이고 신뢰할 수 있는 선택입니다. \n 가족과 함께 편안한 여행을 떠나세요!"
        },
        "G80 (RG3)": {
            1: "고급스러운 세단을 원하신다면 G80 (RG3)!\n  VIP 고객님께 딱 맞는 차량으로, 품격과 스타일을 모두 갖춘 선택입니다.\n  차 한 대로 고급스러움을 완성해 보세요."
        },
        "G90 (HI)": {
            1: "한 단계 더 높은 품격을 원하시는 고객님께 G90!\n  프리미엄 세단의 대명사로, 고급스러움과 편안함을 동시에 제공하는 차량입니다.\n  최상의 편안함을 원하신다면 G90을 선택하세요.",
            7: "거래 금액이 매우 높고, 친환경차를 선호하시는 고객님께 딱 맞는 고급 전기차, G90!\n  프리미엄 이미지를 더한 친환경차로, 완벽한 선택입니다."
        },
        "IONIQ 6 (CE)": {
            1: "친환경차에 대한 관심이 늘고 있는 고객님께, 고급 전기차 IONIQ 6! \n 고급스러운 외관과 첨단 기술을 갖춘 차량으로, 친환경을 고려하면서도 세련된 스타일을 제공합니다.",
            7: "친환경을 생각하는 고객님께 더욱 특별한 IONIQ 6! \n 고급스러움과 친환경성을 동시에 갖춘 전기차로, 미래 지향적인 선택이 될 것입니다."
        },
        "i30 (PD)": {
            2: "가격이 저렴하고 실용적인 소형차, i30! \n 연령대가 높고 거래 금액이 적은 고객님께 부담 없는 유지비와 실용성을 제공하는 완벽한 선택입니다.",
            6: "저렴한 가격으로 실용성을 고려한 i30! \n 거래 금액과 구매 빈도가 낮은 고객님께 실용적이고 경제적인 소형차를 추천드립니다."
        },
        "Tucson (NX4 PHEV)": {
            3: "환경을 고려한 플러그인 하이브리드 SUV, Tucson!\n  친환경차 비율이 높은 고객님께 적합한 선택으로, 실용적인 공간과 뛰어난 연비를 자랑합니다.",
            4: "연료 효율성을 중시하는 고객님께 맞춤 추천!\n  Tucson은 플러그인 하이브리드로, 경제적인 연비와 친환경성을 모두 고려한 차량입니다."
        },
        "Grandeur (GN7 HEV)": {
            3: "고객님께 적합한 차량, Grandeur HEV! \n 실용적이고 연비가 뛰어난 하이브리드 세단으로, 경제적인 선택이면서도 고급스러운 느낌을 제공합니다.",
            5: "연비가 뛰어난 하이브리드 세단, Grandeur! \n 거래 금액이 적은 고객님께 적합하며, 실용적이고 신뢰할 수 있는 선택입니다."
        },
        "IONIQ (AE EV)": {
            4: "친환경차에 관심많은 고객님께 가격대가 적당한 전기차인 IONIQ을 추천합니다. \n IONIQ은 연료비가 적고 실용적인 전기차로 적합합니다."
        },
        "G70 (IK)": {
            2: "고객님께 고급스러움을 더할 수 있는 G70!\n  가격대가 적당하면서도 고급스러움을 갖춘 차량으로, 차별화된 경험을 선사합니다.",
            5: "고급스러운 느낌의 세단을 선호하는 고객님께, G70! \n 거래 금액이 적더라도 품격을 높여 줄 차량입니다."
        },
        "Avante (CN7 HEV)": {
            2:"가격 대비 뛰어난 성능을 자랑하는 Avante (CN7 HEV)! 뛰어난 연비와 친환경적인 장점으로 실용적인 선택이 될 것입니다.\n경제적이면서도 환경을 고려한 현명한 선택을 하세요.",
            6:"젊은 고객님들에게 더 없이 좋은 가격 대비 성능의 Avante (CN7 N)! 좋은 연비로 실용적이면서도 트렌디한 선택을 원하신다면 이 차가 바로 정답입니다."
        
        }
    }

    # 세션 상태에서 필요한 값 가져오기
    cluster_id = st.session_state.get("Cluster")
    recommended_vehicles = cluster_recommendations.get(cluster_id, [])
    customer_type, characteristics = cluster_description.get(cluster_id, ("알 수 없는 클러스터", "특징 정보 없음"))

    # 고객이 직접 선택한 차량 반영
    selected_vehicle = st.session_state.get("selected_vehicle", "")
    구매한제품 = st.session_state.get("구매한제품", "")

    # 고객이 선택한 차량이 추천 리스트에 없으면 추가
    if 구매한제품 and 구매한제품 not in recommended_vehicles:
        recommended_vehicles.append(구매한제품)

    # 📝 고객 정보 출력
    st.text(f"예측된 클러스터: {cluster_id}")
    st.text("고객의 성향에 맞춘 추천 차량 목록입니다.")
    st.text(f"고객 유형: {customer_type}")
    st.text(f"특징: {characteristics}")

    if recommended_vehicles:
        # 차량 선택
        selected_vehicle = st.selectbox(
            "구입 희망 차량을 선택하세요",
            recommended_vehicles,
            key="vehicle_select_box",
            index=recommended_vehicles.index(st.session_state.get("selected_vehicle", recommended_vehicles[0])),
        )

        if selected_vehicle:
            # 🚗 **차량 데이터 가져오기**
            vehicle_info = vehicle_data.get(selected_vehicle, {})

            # 🚘 차량 세부 정보 출력
            st.image(vehicle_info.get("image", "img/default.png"), use_container_width=True)
            st.text(vehicle_info.get("description", "차량에 대한 정보가 없습니다."))
            st.markdown(f"[차량 상세정보 확인하기]({vehicle_info.get('link', '#')})", unsafe_allow_html=True)
            st.text(f"가격: {vehicle_info.get('price', '가격 정보 없음')}원")

        else:
            st.warning("추천 차량이 없습니다. 다시 예측을 시도해 주세요.")

        # 🚗 **차량 선택 완료 버튼**
        if st.button("선택 완료"):
            st.session_state["거래금액"] = vehicle_info.get("price", "가격 정보 없음")  # 🚘 최종 선택 차량의 가격 저장
            st.session_state["selected_vehicle"] = selected_vehicle
            st.success(f"{selected_vehicle} 선택 완료! 이제 고객 정보를 저장합니다.")
            st.session_state["step"] = 3  # 고객 정보 저장 단계로 이동
            st.rerun()
            


def step3_customer_data_storage():
    st.title("📝 고객 정보 입력 및 저장")

    # 고객 정보 입력 폼
    with st.form(key="customer_info_form"):
        이름 = st.text_input("이름")
        휴대폰번호 = validate_phone_number(st.text_input("휴대폰 번호 입력", placeholder="필수입니다.", key="phone_input"))
        이메일 = validate_email(st.text_input("이메일 입력", placeholder="필수입니다.", key="email_input"))
        주소 = st.text_input("주소")
        아이디 = st.text_input("아이디")
        가입일 = st.date_input("가입일")

        # 고객 정보 저장하기 버튼
        submit_button = st.form_submit_button("고객정보 저장하기")

        if submit_button:
            if not (이름 and 휴대폰번호 and 이메일 and 주소 and 아이디 and 가입일):
                st.error("⚠️ 모든 항목을 입력해야 합니다!")
                st.stop()

            # 🚀 **세션 상태에서 필요한 값 가져오기**
            생년월일 = st.session_state.get("생년월일", "")
            연령 = st.session_state.get("연령", calculate_age(생년월일) if 생년월일 else "")
            성별 = st.session_state.get("성별", "")
            고객세그먼트 = st.session_state.get("고객세그먼트", "")
            selected_vehicle = st.session_state.get("selected_vehicle", "")
            차량구분 = st.session_state.get("차량구분", "")
            친환경차 = is_eco_friendly(selected_vehicle)
            구매한제품 = selected_vehicle
            제품구매날짜 = st.session_state.get("제품구매날짜", "")
            거래금액 = st.session_state.get("거래금액", "")
            거래방식 = st.session_state.get("거래방식", "")
            구매빈도 = st.session_state.get("구매빈도", "")
            제품구매경로 = st.session_state.get("제품구매경로", "")
            제품출시년월 = launch_dates.get(selected_vehicle, "")
            Cluster = st.session_state.get("Cluster", "")
            시구 = extract_sigu(주소)

            # 🚗 **고객 정보 저장**
            full_data = pd.DataFrame([[
                이름, 생년월일, 연령, 성별, 휴대폰번호, 이메일, 주소, 아이디, 가입일, 고객세그먼트,
                차량구분, 구매한제품, 친환경차, 제품구매날짜, 거래금액, 거래방식, 구매빈도, 제품구매경로, 제품출시년월, Cluster, 시구
            ]], columns=[
                "이름", "생년월일", "연령", "성별", "휴대폰번호", "이메일", "주소", "아이디", "가입일",
                "고객 세그먼트", "차량구분", "구매한 제품", "친환경차", "제품 구매 날짜", "거래 금액",
                "거래 방식", "제품 구매 빈도", "제품 구매 경로", "제품 출시년월", "Cluster", "시구"
            ])

            # 📂 **CSV 파일에 저장**
            file_path = 'data/고객정보.csv'
            file_exists = pd.io.common.file_exists(file_path)
            full_data.to_csv(file_path, mode='a', header=not file_exists, index=False)

            st.text(f"고객 정보가 {file_path}에 저장되었습니다.")

            # 📲 **SMS 발송**
            message_body = f"안녕하세요! 고객님을 환영합니다. 선택하신 차량: {selected_vehicle}"
            if send_sms(휴대폰번호, message_body):
                st.success("📩 문자가 성공적으로 발송되었습니다.")
            else:
                st.error("⚠️ 문자 발송에 실패했습니다.")

            # 📧 **이메일 발송**
            promo_email.send_promotion_email(이메일, 이름, selected_vehicle)
            st.success("📧 이메일이 성공적으로 발송되었습니다.")

            # 이메일 전송 로그 저장
            log_entry = pd.DataFrame([[이메일, 이름, Cluster, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                                    columns=["이메일", "이름", "클러스터 ID", "전송 시간"])
            
            # CSV 파일에 저장
            log_file_path = 'data/이메일_전송_로그.csv'
            file_exist = pd.io.common.file_exists(log_file_path)
            log_entry.to_csv(log_file_path, mode='a', header=not file_exist, index=False)
            

if __name__ == "__main__":

    run_input_customer_info()
