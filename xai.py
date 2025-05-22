import os
import sys
import requests
import yaml

config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
if not os.path.exists(config_path):
    print("未找到config.yaml，请先创建并配置API KEY！")
    sys.exit(1)

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
api_key = config.get('xai', {}).get('api_key')
if not api_key:
    print("config.yaml中未找到[xai][api_key]，请检查配置！")
    sys.exit(1)

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

print("欢迎使用XAI对话助手，输入exit或quit退出。\n")
while True:
    question = input("请输入你的问题：")
    if question.strip().lower() in ("exit", "quit"):
        print("已退出。")
        break
    if not question.strip():
        continue
    payload = {
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ],
        "search_parameters": {
            "mode": "auto"
        },
        "model": "grok-3-latest"
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        data = response.json()
        print("AI：" + data["choices"][0]["message"]["content"] + "\n")
    except Exception as e:
        print("请求失败或解析出错：", e)
        print(response.text)