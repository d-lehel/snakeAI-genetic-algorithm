import numpy as np

class NeuralNet:
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        
        # in   h1   h2   out 
    
        # 1
        # .    1
        # .    .    1    
        # .    .    .    1 -> up
        # .    .    .    2 -> right
        # .    .    .    3 -> down
        # .    .    .    4 -> left
        # .    .   12
        # .    24
        # 32
        
        # first hidden layer = [32,24], hidden1 biases = [24]
        self.weights1 = np.random.randn(input_size, hidden1_size)
        self.biases1 = np.random.randn(hidden1_size)* 0.1 # ???
        
        # second hidden layer = [24,12], hidden2 biases = [12]
        self.weights2 = np.random.randn(hidden1_size, hidden2_size)
        self.biases2 = np.random.randn(hidden2_size)* 0.1
        # output layer = [12, 4], output biases = [4]
        self.weights3 = np.random.randn(hidden2_size, output_size)
        self.biases3 = np.random.randn(output_size)* 0.1
    
    def forward(self, input):
        # pass through the network
        # dot - scalar multiplication
        hidden_layer1 = np.maximum(0, np.dot(input, self.weights1) + self.biases1)
        hidden_layer2 = np.maximum(0, np.dot(hidden_layer1, self.weights2) + self.biases2)
        output_layer = np.dot(hidden_layer2, self.weights3) + self.biases3
        return output_layer
    
# test
# net = NeuralNet(32,24,12,4)
# print('weights row size',len(net.weights1))
# print('weights row[0] size',len(net.weights1[0]))
    
