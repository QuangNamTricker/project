import requests

def get_ip_info(ip=""):
    """
    Lấy thông tin vị trí cụ thể dựa trên địa chỉ IP.
    Nếu không nhập IP, API sẽ trả thông tin IP công khai hiện tại của bạn.
    """
    try:
        # Sử dụng ipinfo.io API để lấy thông tin IP
        url = f"https://ipinfo.io/{ip}/json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            location = data.get("loc", "Không rõ").split(",")
            latitude, longitude = location if len(location) == 2 else ("Không rõ", "Không rõ")

            # Hiển thị thông tin
            print(f"Địa chỉ IP: {data.get('ip', 'Không rõ')}")
            print(f"Thành phố: {data.get('city', 'Không rõ')}")
            print(f"Khu vực: {data.get('region', 'Không rõ')}")
            print(f"Quốc gia: {data.get('country', 'Không rõ')}")
            print(f"Vĩ độ: {latitude}")
            print(f"Kinh độ: {longitude}")
            print(f"Nhà cung cấp mạng: {data.get('org', 'Không rõ')}")
        else:
            print("Không thể lấy thông tin IP. Kiểm tra lại địa chỉ IP hoặc API.")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

if __name__ == "__main__":
    # Nhập địa chỉ IP (để trống để kiểm tra IP công khai của chính bạn)
    ip_to_check = input("Nhập địa chỉ IP cần kiểm tra (để trống nếu kiểm tra IP của bạn): ").strip()
    get_ip_info(ip_to_check)
