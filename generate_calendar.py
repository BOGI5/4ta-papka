from openai import OpenAI
import json

with open("key.txt", "r") as file:
    key = file.read()

client = OpenAI(api_key = key)

def generate_recipes(input_info):
    input_formatted = '\n'.join([f"{key}: {value}" for key, value in input_info.items()])
    print("start")
    content = (
        "You are a cooking assistant. Make a list of 10 recipes. Format them like a json file and print ONLY then info.You should have label, totalTime(Time to make), calories, instructions(step by step in one string), ingridients and number_of_meals:\n"
        "Use this info:\n"
        f"{input_formatted}"
    )

    
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
    print("recipes_string:", recipes_string)  # Debugging print
    recipes = string_to_dictionary(recipes_string)
    print("recipes:", recipes) 
    
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
        
        if meals_per_week >= (8-day) * 7:
            calendar[meal_day].append(sorted_recipes_desc[recipes_index]["label"])
            meals_per_week -= int(sorted_recipes_desc[recipes_index]["number_of_meals"])
            recipes_index += 1
            
    return calendar




    

input_info = {
  "cuisine_preference": "Italian, Mexican",
  "favorite_foods": ["lasagna", "tacos", "sushi"],
  "dietary_restrictions": "none",
  "dislikes_allergies": ["shellfish"],
  "cooking_skill_level": "intermediate",
  "specific_appliances": ["slow cooker", "blender"],
  "available_prep_time": "30 to 45 minutes",
  "meals_per_day": 3
}

print(calculate_calendar(input_info))
