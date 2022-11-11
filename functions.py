import os
import json

seen_items = {}


def unique_items(a_list: list):
    items = []
    for x in a_list:
        if x not in items:
            items.append(x)
    return len(items)


def init():
    os.makedirs("recipes", exist_ok=True)
    recipe_types = [
        "tconstruct",
        "tconstruct/casting",
        "tconstruct/casting/table",
        "tconstruct/casting/basin",
        "tconstruct/melting",
        "tconstruct/alloying",
        "create",
        "create/mixing",
        "create/milling",
        "create/crushing",
        "create/pressing",
        "create/mixing",
        "create/compacting",
        "create/filling",
        "create/draining",
    ]
    for recipe_type in recipe_types:
        y = "recipes/" + recipe_type
        os.makedirs(y, exist_ok=True)


crushed_ores_with_corresponding_molten_metals = [
    "iron",
    "gold",
    "copper",
    "zinc",
    "aluminum",
    "lead",
    "nickel",
    "osmium",
    "platinum",
    "silver",
    "tin",
    "uranium"
]

mgold = "tconstruct:molten_gold"
miron = "tconstruct:molten_iron"
mcopper = "tconstruct:molten_copper"
mzinc = "tconstruct:molten_zinc"
mbrass = "tconstruct:molten_brass"
ma = "econstruct:molten_andesite"
maa = "econstruct:molten_andesite_alloy"
air = "minecraft:air"


def c(msg):
    return "create:" + msg


def t(msg):
    return "tconstruct:" + msg


def tm(msg):
    return "tconstruct:molten_" + msg


def ingots(n: int):
    return n * 90


def nuggets(n: int):
    return n * 10


def ingots_nuggets(ingot: int, nugget: int):
    return ingot * 90 + nugget * 10


def aingots_nuggets(ingot: int, nugget: int):
    return ingot * 90 + nugget * 10


def write_recipe(name: str, recipe: dict):
    x = open(name, "w")
    x.write(json.dumps(recipe, sort_keys=True, indent=2))
    x.close()


def table(fluid: str, output: str, amount: int = 90, item: str = "minecraft:air", time: int = 80,
          basin_mode=False, tag=False, consume_cast=False):
    name = f"recipes/tconstruct/casting/{'basin' if basin_mode else 'table'}/{output.split(':')[1].replace('/', '_')}_from_casting_{fluid.split(':')[1].replace('/', '_')}_on_{item.split(':')[1].replace('/', '_')}.json "
    recipe = {
        "type": "tconstruct:casting_" + ("basin" if basin_mode else "table"),
        "cast": {
            ("tag" if tag else "item"): item
        },
        "fluid": {
            "name": fluid,
            "amount": amount
        },
        "cast_consumed": consume_cast,
        "result": output,
        "cooling_time": time
    }
    if item == "minecraft:air":
        recipe.pop("cast")
    write_recipe(name, recipe)


def basin(fluid: str, output: str, amount: int, item: str = "minecraft:air", cooling_time: int = 80):
    table(fluid, output, amount, item, cooling_time, True)


def melt(item: str, fluid: str, amount: int, time: int = 240, temp: int = 1000, tag: bool = False,
         byproducts: list = None, amounts: list = None):
    if byproducts is None:
        byproducts = []
        amounts = []
    byproducts = [{"fluid": byproducts[x], "amount": amounts[x]} for x in range(len(byproducts))]

    name = f"recipes/tconstruct/melting/melting_{item.split(':')[1].replace('/', '_')}.json"
    recipe = {
        "type": "tconstruct:melting",
        "ingredient": {
            ("tag" if tag else "item"): item
        },
        "result": {
            "fluid": fluid,
            "amount": amount
        },
        "temperature": temp,
        "time": time,
        "byproducts": byproducts
    }
    if not byproducts:
        recipe.pop("byproducts")
    write_recipe(name, recipe)


def alloy(fluids: list, amounts: list, output: str, amount: int, temp=1000):
    recipe = {
        "type": "tconstruct:alloy",
        "inputs": [],
        "result": {
            "fluid": output,
            "amount": amount
        },
        "temperature": temp
    }
    for i in range(len(fluids)):
        recipe["inputs"].append({"name": fluids[i], "amount": amounts[i]})
    fluids_str = fluids[0].split(":")[1]
    fluids.pop(0)
    for fluid in fluids:
        fluids_str += "_" + fluid.split(":")[1]
    name = f"recipes/tconstruct/alloying/{fluids_str}_alloyto_{output.split(':')[1].replace('/', '_')}.json"
    write_recipe(name, recipe)
