import time
import schedule
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.text import MIMEText
import smtplib
from crypto_util import decrypt_password 


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモードを有効にする
    options.add_argument('--disable-gpu')  # GPUを無効にする（ヘッドレスモードで推奨）
    return webdriver.Chrome(options=options)

def scrape_notifications(user_id, password):
    driver = webdriver.Chrome()  # 適切なWebDriverを指定してください

    try:
        # 1. ログイン
        #URLが変更されて、ログインのエラーが面からスタートされるように変更をした
        driver.get("REDACTED_CP_URL")
        # 「ログイン画面へ」ボタンをクリック
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="ログイン画面へ"]').click()
        driver.find_element(By.NAME, "userId").send_keys(user_id)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "loginButton").click()

        # 2. ログイン完了後、「すべて見る」をクリック
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "すべて見る"))
        ).click()

        notifications = []

        # 「レポート提出期限通知」と「レポート評価通知」の両方を処理
        for link_text in ["レポート提出期限通知", "レポート評価通知"]:
            try:
                report_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text))
                )
                report_link.click()

                # 5件分のデータを収集
                for i in range(5):
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "cs_table3a"))
                        )
                        detail_table = driver.find_element(By.CLASS_NAME, "cs_table3a")
                        rows = detail_table.find_elements(By.TAG_NAME, "tr")

                        notification = {
                            "発信日時": rows[2].find_elements(By.TAG_NAME, "td")[0].text,
                            "関連講義名": rows[4].find_elements(By.TAG_NAME, "td")[0].text,
                            "内容": rows[5].find_elements(By.TAG_NAME, "td")[0].text.strip(),
                            "種類": link_text
                        }
                        notifications.append(notification)

                        # 「次へ」ボタンをクリックして次の通知へ
                        next_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@class='cs_submitBt changeProcessed' and @value='次へ']"))
                        )
                        next_button.click()
                        time.sleep(1)
                    except Exception as e:
                        print(f"{link_text}でエラーが発生しました: {e}")
                        break

                # 一覧に戻る（必要に応じて）
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "すべて見る"))
                )
            except Exception as e:
                print(f"{link_text}のリンクが見つかりません: {e}")

        return notifications
    finally:
        driver.quit()

def send_email(email_address, password, recipient, notifications):
    # メール本文の生成
    if notifications:
        body = "\n\n".join(
            f"【発信日時】{n['発信日時']}\n【関連講義名】{n['関連講義名']}\n【内容】{n['内容']}"
            for n in notifications
        )
    else:
        body = "お知らせが見つかりませんでした。"

    # メールの設定
    message = MIMEText(body)
    message["Subject"] = "CoursePower お知らせメール"
    message["From"] = email_address
    message["To"] = recipient

    # Gmail SMTPサーバーで送信
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, password)
        smtp.send_message(message)

# JSONファイルからユーザーデータを読み込む
def load_user_data():
    with open("user_data.json", "r", encoding="utf-8") as file:
        return json.load(file)


# ユーザーごとのジョブを生成
def create_job(user_data):
    def job():
        user_id = user_data["user_id"]
        encrypted_password = user_data["password"]
        password = decrypt_password(encrypted_password)
        recipient_email = user_data["recipient_email"]
        
        # 固定送信元情報（アプリパスワードを使うGmailアカウント）
        gmail_app_password = "送信元のアプリパスワード"  # ←アプリパスワード
        email_address = "送信元のメールアドレス"  # ←送信元

        # 通知をスクレイピングしてメールを送信
        notifications = scrape_notifications(user_id, password)
        send_email(email_address, gmail_app_password, recipient_email, notifications)
        print(f"{user_id} にお知らせのメールを送信しました！")
    
    return job

# 各ユーザーに対してスケジューリング
user_data_list = load_user_data()
for user_data in user_data_list:
    schedule_time = user_data["schedule"]
    schedule.every().day.at(schedule_time).do(create_job(user_data))
    print(f"{user_data['user_id']} のスケジュールを {schedule_time} に登録しました")

# メインループ
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)