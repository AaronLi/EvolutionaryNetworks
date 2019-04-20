from enum import Enum, auto

from lib.neural_network import *
from lib.game_world import world_map
from lib.math_tools import sind, cosd, clamp
import copy, random
from lib.neural_network import network_mutator


class NetworkInputs(Enum):
    ROTATION = 0
    VELOCITY = auto()
    PREFERRED_TEMPERATURE = auto()
    ENERGY = auto()
    TEMPERATURE = auto()
    VIEW0_FOOD = auto()
    VIEW0_TEMPERATURE = auto()
    VIEW0_IS_WATER = auto()
    VIEW0_IS_NULL = auto()
    VIEW1_FOOD = auto()
    VIEW1_TEMPERATURE = auto()
    VIEW1_IS_WATER = auto()
    VIEW1_IS_NULL = auto()
    VIEW2_FOOD = auto()
    VIEW2_TEMPERATURE = auto()
    VIEW2_IS_WATER = auto()
    VIEW2_IS_NULL = auto()
    POSITION_FOOD = auto()
    POSITION_TEMPERATURE = auto()
    POSITION_IS_WATER = auto()
    POSITION_IS_NULL = auto()
    CAN_REPRODUCE = auto()

class NetworkOutputs:
    ROTATE = 0 # 2*(output - 0.5) gives how much of the max rotation speed to rotate left or right
    VELOCITY = 1
    EAT = 2 # > 0.5 is should eat
    REPRODUCE = 3 # > 0.5 is should reproduce

