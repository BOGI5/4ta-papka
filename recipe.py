import requests
from generate_instructions import generate_instructions

app_id = "da7e241d"
app_key = "f7205515fdb6c693a5c6841b413f62b4"

base_url = "https://api.edamam.com/search"

def get_recipe(recipe_name):
    params = {
        "q": recipe_name,
        "app_id": app_id,
        "app_key": app_key
    }

    response = requests.get(base_url, params=params)
    recipe_info = {} 

    if response.status_code == 200:
        data = response.json()
        
        if 'hits' in data and data['hits']:
            hit = data['hits'][0] 
            recipe = hit['recipe']

            recipe_info = {
                "Recipe": recipe['label'],
                "Time to make": recipe['totalTime'],
                "Calories": recipe['calories'],
                "Ingredients": recipe['ingredientLines'],
                "Generated Recipe Reception": generate_instructions(recipe['label'], recipe['ingredientLines'], recipe['totalTime'])
            }
        else:
            recipe_info = {"Error": "No recipe found"}
    else:
        recipe_info = {"Error": f"Failed to fetch recipes. Status code: {response.status_code}"}

    return recipe_info
