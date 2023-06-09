# attempt #2 Small program to collect common and rare material prices from
# http://kamadan.gwtoolbox.com and calculating the feasibility of
# different artisan recipies (are they cheaper or more expensive
# than buying from a vendor directly?

import requests
import re
from bs4 import BeautifulSoup, SoupStrainer
from dataclasses import dataclass


@dataclass
class Material:
    name: str
    artisan_recipe : list = None
    artisan_cost: int = None
    price: int = 0
    common: bool = False
    
    def set_price(self, price):
        self.price = price if not self.common else price // 10
            
    def get_buying_strategy(self, materials) -> (int, str):
        if self.artisan_recipe is None:
            return {
                    'name': self.name,
                    'price': self.price,
                    'source': 'vendor',
            }

        else:
            artisan_price = 0
            for ingredient in self.artisan_recipe:
                amount, matid = ingredient
                artisan_price += amount * materials[matid].price 
            artisan_price += self.artisan_cost
            if artisan_price < self.price:
                return {
                        'name': self.name,
                        'price': artisan_price,
                        'source': 'artisan',
                }
            else:
                return {
                        'name': self.name,
                        'price': self.price,
                        'source': 'vendor',
                }
    
def materialdict() -> dict:
    materials = {
        922: Material('Lump of Charcoal', artisan_recipe=[(10, 946)],
                      artisan_cost=200,
        ),
        921: Material('Bone', common=True),
        923: Material('Monstrous Claw'),
        925: Material('Bolt of Cloth', common=True),
        926: Material('Bolt of Linen',
                      artisan_recipe=[(5, 934)],
                      artisan_cost=200,
        ),
        927: Material('Bolt of Damask',
                      artisan_recipe=[(5, 934), (5, 929)],
                      artisan_cost=200,
        ),
        928: Material('Bolt of Silk', 
                      artisan_recipe=[(10, 925), (10, 929)],
                      artisan_cost=250,
        ),
        929: Material('Pile of Glittering Dust', common=True),
        930: Material('Glob of Ectoplasm'),
        931: Material('Monstrous Eye'),
        932: Material('Monstrous Fang'),
        933: Material('Feather', common=True),
        934: Material('Plant Fiber', common=True),
        935: Material('Diamond'),
        936: Material('Onyx Gemstone'),
        937: Material('Ruby'),
        938: Material('Sapphire'),
        939: Material('Tempered Glass Vial', 
                       artisan_recipe=[(5, 929)],
                       artisan_cost=20,
        ),
        940: Material('Tanned Hide Square'),
        941: Material('Fur Square'),
        942: Material('Leather Square', 
                      artisan_recipe=[(5, 940)],
                      artisan_cost=50,
                      common=True
        ),
        943: Material('Elonian Leather Square',
                      artisan_recipe=[(5, 940), (5, 929)],
                      artisan_cost=50,
        ),
        944: Material('Vial of Ink',
                      artisan_recipe=[(4, 934), (1, 939)],
                      artisan_cost=20,
        ),
        945: Material('Obsidian Shard'),
        946: Material('Wood Plank', common=True),
        948: Material('Iron Ingot', common=True),
        949: Material('Steel Ingot', 
                      artisan_recipe=[(10, 948), (1, 922)],
                      artisan_cost=200,
        ),
        950: Material('Deldrimor Steel Ingot',
                      artisan_recipe=[(10, 948), (1, 922), (5, 929)],
                      artisan_cost=200,
        ),
        951: Material('Roll of Parchment', 
                      artisan_recipe=[(5, 946)],
                      artisan_cost=20,
        ),
        952: Material('Roll of Vellum',
                      artisan_recipe=[(5, 946), (5, 929)],
                      artisan_cost=20,
        ),
        953: Material('Scale', common=True),
        954: Material('Chitin Fragment', common=True),
        955: Material('Granite Slab', common=True),
        956: Material('Sprit Wood Plank', 
                      artisan_recipe=[(5, 946), (10, 929)],
                      artisan_cost=100,
        ),
        6532: Material('Amber Chunk'),
        6533: Material('Jadeite Shard'),
    }
    URL = 'https://kamadan.gwtoolbox.com'
    only_script = SoupStrainer("script")
    material_string = str(BeautifulSoup(requests.get(URL).text, 'html.parser', parse_only=only_script))
    regex = r'"([96]\d{2,3})":{"p":(\d+),'
    for match in re.findall(regex, material_string):
        matid, curprice = match
        materials[int(matid)].set_price(int(curprice))
    return materials

def print_material_report():
    materials = materialdict()
    for material in materials.values():
        strategy =  material.get_buying_strategy(materials)
        print(f'{strategy["name"]:31}'
              f'{strategy["price"]:5,d}'
              f'g from {strategy["source"]}'
        )        
        if strategy["source"] == 'artisan':
            for ingredient in material.artisan_recipe:
                amount, matid = ingredient
                strategy = materials[matid].get_buying_strategy(materials)
                print(f'__>{amount:3d}'
                      f' {strategy["name"]:24}'
                      f'{strategy["price"]:5,d}'
                      f'g from {strategy["source"]}')

if __name__ == '__main__':
    print_material_report()