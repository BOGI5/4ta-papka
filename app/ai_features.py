import json
from functools import cache

import requests
from openai import OpenAI

with open("key.txt", "r") as file:
    key = file.read()

client = OpenAI(api_key=key)


def generate_recipes(input_info):
  input_formatted = "\n".join(
      [f"{key}: {value}" for key, value in input_info.items()])
  print("start")
  content = ('''
#Role
You are the best cooking assistant who is also good at programing

#Task
You are a cooking assistant. Make a list of recipes. The recipes should be something
that the person can eat for a whole meal like a whole dinner or breackfast.
Format them like a json file and print ONLY the result.You should have label,
totalTime(Time to make in minutes), calories, instructions(step by step in one string),
ingridients and number_of_meals

## Use only this schema!
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

## User Input
This is the user's input. It is very imoprtant!!!'''
             f"{input_formatted}"
             '''
VERY IMPORTANT:the number of the recipes in the json should be = (number_of_meals from the input)*7 + 2

#Context
The result of your answer is used in a function directly, so make sure it is in json.
Also this function is very important for me.

#Notes
Don't include '''
             ''' in your answer. Your answer should start with [ and end with ]
Also make sure that the calories are realistic for 1 portion
''')

  response = client.chat.completions.create(model="gpt-4-turbo",
                                            messages=[{
                                                "role": "user",
                                                "content": content
                                            }])

  response_content = response.choices[0].message.content
  print(response_content)
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

  sorted_recipes_desc = sorted(recipes,
                               key=lambda x: x["number_of_meals"],
                               reverse=True)

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
      meals_per_week -= int(
          sorted_recipes_desc[recipes_index]["number_of_meals"])
      recipes_index += 1

  print(calendar)
  return calendar


def generate_email(input_info):
  content = (
      "Write an email where you order this ingrideints, location, and phone number:i\n"
      f"{input_info}"
      "Write ONLY the email body! Make it so it is ready to be send directly. Don't generate thing like [name]!!!"
  )

  response = client.chat.completions.create(model="gpt-4",
                                            messages=[{
                                                "role": "user",
                                                "content": content
                                            }])

  response_content = response.choices[0].message.content
  return response_content


@cache
def generate_recipe_from_meal_image(imagebase64_image_path):
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {key}"
  }

  payload = {
      "model":
      "gpt-4-turbo",
      "messages": [{
          "role":
          "user",
          "content": [
              {
                  "type":
                  "text",
                  "text":
                  '''
#Role
You are the best cooking assistant who is also good at programing

#Task
You are given an image. Recognize the meal on the image and generate a recipe for it.
Format it like a json file and print ONLY the result.You should have label,
totalTime(Time to make in minutes), calories, instructions(step by step in one string),
ingridients and number_of_meals

## Use only this schema!
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

#Context
The result of your answer is used in a function directly, so make sure it is in json.
Also this function is very important for me.

#Notes
Don't include '''
                  ''' in your answer. Your answer should start with [ and end with ]
Also make sure that the calories are realistic for 1 portion
''',
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{imagebase64_image_path}"
                  },
              },
          ],
      }],
      "max_tokens":
      300,
  }

  response = requests.post("https://api.openai.com/v1/chat/completions",
                           headers=headers,
                           json=payload)

  response_content = response.json()["choices"][0]["message"]["content"]
  recipe = string_to_dictionary(response_content)
  return recipe


@cache
def generate_recipe_from_groceries_image(imagebase64_image_path):
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {key}"
  }

  payload = {
      "model":
      "gpt-4-vision-preview",
      "messages": [{
          "role":
          "user",
          "content": [
              {
                  "type":
                  "text",
                  "text":
                  '''
#Role
You are the best cooking assistant who is also good at programing

#Task
You are given an image. Recognize all the imgredients on the image and generate a recipe from them. You dont't have to use all the ingredioents. The recipe should be mostly if not 100% of ingredients on the image. If it is needed you can add something small that is very crucial for the recipe but att leat 80% should be from the products we have.
Format it like a json file and print ONLY the result.You should have label,
totalTime(Time to make in minutes), calories, instructions(step by step in one string),
ingridients and number_of_meals

## Use only this schema!
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

#Context
The result of your answer is used in a function directly, so make sure it is in json.
Also this function is very important for me.

#Notes
Don't include '''
                  ''' in your answer. Your answer should start with [ and end with ]
Also make sure that the calories are realistic for 1 portion
''',
              },
              {
                  "type": "image_url",
                  "image_url": {
                      "url": f"data:image/jpeg;base64,{imagebase64_image_path}"
                  },
              },
          ],
      }],
      "max_tokens":
      300,
  }

  response = requests.post("https://api.openai.com/v1/chat/completions",
                           headers=headers,
                           json=payload)

  response_content = response.json()["choices"][0]["message"]["content"]
  recipe = string_to_dictionary(response_content)
  return recipe

def generate_shopping_list(input_info):
  content = (
    '''
#Role
You are cooking assistant.

#Task
You are given some recipes. Make a shopping list with all the groceries, needed to buy.

The recipes:'''
   f"{input_info}"
'''
#Example
eggs,tomatoes,bananas,cheese,milk,bread

#Context
Your answer is put directly in a function to split it by ,. So Format it exactly like the example.
''')

  response = client.chat.completions.create(model="gpt-4",
                                            messages=[{
                                                "role": "user",
                                                "content": content
                                            }])

  response_content = response.choices[0].message.content
  
  shopping_list = response_content.split(',')
  
  return shopping_list
