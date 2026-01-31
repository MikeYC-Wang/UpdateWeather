import requests
import os
import re

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
    res = requests.get(URL)
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
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 替換註解中的內容
    pattern = r".*?"
    replacement = f"\n\n> {weather_str}\n\n"
    
    if re.search(pattern, content, flags=re.DOTALL):
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open("README.md", "w", encoding="utf-8") as f:
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