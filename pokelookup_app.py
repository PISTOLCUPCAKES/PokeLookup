import os
import customtkinter
from PIL import Image
from pokelookup_core import Pokemon, PokeLookup


APP_WIDTH = 1000
APP_HEIGHT = 600

BASE_IMAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sprites")
TYPE_IMAGE_PATH = os.path.join(BASE_IMAGE_PATH, "types")
TYPE_SPRITE_SIZE = (144, 32)
POKEMON_IMAGE_PATH = os.path.join(BASE_IMAGE_PATH, "pokemon")
POKEMON_SPRITE_SIZE = (192, 192)
FONT_FAMILY = "Roboto"
FONT_SIZE = 24


class PokemonDetailsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # pokemon name label
        self.name_label = customtkinter.CTkLabel(self, text="???")
        self.name_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # type 1
        self.type1_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(TYPE_IMAGE_PATH, "unknown.png")),
                                                  dark_image=Image.open(os.path.join(TYPE_IMAGE_PATH, "unknown.png")),
                                                  size=(144, 32))
        self.type1_image_label = customtkinter.CTkLabel(self, image = self.type1_image, text="")
        self.type1_image_label.grid(row=1, column=0, padx=5, pady=(0,5))

        # type 2
        self.type2_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(TYPE_IMAGE_PATH, "unknown.png")),
                                                  dark_image=Image.open(os.path.join(TYPE_IMAGE_PATH, "unknown.png")),
                                                  size=(144, 32))
        self.type2_image_label = customtkinter.CTkLabel(self, image = self.type2_image, text="")
        self.type2_image_label.grid(row=1, column=1, padx=5, pady=(0,5))
        # self.type2_image_label.grid_remove()

        # pokemon sprite
        self.sprite_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(POKEMON_IMAGE_PATH, "0.png")),
                                                   dark_image=Image.open(os.path.join(POKEMON_IMAGE_PATH, "0.png")),
                                                   size=(192, 192))
        self.sprite_image_label = customtkinter.CTkLabel(self, image=self.sprite_image, text="")
        self.sprite_image_label.grid(row=2, column=0, columnspan=2, padx=5)
    

    def set_name(self, name: str):
        self.name_label.configure(text=name)

    def set_types(self, type1: customtkinter.CTkImage, type2: customtkinter.CTkImage):
        self.type1_image_label.configure(image = type1)
        self.type2_image_label.configure(image = type2)
    
    def set_pokemon_sprite(self, sprite: customtkinter.CTkImage):
        self.sprite_image_label.configure(image = sprite)


class TypeChartFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("PokeLookup")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        self.APP_FONT = customtkinter.CTkFont(family = FONT_FAMILY, size = FONT_SIZE)

        # configure grid layout (3x2)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.pokemon_details_frame = PokemonDetailsFrame(self)
        self.pokemon_details_frame.name_label.configure(font=self.APP_FONT)
        self.pokemon_details_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.search_bar = customtkinter.CTkEntry(self, placeholder_text="Pokemon Lookup", bg_color="transparent")
        self.search_bar.bind("<Return>", self.search_button_event)
        self.search_bar.grid(row=0, column=1, sticky="nesw", padx=5, pady=5)

        self.search_button = customtkinter.CTkButton(self, text="Search", command = self.search_button_event)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.type_chart_frame = TypeChartFrame(self)
        self.type_chart_frame.configure(fg_color="transparent")
        self.type_chart_frame.grid(row=1, column=1, columnspan=2, sticky="nesw")

        self.pokelookup = PokeLookup()


    def search_button_event(self, event = None):
        search_text = self.search_bar.get()
        print(f"Searching for: {search_text}")
        pokemon = self.pokelookup.find_pokemon(search_text)

        if pokemon is not None:
            # pokemon was found, set all our fields
            print(pokemon)

            # name
            self.pokemon_details_frame.set_name(pokemon.name.title())
            
            # types
            type1_image = Image.open(os.path.join(TYPE_IMAGE_PATH, f"{pokemon.type1.value}.png"))
            type1_ctk = customtkinter.CTkImage(dark_image=type1_image, light_image=type1_image, size=TYPE_SPRITE_SIZE)

            type2_file_name = "none" if pokemon.type2 is None else pokemon.type2.value
            type2_image = Image.open(os.path.join(TYPE_IMAGE_PATH, f"{type2_file_name}.png"))
            type2_ctk = customtkinter.CTkImage(dark_image=type2_image, light_image=type2_image, size=TYPE_SPRITE_SIZE)

            self.pokemon_details_frame.set_types(type1_ctk, type2_ctk)

            # pokemon sprite
            sprite_image = Image.open(os.path.join(POKEMON_IMAGE_PATH, f"{pokemon.id}.png"))
            sprite_ctk = customtkinter.CTkImage(dark_image=sprite_image, light_image=sprite_image, size=POKEMON_SPRITE_SIZE)
            self.pokemon_details_frame.set_pokemon_sprite(sprite_ctk)
        else:
            # pokemon not found, set fields to unknown
            print(f"Unable to find {search_text}")

            # name
            self.pokemon_details_frame.set_name("???")
            
            # types
            type1_image = Image.open(os.path.join(TYPE_IMAGE_PATH, "unknown.png"))
            type1_ctk = customtkinter.CTkImage(dark_image=type1_image, light_image=type1_image, size=TYPE_SPRITE_SIZE)

            type2_image = Image.open(os.path.join(TYPE_IMAGE_PATH, "unknown.png"))
            type2_ctk = customtkinter.CTkImage(dark_image=type2_image, light_image=type2_image, size=TYPE_SPRITE_SIZE)

            self.pokemon_details_frame.set_types(type1_ctk, type2_ctk)

            # pokemon sprite
            sprite_image = Image.open(os.path.join(POKEMON_IMAGE_PATH, "0.png"))
            sprite_ctk = customtkinter.CTkImage(dark_image=sprite_image, light_image=sprite_image, size=POKEMON_SPRITE_SIZE)
            self.pokemon_details_frame.set_pokemon_sprite(sprite_ctk)
        
        self.search_bar.focus_set()
        self.search_bar.select_to(len(search_text))


################################################################################
#  Function:  main                                                             #
#  Purpose:   do all the stuff                                                 #
################################################################################
def main():
    app = App()
    app.mainloop()


################################################################################
#  Script entry point                                                          #
################################################################################
if __name__ == "__main__":
    main()
