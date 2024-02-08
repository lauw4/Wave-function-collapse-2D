import tkinter as tk

class Player():
    def __init__(self, name, image_path, canvas, initial_position=(0, 0)):
        self.name = name
        self.image_path = image_path
        self.canvas = canvas
        self.position = initial_position
        self.load_image()

    def load_image(self):
        self.image = tk.PhotoImage(file=self.image_path)
        self.character = self.canvas.create_image(self.position[0], self.position[1], anchor=tk.NW, image=self.image)

    def move(self, direction):
        x, y = self.position
        if direction == "north":
            y -= 1
        elif direction == "south":
            y += 1
        elif direction == "west":
            x -= 1
        elif direction == "east":
            x += 1

        # Check if the new position is on the road
        if self.is_on_road(x, y):
            self.position = (x, y)
            self.canvas.coords(self.character, x * 16, y * 16)

    def is_on_road(self, x, y,world):
        road_tile = world[y][x]  # Assuming (0, 0) is the top-left corner
        return road_tile == "road"  # Assuming "road" represents the road tile
    

def move_player(event, player):
    if event.keysym in ["Up", "Down", "Left", "Right"]:
        player.move(event.keysym.lower())

# get tile where the player is standing (Class mapp.getland) 
# get the sides of the tile if they are road or not (y-1.map.getland)
# if there is a road in there move to the road tile
# check if the road in on the edge of the map (have less than 4 neighbours)

