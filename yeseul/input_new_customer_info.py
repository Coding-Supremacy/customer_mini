import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import re
import time
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

# 예측을 위한 입력값을 처리하는 함수
def run_input_customer_info():
    if "step" not in st.session_state:
        st.session_state["step"] = 1  # 첫 번째 단계로 시작
    
    if st.session_state["step"] == 1:
        run_input_step1()  # 고객 정보 입력
    elif st.session_state["step"] == 2:
        step2_vehicle_selection()  # 차량 선택
    elif st.session_state["step"] == 3:
        step3_customer_data_storage()  # 고객 정보 저장

# 예측을 위한 입력값을 처리하는 함수
def run_input_step1():
    st.title('📋 고객 정보 입력')

    # 모델 로드
    model = joblib.load("model/model4.pkl")

    st.info("""
            #### 정보를 입력하고 예측 버튼을 눌러주세요.
            #### 모든 항목은 필수입니다.
            """)

    with st.form(key="customer_info_form"):
        col1, col2 = st.columns([1, 1])
        with col1:
            # 고객 정보 입력 항목들 (성별, 생일, 고객세그먼트, 거래금액 등)
            성별 = st.selectbox("성별 선택", ["남", "여"])

            # 현재 날짜에서 20년 전의 날짜를 구하기
            today = datetime.today()
            year_20_years_ago = today.replace(year=today.year - 20)

            # 만약 오늘이 2월 29일이라면, 20년 전 날짜가 존재하지 않을 수 있기 때문에, 월과 일을 조정합니다.
            if year_20_years_ago.month == 2 and year_20_years_ago.day == 29:
                year_20_years_ago = year_20_years_ago.replace(day=28)


            # 생년월일 입력 (1900년부터 20년 전 날짜까지 선택 가능)
            생년월일 = st.date_input("생년월일 입력", min_value=datetime(1900, 1, 1), max_value=year_20_years_ago)
            if 생년월일:
                today = datetime.today()
                연령 = today.year - 생년월일.year - ((today.month, today.day) < (생년월일.month, 생년월일.day))
            고객세그먼트 = st.selectbox("고객 세그먼트 선택", ["신규", "VIP", "일반", "이탈가능"], index=0)
            거래금액 = st.number_input("고객 예산 입력", min_value=10000000, step=1000000)
            구매빈도 = st.number_input("제품 구매 빈도 입력", min_value=1, step=1, value=1)



        with col2:
            차량구분 = st.selectbox("희망 차량 구분 선택", ["준중형 세단", "중형 세단", "대형 세단", "SUV", "픽업트럭"])
            거래방식 = st.selectbox("거래 방식 선택", ["카드", "현금", "계좌이체"])
            구매경로 = st.selectbox("구매 경로 선택", ["온라인", "오프라인"], index=1)
            구매한제품 = st.selectbox("구입 희망 모델 선택", list(launch_dates.keys()))
            제품구매날짜 = st.date_input("제품 구매 날짜 입력")

        submitted = st.form_submit_button("예측하기")
        if submitted:
            # 모든 항목을 입력해야 함
            if not (성별 and 거래금액 and 구매빈도 and 차량구분 and 거래방식 and 구매경로 and 구매한제품 and 제품구매날짜):
                st.error("⚠️ 모든 항목을 입력해야 합니다!")
                st.stop()

            # 생년월일로 연령 계산
            today = datetime.today()
            연령 = today.year - 생년월일.year - ((today.month, today.day) < (생년월일.month, 생년월일.day))

            # 세션 상태에 입력된 값을 저장
            st.session_state["성별"] = 성별
            st.session_state["생년월일"] = 생년월일
            st.session_state["고객세그먼트"] = 고객세그먼트
            st.session_state["거래금액"] = 거래금액
            st.session_state["구매빈도"] = 구매빈도
            st.session_state["차량구분"] = 차량구분
            st.session_state["거래방식"] = 거래방식
            st.session_state["구매경로"] = 구매경로
            st.session_state["구매한제품"] = 구매한제품
            st.session_state["제품구매날짜"] = 제품구매날짜
            st.session_state["연령"] = 연령
            st.session_state["제품구매빈도"] = 구매빈도
            st.session_state["제품구매경로"] = 구매경로
            st.session_state["제품출시년월"] = launch_dates.get(구매한제품)
            st.session_state["구매한제품"] = 구매한제품
            st.session_state["친환경차"] = "여" if 구매한제품 in eco_friendly_models else "부"



            # 예측 데이터 준비
            input_data = pd.DataFrame([[연령, 거래금액, 구매빈도, 성별, 차량구분, 거래방식, launch_dates.get(구매한제품), 제품구매날짜, 고객세그먼트, "여" if 구매한제품 in eco_friendly_models else "부"]],
                                    columns=["연령", "거래 금액", "제품 구매 빈도", "성별", "차량구분", "거래 방식", "제품 출시년월", "제품 구매 날짜", "고객 세그먼트", "친환경차"])

            # 예측 실행
            prediction = model.predict(input_data)
            cluster_id = prediction[0]
            customer_type, characteristics = cluster_description.get(cluster_id, ("알 수 없는 클러스터", "특징 정보 없음"))

            st.text(f"예측된 클러스터: {cluster_id}")
            st.text(f"고객 유형: {customer_type}")
            st.text(f"특징: {characteristics}")

            st.session_state["Cluster"] = cluster_id

            st.session_state["step"] = 2  # 차량 선택 단계로 넘어가기
            st.session_state["recommended_vehicles"] = get_recommended_vehicles(cluster_id, "여" if 구매한제품 in eco_friendly_models else "부")
            st.rerun()


