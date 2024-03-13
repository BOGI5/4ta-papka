from openai import OpenAI

with open("key.txt", "r") as file:
    key = file.read()

client = OpenAI(api_key = key)

response = client.chat.completions.create(
    model="gpt-4", 
    messages=[{"role": "user", "content": "Kolko e 2+2"}]
)

response_content = response.choices[0].message.content
print(response_content)
