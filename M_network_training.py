import pickle
import snake_brain as sb

input_data = []
target_data = []

with open('training_data.pickle', 'rb') as f:
    data = pickle.load(f)
    input_data = data[0]
    target_data = data[1]

brain = sb.NeuralNet(32, 24, 12, 4)

# before training    
# print(brain.weights1[0])    

brain.train(input_data, target_data)

with open('manual_trained_brain.pickle', 'wb') as f:
    pickle.dump(brain, f)
    print('data saved!')
    
# after training
# print(brain.weights1[0])
