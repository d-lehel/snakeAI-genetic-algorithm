import snake_training as game
import pickle

# testing the best individual from training
with open('brain.pickle', 'rb') as f:
    net = pickle.load(f)
game.gameplay(net, True)