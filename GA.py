import snake_training as g
import snake_brain
import pickle
import random
import numpy as np

#####################
### GA parameters ###
#####################

solved = False
population = []
population_size = 1000
fitness_values = [0] * 1000
selection_rate = 0.5
mutation_rate = 0.2
generation = 0
max_generation = 10

###################
### GA fuctions ###
###################

def initialize(population_size):
    """ create the first population randomly"""

    for i in range(population_size):
        population.append(snake_brain.NeuralNet(32, 24, 12, 4) )
        
    print('\n<<< population initialized, size =',len(population), '>>>')

def fitness(population):
    """ calculate a fitness value for all indiviual by gameplay"""
    
    print('<<< fitness values calculated>>>')
    
    for i in range(len(population)):
        game = g.Game()
        fitness_values[i] = game.gameplay(population[i])
        
def sort():
    """ sort the population by their fitness values """
    global population, fitness_values
    population, fitness_values = zip(*sorted(zip(population, fitness_values), key=lambda x: x[1]))
    population = list(population)
    fitness_values = list(fitness_values)

    print("<<< population sorted >>> \n")
    for i in range(10): 
        print(f"individual[{i}] fitness = {fitness_values[i]}")
    print('\n') 
    for i in range(len(population)-10, len(population)):
        print(f"individual[{i}] fitness = {fitness_values[i]}")

def selection():
    """ select the parents and kill the weaks """
    global population
    for i in range(int(population_size*selection_rate)):
        population.pop(0)
        fitness_values.pop(0)
        
    print('\n<<< selection completed, killed = ',population_size*selection_rate,'>>>')

def crossover():
    """ make new childs """
    global mutation_rate
    
    global population, fitness_values
    n = int(population_size*selection_rate/2)
    for i in range(n):
        # choose random 2 parent
        parent_A = random.randrange(n)
        parent_B = random.randrange(n)
        # until they will be different
        while parent_A == parent_B:
            parent_A = random.randrange(n)
            parent_B = random.randrange(n)  

             # create two child neurons from two parent neurons
        child1 = snake_brain.NeuralNet(32, 24, 12, 4)
        child2 = snake_brain.NeuralNet(32, 24, 12, 4)
        
        # perform multipoint crossover
        for j in range(child1.weights1.shape[0]):
            for k in range(child1.weights1.shape[1]):
                if random.random() < 0.5:
                    child1.weights1[j][k] = population[parent_A].weights1[j][k]
                    child2.weights1[j][k] = population[parent_B].weights1[j][k]
                else:
                    child1.weights1[j][k] = population[parent_B].weights1[j][k]
                    child2.weights1[j][k] = population[parent_A].weights1[j][k]
        
        for j in range(child1.weights2.shape[0]):
            for k in range(child1.weights2.shape[1]):
                if random.random() < 0.5:
                    child1.weights2[j][k] = population[parent_A].weights2[j][k]
                    child2.weights2[j][k] = population[parent_B].weights2[j][k]
                else:
                    child1.weights2[j][k] = population[parent_B].weights2[j][k]
                    child2.weights2[j][k] = population[parent_A].weights2[j][k]
        
        for j in range(child1.weights3.shape[0]):
            for k in range(child1.weights3.shape[1]):
                if random.random() < 0.5:
                    child1.weights3[j][k] = population[parent_A].weights3[j][k]
                    child2.weights3[j][k] = population[parent_B].weights3[j][k]
                else:
                    child1.weights3[j][k] = population[parent_B].weights3[j][k]
                    child2.weights3[j][k] = population[parent_A].weights3[j][k]
        
        # mutate the children
        mutation(child1, mutation_rate)
        mutation(child2, mutation_rate)
        
        # add the new childs to the population
        population = list(population)
        fitness_values = list(fitness_values)
        population.append(child1)
        population.append(child2)
        fitness_values.append(0)
        fitness_values.append(0)
        
    print('<<< crossover completed, population size =',len(population),'>>>')
 
def mutation(child, mutation_rate):
    """ mutate the new childs """
    for i in range(child.weights1.shape[0]):
        for j in range(child.weights1.shape[1]):
            if random.random() < mutation_rate:
                child.weights1[i][j] += np.random.normal(0, 0.1)
    
    for i in range(child.weights2.shape[0]):
        for j in range(child.weights2.shape[1]):
            if random.random() < mutation_rate:
                child.weights2[i][j] += np.random.normal(0, 0.1)
    
    for i in range(child.weights3.shape[0]):
        for j in range(child.weights3.shape[1]):
            if random.random() < mutation_rate:
                child.weights3[i][j] += np.random.normal(0, 0.1)

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

    while (generation < max_generation):
        fitness(population)
        
        if solved==True:
            break
            # save brain out
        sort()
        selection()
        crossover()
        # todo
        # mutation()
        generation += 1 
 
training()

#save the net to a file
with open('brains.pickle', 'wb') as f:
    pickle.dump(population, f)
       
        
# todo error -> kulombseg van a training es visual gameplay kozott -> le kell ellenorizni
# nem azonos eredmeny ad a tesztnel mivel az almakat random generalja - tombbe kellene tarolni a generalasokat
# tesztek mindenhova hogyan nez ki egy mutacio? egy crossover barmi print print print
# crossover es mutacio megertese
# fitness kiertekeles javitasa
