import requests
import json
from tqdm import tqdm
from enum import Enum
from timeit import default_timer as timer


BASE_URL = "https://pokeapi.co/api/v2"
POKEDEX_RANGE = range(1, 386+1) # gen 3 is 1-386 inclusive
pokedex = {}

class PokeType(Enum):
    NORMAL   = 0
    FIGHTING = 1
    FLYING   = 2
    POISON   = 3
    GROUND   = 4
    ROCK     = 5
    BUG      = 6
    GHOST    = 7
    STEEL    = 8
    FIRE     = 9
    WATER    = 10
    GRASS    = 11
    ELECTRIC = 12
    PSYCHIC  = 13
    ICE      = 14
    DRAGON   = 15
    DARK     = 16
    UNKNOWN  = 10001


TYPE_CHART = [
    # Attack type in rows, Defender type in columns
    #                                                           Defending Type
    # Normal    Fighting    Flying  Poison  Ground  Rock    Bug     Ghost   Steel   Fire    Water   Grass   Electric    Psychic Ice     Dragon  Dark
    # Normal
    [ 1,        1,          1,      1,      1,      0.5,    1,      0,      0.5,    1,      1,      1,      1,          1,      1,      1,      1   ],
    # Fighting
    [ 2,        1,          0.5,    0.5,    1,      2,      0.5,    0,      2,      1,      1,      1,      1,          0.5,    2,      1,      2   ],
    # Flying
    [ 1,        2,          1,      1,      1,      0.5,    2,      1,      0.5,    1,      1,      2,      0.5,        1,      1,      1,      1   ],
    # Poison
    [ 1,        1,          1,      0.5,    0.5,    0.5,    1,      0.5,    0,      1,      1,      2,      1,          1,      1,      1,      1   ],
    # Ground
    [ 1,        1,          0,      2,      1,      2,      0.5,    1,      2,      2,      1,      0.5,    2,          1,      1,      1,      1   ],
    # Rock
    [ 1,        0.5,        2,      1,      0.5,    1,      2,      1,      0.5,    2,      1,      1,      1,          1,      2,      1,      1   ],
    # Bug
    [ 1,        0.5,        0.5,    0.5,    1,      1,      1,      0.5,    0.5,    0.5,    1,      2,      1,          2,      1,      1,      2   ],
    # Ghost
    [ 0,        1,          1,      1,      1,      1,      1,      2,      0.5,    1,      1,      1,      1,          2,      1,      1,      0.5 ],
    # Steel
    [ 1,        1,          1,      1,      1,      2,      1,      1,      0.5,    0.5,    0.5,    1,      0.5,        1,      2,      1,      1   ],
    # Fire
    [ 1,        1,          1,      1,      1,      0.5,    2,      1,      2,      0.5,    0.5,    2,      1,          1,      2,      0.5,    1   ],
    # Water
    [ 1,        1,          1,      1,      2,      2,      1,      1,      1,      2,      0.5,    0.5,    1,          1,      1,      0.5,    1   ],
    # Grass
    [ 1,        1,          0.5,    0.5,    2,      2,      0.5,    1,      0.5,    0.5,    2,      0.5,    1,          1,      1,      0.5,    1   ],
    # Electric
    [ 1,        1,          2,      1,      0,      1,      1,      1,      1,      1,      2,      0.5,    0.5,        1,      1,      0.5,    1   ],
    # Psychic
    [ 1,        2,          1,      2,      1,      1,      1,      1,      0.5,    1,      1,      1,      1,          0.5,    1,      1,      0   ],
    # Ice
    [ 1,        1,          2,      1,      2,      1,      1,      1,      0.5,    0.5,    0.5,    2,      1,          1,      0.5,    2,      1   ],
    # Dragon
    [ 1,        1,          1,      1,      1,      1,      1,      1,      0.5,    1,      1,      1,      1,          1,      1,      2,      1   ],
    # Dark
    [ 1,        0.5,        1,      1,      1,      1,      1,      2,      0.5,    1,      1,      1,      1,          2,      1,      1,      0.5 ]
]


