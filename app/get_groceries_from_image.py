import base64
import requests

with open("key.txt", "r") as file:
    key = file.read()

def get_groceries_from_image(imagebase64_image_path):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Make a list with ALL the Groceries in this image. Print only the groceries and nothing else. Print ONLY their names!!"
            "Example:"
            "bananas"
            "tomatoes"
            "onion"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    print(type(response.json()))
    print()
    print()
    print()
    response_content = response.json()["choices"][0]["message"]["content"]
    return response_content

