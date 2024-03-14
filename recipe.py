import requests
from generate_instructions import generate_instructions

app_id = "da7e241d"
app_key = "f7205515fdb6c693a5c6841b413f62b4"

base_url = "https://api.edamam.com/search"

recipe_name = "fries "

params = {
    "q": recipe_name,
    "app_id": app_id,
    "app_key": app_key
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    
    
    
    
    if 'hits' in data:
        for hit in data['hits']:
            recipe = hit['recipe']

            print("Recipe: ", recipe['label'])
            print("Time to make: ", recipe['totalTime'])
            print("Calories: ", recipe['calories'])
            print("Uri: ", recipe['uri'])
            
            print("Ingredients:")
            for ingredient in recipe['ingredientLines']:
                print("-", ingredient)

            instructions = generate_instructions(recipe['label'], recipe['ingredientLines'], recipe['totalTime'])
            print("Generated Recipe Reception:\n", instructions)
            print("\n")
                        
            break 
else:
    print("Error:", response.status_code)
