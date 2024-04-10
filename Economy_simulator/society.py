from enum import Enum
import random
import numpy as np
from person import Person
from market import Market

from profession import Student,Farmer,Pharmacist,Plumber,Unempolyed

# farmers one every four 1 / 4 25 % 
# pharmacist one every 15 1 / 15 * 100 ~ 6 %
# Plumber one every 15 ~ 7 %
# Unemployed rest of them = 100 - 25 - 6 - 7 - 5 
# Student 1 every 20 ~ 5%

class Society: 
    def __init__(self, avarage_age = 40, total_population = 1000, birth_rate = 10):
        
        self.market = Market()

        self.total_population = total_population
        self.avarage_age = avarage_age
        self.birth_rate = birth_rate

        self.generate_human_population()

    def tick(self):
        for human in self.population:
            human.tick(self.market) 
    
    def generate_human_population(self):
        self.population = []
        for i in generate_age_array(self.total_population, self.avarage_age):
            self.population.append(generate_human(i, self.market))

def generate_human(age, market : Market) -> Person:
    professions = [Student,Farmer,Pharmacist,Plumber,Unempolyed]

    profession = random.choice(professions)
    human = Person(age,profession())
    if profession is Plumber:
        market.plumbers.append(human)
    return human


def generate_age_array(amount, avarage_age):
    mean = avarage_age
    std_dev = 8

    array_size = amount  

    np.random.seed(42)

    return np.random.normal(mean, std_dev, array_size).astype(np.int16)

