# Small program to collect common and rare material prices from
# http://kamadan.gwtoolbox.com and calculating the feasibility of
# different artisan recipies (are they cheaper or more expensive
# than buying from a vendor directly?

import requests
import sys
import re
from bs4 import BeautifulSoup, SoupStrainer

def print_material_types():
    """Prints if material is common or rare"""
    for id, name in material_names.items():
        kind = 'Common Material' if id in common_materials else 'Rare Material'
        print(f'{name:24}{kind}')

def print_artisan_recipies():
    """Prints the recipies for rare materials available at artisans"""
    for material, recipe in artisan_recipies.items():
        print(f'{material_names[material]}:')
        for ingredients in recipe:
            amount, ingredient = ingredients
            print(f'\t{amount} {material_names[ingredient]}')

def print_material_prices():
    """Print current material prices"""
    for material, price in material_prices.items():
        print(f'{material_names[material]:24}{price:d}g')

def print_artisan_report():
    print(f'{"Material":24}Price@Vendor Cost@Artisan')
    for material, recipe in artisan_recipies.items():
        artisan_cost = 0
        for ingredients in recipe:
            amount, ingredient = ingredients
            price = material_prices[ingredient] // 10 if ingredient in common_materials else material_prices[ingredient]
            artisan_cost += amount * price
        print(f'{material_names[material]:24}{material_prices[material]:12}g{artisan_cost:11}g')

def print_advanced_artisan_report():
    def print_strategy(material, amount):
        if material in artisan_recipies:
            artisan_price = 0
            for ingredients in artisan_recipies[material]:
                _amount, _ingredient = ingredients
                artisan_price += _amount * (material_prices[_ingredient] // 10 if _ingredient in common_materials else material_prices[_ingredient])
            if artisan_price < material_prices[material]:
                price = amount * artisan_price
                source = 'from artisan'
            else:
                price = amount * material_prices[material]
                source = 'from vendor'
        else:
            source = 'from vendor'
            price = amount * (material_prices[material] // 10 if material in common_materials else material_prices[material])     
        print(f'{amount:3d} {material_names[material]:24}{price}g {source}')
        if source == 'from artisan':
            for ingredients in artisan_recipies[material]:
                _amount, _ingredient = ingredients
                print('using...')
                print_strategy(_ingredient, _amount)
    amount = 1
    for material in material_names.keys():
        print_strategy(material, amount)
    
    
args = sys.argv
del args[0] # delete name of script

if args:
    try:
        with open(args[0], mode='rt', encoding='utf-16') as input_file:
            material_string = input_file.read()
    except IOError:
        print('File not Found.')
        material_string = ''
else:
    URL = 'https://kamadan.gwtoolbox.com'
    only_script = SoupStrainer("script")
    material_string = str(BeautifulSoup(requests.get(URL).text, 'html.parser', parse_only=only_script))

material_names = {
# special gold cost material
    000: 'Gold',
# all other material ids
    921: 'Bone',
    922: 'Lump of Charcoal',
    923: 'Monstrous Claw',
    925: 'Bolt of Cloth',
    926: 'Bolt of Linen',
    927: 'Bolt of Damask',
    928: 'Bolt of Silk',
    929: 'Pile of Glittering Dust',
    930: 'Glob of Ectoplasm',
    931: 'Monstrous Eye',
    932: 'Monstrous Fang',
    933: 'Feather',
    934: 'Plant Fibers',
    935: 'Diamond',
    936: 'Onyx Gemstone',
    937: 'Ruby',
    938: 'Sapphire',
    939: 'Tempered Glass Vial',
    940: 'Tanned Hide Square',
    941: 'Fur Square',
    942: 'Leather Square',
    943: 'Elonian Leather Square',
    944: 'Vial of Ink',
    945: 'Obsidian Shard',
    946: 'Wood Plank', 
    948: 'Iron Ingot',
    949: 'Steel Ingot',
    950: 'Deldrimor Steel Ingot',
    951: 'Roll of Parchment',
    952: 'Roll of Vellum',
    953: 'Scale',
    954: 'Chitin Fragment',
    955: 'Granite Slab',
    956: 'Sprit Wood Plank',
    6532: 'Amber Chunk',
    6533: 'Jadeite Shard',
}
# materials are rare if they aren't common
common_materials = frozenset([921, 925, 929, 933, 934, 940, 946, 948, 953, 954, 955])
material_prices = {0: 1} # Gold costs 1g
regex = r'"([96]\d{2,3})":{"p":(\d+),'
for match in re.findall(regex, material_string):
    material, price = match
    material_prices[int(material)] = int(price)
 
# recipies as dict of with format:
# {
#  (MATERIAL_ID: [(INGREDIENT_AMOUNT1, INGREDIENT_ID1), (...), (COST, 0)]),
# }
artisan_recipies = {
    927: [(5, 934), (5, 929), (200, 0)],
    926: [(5, 934), (200, 0)],
    928: [(10, 925), (10, 929), (250, 0)],
    950: [(10, 948), (1, 922), (5, 929), (200, 0)],
    943: [(5, 940), (5, 929), (50, 0)],
    942: [(5, 940), (50, 0)],
    922: [(10, 946), (200, 0)], 
    951: [(5, 946), (20, 0)],
    952: [(5, 946), (5, 929), (20, 0)],
    956: [(5, 946), (10, 929), (100, 0)],
    949: [(10, 948), (1, 922), (200, 0)],
    939: [(5, 929), (20, 0)],
    944: [(4, 934), (1, 939), (20, 0)],
}
print_advanced_artisan_report()
print_artisan_report()  