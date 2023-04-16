import snake_training as game
import pickle

with open('brains_500.pickle', 'rb') as f:
    data = pickle.load(f)
    individuals = data[0]
    parameters = data[1]
    best = individuals[len(individuals)-1]
    
for p in parameters:    
    print('\n',p,parameters[p])
print('\n')

# testing the best individual from training n times
for i in range(2):
    game.gameplay(best, True)