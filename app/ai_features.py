import json

import requests
from openai import OpenAI

with open("key.txt", "r") as file:
    key = file.read()

client = OpenAI(api_key=key)


def generate_recipes(input_info):
    input_formatted = "\n".join(
        [f"{key}: {value}" for key, value in input_info.items()]
    )
    print("start")
    content = (
        "You are a cooking assistant. Make a list of 10 recipes. The recipes should be something that the person can eat for a whole meal like a whole dinner or breackfast. Format them like a json file and print ONLY then info.You should have label, totalTime(Time to make in minutes), calories, instructions(step by step in one string), ingridients and number_of_meals:\n"
        "This is the user's input. It is very imoprtant!!!:\n"
        f"{input_formatted}"
        "The last variable is mod. If it is fitness, aim for higher protein and healthy meals. If it is Taste aim for tastier meals. Also you don't have to make 100% of the recipes with the prefered meals but 60%"
        "Use ONLY this scheme:"
        """
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "label": {
        "type": "string"
      },
      "totalTime": {
        "type": "int"
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
      }
    },
    "required": ["label", "totalTime", "calories", "ingredients", "instructions", "number_of_meals"],
    "additionalProperties": false
  }
"""
    )

    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": content}]
    )

    response_content = response.choices[0].message.content
    return response_content


def string_to_dictionary(string):
    try:
        dictionary = json.loads(string)
        return dictionary
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse string as JSON: {e}"}


def calculate_calendar(input):
    recipes_string = generate_recipes(input)
    recipes = string_to_dictionary(recipes_string)
    if "error" in recipes:
        return recipes

    sorted_recipes_desc = sorted(
        recipes, key=lambda x: x["number_of_meals"], reverse=True
    )

    calendar = {}
    day = 1

    meals_per_day = input["meals_per_day"]
    meals_per_week = int(meals_per_day) * 7

    recipes_index = 0

    for day in range(1, 8):
        meal_day = f"Day {day}"
        calendar[meal_day] = []

        while meals_per_week >= (7 - day) * int(meals_per_day):
            calendar[meal_day].append(sorted_recipes_desc[recipes_index])
            meals_per_week -= int(sorted_recipes_desc[recipes_index]["number_of_meals"])
            recipes_index += 1

    print(calendar)
    return calendar


def generate_email(input_info):
    content = (
        "Write an email where you order this ingrideints, location, and phone number:i\n"
        f"{input_info}"
        "Write ONLY the email body! Make it so it is ready to be send directly. Don't generate thing like [name]!!!"
    )

    response = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": content}]
    )

    response_content = response.choices[0].message.content
    return response_content


def generate_recipe_from_meal_image(imagebase64_image_path):
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
                        "Recognize what is the meal that you see and make a recipe for. You are able to recognize exactly 1 meal at every image!!! It is very imoprtant!!! You can add or replace something small. You don't have to use all of them.:\n"
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
  }"''',
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


def generate_recipe_from_groceries_image(imagebase64_image_path):
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
  }"''',
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
