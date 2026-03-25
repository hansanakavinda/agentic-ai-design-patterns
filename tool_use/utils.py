from agents import agent
from tools import get_current_time, get_weather_from_ip, write_txt_file, generate_qr_code
import json

TOOL_MAPPING = {
    "get_current_time": get_current_time,
    "get_weather_from_ip": get_weather_from_ip,
    "write_txt_file": write_txt_file,
    "generate_qr_code": generate_qr_code
}

def get_response(messages, model):
    
    response = agent(messages, model=model)
    return response

def get_tool_response(tool_call):
    function_name = tool_call["function"]["name"]
    tool_args = json.loads(tool_call["function"]["arguments"])
    tool_output = TOOL_MAPPING[function_name](**tool_args)

    print(f"Executing {function_name}... Result: {tool_output}")

    return {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": json.dumps(tool_output),
    }

    