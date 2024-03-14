from openai import OpenAI


with open("key.txt", "r") as file:
    key = file.read()

client = OpenAI(api_key = key)

def generate_instructions(label, ingredients, time_to_make):
    ingredients_formatted = '\n'.join([f"- {ingredient}" for ingredient in ingredients])
    
    content = (
        f"Return only the reception for this:\n"
        f"Label: {label}\n"
        f"Ingredients:\n"
        f"{ingredients_formatted}\n"
        f"Time to make: {time_to_make}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}]
    )

    response_content = response.choices[0].message.content
    return response_content
