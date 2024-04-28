import os
import math
import customtkinter
from PIL import Image
from pokelookup_core import Pokemon, PokeLookup
from typing import List


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
    
    def set_font(self, f: customtkinter.CTkFont):
        self.name_label.configure(font = f)
    
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

        self.grid_columnconfigure([0,1,2,3], weight=1)

        self.type_chart_label = customtkinter.CTkLabel(self, text="Type Effectiveness")
        self.type_chart_label.grid(row=0, column=0, columnspan=4, padx=5, pady=(0,20), sticky="nesw")

        self.type_eff_images = []
        self.type_eff_labels = []

        num_images = 17
        half_images = math.floor(num_images / 2)
        row = 0
        col = 0
        for i in range(0, num_images):
            # math to calculate rows/columns. Goal here is 4 columns and as many rows as needed. e.g.:
            # <half of images>  <half of labels>    <other half of images>  <other half of labels>
            row = i + 1 if i <= half_images else i - half_images
            col = 0 if i <= half_images else 2

            image = Image.open(os.path.join(TYPE_IMAGE_PATH, f"{i}.png"))
            image_ctk = customtkinter.CTkImage(dark_image=image, light_image=image, size=TYPE_SPRITE_SIZE)
            image_lbl = customtkinter.CTkLabel(master=self, image=image_ctk, text="")
            image_lbl.grid(row=row, column=col, pady=5, sticky="nesw")
            self.type_eff_images.append(image_lbl)

            label = customtkinter.CTkLabel(self, text="?")
            label.grid(row=row, column=col+1, pady=5, sticky="nesw")
            self.type_eff_labels.append(label)
    

    def get_multiplier_fg_color(self, multiplier: float) -> str:
        default = "transparent"
        color = default
        if multiplier < 1:
            color = "#ffc7ce" # light red
        elif multiplier == 1:
            color = default
        elif multiplier > 1:
            color = "#c6efce" # light green
        else:
            color = default
        return color
    
    def get_multiplier_text_color(self, multiplier: float) -> str:
        default = "#dce4ee"
        color = default # gray10 is the default for dark theme
        if multiplier < 1:
            color = "#9c0006" # dark red
        elif multiplier == 1:
            color = default
        elif multiplier > 1:
            color = "#006126" # dark green
        else:
            color = default
        return color
    
    def convert_multiplier_to_text(self, multiplier: float) -> str:
        val = f"{multiplier}"
        if multiplier == 0.5:
            val = "1/2"
        elif multiplier == 0.25:
            val = "1/4"
        return val

    def set_type_chart(self, type_chart: List[float]):
        for i in range(0, len(type_chart)):
            self.type_eff_labels[i].configure(text = self.convert_multiplier_to_text(type_chart[i]))
            self.type_eff_labels[i].configure(fg_color = self.get_multiplier_fg_color(type_chart[i]))
            self.type_eff_labels[i].configure(text_color = self.get_multiplier_text_color(type_chart[i]))

    def reset_type_chart(self):
        for lbl in self.type_eff_labels:
            lbl.configure(text = "?")
            lbl.configure(fg_color = "transparent")
            lbl.configure(text_color = "#dce4ee")

    def set_font(self, f: customtkinter.CTkFont):
        self.type_chart_label.configure(font = f)
        for lbl in self.type_eff_labels:
            lbl.configure(font = f)



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
        self.pokemon_details_frame.set_font(self.APP_FONT)
        self.pokemon_details_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.search_bar = customtkinter.CTkEntry(self, placeholder_text="Pokemon Lookup", bg_color="transparent")
        self.search_bar.bind("<Return>", self.search_button_event)
        self.search_bar.grid(row=0, column=1, sticky="nesw", padx=5, pady=(5, 25))

        self.search_button = customtkinter.CTkButton(self, text="Search", command = self.search_button_event)
        self.search_button.grid(row=0, column=2, padx=5, pady=(5,25))

        self.type_chart_frame = TypeChartFrame(self)
        self.type_chart_frame.configure(fg_color="transparent")
        self.type_chart_frame.grid(row=1, column=1, columnspan=2, sticky="nesw")
        self.type_chart_frame.set_font(self.APP_FONT)

        self.pokelookup = PokeLookup()


    def search_button_event(self, event = None):
        search_text = self.search_bar.get()
        print(f"Searching for: {search_text}")
        pokemon = self.pokelookup.find_pokemon(search_text)

        if pokemon is not None:
            # pokemon was found, set all our fields
            print(pokemon)

            # name
            name_str = f"#{pokemon.id:03} - {pokemon.name.title()}"
            self.pokemon_details_frame.set_name(name_str)
            
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

            # type chart
            self.type_chart_frame.set_type_chart(pokemon.get_type_chart())
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

            self.type_chart_frame.reset_type_chart()
        
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
