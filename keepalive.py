import time
import requests

# 替换成你的 Streamlit 应用网址
URL = "https://bid-rent-model-aj7q2woidzrypoxjgvpsaw.streamlit.app/"

def keep_alive():
    while True:
        try:
            r = requests.get(URL, timeout=10)
            print("Ping:", r.status_code)
        except Exception as e:
            print("Error:", e)
        time.sleep(600)  # 每 10 分钟访问一次

if __name__ == "__main__":
    keep_alive()
