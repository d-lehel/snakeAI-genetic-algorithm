import snake_training as g
import snake_brain
import pickle
import random
import numpy as np
import time


#####################
### GA parameters ###
#####################

solved = False
population = []
population_size = 500
fitness_values = [0] * 500
selection_rate = 0.6
mutation_rate = 0.5
mutation_strenght = 0.5
generation = 0
max_generation = 10
tested_n_times = 5
last_parameters = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0}

###################
### GA fuctions ###
###################


def initialize(population_size):
    """ create the first population randomly"""

    for i in range(population_size):
        population.append(snake_brain.NeuralNet(32, 24, 12, 4))


def fitness(population, tested_n_times):
    """ calculate a fitness value for all indiviual by gameplay"""

    for i in range(len(population)):
        sum_fitness = 0
        for j in range(tested_n_times):
            sum_fitness += g.gameplay(population[i], False)
        fitness_values[i] = sum_fitness / tested_n_times


def sort():
    """ sort the population by their fitness values """
    global population, fitness_values
    population, fitness_values = zip(
        *sorted(zip(population, fitness_values), key=lambda x: x[1]))
    population = list(population)
    fitness_values = list(fitness_values)

    print("<<< population afer sorted >>> \n")
    for i in range(10):
        print(f"individual[{i}] fitness = {fitness_values[i]}")
    print('\n')
    for i in range(len(population)-10, len(population)):
        print(f"individual[{i}] fitness = {fitness_values[i]}")

    print(f'\n<<< Generation: {generation+1} >>>')


def selection():
    """ select the parents and kill the weaks """
    global population
    for i in range(int(population_size*selection_rate)):
        population.pop(0)
        fitness_values.pop(0)


def crossover():
    """ make new childs """
    global population, fitness_values

    n = int(population_size*selection_rate/2)
    for i in range(n):
        # choose random two different parrent
        parent_A = random.randrange(n)
        parent_B = random.randrange(n)
        while parent_A == parent_B:
            parent_A = random.randrange(n)
            parent_B = random.randrange(n)

        # create two child
        child1 = snake_brain.NeuralNet(32, 24, 12, 4)
        child2 = snake_brain.NeuralNet(32, 24, 12, 4)

        # multipoint crossover for weights
        for j in range(len(child1.weights1)):
            for k in range(len(child1.weights1[0])):
                if random.random() < 0.5:
                    child1.weights1[j][k] = population[parent_A].weights1[j][k]
                    child2.weights1[j][k] = population[parent_B].weights1[j][k]
                else:
                    child1.weights1[j][k] = population[parent_B].weights1[j][k]
                    child2.weights1[j][k] = population[parent_A].weights1[j][k]

        for j in range(len(child1.weights2)):
            for k in range(len(child1.weights2[0])):
                if random.random() < 0.5:
                    child1.weights2[j][k] = population[parent_A].weights2[j][k]
                    child2.weights2[j][k] = population[parent_B].weights2[j][k]
                else:
                    child1.weights2[j][k] = population[parent_B].weights2[j][k]
                    child2.weights2[j][k] = population[parent_A].weights2[j][k]

        for j in range(len(child1.weights3)):
            for k in range(len(child1.weights3[0])):
                if random.random() < 0.5:
                    child1.weights3[j][k] = population[parent_A].weights3[j][k]
                    child2.weights3[j][k] = population[parent_B].weights3[j][k]
                else:
                    child1.weights3[j][k] = population[parent_B].weights3[j][k]
                    child2.weights3[j][k] = population[parent_A].weights3[j][k]

        # multipoint crossover for biases
        for j in range(len(child1.biases1)):
            if random.random() < 0.5:
                child1.biases1[j] = population[parent_A].biases1[j]
                child2.biases1[j] = population[parent_B].biases1[j]
            else:
                child1.biases1[j] = population[parent_B].biases1[j]
                child2.biases1[j] = population[parent_A].biases1[j]

        for j in range(len(child1.biases2)):
            if random.random() < 0.5:  # 50%
                child1.biases2[j] = population[parent_A].biases2[j]
                child2.biases2[j] = population[parent_B].biases2[j]
            else:
                child1.biases2[j] = population[parent_B].biases2[j]
                child2.biases2[j] = population[parent_A].biases2[j]

        for j in range(len(child1.biases3)):
            if random.random() < 0.5:
                child1.biases3[j] = population[parent_A].biases3[j]
                child2.biases3[j] = population[parent_B].biases3[j]
            else:
                child1.biases3[j] = population[parent_B].biases3[j]
                child2.biases3[j] = population[parent_A].biases3[j]

        # add the new childs to the population
        population = list(population)
        fitness_values = list(fitness_values)
        population.append(child1)
        population.append(child2)
        fitness_values.append(0)
        fitness_values.append(0)


def mutation():
    """ mutate the new childs """
    global population, selection_rate, mutation_rate, mutation_strenght
    n_snake = int(population_size*selection_rate*mutation_rate)

    for i in range(n_snake):

        # mutation for weights
        for j in range(len(population[i].weights1)):
            for k in range(len(population[i].weights1[0])):
                if random.random() < mutation_strenght:  # 30% chance to mutate this weight
                    population[i].weights1[j][k] += np.random.normal(0, 0.1)

        for j in range(len(population[i].weights2)):
            for k in range(len(population[i].weights2[0])):
                if random.random() < mutation_strenght:
                    population[i].weights2[j][k] += np.random.normal(0, 0.1)

        for j in range(len(population[i].weights3)):
            for k in range(len(population[i].weights3[0])):
                if random.random() < mutation_strenght:
                    population[i].weights3[j][k] += np.random.normal(0, 0.1)

        # mutation for biases
        for j in range(len(population[i].biases1)):
            if random.random() < mutation_strenght:
                population[i].biases1[j] += np.random.normal(0, 0.01)

        for j in range(len(population[i].biases2)):
            if random.random() < mutation_strenght:
                population[i].biases2[j] += np.random.normal(0, 0.01)

        for j in range(len(population[i].biases3)):
            if random.random() < mutation_strenght:
                population[i].biases3[j] += np.random.normal(0, 0.01)

################
### gameplay ###
################


def gameplay(individual):
    pass

################
### training ###
################


def training(from_last):
    global generation, population, tested_n_times, last_parameters

    if from_last == True:
        with open('brains_500.pickle', 'rb') as f:
            data = pickle.load(f)
            population = data[0]
            last_parameters = data[1]
    else:
        initialize(population_size)

    while (generation < max_generation):
        fitness(population, tested_n_times)

        if solved == True:
            break

        sort()
        selection()
        crossover()
        mutation()
        generation += 1


for i in range(2000000):
    generation = 0
    start_time = time.time()
    from_last = True
    training(from_last)

    fitness(population, tested_n_times)
    sort()

    # save the net to a file
    parameters = {"population size   -": population_size,
                  "selection rate    -": selection_rate,
                  "mutation rate     -": mutation_rate,
                  "mutation strenght -": mutation_strenght,
                  "generation        -": max_generation + last_parameters[list(last_parameters.keys())[4]],
                  "tested N times    -": tested_n_times, }

    with open('brains_500.pickle', 'wb') as f:
        pickle.dump([population, parameters], f)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")


# todo error -> kulombseg van a training es visual gameplay kozott -> le kell ellenorizni
# nem azonos eredmeny ad a tesztnel mivel az almakat random generalja - tombbe kellene tarolni a generalasokat
# tesztek mindenhova hogyan nez ki egy mutacio? egy crossover barmi print print print
# crossover es mutacio megertese
# fitness kiertekeles javitasa