class Creature:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0.5
        self.rotation = 0
        self.velocity = 0
        self.rotation_speed = 0
        self.max_move_speed= 0.5 #grid spaces
        self.max_rotation = 40 #degrees per second
        self.preferred_temperature = 0.5
        self.energy = self.max_energy/2
        self.brain = self.construct_network()
        self.temperature = self.preferred_temperature
        self.vision = []
        self.position_tile = None
        self.is_eating = False
        self.is_reproducing = False
        self.age = 0
        self.last_reproduction = 0
        self.generation = 0
        self.colour = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def construct_network(self):
        networkOut = neural_net.Network()

        layers = [
            layer.Layer(len(NetworkInputs.__members__), len(NetworkInputs.__members__)).initialize_random_weights(),

            #layer.Layer(17).initialize_random_weights(),
            #layer.Layer(10).initialize_random_weights(),
            #layer.Layer(15, activation_function=activation_function.relu).initialize_random_weights(),
            layer.Layer(10, activation_function=activation_function.relu).initialize_random_weights(),
            layer.Layer(4, activation_function= activation_function.sigmoid).initialize_random_weights()
        ]

        for i in layers:
            networkOut.add_layer(i)

        return networkOut

    def __feed_network(self):
        """
        Applies inputs from world into the neural network for interpretation
        """
        input_vector = [0 for i in range(self.brain.input_size)]
        input_vector[NetworkInputs.ROTATION.value] = self.rotation/360
        input_vector[NetworkInputs.VELOCITY.value] = self.velocity
        input_vector[NetworkInputs.PREFERRED_TEMPERATURE.value] = self.preferred_temperature
        input_vector[NetworkInputs.ENERGY.value] = self.energy / self.max_energy
        input_vector[NetworkInputs.TEMPERATURE.value] = self.temperature
        input_vector[NetworkInputs.VIEW0_FOOD.value] = self.vision[0].current_food
        input_vector[NetworkInputs.VIEW0_TEMPERATURE.value] = self.vision[0].temperature
        input_vector[NetworkInputs.VIEW0_IS_NULL.value] = self.vision[0].is_null
        input_vector[NetworkInputs.VIEW0_IS_WATER.value] = self.vision[0].is_water
        input_vector[NetworkInputs.VIEW1_FOOD.value] = self.vision[1].current_food
        input_vector[NetworkInputs.VIEW1_TEMPERATURE.value] = self.vision[1].temperature
        input_vector[NetworkInputs.VIEW1_IS_NULL.value] = self.vision[1].is_null
        input_vector[NetworkInputs.VIEW1_IS_WATER.value] = self.vision[1].is_water
        input_vector[NetworkInputs.VIEW2_FOOD.value] = self.vision[2].current_food
        input_vector[NetworkInputs.VIEW2_TEMPERATURE.value] = self.vision[2].temperature
        input_vector[NetworkInputs.VIEW2_IS_NULL.value] = self.vision[2].is_null
        input_vector[NetworkInputs.VIEW2_IS_WATER.value] = self.vision[2].is_water
        input_vector[NetworkInputs.POSITION_FOOD.value] = self.position_tile.current_food
        input_vector[NetworkInputs.POSITION_TEMPERATURE.value] = self.position_tile.temperature
        input_vector[NetworkInputs.POSITION_IS_NULL.value] = self.position_tile.is_null
        input_vector[NetworkInputs.POSITION_IS_WATER.value] = self.position_tile.is_water
        input_vector[NetworkInputs.CAN_REPRODUCE.value] = self.can_reproduce

        self.brain.write_inputs(input_vector)

    def __interpret_network(self):
        """
        Reads outputs from neural network and interprets them
        """
        outputs = self.brain.calculate_output()
        #print(outputs)
        self.velocity = self.max_move_speed*outputs[NetworkOutputs.VELOCITY]
        self.rotation_speed = self.max_rotation*(outputs[NetworkOutputs.ROTATE]-0.5)*2

        if outputs[NetworkOutputs.EAT] > 0.5:
            self.is_eating = True

        if outputs[NetworkOutputs.REPRODUCE] > 0.5:
            self.is_reproducing = True

    def __sense_world(self, world: world_map.WorldMap):
        self.vision = []
        for i in range(-1, 2):
            lookX = cosd(self.rotation + i*45)
            lookY = sind(self.rotation + i*45)

            coordinateX = self.x+lookX
            coordinateY = self.y+lookY

            self.vision.append(world.get_tile(coordinateX, coordinateY))
        self.position_tile = world.get_tile(self.x, self.y)

    def think(self, world):
        self.__sense_world(world)
        self.__feed_network()
        self.__interpret_network()

    def eat(self):
        amount_eaten = min(self.size / 10, self.position_tile.current_food)
        gained_energy = amount_eaten * 500
        if self.position_tile.active and self.energy+gained_energy < self.max_energy:
            self.position_tile.current_food -= amount_eaten
            self.energy += gained_energy
        else:
            self.energy -= self.size * 5

    def update(self, world: world_map.WorldMap):
        """
        Interpret outputs of network and move character
        """
        self.think(world)
        self.rotation= (self.rotation+self.rotation_speed)%360
        self.x = clamp(self.velocity * cosd(self.rotation) + self.x, self.radius, world.x_size - self.radius)
        self.y = clamp(self.velocity * sind(self.rotation) + self.y, self.radius, world.y_size - self.radius-1)
        self.energy -= self.energy_consumption
        self.age+=1

        if self.is_reproducing:
            new_creature = self.reproduce()
            if new_creature is not None:
                world.creatures.append(new_creature)
            self.is_reproducing = False

        if self.is_eating:
            self.eat()
            self.is_eating = False

    def reproduce(self):
        """
        Creates a descendant of this creature if the creature is able to reproduce
        :return: None if the creature is unable to reproduce or a new creature if it is
        """
        if self.can_reproduce:
            self.last_reproduction = self.age
            self.energy -= 300

            new_creature = copy.deepcopy(self)

            new_creature.age = 0
            new_creature.last_reproduction = 0
            new_creature.energy = 280
            new_creature.brain = network_mutator.mutate_network(self.brain)
            new_creature.generation+=1
            new_creature.colour = (clamp(self.colour[0]+random.randint(-1,2), 0, 255), clamp(self.colour[1]+random.randint(-1,2),0, 255), clamp(self.colour[2]+random.randint(-1,2), 0, 255))
            return new_creature
        else:
            return None

    @property
    def max_energy(self):
        return self.size * 800

    @property
    def energy_consumption(self):

        return self.size * 10 + (self.velocity * self.size) + (self.rotation_speed * self.size/360)

    @property
    def is_alive(self):
        return self.energy > 0 and self.temperature > 0

    @property
    def temperature_delta(self):
        # negative if too cold, positive if too hot
        return self.temperature - self.preferred_temperature

    @property
    def can_reproduce(self):
        return self.age - self.last_reproduction > 30 and self.energy > self.max_energy / 1.5 # must be older than 30 time units

    @property
    def radius(self):
        return self.size + self.energy/self.max_energy/2