# 차량 추천 (친환경차 여부 포함)
def get_recommended_vehicles(cluster_id, 친환경차):
    # 클러스터에 따른 추천 차량 목록
    recommended_vehicles = []
    if cluster_id == 0:
        recommended_vehicles = ['클러스터 0 추천모델']
    elif cluster_id == 1:
        recommended_vehicles = ['클러스터 1 추천모델']
    elif cluster_id == 2:
        recommended_vehicles = ['클러스터 2 추천모델']
    elif cluster_id == 3:
        recommended_vehicles = ['클러스터 3 추천모델']
    elif cluster_id == 4:
        recommended_vehicles = ['클러스터 4 추천모델']
    elif cluster_id == 5:
        recommended_vehicles = ['클러스터 5 추천모델']
    elif cluster_id == 6:
        recommended_vehicles = ['클러스터 6 추천모델']
    elif cluster_id == 7:
        recommended_vehicles = ['클러스터 7 추천모델']

    # 친환경차 여부에 따라 추천 차량을 다르게 처리할 수 있다.
    if 친환경차 == "여":
        recommended_vehicles.append("친환경차 모델 추천")
    
    return recommended_vehicles

# 2단계: 고객이 모델 선택 후 인적 사항 입력
def step2_vehicle_selection():
    st.title("🚗 고객님을 위한 차량 추천")

    recommended_vehicles = st.session_state.get("recommended_vehicles", [])
    st.write("추천 차량 목록:", recommended_vehicles)  # 추천 차량 리스트 출력

    if recommended_vehicles:
        # 버튼을 사용하여 회원 가입 진행
        submit_button = st.button("회원 가입")
        if submit_button:  # 버튼 클릭 시
            st.session_state["step"] = 3  # 고객 정보 저장 단계로 이동
            # 화면 새로고침
            st.rerun()
    else:
        st.warning("추천 차량이 없습니다. 다시 예측을 시도해 주세요.")

