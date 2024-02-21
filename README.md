# Recipes

This Python script, titled "Recipes," offers a set of functions for recipe analysis, cost computation, and grocery list creation. The main highlights of the code include:

## Functionalities

### 1. `make_recipe_book`

**Purpose:** Constructs a dictionary mapping each compound food item to a list of associated ingredient lists. A compound food item is a food item made up of other foods. 


### 2. `make_atomic_costs`

**Purpose:** Generates a dictionary mapping each atomic food item to its cost. An atomic food item is a food that is not made up of any other foods. 



### 3. `lowest_cost`

**Purpose:** Determines the lowest cost of a full recipe for a given food item, considering compound recipes.

**Recursion:** The function employs recursion to handle compound recipes.

### 4. `scale_recipe`

**Purpose:** Scales the quantities of ingredients in a recipe by a factor n.


### 5. `make_grocery_list`

**Purpose:** Creates an overall grocery list by summing ingredient quantities across multiple recipes.


### 6. `cheapest_flat_recipe`

**Purpose:** Identifies the cheapest full recipe for a given food item, considering compound recipes.

**Recursion:** The function utilizes recursion to handle compound recipes.

### 7. `ingredient_mixes`

**Purpose:** Computes all possible combinations of ingredient recipes from a list of flat recipes.


### 8. `all_flat_recipes`

**Purpose:** Produces a list of all possible flat recipes for a given food item.

**Recursion:** The function employs recursion to handle compound recipes.

## Testing

The script includes a test scenario at the end, focusing on the example recipes provided in the `test_recipes/example_recipes.pickle` file. The code also sets a recursion limit using `sys.setrecursionlimit(20_000)`.


## Test Cases

- Test cases are available in `test.py`, which is written by the MIT 6.101 course staff. These tests ensure the correctness and functionality of the implemented code. The test_recipes folder contains files that are used in test.py.
