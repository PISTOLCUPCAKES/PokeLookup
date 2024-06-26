import requests
import json
from tqdm import tqdm
from enum import Enum
from timeit import default_timer as timer
from typing import List
from rapidfuzz import fuzz, utils


BASE_URL = "https://pokeapi.co/api/v2"
POKEDEX_RANGE = range(1, 386+1) # gen 3 is 1-386 inclusive


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


    def get_type_effectiveness(self, attack_type: PokeType) -> float:
        """
        Calculates and returns an attacks effectiveness against this Pokemon
    
        Parameters:
            attack_type (PokeType): The type of the attack
    
        Returns:
            float: The effectiveness (or damage multiplier) of specified attack type vs this Pokemon
    
        """
        type1_effectiveness = TYPE_CHART[attack_type.value][self.type1.value]
        type2_effectiveness = 1 if self.type2 is None else TYPE_CHART[attack_type.value][self.type2.value]
        overall_effectiveness = type1_effectiveness * type2_effectiveness
        return round(overall_effectiveness) if overall_effectiveness == round(overall_effectiveness) else overall_effectiveness # this seems silly but it will convert '1.0' to '1'

    def get_type_chart(self) -> List[float]:
        """
        returns type effectiveness for each type against this pokemon
    
        Returns:
            List[float]: List of type effectiveness against this pokemon in PokeType order. e.g., for Fighting you can get the multiplier by list[PokeType.FIGHTING.value]
        """
        type_chart = []
        for t in PokeType:
            type_chart.insert(t.value, self.get_type_effectiveness(t))
        return type_chart


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


class PokeLookup:
    def __init__(self):
        self.pokedex = self._load_pokedex()
    
    def _download_pokemon_data(self):
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


    def _load_pokedex(self) -> dict:
        """
        Loads pokedex data from json file
        """
        with open("pokemon.json", "r") as f:
            return json.load(f)



    def find_pokemon(self, search_name) -> Pokemon:
        """
        Search pokedex for a pokemon by name and return it if found

        Parameters:
            name (str): name of the pokemon
            id   (int): id of the pokemon

        Returns:
            Pokemon: instance of Pokemon with pokemon's details

        """
        match = None
        fuzz_idx = None
        fuzz_ratio = 0
        
        for i, p in enumerate(self.pokedex):

            # check for an exact match. If we get one then we can break the loop
            if p['name'] == search_name.lower() or str(p['id']) == search_name:
                match = i
                break
            
            # check for fuzzy matches, we'll keep track of the best match and then use that if we don't end up getting an exact match
            temp_ratio = fuzz.ratio(search_name, p['name'], processor=utils.default_process)
            if temp_ratio > fuzz_ratio:
                fuzz_idx = i
                fuzz_ratio = temp_ratio

        if match is None:
            print(f"Using fuzzy match: {fuzz_idx}")
            match = fuzz_idx
        else:
            print(f"Using exact match: {match}")

        # this shouldn't ever happen since we're just using best fuzzy match when theres no exact match, but just in case
        if match is None:
            return None
        
        p = self.pokedex[match]

        id = p['id']
        name = p['name']
        current_type1 = p['types'][0]['type']['name']
        current_type2 = p['types'][1]['type']['name'] if len(p['types']) > 1 else None

        type1 = current_type1
        type2 = current_type2

        for t in p['past_types']:
            # e.g., "generation-v" means the pokemon was <past_types> in generation 5 and earlier
            # e.g., clefairy was normal through gen 5 and became fairy in gen 6
            # we only intend to support gen 3 pokemon and type changes were only made after gen 1 and after gen 5
            # So use gen 5 past_types if they exist, otherwise use types
            if t['generation']['name'] == "generation-v":
                type1 = t['types'][0]['type']['name']
                type2 = t['types'][1]['type']['name'] if len(t['types']) > 1 else None

        poketype1 = PokeType[type1.upper()]
        poketype2 = PokeType[type2.upper()] if type2 is not None else None
        poke = Pokemon(id, name, poketype1, poketype2)
        return poke


################################################################################
#  Function:  main                                                             #
#  Purpose:   do all the stuff                                                 #
################################################################################
def main():
    # download_pokemon_data()
    pokelookup = PokeLookup()

    print(TYPE_CHART[PokeType.NORMAL.value])
    print(f"Ghost attacking Normal. Expecting 0: {TYPE_CHART[PokeType.GHOST.value][PokeType.NORMAL.value]}")
    print(f"Normal attacking Ghost. Expecting 0: {TYPE_CHART[PokeType.NORMAL.value][PokeType.GHOST.value]}")
    print(f"Fighting attacking Normal. Expecting 2: {TYPE_CHART[PokeType.FIGHTING.value][PokeType.NORMAL.value]}")
    print(f"Dark attacking Ghost. Expecting 2: {TYPE_CHART[PokeType.DARK.value][PokeType.GHOST.value]}")
    print(f"Dark attacking Dark. Expecting 0.5: {TYPE_CHART[PokeType.DARK.value][PokeType.DARK.value]}")
    print(f"Ice attacking Steel. Expecting 0.5: {TYPE_CHART[PokeType.ICE.value][PokeType.STEEL.value]}")


    while True:
        print("What pokemon would you like to lookup?")
        i = input()

        pokemon = pokelookup.find_pokemon(i)
        if pokemon is None:
            print(f"Pokemon '{i}' not found. Sorry!")
            continue
        print(pokemon)
        # print(pokemon.get_type_chart())
        # pokemon.get_type_effectiveness(PokeType.NORMAL)
        # pokemon.get_type_effectiveness(PokeType.FIGHTING)
        # pokemon.get_type_effectiveness(PokeType.FLYING)
        # pokemon.get_type_effectiveness(PokeType.POISON)
        # pokemon.get_type_effectiveness(PokeType.GROUND)
        # pokemon.get_type_effectiveness(PokeType.ROCK)
        # pokemon.get_type_effectiveness(PokeType.BUG)
        # pokemon.get_type_effectiveness(PokeType.GHOST)
        # pokemon.get_type_effectiveness(PokeType.STEEL)
        # pokemon.get_type_effectiveness(PokeType.FIRE)
        # pokemon.get_type_effectiveness(PokeType.WATER)
        # pokemon.get_type_effectiveness(PokeType.GRASS)
        # pokemon.get_type_effectiveness(PokeType.ELECTRIC)
        # pokemon.get_type_effectiveness(PokeType.PSYCHIC)
        # pokemon.get_type_effectiveness(PokeType.ICE)
        # pokemon.get_type_effectiveness(PokeType.DRAGON)
        # pokemon.get_type_effectiveness(PokeType.DARK)


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
