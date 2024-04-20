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
        '''
        #Role
        You are the best cooking assistant in the world who is also good at programming.
                        
        #Task                
        Make a list of 10 recipes. The recipes should be something that the person can eat for a whole meal like a whole dinner or breackfast. Format them like a json file and print ONLY then info.You should have label, totalTime(Time to make in minutes), calories, instructions(step by step in one string), ingridients and number_of_meals:\n"
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

        #Specifics
        This task is very important for me and our company. My future depends on it.

        #Context
        The output of your message is used in a program that generates recipes. Your whole answer is directly put in a function in a function that makes it from a string to a json. That is why it is very important to not include any other information and return only the schema so I don't get errors in the code later!

        #Example:
        [
          {
            "label": "Avocado Toast",
            "totalTime": 10,
            "calories": 300,
            "ingredients": "1 ripe avocado, 2 slices of whole grain bread, salt, pepper, and chili flakes",
            "instructions": "Toast the bread slices. Mash the avocado and spread it on the toasted bread. Season with salt, pepper, and chili flakes.",
            "number_of_meals": 1
          },
          {
            "label": "Blueberry Pancakes",
            "totalTime": 20,
            "calories": 350,
            "ingredients": "1 cup flour, 1 tbsp sugar, 1 tsp baking powder, 1/2 tsp salt, 1 cup milk, 1 egg, 1 tbsp melted butter, 1/2 cup blueberries",
            "instructions": "Mix dry ingredients. In another bowl, whisk milk, egg, and butter. Combine with dry ingredients. Fold in blueberries. Cook on a hot griddle.",
            "number_of_meals": 2
          },
          {
            "label": "Vegetarian Omelette",
            "totalTime": 15,
            "calories": 250,
            "ingredients": "2 eggs, 1/2 cup chopped bell peppers, 1/4 cup chopped onions, 1/4 cup shredded cheese, salt, and pepper",
            "instructions": "Beat the eggs with salt and pepper. Pour into a heated skillet. Add vegetables and cheese. Cook until eggs are set and fold omelette.",
            "number_of_meals": 1
          },
          {
            "label": "Chicken Caesar Salad",
            "totalTime": 20,
            "calories": 400,
            "ingredients": "2 cups chopped romaine lettuce, 1/2 grilled chicken breast, 1/4 cup Caesar dressing, 1/4 cup croutons, Parmesan cheese",
            "instructions": "Toss lettuce, sliced chicken, and croutons with Caesar dressing. Sprinkle with Parmesan cheese.",
            "number_of_meals": 1
          },
          {
            "label": "Spaghetti Carbonara",
            "totalTime": 25,
            "calories": 500,
            "ingredients": "200g spaghetti, 100g pancetta, 2 cloves garlic, 2 large eggs, 1/2 cup grated Parmesan cheese, black pepper",
            "instructions": "Cook spaghetti. Sauté pancetta and garlic. Mix eggs and cheese. Combine all with pasta. Season with pepper.",
            "number_of_meals": 2
          },
          {
            "label": "Beef Stir-Fry",
            "totalTime": 30,
            "calories": 450,
            "ingredients": "200g sliced beef, 1 cup mixed vegetables, 2 tbsp soy sauce, 1 tbsp oyster sauce, 1 tsp sesame oil",
            "instructions": "Stir-fry beef until browned. Add vegetables and sauces. Cook until vegetables are tender.",
            "number_of_meals": 2
          },
          {
            "label": "Vegetable Soup",
            "totalTime": 40,
            "calories": 200,
            "ingredients": "1 cup diced carrots, 1 cup diced potatoes, 1/2 cup diced onions, 4 cups vegetable broth, salt, and pepper",
            "instructions": "Simmer all ingredients in broth until vegetables are tender. Season with salt and pepper.",
            "number_of_meals": 4
          },
          {
            "label": "Grilled Salmon",
            "totalTime": 20,
            "calories": 370,
            "ingredients": "1 salmon fillet, 1 tbsp olive oil, 1 tsp lemon juice, salt, and pepper",
            "instructions": "Season salmon with oil, lemon juice, salt, and pepper. Grill until cooked through.",
            "number_of_meals": 1
          },
          {
            "label": "Quinoa Salad",
            "totalTime": 30,
            "calories": 320,
            "ingredients": "1 cup cooked quinoa, 1/2 cup cherry tomatoes, 1/2 cucumber, 1/4 cup feta cheese, 2 tbsp olive oil, 1 tbsp lemon juice",
            "instructions": "Combine all ingredients. Toss with olive oil and lemon juice.",
            "number_of_meals": 2
          },
          {
            "label": "Lentil Curry",
            "totalTime": 45,
            "calories": 410,
            "ingredients": "1 cup lentils, 1 large onion, 2 cloves garlic, 1 tbsp curry powder, 1 can coconut milk, 2 cups water",
            "instructions": "Sauté onion and garlic. Add lentils, curry powder, coconut milk, and water. Simmer until lentils are tender.",
            "number_of_meals": 4
          }
        ]

        #Notes
        In the example you see just how your whole answer should be structured. when making the list keep in mind the user input.            
''')
    print("end")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}]
    )
    print(response)
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
        model="gpt-3.5 Turbo", messages=[{"role": "user", "content": content}]
    )

    response_content = response.choices[0].message.content
    return response_content


