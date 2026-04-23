import requests
import json
from dotenv import load_dotenv
import os

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
      "tools": [
        {
          "type": "function",
          "function": {
            "name": "get_current_time",
            "description": "Get the current time",
            "parameters": {
              "type": "object",
              "properties": {}, 
              "required": []
            }
          }
        },
        {
          "type": "function",
          "function": {
            "name": "get_weather_from_ip",
            "description": "Get the current weather for the user's location",
            "parameters": {
              "type": "object",
              "properties": {}, 
              "required": []
            }
          }
        },
        {
          "type": "function",
          "function": {
            "name": "write_txt_file",
            "description": "Write a text file",
            "parameters": {
              "type": "object",
              "properties": {
                "file_path": {
                  "type": "string",
                  "description": "Path to the file to write"
                },
                "content": {
                  "type": "string",
                  "description": "Content to write to the file"
                }
              },
              "required": ["file_path", "content"]
            }
          }
        },
        {
          "type": "function",
          "function": {
            "name": "generate_qr_code",
            "description": "Generate a QR code",
            "parameters": {
              "type": "object",
              "properties": {
                "data": {
                  "type": "string",
                  "description": "Data to encode in the QR code"
                },
                "filename": {
                  "type": "string",
                  "description": "Name of the output file"
                },
                "image_path": {
                  "type": "string",
                  "description": "Path to the image to use in the QR code"
                }
              },
              "required": ["data", "filename", "image_path"]
            }
          }
        }
      ],
    })
  )

  if response.status_code != 200:
    raise Exception(f"Error while generating code: {response.status_code} - {response.text}")

  data = response.json()

  return data['choices'][0]['message']