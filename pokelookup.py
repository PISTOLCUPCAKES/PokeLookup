import requests
import json


BASE_URL = "https://pokeapi.co/api/v2"
POKEDEX_RANGE = range(1, 386+1) # gen 3 is 1-386 inclusive
# POKEDEX_RANGE = range(1, 15+1) # we'll just grab 6 pokemon for testing/development

# def function_name(parm1: type, parm2: type) -> return_type:
#     """
#     description

#     Parameters:
#         parm1 (type): description
#         parm1 (type): description

#     Returns:
#         return_type: description

#     """
#     pass

class Pokemon:
    def __init__(self, d: dict):
        self.d = d
        self.id = d['id']
        self.name = d['name']
        self.species_name = d['species']['name']
        self.type1 = d['types'][0]['type']['name']
        self.type2 = None
        if len(d['types']) > 1:
            self.type2 = d['types'][1]['type']['name']
        else:
            self.type2 = None
        self.past_types = d['past_types']
    
    def __str__(self):
        # No. 1
        # Bulbasaur - Bulbasaur (species)
        # Grass | Poison
        # ------------------------------
        poke = f"No. {self.id}\n"
        poke = poke + f"{self.name.title()} - {self.species_name.title()}\n"
        poke = poke + f"{self.type1.title()}" # type 1
        if self.type2:
            poke = poke + f" | {self.type2.title()}" # type 2
        poke = poke + "\n" # add our new line after types
        poke = poke + "------------------------------\n"
        return poke


def download_pokemon_data():
    headers = {
        "content-type": "application/json"
    }
    with open("pokemon.txt", "w") as f:
        for x in POKEDEX_RANGE:
            url = f"{BASE_URL}/pokemon/{x}"
            response = requests.get(url, headers=headers)
            d = response.json()
            p = Pokemon(d)
            f.write(str(p))

        # print(type(json.dumps(response.json())))
        # print(f"id: {d['id']}")
        # print(f"name: {d['name']}")
        # print(f"species-name: {d['species']['name']}")
        # print(f"types: {d['types']}")
        # print(f"num types: {len(d['types'])}")
        # print(f"type1: {d['types'][0]['type']['name']}")
        # print(f"type1: {d['types'][1]['type']['name']}")
        # print(f"past-types: {d['past_types']}")

        # print(f": {d['']}")
        # print(f": {d['']}")
        # print(f": {d['']}")
        # print("-----------------------------------------------------------------")



################################################################################
#  Function:  main                                                             #
#  Purpose:   do all the stuff                                                 #
################################################################################
def main():
    download_pokemon_data()
    pass


################################################################################
#  Script entry point                                                          #
################################################################################
if __name__ == "__main__":
    main()
