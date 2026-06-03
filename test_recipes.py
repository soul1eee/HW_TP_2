import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_init():
    ingredient = Ingredient("Мука", 500.0, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500.0, "г")
    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_eq():
    ingredient1 = Ingredient("Мука", 500.0, "г")
    ingredient2 = Ingredient("Мука", 900.0, "г")
    ingredient3 = Ingredient("Яйца", 500.0, "г")
    ingredient4 = Ingredient("Мука", 500.0, "кг")

    assert ingredient1 == ingredient2
    assert ingredient1 != ingredient3
    assert ingredient1 != ingredient4


def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -10.0, "г")


def test_recipe_init():
    recipe = Recipe("Пицца")
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 0


def test_recipe_add_ingredient():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 300, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 500.0


def test_recipe_scale():
    recipe = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    scaled = recipe.scale(2)

    assert scaled is not recipe
    assert scaled.ingredients[0].quantity == 600.0
    assert recipe.ingredients[0].quantity == 300.0


def test_recipe_scale_negative():
    recipe = Recipe("Пицца")
    with pytest.raises(ValueError):
        recipe.scale(-1)


def test_recipe_len():
    recipe = Recipe("Салат")
    recipe.add_ingredient(Ingredient("Помидоры", 200, "г"))
    recipe.add_ingredient(Ingredient("Огурцы", 150, "г"))
    recipe.add_ingredient(Ingredient("Помидоры", 100, "г"))

    assert len(recipe) == 2


def test_shopping_list_add_recipe():
    sl = ShoppingList()
    recipe = Recipe("Кекс", [Ingredient("Сахар", 200, "г")])
    sl.add_recipe(recipe, 2)

    assert len(sl._items) == 1
    assert sl._items[0][0].quantity == 400.0


def test_shopping_list_add_negative_portions():
    sl = ShoppingList()
    recipe = Recipe("Пирог")
    with pytest.raises(ValueError):
        sl.add_recipe(recipe, -1)


def test_shopping_list_remove_recipe():
    sl = ShoppingList()
    recipe = Recipe("Кекс", [Ingredient("Сахар", 200, "г")])
    sl.add_recipe(recipe, 1)
    sl.remove_recipe("Кекс")
    assert len(sl._items) == 0


def test_shopping_list_get_list():
    sl = ShoppingList()
    r1 = Recipe("Пирог", [Ingredient("Мука", 200, "г"), Ingredient("Крахмал", 100, "г")])
    r2 = Recipe("Кекс", [Ingredient("Мука", 100, "г")])

    sl.add_recipe(r1, 1)
    sl.add_recipe(r2, 2)

    buy_list = sl.get_list()
    assert len(buy_list) == 2
    assert buy_list[0].name == "Крахмал"
    assert buy_list[1].quantity == 400.0
    assert buy_list[1].name == "Мука"


def test_shopping_list_add():
    sl1 = ShoppingList()
    sl1.add_recipe(Recipe("Пирог", [Ingredient("Мука", 200, "г")]), 1)

    sl2 = ShoppingList()
    sl2.add_recipe(Recipe("Кекс", [Ingredient("Сахар", 100, "г")]), 1)

    sl3 = sl1 + sl2
    assert len(sl3._items) == 2
    assert sl1 is not sl3 and sl2 is not sl3