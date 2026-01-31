import requests
import os
import re
import urllib3

# 關閉 SSL 警告 (因為我們要略過驗證)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 設定基隆市
LOCATION = "基隆市"
API_KEY = os.getenv("CWA_API_KEY")
URL = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={API_KEY}&locationName={LOCATION}"

def get_weather_emoji(wx):
    if "雨" in wx: return "🌧️"
    if "雲" in wx and "晴" in wx: return "⛅"
    if "雲" in wx: return "☁️"
    if "晴" in wx: return "☀️"
    return "✨"

def get_weather():
    # 關鍵修改：加入 verify=False 來略過 SSL 驗證
    res = requests.get(URL, verify=False)
    data = res.json()
    
    # 取得氣象資料
    location_data = data['records']['location'][0]['weatherElement']
    
    # 解析數據 (取當前時段)
    wx = location_data[0]['time'][0]['parameter']['parameterName']    # 天氣現象
    pop = location_data[1]['time'][0]['parameter']['parameterName']   # 降雨機率
    min_t = location_data[2]['time'][0]['parameter']['parameterName'] # 最低溫
    max_t = location_data[4]['time'][0]['parameter']['parameterName'] # 最高溫
    
    emoji = get_weather_emoji(wx)
    
    # 格式化輸出
    return f"{emoji} **{LOCATION}目前天氣**：{wx} | 🌡️ {min_t}-{max_t}°C | ☔ 降雨機率 {pop}%"

def update_readme(weather_str):
    # 取得腳本所在的絕對路徑 (確保在任何地方執行都找得到檔案)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "README.md")

    if not os.path.exists(file_path):
        print(f"Error: README.md not found at {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 替換註解中的內容
    pattern = r".*?"
    replacement = f"\n\n> {weather_str}\n\n"
    
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README updated successfully!")
    else:
        print("Error: Could not find markers in README.md")

if __name__ == "__main__":
    if not API_KEY:
        print("Error: CWA_API_KEY is not set.")
    else:
        try:
            weather_info = get_weather()
            update_readme(weather_info)
        except Exception as e:
            print(f"An error occurred: {e}")
