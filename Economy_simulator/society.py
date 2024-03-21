from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt
from person import Person
from market import Market

class Market: 
    def __init__(self, avarage_age = 40, total_population = 1000, birth_rate = 10):
        
        self.market = Market()

        self.total_population = total_population
        self.avarage_age = avarage_age
        self.birth_rate = birth_rate

        self.generate_human_population()

    def tick(self):
        for human in self.population:
            human.tick() 
    
    def generate_human_population(self):
        pass


def generate_age_array(amount, avarage_age):
    mean = avarage_age
    std_dev = 8

    array_size = amount  

    np.random.seed(42)

    return np.random.normal(mean, std_dev, array_size).astype(np.int16)

