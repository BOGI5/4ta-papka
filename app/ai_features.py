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
  ingridients and number_of_meals. If needed, work only in kg or grams, nor pounds.

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

  ## number_of_meals should me more than 1!             

  ## User Input
  This is the user's input. It is very imoprtant!!!'''
               f"{input_formatted}"
               '''
  VERY IMPORTANT:the number of the recipes in the json should be = (number_of_meals from the input)*7 + 2

  ##Error
  If there is any error and you can't complete the task just print a
  dictionary like this and replace your message with the reason of the error:
  {"error": your message}
  
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


    return calendar


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
  ingridients and number_of_meals. If needed, work only in kg or grams, nor pounds.

  #Make it like this example
  {
      "label": "Vegetable Stir Fry",
      "totalTime": 30,
      "calories": 300,
      "ingredients": "1 cup broccoli, 1 bell pepper, 1 carrot, 1 onion, 2 tbsp soy sauce",
      "instructions": "1. Chop vegetables. 2. Heat oil in a pan. 3. Add vegetables and stir-fry for 10 minutes. 4. Add soy sauce and cook for another 5 minutes. 5. Serve hot.",
      "number_of_meals": 4
  }

  ##Error
  If there is any error(for examle cant find a real meal or you find
  more than 1 meal) and you can't complete the task just print a
  dictionary like this and replace your message with the reason of the error:
  {"error": your message}
  
  #Context
  ##The result of your answer is used in a function directly, so make sure it is in json!!
  Also this function is very important for me.

  #Notes
  Don't include '''
                    ''' in your answer. Your answer should start with { and end with }
  Also make sure that the calories are realistic for 1 portion

  ##CAUTION if image has no meal, make this dict: {"error": <explanaition of the error>}!!!
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
    if recipe.get("error") is not None:
      raise Exception
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
  ingridients and number_of_meals. If needed, work only in kg or grams, nor pounds.

  #Make it like this example
  {
      "label": "Vegetable Stir Fry",
      "totalTime": 30,
      "calories": 300,
      "ingredients": "1 cup broccoli, 1 bell pepper, 1 carrot, 1 onion, 2 tbsp soy sauce",
      "instructions": "1. Chop vegetables. 2. Heat oil in a pan. 3. Add vegetables and stir-fry for 10 minutes. 4. Add soy sauce and cook for another 5 minutes. 5. Serve hot.",
      "number_of_meals": 4
  }

  ##Error
  If there is any error(for example you can't find any products) and
  you can't complete the task just print a dictionary like this and
  replace your message with the reason of the error:
  {"error": your message}
  
  #Context
  ##The result of your answer is used in a function directly, so make sure it is in json!!
  Also this function is very important for me.

  #Notes
  Don't include '''
                    ''' in your answer. Your answer should start with { and end with }
  Also make sure that the calories are realistic for 1 portion

  ##CAUTION if image has no groceries, make this dict: {"error": <explanaition of the error>}!!!
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
    if recipe.get("error") is not None:
      raise Exception
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

  #Notes
  Мake sure there are no duplicate groceries.
  ''')

    response = client.chat.completions.create(model="gpt-4",
                                              messages=[{
                                                  "role": "user",
                                                  "content": content
                                              }])

    response_content = response.choices[0].message.content

    shopping_list = response_content.split(',')

    return shopping_list
