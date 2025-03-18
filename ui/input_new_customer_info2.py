import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import re
from num2words import num2words
import requests
import base64
import time

import ui.promo_email as promo_email




# # secrets.toml에서 client_id와 client_secret 불러오기
# client_id = st.secrets["KAKAO"]["client_id"]
# redirect_uri = st.secrets["KAKAO"]["redirect_uri"]


# 클러스터 ID에 대한 설명
cluster_description = {
    0: ("고연령층 세단 구매 고객", "50대 후반, 준중형 세단 선호, 카드 결제, 거래 금액 높음,주로 VIP 고객"),
    1: ("고급차 VIP 고객", "40~50대, 고급 세단(G80, G70 등) 구매, 거래 금액 높음,주로 VIP 고객"),
    2: ("SUV 패밀리 고객", "30~40대, 중형대형 SUV 선호, 가족용 차량, 주로 일반 고객"),
    3: ("신차 선호 고객", "최근 출시된 차량 구매, 반복 구매 가능성 높음, 주로 신규 고객"),
    4: ("경제형 차량 구매 고객", "30~40대, 보급형 세단(아반떼, 쏘나타) 구매, 카드 결제, 주로 일반 고객"),
    5: ("현금 구매 고객", "50대 이상, 중고차 및 SUV 구매, 현금 결제 비율 높음, 주로 일반 고객")
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

# 숫자를 한글로 변환하는 함수 (천 단위 포맷 처리)
def number_to_korean(num):
    if num == 0:
        return "0 원"  # 0일 경우 처리
    return num2words(num, to='currency', lang='ko')

# # 카카오 로그인 URL 생성
# def create_kakao_login_url():
#     KAKAO_CLIENT_ID = client_id
#     REDIRECT_URI = redirect_uri  # 리디렉션 URI
#     KAKAO_AUTH_URL = f"https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={KAKAO_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
#     return KAKAO_AUTH_URL

# 카카오 OAuth 인증 코드로 액세스 토큰을 얻는 함수
#앱 키 secret.toml에서 가져오기


# def get_access_token_from_kakao(code):
#     url = "https://kauth.kakao.com/oauth/token"


#     data = {
#         "grant_type": "authorization_code",
#         "client_id": client_id,  # 카카오 개발자 센터에서 받은 앱 키
#         "redirect_uri": redirect_uri,  # 리디렉션 URI
#         "code": code
#     }
#     response = requests.post(url, data=data)
#     if response.status_code == 200:
#         access_token = response.json().get("access_token")
#         return access_token
#     else:
#         st.error("액세스 토큰 발급 실패")
#         return None

# # 카카오톡 메시지 전송 함수
# def send_kakao_message_to_customer(access_token):
#     kakao_url = "http://pf.kakao.com/_lkVXn"  # 카카오 채널 URL
#     message = f"안녕하세요! 카카오톡 친구 추가를 통해 다양한 혜택을 확인해보세요! {kakao_url}"

#     url = "https://kapi.kakao.com/v2/api/talk/memo/send"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "template_object": {
#             "object_type": "text",
#             "text": message,
#             "link": {
#                 "web_url": kakao_url,
#                 "mobile_web_url": kakao_url
#             }
#         }
#     }

#     response = requests.post(url, headers=headers, json=data)

#     if response.status_code == 200:
#         st.success("카카오톡 친구 추가 링크가 성공적으로 전송되었습니다!")
#     else:
#         st.error(f"메시지 전송 실패: {response.status_code}, {response.text}")

def run_input_customer_info():
    # 고객 개인정보 입력.
    st.title('고객 정보 입력')
    

    # 모델 로드
    model = joblib.load("model2.pkl")

    # 입력 폼 생성
    st.header("데이터 입력")
    st.write("고객 정보를 입력하고 예측 버튼을 눌러주세요.")
    
    with st.form(key="customer_info_form"):
        # 사용자 입력 받기 (각각의 입력창에 고유한 key 지정)
        col1, col2 = st.columns([1, 1])
        with col1:
            이름 = st.text_input("이름 입력", key="name_input")
            성별 = st.selectbox("성별 선택", ["남", "여"], key="gender_select")
            휴대폰번호 = st.text_input("휴대폰 번호 입력", key="phone_input")
            # 하이픈을 포함한 휴대폰 번호 포맷팅
            휴대폰번호 = re.sub(r'[^0-9]', '', 휴대폰번호)  # 숫자만 추출

            이메일 = st.text_input("이메일 입력", key="email_input")
            주소 = st.text_input("주소 입력", key="address_input")
            아이디 = st.text_input("아이디 입력", key="id_input")
            가입일 = st.date_input("가입일 입력", min_value=datetime(1900, 1, 1), key="registration_date_input")
            

            # 현재 날짜에서 20년 전의 날짜를 구하기
            today = datetime.today()
            year_20_years_ago = today.replace(year=today.year - 20)

            # 만약 오늘이 2월 29일이라면, 20년 전 날짜가 존재하지 않을 수 있기 때문에, 월과 일을 조정합니다.
            if year_20_years_ago.month == 2 and year_20_years_ago.day == 29:
                year_20_years_ago = year_20_years_ago.replace(day=28)

            # 생년월일 입력 (1900년부터 20년 전 날짜까지 선택 가능)
            생년월일 = st.date_input("생년월일 입력", min_value=datetime(1900, 1, 1), max_value=year_20_years_ago, key="dob_input")
            if 생년월일:
                today = datetime.today()
                연령 = today.year - 생년월일.year - ((today.month, today.day) < (생년월일.month, 생년월일.day))
                st.write(f"계산된 나이: {연령}세")
        with col2:
            
            고객세그먼트 = st.selectbox("고객 세그먼트 선택", ["신규","VIP", "일반","이탈가능"], index=0, key="customer_segment_select")
            # 거래금액 입력 (천 단위로 입력받기)
            거래금액 = st.number_input("거래 금액 입력", min_value=0, step=1000000, key="transaction_amount_input")
            
            # 입력한 거래금액을 천 단위로 표시
            거래금액_한글 = number_to_korean(int(거래금액))
            st.write(f"입력하신 금액: {거래금액_한글}")

            구매빈도 = st.number_input("제품 구매 빈도 입력", min_value=1, step=1, key="purchase_frequency_input")
            차량구분 = st.selectbox("차량 구분 선택", ["준중형 세단", "중형 세단", "대형 세단", "SUV", "픽업트럭"], key="vehicle_type_select")
            거래방식 = st.selectbox("거래 방식 선택", ["카드", "현금", "계좌이체"], key="transaction_method_select")
            구매경로 = st.selectbox("구매 경로 선택", ["온라인", "오프라인"], key="purchase_path_select")

            # 구매한 제품 선택
            구매한제품 = st.selectbox("구입 모델 선택", list(launch_dates.keys()), key="purchased_product_select")
            제품구매날짜 = st.date_input("제품 구매 날짜 입력", min_value=datetime(1900, 1, 1), key="purchase_date_input")

            # 선택된 제품에 따른 자동 출시 년월 매핑
            제품출시년월 = launch_dates.get(구매한제품, "")
            
            if 제품출시년월:
                st.write(f"선택하신 모델의 출시 년월: {제품출시년월}")

            # 이메일 검사 (@ 포함 여부 확인)
            if '@' not in 이메일:
                st.error("이메일에 '@' 문자가 포함되어야 합니다.")
                return
            
            # 휴대폰 번호가 11자리인지 확인
            if len(휴대폰번호) != 11:
                st.error("휴대폰 번호는 11자리 숫자여야 합니다.")
                return
            
        # ✅ 폼 내에서 버튼 추가 (버튼이 보이지 않는 문제 해결됨!)
        submitted = st.form_submit_button("예측하기")
        # 모델에 맞는 컬럼만 사용하여 입력 데이터 준비
        if submitted:
            # 필요한 컬럼만 포함된 데이터프레임 생성
            input_data = pd.DataFrame([[연령, 거래금액, 구매빈도, 성별, 차량구분, 거래방식, 제품출시년월, 제품구매날짜, 고객세그먼트]],
                                    columns=["연령", "거래 금액 (Transaction Amount)", "제품 구매 빈도 (Purchase Frequency)", 
                                            "성별 (Gender)", "차량구분(vehicle types)", "거래 방식 (Transaction Method)", 
                                            "제품 출시년월 (Launch Date)", "제품 구매 날짜 (Purchase Date)", "고객 세그먼트 (Customer Segment)"])

            # 예측 실행
            prediction = model.predict(input_data)
            
            # 예측된 클러스터 ID에 따른 고객 유형 및 특징 출력
            cluster_id = prediction[0]
            customer_type, characteristics = cluster_description.get(cluster_id, ("알 수 없는 클러스터", "특징 정보 없음"))
            
            st.write(f"예측된 클러스터: {cluster_id}")
            st.write(f"고객 유형: {customer_type}")
            st.write(f"특징: {characteristics}")
            # # 예측 후 카카오톡 메시지 전송 (액세스 토큰 필요)
            # access_token = "YOUR_ACCESS_TOKEN"  # 카카오 로그인 후 얻은 액세스 토큰

            # if access_token:
            #     send_kakao_message_to_customer(access_token)

            # 클러스터링 결과와 고객 정보를 데이터프레임에 추가 (전체 고객 정보도 포함)
            input_data["Cluster"] = cluster_id
            # 모든 입력된 고객 정보를 포함하여 데이터 저장
            # 고객 정보를 포함한 데이터프레임 생성
            full_data = pd.DataFrame([[이름, 생년월일, 연령, 성별, 휴대폰번호, 이메일, 주소, 아이디, 가입일, 고객세그먼트, 차량구분, 구매한제품, 제품구매날짜, 거래금액, 거래방식, 구매빈도, 구매경로, 제품출시년월, cluster_id]],
                                    columns=["이름 (Name)", "생년월일 (Date of Birth)","연령", "성별 (Gender)", "휴대폰번호 (Phone Number)", 
                                            "이메일 (Email)", "주소 (Address)", "아이디 (User ID)", "가입일 (Registration Date)", "고객 세그먼트 (Customer Segment)",
                                            "차량구분(vehicle types)", "구매한 제품 (Purchased Product)", "제품 구매 날짜 (Purchase Date)", 
                                            "거래 금액 (Transaction Amount)", "거래 방식 (Transaction Method)", 
                                            "제품 구매 빈도 (Purchase Frequency)", "제품 구매 경로 (Purchase Path)", 
                                            "제품 출시년월 (Launch Date)", "Cluster"])

            # 고객 데이터를 CSV 파일에 추가
            file_path = '클러스터링고객데이터_2.csv'
            file_exists = pd.io.common.file_exists(file_path)

            # 데이터 저장
            full_data.to_csv(file_path, mode='a', header=not file_exists, index=False)
            st.write(f"고객 정보가 {file_path}에 저장되었습니다.")
            print(f"파일 저장 위치: {file_path}")

            # ClickSend API를 사용하여 SMS 보내기
            clicksend_username = st.secrets["CLICKSEND"]["CLICKSEND_USERNAME"]  # ClickSend 계정 사용자 이름
            clicksend_api_key = st.secrets["CLICKSEND"]["CLICKSEND_API_KEY"]    # ClickSend API 키

            # 수신자 번호 및 메시지 내용
            to_number = "+82" + 휴대폰번호[1:]
            message_body = f"안녕하세요! 고객님을 환영합니다. 예측된 클러스터: {cluster_id}, 고객 유형: {customer_type}"

            # API 요청 URL 및 헤더 설정
            url = "https://rest.clicksend.com/v3/sms/send"
            auth_header = f"Basic {base64.b64encode(f'{clicksend_username}:{clicksend_api_key}'.encode()).decode()}"

            headers = {
                "Authorization": auth_header,
                "Content-Type": "application/json"
            }

            # 요청 데이터
            data = {
                "messages": [
                    {
                        "source": "sdk",
                        "body": message_body,
                        "to": to_number
                    }
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                print("Message sent successfully:", response.json())
            except Exception as e:
                print("Error sending SMS:", e)


            # 이메일 발송
            promo_email.send_promotion_email(이메일, 이름, cluster_id)

            with st.spinner("이메일 발송 중.."):
                time.sleep(3)
                st.success("이메일이 성공적으로 발송되었습니다.")
    

if __name__ == "__main__":
    run_input_customer_info()
