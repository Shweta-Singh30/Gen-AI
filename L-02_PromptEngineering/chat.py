from dotenv import load_dotenv
from openai import OpenAI
 
load_dotenv()

client=OpenAI()

system_promt="""
you arean AI Assistent who is specialized in maths.
you should not answer any quary thatisnot related to maths.

for a given quary help user to solve that along with explanations.

example:
input:2+2
output:2+2 is 4 which i calculated by adding 2 with 2.

input:what is your name?
output:bruh? what are you asking? are you ok?is it math question? 
"""



result = client.chat.completions.create(
    model="gpt-4",
    temperature=0.5,  
    max_tokens=30,
    messages=[
        {"role": "system", "content": system_promt},
        {"role": "user", "content": "what is today weather"}
    ]
)


print(result.choices[0].message.content)
