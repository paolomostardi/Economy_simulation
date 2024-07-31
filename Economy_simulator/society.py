from enum import Enum
import random
import numpy as np
from person import Person
from market import Market

import pprint

from profession import Student,Farmer,Pharmacist,Plumber,Unempolyed

class Society: 
    def __init__(self, avarage_age = 40, total_population = 1250, birth_rate = 10):
        
        self.market = Market()

        self.total_population = total_population
        self.avarage_age = avarage_age
        self.birth_rate = birth_rate

        self.current_id = 0
        self.population_history = []
        self.hunger_history = []
        self.sickness_history = []
        self.thirst_history = []
        self.population = []
        self.population = self.generate_human_population()

    def tick(self):
        self.market.update_prices()
        self.market.reset_production()

        self.population_history.append(len(self.population))
        self.hunger_history.append(self.count_hungry())
        self.sickness_history.append(self.count_sick())
        self.thirst_history.append(self.count_thirst())


        for human in self.population:

            # erasing the human from the population if it dies 
            if human.tick(market=self.market):
                self.population.remove(human)
                if human.profession.__class__ == Plumber: 
                    self.market.remove_plumber(human.id)

    def generate_new_id(self):
        self.current_id += 1
        return self.current_id
    
    def generate_human_population(self):
        population = []
        for i in generate_age_array(self.total_population, self.avarage_age):
            population.append(generate_human(i, self.market, id = self.generate_new_id()))
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


# farmers one every four 1 / 4 25 % 
# pharmacist one every 15 1 / 15 * 100 ~ 6 %
# Plumber one every 15 ~ 7 %
# Unemployed rest of them = 100 - 25 - 6 - 7 - 5 = 57
# Student 1 every 20 ~ 5%

def generate_human(age, market : Market,id : int) -> Person:

    professions = [Student,Farmer,Pharmacist,Plumber,Unempolyed]
    professions_probabilities = [5,25,6,7,57]
    profession = random.choices(professions,professions_probabilities)


    human = Person(age=age,profession=profession[0](),id=id)
    if human.is_plumber():
        market.plumbers.append(human)
    return human

def generate_age_array(amount, avarage_age):
    mean = avarage_age
    std_dev = 8

    array_size = amount  

    np.random.seed(42)

    return np.random.normal(mean, std_dev, array_size).astype(np.int16)

