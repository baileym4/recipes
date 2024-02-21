"""
6.101 Lab 6:
Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    compound_dict = {}
    for item in recipes:
        classification = item[0]
        food = item[1]
        ingredients = item[2]
        # if not in dict add
        if classification == "compound":
            if food not in compound_dict.keys():
                compound_dict[food] = [ingredients]
            # if multiple ways to make add
            else:
                compound_dict[food].append(ingredients)
    return compound_dict


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    atomic_dict = {}
    for item in recipes:
        if item[0] == "atomic":
            atomic_dict[item[1]] = item[2]
    return atomic_dict


def lowest_cost(recipes, food_item, restriction=[]):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """

    food_dict = make_recipe_book(recipes)
    single_food = make_atomic_costs(recipes)
    restriction = set(restriction)
    if food_item in restriction:
        return None
    if food_item in single_food:
        return single_food[food_item]
    elif food_item in food_dict:
        ingredients = food_dict[food_item]
        min_cost = float("inf")
        for recipe in ingredients:
            current_cost = 0
            valid = True
            for food, quantity in recipe:
                item_cost = lowest_cost(recipes, food, restriction)
                if item_cost is not None:
                    current_cost += item_cost * quantity
                else:
                    valid = False
                    break
            if valid:
                if current_cost < min_cost:
                    min_cost = current_cost
        if min_cost == float("inf"):
            return None
        return min_cost


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    # make new dict:
    scaled_dict = {}
    for val in flat_recipe:
        scaled_dict[val] = flat_recipe[val] * n
    return scaled_dict


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    final = {}
    for recipe in flat_recipes:
        for ingredient in recipe:
            amount = recipe[ingredient]
            if ingredient not in final:
                final[ingredient] = amount
            else:
                final[ingredient] += amount

    return final


def cheapest_flat_recipe(recipes, food_item, restriction=[]):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    # intialize dictionary
    food_dict = make_recipe_book(recipes)
    single_food = make_atomic_costs(recipes)
    restriction = set(restriction)

    # if looking for excluded
    if food_item not in single_food and food_item not in food_dict:
        return None
    # if looking for restricted item
    if food_item in restriction:
        return None

    # base case
    if food_item in single_food:
        return {food_item: 1}

    # if compound food
    elif food_item in food_dict:
        ingredients = food_dict[food_item]
        all_recipes = []  # list of flat recipes
        for recipe in ingredients:
            flat_recipes = []
            for individual_ingredient, quantity in recipe:
                unscaled_flat_recipe = cheapest_flat_recipe(
                    recipes, individual_ingredient, restriction
                )
                if unscaled_flat_recipe is None:
                    break
                current_flat = scale_recipe(unscaled_flat_recipe, quantity)
                flat_recipes.append(current_flat)
            if len(flat_recipes) == len(recipe):  # make sure nothing was excluded
                all_recipes.append(make_grocery_list(flat_recipes))
    min_cost_recipe = float("inf")
    final_recipe = []
    if len(all_recipes) == 0:
        return None
    # find min cost recipe 
    else:
        for recipe_option in all_recipes:
            current_cost = get_cost(recipe_option, single_food)
            if current_cost < min_cost_recipe:
                min_cost_recipe = current_cost
                final_recipe = recipe_option

    return final_recipe


def get_cost(flat_recipe, single_food):
    """
    returns the cost of a flat recipe 
    """
    total_cost = 0
    for ingredient in flat_recipe:
        quantity = flat_recipe[ingredient]
        price = single_food[ingredient]
        total_cost += quantity * price
    return total_cost


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes for a certain ingredient, compute and return a list of flat
    recipe dictionaries that represent all the possible combinations of
    ingredient recipes.
    """
    if len(flat_recipes) == 1:
        return flat_recipes[0]
    else:
        final = []
        possibilities = ingredient_mixes(flat_recipes[1:])
        # find possibilities of one type with the rest of mixes
        for option in possibilities:
            for ingredient in flat_recipes[0]:
                final.append(make_grocery_list([option, ingredient]))

    return final


def all_flat_recipes(recipes, food_item, restriction=[]):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    # find flat recipies for a given food item
    restriction = set(restriction)
    atomic_food = make_atomic_costs(recipes)
    recipe_book = make_recipe_book(recipes)

    def recursive_helper(food_item):
        if food_item in restriction:
            return []
        if food_item in atomic_food:
            return [{food_item: 1}]
        if food_item not in recipe_book:
            return []
        result = []
        for recipe in recipe_book[food_item]:
            current_recipe = []
            for ingredient, quantity in recipe:
                flat_ingredient = recursive_helper(ingredient)
                scaled_ingredients = []
                # scale recipes
                for single_flat in flat_ingredient:
                    scaled_ingredients.append(scale_recipe(single_flat, quantity))
                current_recipe.append(scaled_ingredients)
            # get all valid posibilities
            result.extend(ingredient_mixes(current_recipe)) 
        return result 

    return recursive_helper(food_item)


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!
    # atom_dict = make_atomic_costs(example_recipes)
    # current_cost = 0
    # for val in atom_dict:
    #     current_cost += atom_dict[val]
    # print("cost", current_cost)
    # comp_dict = make_recipe_book(example_recipes)
    # mult = 0
    # for v in comp_dict:
    #     if len(comp_dict[v]) == 2:
    #         mult += 1
    # print("mult", mult)
    # print(lowest_cost(example_recipes, "time"))
    # soup = {'carrots': 5, 'celery': 3, 'broth': 2,
    # 'noodles': 1, 'chicken': 3, 'salt': 10}
    # ans = scale_recipe(soup, 3)
    # correct = {"carrots": 15, "celery": 9, "broth": 6, "noodles": 3,
    # "chicken": 9, "salt": 30}
    # if ans == correct:
    #     print("slayed")
    # print(ans)
    # carrot_cake = {"carrots": 5, "flour": 8, "sugar": 10,
    # "oil": 5, "eggs": 4, "salt": 3}
    # bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
    # grocery_list = [soup, carrot_cake, bread]
    # ans_1 = make_grocery_list(grocery_list)
    # correct_1 = {'carrots': 10, 'flour': 18, 'sugar': 13, 'oil': 8,
    # 'eggs': 4, 'salt': 18, 'yeast': 15, 'celery': 3,
    # 'broth': 2, 'noodles': 1, 'chicken': 3}
    # if ans_1 == correct_1:
    #     print("yay!")
    cookie_recipes = [
    ('compound', 'cookie sandwich', [('cookie', 2), ('ice cream scoop', 3)]),
    ('compound', 'cookie', [('chocolate chips', 3)]),
    ('compound', 'cookie', [('sugar', 10)]),
    ('atomic', 'chocolate chips', 200),
    ('atomic', 'sugar', 5),
    ('compound', 'ice cream scoop', [('vanilla ice cream', 1)]),
    ('compound', 'ice cream scoop', [('chocolate ice cream', 1)]),
    ('atomic', 'vanilla ice cream', 20),
    ('atomic', 'chocolate ice cream', 30),
]
    ans = all_flat_recipes(cookie_recipes, 'cookie sandwich')
    #print(ans)
    ans1 = all_flat_recipes(cookie_recipes, 'cookie sandwich', 
                            ('sugar', 'chocolate ice cream'))
    print(ans1)
