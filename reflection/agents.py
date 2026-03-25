import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

def code_generation_agent(prompt, model):
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "model": model,
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ],
      "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "code",
        "strict": True,
        "schema": {
          "type": "object",
          "properties": {
            "python_code": {
              "type": "string",
              "description": "python code to generate chart",
            }
          },
          "required": ["python_code"],
          "additionalProperties": False,
        },
      },
    },
    })
  )

  if response.status_code != 200:
    raise Exception(f"Error while generating code: {response.status_code} - {response.text}")

  data = response.json()

  return data['choices'][0]['message']['content']


def reflect_and_regenerate_agent(prompt, model, media_type,b64):

  data_url = f"data:{media_type};base64,{b64}"

  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    },
    data=json.dumps({
      "model": model,
      "messages": [
        {
          "role": "user",
          "content": [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ]
        }
      ],
      "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "feedback and code",
        "strict": True,
        "schema": {
          "type": "object",
          "properties": {
            "feedback": {
              "type": "string",
              "description": "feedback on the chart",
            },
            "python_code": {
              "type": "string",
              "description": "python code to generate chart",
            }
          },
          "required": ["feedback","python_code"],
          "additionalProperties": False,
        },
      },
    },
    })
  )

  if response.status_code != 200:
    raise Exception(f"Error while reflecting on chart: {response.status_code} - {response.text}")

  data = response.json()

  return data['choices'][0]['message']['content']