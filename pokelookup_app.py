import os
import customtkinter
from PIL import Image


APP_WIDTH = 1000
APP_HEIGHT = 600

class PokemonDetailsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # pokemon name label
        self.name_label = customtkinter.CTkLabel(self, text="Bulbasaur")
        self.name_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        # setup paths to sprites
        base_image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sprites")
        type_image_path = os.path.join(base_image_path, "types", "generation-viii", "brilliant-diamond-and-shining-pearl")
        pokemon_image_path = os.path.join(base_image_path, "pokemon")

        # type 1
        self.type1_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(type_image_path, "12.png")),
                                                  dark_image=Image.open(os.path.join(type_image_path, "12.png")),
                                                  size=(144, 32))
        self.type1_image_label = customtkinter.CTkLabel(self, image = self.type1_image, text="")
        self.type1_image_label.grid(row=1, column=0, padx=5, pady=(0,5))

        # type 2
        self.type2_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(type_image_path, "4.png")),
                                                  dark_image=Image.open(os.path.join(type_image_path, "4.png")),
                                                  size=(144, 32))
        self.type2_image_label = customtkinter.CTkLabel(self, image = self.type2_image, text="")
        self.type2_image_label.grid(row=1, column=1, padx=5, pady=(0,5))
        # self.type2_image_label.grid_remove()

        # pokemon sprite
        self.sprite_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(pokemon_image_path, "1.png")),
                                                   dark_image=Image.open(os.path.join(pokemon_image_path, "1.png")),
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


# class SearchFrame(customtkinter.CTkFrame):
#     def __init__(self, master):
#         super().__init__(master)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_columnconfigure(1, weight=0)

#         self.entry = customtkinter.CTkEntry(self, placeholder_text="Pokemon Lookup")
#         self.entry.grid(row=0, column=0, sticky="nesw", padx=5, pady=5)

#         self.search_button =customtkinter.CTkButton(self, text="Search", command = None)
#         self.search_button.grid(row=0, column=1, padx=5, pady=5)

#     def search_button_event(self):
#         pass


class TypeChartFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("PokeLookup")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        # configure grid layout (3x2)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.pokemon_details_frame = PokemonDetailsFrame(self)
        self.pokemon_details_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.search_bar = customtkinter.CTkEntry(self, placeholder_text="Pokemon Lookup", bg_color="transparent")
        self.search_bar.grid(row=0, column=1, sticky="nesw", padx=5, pady=5)

        self.search_button = customtkinter.CTkButton(self, text="Search", command = self.search_button_event)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.type_chart_frame = TypeChartFrame(self)
        self.type_chart_frame.configure(fg_color="transparent")
        self.type_chart_frame.grid(row=1, column=1, columnspan=2, sticky="nesw")


    def search_button_event(self):
        print("button pressed")


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
