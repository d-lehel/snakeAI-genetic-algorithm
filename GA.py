import game_training as game
import snake_brain

#####################
### GA parameters ###
#####################

solved = False
population = []
population_size = 10
fitness_values = [0] * 10
selection_rate = 0.5
mutation_rate = 0.5
generation = 0

###################
### GA fuctions ###
###################

def initialize(population_size):
    """ create the first population randomly"""
    for i in range(population_size):
        net = snake_brain.NeuralNet(32, 24, 12, 4) 
        population.append(net)
        
    print('population initialized!')

def fitness(population):
    """ calculate a fitness value for all indiviual by gameplay"""
    print('calculate fitness values!')
    
    for i in range(len(population)):
        fitness_values[i] = game.gameplay(population[i])
        print('calculated value for index-',i, fitness_values[i])
        
def sort():
    """ sort the population by their fitness values """

def selection():
    """ select the parents and kill the weaks """

def crossover():
    """ make new childs """
 
def mutation():
    """ mutate the new childs """

################
### gameplay ###
################

def gameplay(individual):
    pass

################
### training ###
################

def training():
    global generation, population
    
    initialize(population_size)

    while (generation < 100):
        fitness(population)
        
        if solved==True:
            break
            # save brain out
        
        sort()
        selection()
        crossover()
        mutation()
        generation += 1 
        
initialize(population_size)
fitness(population)
        
