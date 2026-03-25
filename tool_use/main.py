from utils import get_response, get_tool_response

system_prompt = """
    You are a helpful assistant.

    your task is to answer the user prompt

    You have given access to the following tools

    - get_current_time(): returns the current time as string
    - get_weather_from_ip(): returns the current weather for the user's location
    - write_txt_file(file_path: str, content: str): writes a string into a .txt file (overwrites if exists)
    - generate_qr_code(data: str, filename: str, image_path: str): generates a QR code image given data and an image path

    """

prompt = "Can you help me create a qr code that goes to www.hansanakavinda.me from the image logo.png? Also write me a txt note with the current weather please."
model = "stepfun/step-3.5-flash:free"

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": prompt}
]

def run_workflow():
    
    response = get_response(messages, model)
    
    i = 0
    while response.get("tool_calls") and i < 5:
        i+=1
        print("calling llm for the ", i, " time")
        messages.append(response)
        for tool_call in response["tool_calls"]:
            tool_response = get_tool_response(tool_call)
            messages.append(tool_response)
            
        response = get_response(messages, model)
        print(response['content'])
    

if __name__ == "__main__":
    try:
        run_workflow()
    except Exception as e:
        print(e)