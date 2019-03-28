from lib.neural_network import activation_function as activaction
import numpy as np

class Layer:
    def __init__(self, num_nodes, input_vector_dimension = 0):
        """
        Constructor for the layer. Takes the size of the new layer and the size of the input vector
        :param num_nodes: The number of nodes in this layer
        :param input_vector_dimension:  The number of values in the layer before this
        """

        #the output vector that is accessed by child layers
        self.output_vector = np.ndarray((num_nodes,), dtype=np.float32)



        self.num_nodes = num_nodes
        self.set_input_size(input_vector_dimension)

    def initialize_random_weights(self):
        """
        Generates random weights for the input_weights of this layer
        """
        self.input_weights = np.random.rand(self.num_nodes, self.input_size)
        return self

    def calculate_output_vector(self, parent_layer, activation_function = activaction.sigmoid):
        self.output_vector = np.zeros((self.num_nodes, ))
        for output_node in range(self.num_nodes):
            for input_node in range(self.input_size):
                self.output_vector[output_node] += activation_function(parent_layer.output_vector[input_node] * self.input_weights[output_node, input_node])

        for i in range(self.output_vector.shape[0]):
            self.output_vector[i]/=parent_layer.output_vector.shape[0]

    def set_input_size(self, new_size):
        self.input_size = new_size
        # x is a node on this layer, y is the weight of the y'th parent node on the x'th node
        self.input_weights = np.ndarray((self.num_nodes, self.input_size), dtype=np.float32)

