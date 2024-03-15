import requests
import base64
import json

with open("key.txt", "r") as file:
    key = file.read()

def string_to_dictionary(string):
    try:
        dictionary = json.loads(string)
        return dictionary
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse string as JSON: {e}"}


def recipe_from_image(imagebase64_image_path):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        
                        "text": "You are a cooking assistant. Make a recipe. Format it like a json file and print ONLY the info.You should have label, totalTime(Time to make), calories, instructions(step by step in one string), ingridients and number_of_meals.\n"
        "Use the ingridients that you see!!! It is very imoprtant!!! You can add or replace something small. You don't have to use all of them.:\n"
        '''"Use ONLY this scheme AND RETURN only A VALID! JSON: (DONT INCLUDE ```json ```)"
    "{"
    "type": "object",
    "properties": {
      "label": {
        "type": "string"
      },
      "totalTime": {
        "type": "string"
      },
      "calories": {
        "type": "int"
      },
      "ingredients": {
        "type": "string"
        }
      },
      "instructions": {
        "type": "string"
      },
      "number_of_meals": {
        "type": "int"
      },
    "required": ["label", "totalTime", "calories", "ingredients", "instructions", "number_of_meals"],
    "additionalProperties": false
    "}"
  }"'''
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{imagebase64_image_path}"
                        },
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    response_content = response.json()["choices"][0]["message"]["content"]
    recipe = string_to_dictionary(response_content)
    return recipe
