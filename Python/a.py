import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import undetected_chromedriver as uc

def setup_driver():
    """Cấu hình trình duyệt"""
    options = Options()
    options.add_argument("--headless")  # Chạy ở chế độ không hiển thị trình duyệt
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    return driver

def login_garena(driver, username, password):
    """Đăng nhập tài khoản Garena"""
    driver.get("https://www.garena.sg/login")

    try:
        # Điền thông tin đăng nhập
        time.sleep(2)
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
        
        # Chờ đợi sau khi gửi thông tin
        time.sleep(5)

        # Kiểm tra kết quả đăng nhập
        if "dashboard" in driver.current_url:
            status = "success"
        else:
            status = "failed"

    except Exception as e:
        status = f"error: {e}"
    return status

def check_account_links(driver):
    """Kiểm tra liên kết email và số điện thoại"""
    email_linked = False
    phone_linked = False

    try:
        # Truy cập vào cài đặt tài khoản
        driver.get("https://www.garena.sg/settings")
        time.sleep(5)

        # Kiểm tra liên kết email
        email_section = driver.find_element(By.XPATH, "//div[contains(text(),'Email')]")
        if "Đã liên kết" in email_section.text:
            email_linked = True

        # Kiểm tra liên kết số điện thoại
        phone_section = driver.find_element(By.XPATH, "//div[contains(text(),'Số điện thoại')]")
        if "Đã liên kết" in phone_section.text:
            phone_linked = True

    except Exception as e:
        print(f"Lỗi khi kiểm tra liên kết: {e}")
    
    return email_linked, phone_linked

def main():
    # Đọc danh sách tài khoản từ file CSV
    accounts = pd.read_csv("accounts.csv")
    results = []

    # Khởi tạo trình duyệt
    driver = setup_driver()

    for index, row in accounts.iterrows():
        username = row['username']
        password = row['password']
        
        print(f"Đang kiểm tra tài khoản: {username}")
        
        # Đăng nhập
        status = login_garena(driver, username, password)

        # Nếu đăng nhập thành công, kiểm tra trạng thái liên kết
        email_linked, phone_linked = False, False
        if status == "success":
            email_linked, phone_linked = check_account_links(driver)

        # Lưu kết quả
        results.append({
            "username": username,
            "status": status,
            "email_linked": email_linked,
            "phone_linked": phone_linked
        })

    # Lưu kết quả vào file CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("results.csv", index=False)
    print("Kiểm tra hoàn tất. Kết quả được lưu vào file 'results.csv'.")

    driver.quit()

if __name__ == "__main__":
    main()
