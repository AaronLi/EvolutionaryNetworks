from noise import pnoise2
from lib import math_tools
from lib.game_world import game_tile
from pygame import Surface, draw

class WorldMap():

    def __init__(self, xSize, ySize, frequency, water_threshold):
        self.x_size = xSize
        self.y_size = ySize
        self.frequency = frequency
        self.threshold = water_threshold
        self.value_map = []
        self.game_map = []
        self.generate_map()
        self.creatures = []


    def generate_map(self):
        self.value_map = [[math_tools.clamp((pnoise2(j/self.frequency,i/self.frequency)*4+1)/2, 0, 1) for j in range(self.x_size)] for i in range(self.y_size)]
        self.__threshold_map()
        self.__populate_with_tiles()

    def __threshold_map(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                if self.value_map[i][j] < self.threshold:
                    self.value_map[i][j] = 0

    def __populate_with_tiles(self):
        self.game_map = [[game_tile.GameTile(self.value_map[i][j]) for j in range(self.x_size)] for i in range(self.y_size)]

    def update(self):
        total_food = 0
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.game_map[i][j].update()
                total_food+=self.game_map[i][j].current_food

        for i in range(len(self.creatures)-1, -1, -1):

            if self.creatures[i].is_alive:
                self.creatures[i].update(self)
            else:
                del self.creatures[i]
        return total_food

    def get_tile(self, x, y):
        x,y = int(x), int(y)
        if x in range(0, self.x_size) and y in range(0,self.y_size):
            return self.game_map[y][x]
        else:
            return game_tile.null_tile

    def draw(self, scale):
        sOut = Surface((self.x_size*scale, self.y_size*scale))

        for i in range(self.y_size):
            for j in range(self.x_size):
                draw.rect(sOut, self.get_tile(j, i).colour, (j*scale, i*scale, scale, scale))

        for i in self.creatures:
            cSize = i.radius
            draw.circle(sOut, i.colour, (int(i.x*scale), int(i.y*scale)), int(cSize * scale))

            for j in range(-1, 2):
                draw.line(sOut, (255-i.colour[0],255-i.colour[1],255-i.colour[2]), (int(i.x*scale), int(i.y*scale)), (int(i.x*scale) + i.look_distance * math_tools.cosd(i.rotation + i.view_cone*j) * scale, int(i.y*scale) + i.look_distance*scale* math_tools.sind(i.rotation + i.view_cone*j)))
        return sOut

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    import time as pytm
    import evolutionary_neural_creature.creature as enc

    wm = WorldMap(200, 200, 32, 0.35)
    creature = enc.Creature()

    imageOut = Image.new("RGB", (wm.x_size, wm.y_size))

    imDraw = ImageDraw.Draw(imageOut)

    for step in range(50):
        image_start = pytm.time()

        for i in range(wm.y_size):
            for j in range(wm.x_size):
                imDraw.point((j,i), wm.game_map[j][i].colour)

        imageOut.save("world_progression/noise%03d.png"%step)
        image_time = pytm.time() - image_start

        step_start=  pytm.time()
        wm.update()
        print("%3d %.3f %.3f"%(step + 1,pytm.time() - step_start, image_time))