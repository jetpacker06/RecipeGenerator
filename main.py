import os
import json

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
mgold = "tconstruct:molten_gold"
miron = "tconstruct:molten_iron"
for recipe_type in recipe_types:
    y = "recipes/" + recipe_type
    os.makedirs(y, exist_ok=True)


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


def write_recipe(name: str, recipe: dict):
    x = open(name, "w")
    x.write(json.dumps(recipe, sort_keys=True, indent=2))
    x.close()


def table(fluid: str, output: str, amount: int = 90, item: str = "minecraft:air", cooling_time: int = 80,
          basin_mode=False):
    name = f"recipes/tconstruct/casting/table/{output.split(':')[1]}_from_casting_{fluid.split(':')[1]}_on_" \
           f"{item.split(':')[1]}.json"
    recipe = {
        "type": "tconstruct:casting_" + ("basin" if basin_mode else "table"),
        "cast": {
            "item": item
        },
        "fluid": {
            "fluid": fluid,
            "amount": amount
        },
        "result": output,
        "cooling_time": cooling_time
    }
    write_recipe(name, recipe)


def basin(fluid: str, output: str, amount: int, item: str = "minecraft:air", cooling_time: int = 80):
    table(fluid, output, amount, item, cooling_time, True)


def melt(item: str, fluid: str, amount: int, time: int, temp: int = 1000):
    name = f"recipes/tconstruct/melting/melting_{item.split(':')[1]}.json"
    recipe = {
        "type": "tconstruct:melting",
        "ingredient": {
            "item": item
        },
        "result": {
            "fluid": fluid,
            "amount": amount
        },
        "temperature": temp,
        "time": time
    }
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
        recipe["inputs"].append({"fluid": fluids[i], "amount": amounts[i]})
    fluids_str = fluids[0].split(":")[1]
    fluids.pop(0)
    for fluid in fluids:
        fluids_str += "_" + fluid.split(":")[1]
    name = f"recipes/tconstruct/alloying/{fluids_str}_alloyto_{output.split(':')[1]}.json"
    write_recipe(name, recipe)


table(mgold, c("wrench"), ingots(3), c("cogwheel"))
melt(c("wrench"), mgold, ingots(3), 120)
alloy(["tconstruct:molten_gold", "tconstruct:molten_diamond"], [90, 20], "tconstruct:molten_quartz", 90)
