import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def get_weather(str):
    return "35 degree cel."

system_prompt = f"""
    You are an helpfull AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""







messages={
    {"role":"system","content":system_prompt}
    
}

quary=input(">")

messages.append({"role":"user","content":quary})



question=input("> ")

while True:
    result = client.chat.completions.create(
        model="gpt-4",
        temperature=0.5,  
        max_tokens=200,
        messages=messages
    )

    parsed_output=json.loads(result.choices[0].message.content)
    messages.append({"role":"assitent","content":json.dumps(parsed_output)})


