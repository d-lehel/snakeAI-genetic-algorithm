import simulation as game
import pickle

# rank -10000, -2000, -1000, -500 
with open('brains-1000.pickle', 'rb') as f:
    data = pickle.load(f)
    individuals = data[0]
    parameters = data[2]
    best = individuals[len(individuals)-1]
    
for p in parameters:    
    print('\n',p,parameters[p])
print('\n')

# testing the best individual from training
for i in range(1):
    game.gameplay(best, True, True, 0.7)