import requests
import json

# FastAPI 服务器地址
url = "http://127.0.0.1:8000/chat/"

# 请求数据：这里你可以自定义 prompt 和 model
data = {
    "prompt": "今天是几月几日？",
    "model": "deepseek-r1:1.5b"
}

# 发送 POST 请求到 FastAPI
response = requests.post(url, json=data)

# 打印响应结果
if response.status_code == 200:
    print("请求成功！")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))  # 确保中文显示正常
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("错误信息：", response.text)
