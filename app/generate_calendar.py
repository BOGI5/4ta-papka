from openai import OpenAI
import json

with open("key.txt", "r") as file:
    key = file.read()

client = OpenAI(api_key = key)

def generate_recipes(input_info):
    input_formatted = '\n'.join([f"{key}: {value}" for key, value in input_info.items()])
    print("start")
    content = (
        "You are a cooking assistant. Make a list of 10 recipes. Format them like a json file and print ONLY then info.You should have label, totalTime(Time to make in minutes), calories, instructions(step by step in one string), ingridients and number_of_meals:\n"
        "This is the user's input. It is very imoprtant!!!:\n"
        f"{input_formatted}"
        "Use ONLY this scheme:"'''
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
''')

    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}]
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
    if 'error' in recipes:
        return recipes
    
    sorted_recipes_desc = sorted(recipes, key=lambda x: x["number_of_meals"], reverse=True)
    
    calendar = {}
    day = 1
    
    meals_per_day = input["meals_per_day"]
    meals_per_week = int(meals_per_day)*7

    recipes_index = 0
    
    for day in range(1, 8):
        meal_day = f"Day {day}"
        calendar[meal_day] = []
        
        if meals_per_week >= (7-day) * int(meals_per_day):
            calendar[meal_day].append(sorted_recipes_desc[recipes_index])
            meals_per_week -= int(sorted_recipes_desc[recipes_index]["number_of_meals"])
            recipes_index += 1
            
    return calendar
