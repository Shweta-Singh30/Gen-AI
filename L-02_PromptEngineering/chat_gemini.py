from google import genai
from google.genai import types

client=genai.Client(api_key='AIzaSyD_74-r7KWENYlV6pw7pc10c9J2hHTiqqk')

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)

print(response.text)