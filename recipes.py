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

