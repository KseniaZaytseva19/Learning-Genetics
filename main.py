from PIL import Image
from random import randint, choice, random


MAX_EPOCHS = 100_0000
DESIRED_FITNESS = 5_000
VERBOSE = True
POPULATION_SIZE = 10
SOURCE_FILENAME = 'images/heart_orig.png'

def open():
    image = Image.open(SOURCE_FILENAME)
    image = image.resize((16, 16), resample=Image.Resampling.NEAREST)
    image_list = []
    for x in range(0, 16):
        for y in range(0, 16):
            image_list.append(image.getpixel((x,y)))
    return image_list

def create_population():
    population = []
    for i in range(POPULATION_SIZE):
        individual = []
        for p in range(256):
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            individual.append((r, g, b))
        population.append(individual)

    return population

def fitness(individual, reference):
    distance = 0
    for i in range(0, 255):
        error1 = abs(individual[i][0] - reference[i][0])
        error2 = abs(individual[i][1] - reference[i][1])
        error3 = abs(individual[i][2] - reference[i][2])
        distance += error1 + error2 + error3
    return distance

def evaluate_population(population, reference):
    fitness_list = []
    for individual in population:
        fitness_list.append(fitness(individual, reference))
    return fitness_list

def drop_worst(population, reference, proportion=0.5):
    fitness_list = evaluate_population(population, reference)
    scored_population = list(zip(population, fitness_list))
    scored_population.sort(key=lambda k: k[1])
    amount_drop = int(proportion * len(population))
    sorted_population = scored_population[amount_drop-1:]
    population = []
    for i in range(len(sorted_population)-1):
        population.append(scored_population[i][0])
    return population, max(fitness_list)

def crossover(population):
    parent1 = population[randint(0, len(population)-1)]
    parent2 = choice(population)
    new_individual = []
    chance = random()
    if chance > 0.5:
        for i in range(len(parent2)):
            if i % 2 == 0:
                new_individual.append(parent1[i])
            else:
                new_individual.append(parent2[i])
    else:
        half1 =  parent1[:len(parent1)//2]
        half2 = parent2[len(parent2)//2:]
        new_individual = half1 + half2
    return new_individual

def mutation(individual):
    if random() < 0.5:
        return individual
    p = randint(0, len(individual)-1)
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    individual[p] = (r, g, b)
    return individual

def make_children(population):
    while len(population) != POPULATION_SIZE:
        child = crossover(population)
        child = mutation(child)
        population.append(child)
    return population

def get_best(population, reference):
    fitness_list = evaluate_population(population, reference)
    scored_population = list(zip(population, fitness_list))
    scored_population.sort(key=lambda k: k[1])
    return scored_population[0][0]

def save_image(individual):
    image = Image.new('RGB', (16, 16))
    for x in range(0, 16):
        for y in range(0, 16):
            image.putpixel((x, y), individual[x*16+y])
    image = image.resize((256, 256), resample=Image.Resampling.NEAREST)
    image.show()
    image.save('heart_5f.png')

reference_image = open()
current_population = create_population()
best_score = 200_000
epoch = 0
while best_score > DESIRED_FITNESS and epoch < MAX_EPOCHS:
    current_population, best_score = drop_worst(current_population, reference_image)
    current_population = make_children(current_population)
    epoch += 1
    if VERBOSE:
        print('Epoch:', epoch, ', Best fitness:', best_score)
best_individual = get_best(current_population, reference_image)
save_image(best_individual)