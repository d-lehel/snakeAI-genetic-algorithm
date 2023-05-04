import simulation as game
import pickle

with open('manual_trained_brain.pickle', 'rb') as f:
    net = pickle.load(f)
    # testing
    for i in range(2):
        game.gameplay(net, True, True, 10)