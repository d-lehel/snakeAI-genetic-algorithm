import numpy as np

class NeuralNet:
    def __init__(self, input_size, hidden1_size, hidden2_size, output_size):
        """
            input layer size = 32
            first hidden layer size = 24
            second hidden layer size = 12
            output layer size = 4
        """
        
        self.weights1 = np.random.randn(input_size, hidden1_size)
        self.biases1 = np.random.randn(hidden1_size)* 0.1
        
        self.weights2 = np.random.randn(hidden1_size, hidden2_size)
        self.biases2 = np.random.randn(hidden2_size)* 0.1
        self.weights3 = np.random.randn(hidden2_size, output_size)
        self.biases3 = np.random.randn(output_size)* 0.1
        
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, input):
        hidden_layer1 = self.relu(np.dot(input, self.weights1) + self.biases1)
        hidden_layer2 = self.relu(np.dot(hidden_layer1, self.weights2) + self.biases2)
        self.hidden_layer1 = hidden_layer1  # save as attribute
        self.hidden_layer2 = hidden_layer2  # save as attribute
        output_layer = np.dot(hidden_layer2, self.weights3) + self.biases3
        return output_layer
    
      # input data:  [[1 0 0 ... 1 0 0]
        #              [1 0 0 ... 1 0 0]
        #              [1 0 0 ... 1 0 0]
        #              ...
        #              [1 0 0 ... 0 0 0]
        #              [1 0 1 ... 0 0 0]
        #              [1 0 1 ... 0 0 0]]
       
        # target data:  [[0 1 0 0]
        #               [0 1 0 0]
        #               [0 1 0 0]
        #               ...
        #               [0 1 0 0]
        #               [0 0 1 0]
        #               [0 1 0 0]]
    
    def train(self, input_data, target_data, learning_rate=0.001, epochs=1000, batch_size=32):
       
        num_batches = input_data.shape[0] // batch_size
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            epoch_accuracy = 0.0
            
            for i in range(num_batches):
                # Get batch of inputs and targets
                batch_input = input_data[i*batch_size:(i+1)*batch_size]
                batch_target = target_data[i*batch_size:(i+1)*batch_size]

                # Forward pass
                hidden_layer1 = self.relu(np.dot(batch_input, self.weights1) + self.biases1)
                hidden_layer1 = (hidden_layer1 - np.mean(hidden_layer1, axis=0)) / np.sqrt(np.var(hidden_layer1, axis=0) + 1e-8)
                hidden_layer2 = self.relu(np.dot(hidden_layer1, self.weights2) + self.biases2)
                hidden_layer2 = (hidden_layer2 - np.mean(hidden_layer2, axis=0)) / np.sqrt(np.var(hidden_layer2, axis=0) + 1e-8)
                output_layer = np.dot(hidden_layer2, self.weights3) + self.biases3

                # Compute loss and accuracy
                softmax_output = np.exp(output_layer) / np.sum(np.exp(output_layer), axis=1, keepdims=True)
                cross_entropy_loss = -np.sum(batch_target*np.log(softmax_output+1e-8))
                epoch_loss += cross_entropy_loss
                predicted_labels = np.argmax(softmax_output, axis=1)
                true_labels = np.argmax(batch_target, axis=1)
                epoch_accuracy += np.sum(predicted_labels == true_labels) / batch_size

                # Backward pass
                grad_output = (softmax_output - batch_target) / batch_size
                grad_hidden2 = np.dot(grad_output, self.weights3.T)
                grad_hidden2[hidden_layer2 <= 0] = 0
                grad_hidden1 = np.dot(grad_hidden2, self.weights2.T)
                grad_hidden1[hidden_layer1 <= 0] = 0

                # Update weights and biases
                grad_weights3 = np.dot(hidden_layer2.T, grad_output)
                grad_biases3 = np.sum(grad_output, axis=0)
                grad_weights2 = np.dot(hidden_layer1.T, grad_hidden2)
                grad_biases2 = np.sum(grad_hidden2, axis=0)
                grad_weights1 = np.dot(batch_input.T, grad_hidden1)
                grad_biases1 = np.sum(grad_hidden1, axis=0)

                self.weights3 -= learning_rate * grad_weights3
                self.biases3 -= learning_rate * grad_biases3
                self.weights2 -= learning_rate * grad_weights2
                self.biases2 -= learning_rate * grad_biases2
                self.weights1 -= learning_rate * grad_weights1
                self.biases1 -= learning_rate * grad_biases1

                epoch_loss /= num_batches
                epoch_accuracy /= num_batches
                
                if epoch % 50 == 0:
                    print(f"Epoch {epoch}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_accuracy:.4f}")
