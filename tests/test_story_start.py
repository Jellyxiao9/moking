"""
测试故事开始 API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

url = "http://localhost:8000/story/start"
data = {
    "world": "noir",
    "opening": "我是一个侦探"
}

response = requests.post(url, json=data)
print(f"状态码: {response.status_code}")
print(f"返回内容: {response.text}")