class Pokemon:
    def __init__(self, id: int, name: str, type1: PokeType, type2: PokeType):
        self.id = id
        self.name = name
        self.type1 = type1
        self.type2 = type2

    def __str__(self):
        # No. 1
        # Bulbasaur
        # Grass | Poison
        # ------------------------------
        poke = f"No. {self.id}\n"
        poke = poke + f"{self.name.title()}\n"
        poke = poke + f"{self.type1.name.title()}" # type 1
        if self.type2 is not None:
            poke = poke + f" | {self.type2.name.title()}" # type 2
        poke = poke + "\n" # add our new line after types
        poke = poke + "------------------------------\n"
        return poke


def download_pokemon_data():
    """
    downloads pokemon data and saves locally to pokemon.json
    This local file can then be used as the app database instead of hammering pokeapi with API calls
    """
    headers = {
        "content-type": "application/json"
    }
    pokelist = []
    
    for x in tqdm(POKEDEX_RANGE, desc="Fetching Pokemon..."):
        url = f"{BASE_URL}/pokemon/{x}"
        response = requests.get(url, headers=headers)
        d = response.json()
        pokelist.append(d)
    
    with open("pokemon.json", "w") as f:
        json.dump(pokelist, f)


def load_pokedex() -> dict:
    """
    Loads pokedex data from json file
    """
    with open("pokemon.json", "r") as f:
        return json.load(f)



def find_pokemon(name: str) -> Pokemon:
# def find_pokemon(name) -> Pokemon:
    """
    Search pokedex for a pokemon by name and return it if found

    Parameters:
        name (str): name of the pokemon
        id   (int): id of the pokemon

    Returns:
        Pokemon: instance of Pokemon with pokemon's details

    """
    global pokedex
    
    for p in pokedex:
        # TODO - perhaps try using rapidfuzz for fuzzy searching - https://pypi.org/project/rapidfuzz/
        if p['name'] == name or p['id'] == id:
            # we have our element
            data_id = p['id']
            data_name = p['name']

            data_type1 = p['types'][0]['type']['name']
            type1 = PokeType[data_type1.upper()]
            
            type2 = None
            if len(p['types']) > 1:
                data_type2 = p['types'][1]['type']['name']
                type2 = PokeType[data_type2.upper()]
            poke = Pokemon(data_id, data_name, type1, type2)
            return poke
    return None


################################################################################
#  Function:  main                                                             #
#  Purpose:   do all the stuff                                                 #
################################################################################
def main():
    # download_pokemon_data()

    print(TYPE_CHART[PokeType.NORMAL.value])
    print(f"Ghost attacking Normal. Expecting 0: {TYPE_CHART[PokeType.GHOST.value][PokeType.NORMAL.value]}")
    print(f"Normal attacking Ghost. Expecting 0: {TYPE_CHART[PokeType.NORMAL.value][PokeType.GHOST.value]}")
    print(f"Fighting attacking Normal. Expecting 2: {TYPE_CHART[PokeType.FIGHTING.value][PokeType.NORMAL.value]}")
    print(f"Dark attacking Ghost. Expecting 2: {TYPE_CHART[PokeType.DARK.value][PokeType.GHOST.value]}")
    print(f"Dark attacking Dark. Expecting 0.5: {TYPE_CHART[PokeType.DARK.value][PokeType.DARK.value]}")
    print(f"Ice attacking Steel. Expecting 0.5: {TYPE_CHART[PokeType.ICE.value][PokeType.STEEL.value]}")


    global pokedex
    pokedex = load_pokedex()

    while True:
        print("What pokemon would you like to lookup?")
        i = input()

        pokemon = find_pokemon(i)
        print(pokemon)


    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")
    # print(f": {TYPE_EFFECTIVENESS[PokeType..value][PokeType..value]}")



################################################################################
#  Script entry point                                                          #
################################################################################
if __name__ == "__main__":
    main()
