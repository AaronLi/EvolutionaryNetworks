import numpy as np
import lib.neural_network.activation_function as af

class Network:
    def __init__(self):

        self.layers = []

    def add_layer(self, new_layer):
        self.insert_layer(len(self.layers), new_layer)
        return self

    def insert_layer(self, index, new_layer):
        if index > 0:
            new_layer.set_input_size(self.layers[index-1].num_nodes)

        new_layer.initialize_random_weights()
        self.layers.insert(index, new_layer)
        return self

    @property
    def input_size(self):
        return self.layers[0].input_size

    def write_inputs(self, input_vector):
        np.copyto(self.layers[0].output_vector, input_vector)

    def calculate_output(self):

        for layerIndex in range(1, len(self.layers)):
            self.layers[layerIndex].calculate_output_vector(self.layers[layerIndex-1])

        outVector = self.layers[-1].output_vector.copy(order='k')

        return outVector