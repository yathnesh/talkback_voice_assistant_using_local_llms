import requests
import json

url = "http://localhost:11434/api/generate"

headers = {
  'Content-Type': 'application/json',
}

data = {
  "model": "llama3",
  "stream": False,
  "prompt": "Why is the sky blue?"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
  print(json.loads(response.text)["response"])
else:
  print("Error:",response.status_code, response.text)