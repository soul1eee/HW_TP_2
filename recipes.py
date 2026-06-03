class Ingredient:
    def __init__(self, name: str, quantity: float, unit: str):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name and self.unit == other.unit
        return False

class Recipe:
    def __init__(self, title: str, ingredients=None):
        self.title = title
        self.ingredients = []
        if ingredients:
            for ingredient in ingredients:
                self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient: Ingredient):
        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(Ingredient(ingredient.name, ingredient.quantity, ingredient.unit))

    @staticmethod
    def is_valid_ratio(ratio):
        return (isinstance(ratio, int) or isinstance(ratio, float)) and ratio > 0

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        scaled_ingredients = []
        for ingridient in self.ingredients:
            scaled_ingredients.append(Ingredient(ingridient.name, ingridient.quantity * ratio, ingridient.unit))
        return Recipe(self.title, scaled_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_str = ""
        for ingridient in self.ingredients:
            ingredients_str += f"{ingridient}\n"
        return f"Рецепт: {self.title}\nИнгредиенты:\n{ingredients_str}"

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe: Recipe, portions: float):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title: str):
        tmp_list = []
        for item in self._items:
            if item[1] != title:
                tmp_list.append(item)
        self._items = tmp_list

    def get_list(self):
        res_dict = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in res_dict:
                res_dict[key] += ingredient.quantity
            else:
                res_dict[key] = ingredient.quantity

        result = [Ingredient(name, qty, unit) for (name, unit), qty in res_dict.items()]
        result.sort(key=lambda x: x.name)
        return result

    def __add__(self, other: ShoppingList):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list

class DietaryRecipe(Recipe):
    def __init__(self, title: str, diet_type: str, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным числом")
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(scaled_recipe.title, self.diet_type, scaled_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"

