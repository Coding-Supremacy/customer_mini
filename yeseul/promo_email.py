import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import pandas as pd



# SMTP 서버 설정
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "qhrehlwl111@gmail.com"
EMAIL_PASSWORD = "nyaw spns mndv gsnb"  # 보안 강화를 위해 앱 비밀번호 사용

# 프로모션 이메일 내용 불러오기
df = pd.read_csv('yeseul/클러스터링별_이메일_UTF8.csv')

# 클러스터 그룹별 랜덤 이메일 선택 함수
def get_random_email_content(cluster_id):
    # 클러스터 ID에 해당하는 이메일 본문과 제목을 랜덤하게 선택하여 반환

    # 해당 클러스터 ID의 데이터 필터링
    cluster_emails = df[df["클러스터 ID"] == cluster_id][["이메일 본문", "제목"]]

    if not cluster_emails.empty:
        # 랜덤으로 하나 선택
        selected_email = cluster_emails.sample(n=1).iloc[0]
        return selected_email["이메일 본문"], selected_email["제목"]
    else:
        return "맞춤 프로모션 정보를 찾을 수 없습니다.", "제목 없음"

def send_promotion_email(이메일, 이름, cluster_id):
        
    random_body, random_subject = get_random_email_content(cluster_id)

    
    # 이메일 제목
    subject = f"[프로모션] {random_subject}"

    # 이메일 본문 (이미지 포함)
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px;">
        <table style="width: 100%; max-width: 800px; margin: auto; background: white; padding: 30px; 
                    border-radius: 15px; box-shadow: 0px 5px 15px rgba(0,0,0,0.1);">
            <!-- 헤더 영역 (로고) -->
            <tr>
                <td style="text-align: center; padding: 20px; background: #005bac; color: white; 
                        border-top-left-radius: 15px; border-top-right-radius: 15px;">
                    <h1 style="margin: 0;">🚗 현대자동차 프로모션 🚗</h1>
                </td>
            </tr>
            
            <!-- 본문 내용 -->
            <tr>
                <td style="padding: 30px; text-align: center;">
                    
                    <!-- 현대 로고 -->
                    <a href="https://www.hyundai.com" target="_blank">
                    <img src="cid:hyundai_logo"
                        alt="현대 로고" style="width: 100%; max-width: 500px; border-radius: 10px;">
                    </a>

                    <p style="font-size: 18px;">안녕하세요, <strong>{이름}</strong>님!</p>

                    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; font-size: 16px; margin-top: 20px;">
                        {random_body}
                    </div>
                    
                    <a href="https://www.hyundai.com" 
                        style="display: inline-block; background: #005bac; color: white; padding: 15px 30px; 
                            text-decoration: none; border-radius: 8px; margin-top: 20px; font-size: 16px;">
                        지금 확인하기
                    </a>
                </td>
            </tr>

            <!-- 푸터 (고객센터 안내) -->
            <tr>
                <td style="padding: 15px; font-size: 14px; text-align: center; color: gray;">
                    ※ 본 메일은 자동 발송되었으며, 문의는 고객센터를 이용해주세요.
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # 이메일 생성
    msg = MIMEMultipart()
    msg["From"] = "현대자동차"
    msg["To"] = 이메일
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

        # 로고 이미지 첨부 (CID 참조)
    with open("img/hyundai_logo.jpg", "rb") as img_file:
        img = MIMEImage(img_file.read())
        img.add_header("Content-ID", "<hyundai_logo>")
        msg.attach(img)

    # SMTP 서버 연결 및 이메일 전송
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # 보안 연결
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, 이메일, msg.as_string())

        print(f"✅ 이메일 전송 완료: {이메일}, 제목: {subject}")
    except Exception as e:
        print(f"🚨 이메일 전송 실패: {str(e)}")