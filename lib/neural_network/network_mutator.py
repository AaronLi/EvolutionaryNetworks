from random import *
from lib.math_tools import random_bump
import copy

def mutate_layer(layerIn):
    layerOut = copy.deepcopy(layerIn)

    for i in range(layerOut.input_weights.shape[0]):
        for j in range(layerOut.input_weights.shape[1]):
            if random() < 0.1:
                layerOut.input_weights[i,j] = random_bump(layerOut.input_weights[i,j], -100, 100, 0.1)

    return layerOut

def mutate_network(networkIn):
    networkOut = copy.deepcopy(networkIn)

    for i in range(len(networkOut.layers)):
        networkOut.layers[i] = mutate_layer(networkOut.layers[i])

    return networkOut