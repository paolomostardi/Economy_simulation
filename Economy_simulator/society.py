from enum import Enum
import random
import numpy as np
from person import Person
from market import Market

import pprint

from profession import Student,Farmer,Pharmacist,Plumber,Unempolyed

# farmers one every four 1 / 4 25 % 
# pharmacist one every 15 1 / 15 * 100 ~ 6 %
# Plumber one every 15 ~ 7 %
# Unemployed rest of them = 100 - 25 - 6 - 7 - 5 
# Student 1 every 20 ~ 5%

class Society: 
    def __init__(self, avarage_age = 40, total_population = 1200, birth_rate = 10):
        
        self.market = Market()

        self.total_population = total_population
        self.avarage_age = avarage_age
        self.birth_rate = birth_rate

        self.population_history = []
        self.hunger_history = []
        self.sickness_history = []
        self.thirst_history = []

        self.population = self.generate_human_population()

    def tick(self):
        self.market.food_cost += 0.01
        self.market.reset_production()

        self.population_history.append(len(self.population))
        self.hunger_history.append(self.count_hungry())
        self.sickness_history.append(self.count_sick())
        self.thirst_history.append(self.count_thirst())


        for human in self.population:
            if human.tick(market=self.market):
                self.population.remove(human)
        
    
    def generate_human_population(self):
        population = []
        for i in generate_age_array(self.total_population, self.avarage_age):
            population.append(generate_human(i, self.market))
        return population

    def count_hungry(self):
        counter = 0 
        for i in self.population:
            if i.hunger > 1 :
                counter += 1 
        return counter
    
    def count_sick(self):
        counter = 0 
        for i in self.population:
            if i.sick > 1 :
                counter += 1 
        return counter    
    
    def count_thirst(self):
        counter = 0 
        for i in self.population:
            if i.thirst > 1 :
                counter += 1 
        return counter    


    def count_professions(self):

        professions = {"Student": 0, "Farmer": 0, "Pharmacist": 0, "Plumber": 0, "Unempolyed": 0}

        for person in self.population:
            profession_name = person.profession.__class__.__name__
            professions[profession_name] += 1

        pprint.pprint(professions)
        return professions
    
    def average_age(self):
        return 15

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

