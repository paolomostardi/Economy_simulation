from enum import Enum
import random
import numpy as np
from person import Person
from market import Market

from profession import Student,Farmer,Pharmacist,Plumber,Unempolyed,Construction

class Society: 
    def __init__(self, avarage_age = 40, total_population = 1250, birth_rate = 0.001):
        
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
        self.death_history = []
        self.tick_counter = 0

    def tick(self):
        self.market.update_prices()
        self.market.reset_production()

        self.population_history.append(len(self.population))
        self.hunger_history.append(self.count_hungry())
        self.sickness_history.append(self.count_sick())
        self.thirst_history.append(self.count_thirst())
        deaths_this_tick = 0

        professions = self.count_professions()
        money_stats = self.profession_money_stats()

        print("\n=== Population & Money Snapshot ===")
        header = f"{'JOB':<15}{'COUNT':>10}{'MONEY':>15}{'$/PERSON':>12}"
        print(header)
        print('-' * len(header))
        total_population = 0
        total_money = 0

        job_money_mapping = {
            'Student': 'student_money',
            'Farmer': 'farmer_money',
            'Pharmacist': 'pharmacist_money',
            'Plumber': 'plumber_money',
            'Construction': 'unemployed_money',
            'Unempolyed': 'unemployed_money'
        }

        for job, count in professions.items():
            money_key = job_money_mapping.get(job, 'unemployed_money')
            money_value = money_stats.get(money_key, 0)
            ratio = money_value / count if count else 0
            print(f"{job:<15}{count:>10}{money_value:>15}{ratio:>12.2f}")
            total_population += count
        total_money = money_stats['total_money']
        print('-' * len(header))
        avg_money = total_money / total_population if total_population else 0
        print(f"{'TOTAL':<15}{total_population:>10}{total_money:>15}{avg_money:>12.2f}")
        print()

        for human in self.population[:]:

            # erasing the human from the population if it dies 
            if human.tick(market=self.market):
                self.population.remove(human)
                if human.profession.__class__ == Plumber: 
                    self.market.remove_plumber(human.id)
                deaths_this_tick += 1
        
        self._handle_births()
        self.death_history.append(deaths_this_tick)
        self.market.print_infos()
        self._print_death_and_population_change()

    def _handle_births(self):
        population_size = len(self.population)
        if population_size == 0:
            births_count = 1
        else:
            births_count = max(1, int(population_size * self.birth_rate))

        for _ in range(births_count):
            newborn = Person(
                age=0,
                id=self.generate_new_id(),
                profession=Student(),
                home_owning=False
            )
            self.population.append(newborn)
            self.total_population += 1

    def generate_new_id(self):
        self.current_id += 1
        return self.current_id
    
    def generate_human_population(self):
        population = []
        for i in generate_age_array(self.total_population, self.avarage_age):
            population.append(generate_human(i, self.market, id = self.generate_new_id()))
        return population

    def _print_death_and_population_change(self):
        death_window = min(100, len(self.death_history))
        if death_window:
            deaths_recent = sum(self.death_history[-death_window:])
            print(f"Deaths in last {death_window} ticks: {deaths_recent}")

        if len(self.population_history) > 1:
            lookback = min(100, len(self.population_history) - 1)
            change = self.population_history[-1] - self.population_history[-(lookback + 1)]
            print(f"Population change last {lookback} ticks: {change}")

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

        professions = {"Student": 0, "Farmer": 0, "Pharmacist": 0, "Plumber": 0,"Construction":0, "Unempolyed": 0}

        for person in self.population:
            profession_name = person.profession.__class__.__name__
            professions[profession_name] += 1

        return professions
    
    def average_age(self):
        return 15
    
    def profession_money_stats(self):
        money_stats = {
            'total_money': 0,
            'farmer_money': 0,
            'pharmacist_money': 0,
            'plumber_money': 0,
            'unemployed_money': 0,
            'student_money': 0
        }

        for human in self.population:
            money_stats['total_money'] += human.money
            if isinstance(human.profession, Farmer):
                money_stats['farmer_money'] += human.money
            elif isinstance(human.profession, Pharmacist):
                money_stats['pharmacist_money'] += human.money
            elif isinstance(human.profession, Plumber):
                money_stats['plumber_money'] += human.money
            elif isinstance(human.profession, Unempolyed):
                money_stats['unemployed_money'] += human.money
            elif isinstance(human.profession, Student):
                money_stats['student_money'] += human.money

        return money_stats


# farmers one every four 1 / 4 25 % 
# pharmacist one every 15 1 / 15 * 100 ~ 6 %
# Plumber one every 15 ~ 7 %
# Unemployed rest of them = 100 - 25 - 6 - 7 - 5 = 57
# Student 1 every 20 ~ 5%

def generate_human(age, market : Market,id : int) -> Person:

    professions = [Student,Farmer,Pharmacist,Plumber,Construction,Unempolyed]
    professions_probabilities = [5,22,6,7,3,57]
    profession = random.choices(professions,professions_probabilities)


    human = Person(age=age,profession=profession[0](),id=id)
    if human.is_plumber():
        market.plumbers.append(human)
    
    human.home_owning = random.choices([True,False], [30,70])
    return human

def generate_age_array(amount, avarage_age):
    mean = avarage_age
    std_dev = 8
    array_size = amount  
    np.random.seed(42)
    return np.random.normal(mean, std_dev, array_size).astype(np.int16)

