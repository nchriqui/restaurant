import json
import random

adjectives = [
    "Délicieux",
    "Savoureux",
    "Épicé",
    "Croustillant",
    "Fumé",
    "Parfumé",
    "Onctueux",
    "Gourmand",
    "Léger",
    "Exotique",
]
foods = [
    "Poulet",
    "Boeuf",
    "Poisson",
    "Légumes",
    "Fruits de mer",
    "Pâtes",
    "Riz",
    "Tofu",
    "Fromage",
    "Salade",
]
food_types = ["entree", "plat", "dessert"]
protein_types = ["viande", "poisson", "vegetarien"]
spicy_possibilities = [0, 1, 2, 3, 4, 5]


def generate_random_dish_name():
    adjective = random.choice(adjectives)
    food = random.choice(foods)
    dish_name = f"{adjective} {food}"
    return dish_name


def generate_random_food_type():
    return random.choice(food_types)


def generate_random_protein_type():
    return random.choice(protein_types)


def generate_random_spicy():
    return random.choice(spicy_possibilities)


def generate_random_apport_cal():
    return random.randint(200, 1000)


dataset = []
for i in range(20000):
    name = generate_random_dish_name()
    food_type = generate_random_food_type()
    protein = generate_random_protein_type()
    apport_calorique = generate_random_apport_cal()
    spicy = generate_random_spicy()
    line = {
        "nom": name,
        "type": food_type,
        "protein": protein,
        "apport_calorique": apport_calorique,
        "epicee": spicy,
    }

    dataset.append(line)

with open(
    "./Data/applications/similarity_recommendation/explo/data/dataset.json", "w"
) as json_file:
    json.dump(dataset, json_file, indent=4)
