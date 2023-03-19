import psycopg2
import ast

# connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="recipedb",
    user="postgres",
    password="postgres",
    port=5432
)

# create a cursor
cur = conn.cursor()

# fetch the recipes from the database
cur.execute("SELECT id, ingredients FROM raw_recipes")
recipes = cur.fetchall()

# iterate over the recipes
for recipe_id, recipe_text in recipes:
    # parse the recipe text into a list of ingredients
    ingredients_list = ast.literal_eval(recipe_text)

    # iterate over the ingredients in the recipe
    for ingredient_name in ingredients_list:
        # check if the ingredient exists in the ingredients table
        cur.execute("SELECT id FROM ingredient WHERE name=%s", (ingredient_name,))
        result = cur.fetchone()

        # if the ingredient doesn't exist, insert it into the ingredients table
        if result is None:
            cur.execute("INSERT INTO ingredient (name) VALUES (%s) RETURNING id", (ingredient_name,))
            ingredient_id = cur.fetchone()[0]
        else:
            ingredient_id = result[0]

        # insert a row into the recipe_ingredients table for this ingredient and recipe
        cur.execute("INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (%s, %s)",
                    (recipe_id, ingredient_id))

# commit the changes and close the connection
conn.commit()
cur.close()
conn.close()