def generate_recipe_from_meal_image(imagebase64_image_path):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}

    payload = {
        "model": "gpt-3.5 Turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '''
                        #Role
                        You are the best cooking assistant in the world who is also good at programming.
                        
                        #Task
                        Generte the recipe that is used for making the meal on the image. Format it like a json file and print ONLY the info.You should have label, totalTime(Time to make), calories, instructions(step by step in one string), ingridients and number_of_meals.
                        Recognize what is the meal that you see and make a recipe for. You are able to recognize exactly 1 meal at every image.
                        Use this schema:
                        {
                          type: object,
                          properties: {
                            label: {
                              type: string
                            },
                            totalTime: {
                              type: string
                            },
                            calories: {
                              type: int
                            },
                            ingredients: {
                              type: string
                            },
                            instructions: {
                              type: string
                            },
                            number_of_meals: {
                              type: int
                            },
                          }
                          "required": ["label", "totalTime", "calories", "ingredients", "instructions", "number_of_meals"],
                          "additionalProperties": false
                        }

                        #Specifics
                        This task is very important for me and our company. My future depends on it.

                        #Context
                        The output of your message is used in a program that generates a recipe by image. Your whole answer is directly put in a function in a function that makes it from a string to a json. That is why it is very important to not include any other information and return only the schema so I don't get errors in the code later!
                        
                        #Example
                        {
                          "label": "Classic Chicken Salad",
                          "totalTime": "30 minutes",
                          "calories": 450,
                          "ingredients": "2 cups diced cooked chicken, 1/2 cup diced celery, 1/4 cup chopped onions, 1/2 cup mayonnaise, salt and pepper to taste",
                          "instructions": "Combine all ingredients in a large bowl. Mix well until evenly coated with mayonnaise. Season with salt and pepper.",
                          "number_of_meals": 4
                        }

                        #Notes
                        What you see under #Example is all your answer!
                        ''',
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
        "model": "gpt-3.5 Turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '''
                        #Role
                        You are the best cooking assistant in the world who is also good at programming.
                        
                        #Task
                        Generte the recipe from the ingrediants that you see on the image. Format it like a json file and print ONLY the info.You should have label, totalTime(Time to make), calories, instructions(step by step in one string), ingridients and number_of_meals.
                        Recognize all the groceries and use them to generate the meal. You don't have to use 100 percent of them, but as much as you need. You can add one to a few ingrediants that you don't see in the image if needed but try to minimize them(the ones that are not in the image). You are able to generate exactly 1 meal at every image.
                        Use this schema:
                        {
                          type: object,
                          properties: {
                            label: {
                              type: string
                            },
                            totalTime: {
                              type: string
                            },
                            calories: {
                              type: int
                            },
                            ingredients: {
                              type: string
                            },
                            instructions: {
                              type: string
                            },
                            number_of_meals: {
                              type: int
                            },
                          }
                          "required": ["label", "totalTime", "calories", "ingredients", "instructions", "number_of_meals"],
                          "additionalProperties": false
                        }

                        #Specifics
                        This task is very important for me and our company. My future depends on it.

                        #Context
                        The output of your message is used in a program that generates a recipe by image. Your whole answer is directly put in a function in a function that makes it from a string to a json. That is why it is very important to not include any other information and return only the schema so I don't get errors in the code later!
                        
                        #Example
                        {
                          "label": "Classic Chicken Salad",
                          "totalTime": "30 minutes",
                          "calories": 450,
                          "ingredients": "2 cups diced cooked chicken, 1/2 cup diced celery, 1/4 cup chopped onions, 1/2 cup mayonnaise, salt and pepper to taste",
                          "instructions": "Combine all ingredients in a large bowl. Mix well until evenly coated with mayonnaise. Season with salt and pepper.",
                          "number_of_meals": 4
                        }

                        #Notes
                        What you see under #Example is all your answer!
''',
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
