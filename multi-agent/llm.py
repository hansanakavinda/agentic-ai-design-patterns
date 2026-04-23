import requests
import json
from dotenv import load_dotenv
import os

import tools

tools_ = tools.get_available_tools()

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def agent(messages, model):
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "model": model,
      "messages": messages,
      "tools": tools_,
    })
  )

  if response.status_code != 200:
    raise Exception(f"Error while generating code: {response.status_code} - {response.text}")

  data = response.json()

  return data['choices'][0]['message']