def step3_customer_data_storage():
    st.title("📝 고객 정보 입력 및 저장")

    # 고객 정보 입력 폼
    with st.form(key="customer_info_form"):
        이름 = st.text_input("이름")
        # 📌 **휴대폰 번호 입력 및 즉시 검증**
        휴대폰번호 = st.text_input("휴대폰 번호 입력", placeholder="필수입니다.", key="phone_input")
        # 하이픈을 포함한 휴대폰 번호 포맷팅
        휴대폰번호 = re.sub(r'[^0-9]', '', 휴대폰번호)  # 숫자만 추출
        if 휴대폰번호 and not re.fullmatch(r"\d{11}", 휴대폰번호):
            st.session_state["phone_error"] = True
        else:
            st.session_state["phone_error"] = False
        # 오류 메시지 표시
        if st.session_state["phone_error"]:
            st.error("⚠️ 휴대폰 번호는 11자리 숫자여야 합니다. (예: 01012345678)")
        이메일 = st.text_input("이메일 입력", placeholder="필수입니다.", key="email_input")

        # 이메일 주소 형식 검증 (정규식 사용)
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if 이메일 and not re.fullmatch(email_regex, 이메일):
            st.session_state["email_error"] = True
        else:
            st.session_state["email_error"] = False

        # 오류 메시지 표시
        if st.session_state["email_error"]:
            st.error("⚠️ 이메일 주소 형식이 올바르지 않습니다. 예: example@domain.com")

        주소 = st.text_input("주소")
        아이디 = st.text_input("아이디")
        가입일 = st.date_input("가입일")

        # 고객 정보 저장하기 버튼
        submit_button = st.form_submit_button("고객정보 저장하기")

        if submit_button:
            if not (이름 and 휴대폰번호 and 이메일 and 주소 and 아이디 and 가입일):
                st.error("⚠️ 모든 항목을 입력해야 합니다!")
                st.stop()

            # 입력된 고객 정보 세션 상태에 저장
            st.session_state["name"] = 이름
            st.session_state["phone"] = 휴대폰번호
            st.session_state["email"] = 이메일
            st.session_state["address"] = 주소
            st.session_state["id"] = 아이디
            st.session_state["registration_date"] = 가입일

            # 세션 상태에서 다른 필요한 값 가져오기
            연령 = st.session_state.get("연령", "")
            생년월일 = st.session_state.get("생년월일", "")
            성별 = st.session_state.get("성별", "")
            고객세그먼트 = st.session_state.get("고객세그먼트", "")
            차량구분 = st.session_state.get("차량구분", "")
            친환경차 = st.session_state.get("친환경차", "")
            구매한제품 = st.session_state.get("구매한제품", "")
            제품구매날짜 = st.session_state.get("제품구매날짜", "")
            거래금액 = st.session_state.get("거래금액", "")
            거래방식 = st.session_state.get("거래방식", "")
            구매빈도 = st.session_state.get("제품구매빈도", "")
            제품구매경로 = st.session_state.get("제품구매경로", "")
            Cluster = st.session_state.get("Cluster", "")
            연령 = st.session_state.get("연령", "")
            구매빈도= st.session_state.get("구매빈도", "")
            제품출시년월= st.session_state.get("제품출시년월", "")



            # 고객 정보 저장
            full_data = pd.DataFrame([[이름, 생년월일, 연령, 성별, 휴대폰번호, 이메일, 주소, 아이디, 가입일, 고객세그먼트, 
                                       차량구분, 구매한제품, 친환경차, 제품구매날짜, 거래금액, 거래방식, 구매빈도, 제품구매경로, 제품출시년월, Cluster]],
                                    columns=["이름", "생년월일", "연령", "성별", "휴대폰번호", "이메일", "주소", "아이디", "가입일", 
                                             "고객 세그먼트", "차량구분", "구매한 제품", "친환경차", "제품 구매 날짜", "거래 금액", 
                                             "거래 방식", "제품 구매 빈도", "제품 구매 경로", "제품 출시년월", "Cluster"])

            # CSV 파일에 저장
            file_path = 'data/고객정보.csv'
            file_exists = pd.io.common.file_exists(file_path)
            full_data.to_csv(file_path, mode='a', header=not file_exists, index=False)

            st.text(f"고객 정보가 {file_path}에 저장되었습니다.")

            # 문자 발송
            clicksend_username = st.secrets["CLICKSEND"]["CLICKSEND_USERNAME"]
            clicksend_api_key = st.secrets["CLICKSEND"]["CLICKSEND_API_KEY"]
            to_number = "+82" + 휴대폰번호[1:]  # 국내 번호 형식으로 변환
            message_body = f"안녕하세요! 고객님을 환영합니다. {이름}님의 클러스터 ID는 {Cluster}입니다."

            # ClickSend API 호출 (문자 발송)
            url = "https://rest.clicksend.com/v3/sms/send"
            auth_header = f"Basic {base64.b64encode(f'{clicksend_username}:{clicksend_api_key}'.encode()).decode()}"

            headers = {"Authorization": auth_header, "Content-Type": "application/json"}

            data = {"messages": [{"source": "sdk", "body": message_body, "to": to_number}]}

            try:
                response = requests.post(url, headers=headers, json=data)
                st.success("문자가 성공적으로 발송되었습니다.")
            except Exception as e:
                st.error("문자 발송에 실패했습니다.")
                print("Error sending SMS:", e)

            # 이메일 발송
            promo_email.send_promotion_email(이메일, 이름, Cluster)
            st.success(f"이메일이 성공적으로 발송되었습니다.{이름}님의 클러스터 ID는 {Cluster}입니다.")

if __name__ == "__main__":

    run_input_customer_info()
