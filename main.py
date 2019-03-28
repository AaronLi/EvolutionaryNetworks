if __name__ == "__main__":
    from lib.neural_network import *


    nw = network.Network()

    l1 = layer.Layer(10)

    l2 = layer.Layer(6)

    l3 = layer.Layer(5)

    l4 = layer.Layer(20)


    nw.add_layer(l1).add_layer(l2).add_layer(l3).add_layer(l4)

    input_values = [float(i) for i in input('Enter 10 values into the vector ').split()]

    nw.write_inputs(input_values)

    nw2 = network_mutator.mutate_network(nw)

    print(nw.calculate_output())

    print(nw2.calculate_output())