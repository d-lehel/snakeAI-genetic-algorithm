import game_training as game
import random
import numpy as np
import pickle


##########################
#### neural net class ####
##########################

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
        net = NeuralNet(32, 24, 12, 4) 
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
        
