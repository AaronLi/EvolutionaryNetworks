import lib.colour_constants as colours

class GameTile:

    MAX_FOOD_PER_TILE = 0.5

    def __init__(self, root_value):
        self.root_value = root_value

        self.growth_reduction = 0.003

        #all values from 0 to 1
        self.current_food = 0
        self.growth_rate = 1 - root_value
        self.temperature = 0.5
        self.is_water = root_value==0
        self.is_null = root_value == -1

    @property
    def colour(self):
        if not self.active:
            return colours.WATER

        colour = (int(self.temperature * 128), min(255,int(self.current_food * 255)+32), int(self.growth_rate * 200))

        return colour

    def update(self):
        if not self.active:
            return

        self.current_food = min((self.temperature * self.growth_rate)*self.growth_reduction+self.current_food, GameTile.MAX_FOOD_PER_TILE)

    @property
    def active(self):
        return not (self.is_water or self.is_null)

null_tile = GameTile(-1)