import requests
import json
from tqdm import tqdm
from enum import Enum
from timeit import default_timer as timer


BASE_URL = "https://pokeapi.co/api/v2"
POKEDEX_RANGE = range(1, 386+1) # gen 3 is 1-386 inclusive
pokedex = {}

class PokeType(Enum):
    NONE = 0
    NORMAL = 1
    FIGHTING = 2
    FLYING = 3
    POISON = 4
    GROUND = 5
    ROCK = 6
    BUG = 7
    GHOST = 8
    STEEL = 9
    FIRE = 10
    WATER = 11
    GRASS = 12
    ELECTRIC = 13
    PSYCHIC = 14
    ICE = 15
    DRAGON = 16
    DARK = 17
    UNKNOWN = 10001


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
        if self.type2 and not(self.type2 == PokeType.NONE):
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
            
            type2 = PokeType['NONE']
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

    global pokedex
    pokedex = load_pokedex()

    while True:
        print("What pokemon would you like to lookup?")
        i = input()

        pokemon = find_pokemon(i)
        print(pokemon)



################################################################################
#  Script entry point                                                          #
################################################################################
if __name__ == "__main__":
    main()
