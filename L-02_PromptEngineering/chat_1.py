from dotenv import load_dotenv
from openai import OpenAI
 
load_dotenv()

client=OpenAI()


result = client.chat.completions.create(
    model="gpt-4",
    temperature=0.5,  
    max_tokens=30,
    messages=[
        
        {"role": "user", "content": "what is today weather"}
    ]
)
