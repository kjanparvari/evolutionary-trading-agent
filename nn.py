import numpy as np


class NN:

    def __init__(self, layer_sizes: list):
        self.layer_sizes = layer_sizes
        self.weights = dict()
        self.biases = dict()
        for layer_number in range(1, self.network_size):
            self.weights[layer_number] = np.random.normal(
                size=(self.layer_sizes[layer_number], self.layer_sizes[layer_number - 1]))
            self.biases[layer_number] = np.zeros(shape=(self.layer_sizes[layer_number], 1))

    @property
    def network_size(self):
        return len(self.layer_sizes)

    @staticmethod
    def activation(array: np.ndarray):
        """
        activation function. currently SIGMOID
        :param array:
        :return:
        """
        return 1 / (1 + np.exp(-array))

    def forward(self, _input: np.ndarray) -> np.ndarray:
        """
        neural network feed forward
        :param _input: custom input data
        :return: last layer
        """
        layers = {
            0: _input
        }
        for layer_number in range(1, self.network_size):
            layers[layer_number] = self.activation(
                np.matmul(self.weights[layer_number], layers[layer_number - 1]) + self.biases[layer_number])
        return layers[self.network_size - 1].copy()

    def copy(self):
        new_nn = NN(self.layer_sizes)
        for layer_number in range(1, self.network_size):
            new_nn.weights[layer_number] = self.weights[layer_number].copy()
            new_nn.biases[layer_number] = self.biases[layer_number].copy()
        return new_nn
