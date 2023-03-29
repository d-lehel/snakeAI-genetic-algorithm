import numpy as np

class NeuralNet:
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size):
        # Initialize the weights and biases for the first hidden layer
        self.weights1 = np.random.randn(input_size, hidden_size1)
        self.biases1 = np.random.randn(hidden_size1)* 0.1 # ???
        
        # Initialize the weights and biases for the second hidden layer
        self.weights2 = np.random.randn(hidden_size1, hidden_size2)
        self.biases2 = np.random.randn(hidden_size2)* 0.1
        
        # Initialize the weights and biases for the output layer
        self.weights3 = np.random.randn(hidden_size2, output_size)
        self.biases3 = np.random.randn(output_size)* 0.1
    
    def forward(self, x):
        # Forward pass through the network
        hidden_layer1 = np.maximum(0, np.dot(x, self.weights1) + self.biases1)
        hidden_layer2 = np.maximum(0, np.dot(hidden_layer1, self.weights2) + self.biases2)
        output_layer = np.dot(hidden_layer2, self.weights3) + self.biases3
        return output_layer