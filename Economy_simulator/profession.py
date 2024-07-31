from market import Market
import random

class Profession():
    def __init__(self, salary = 0):
        self.salary = salary
    
    def work(self, market : Market) -> int:
        return self.salary

class Student(Profession): # should take money from the taxes 
    def work(self, market : Market) -> int:
        return market.food_cost * 2


class Farmer(Profession):
    
    def work(self, market : Market):       
        return market.sell_food(5)
    
class Plumber(Profession):

    def work(self, market: Market) -> int:
        return 0
    
class Pharmacist(Profession):

    def work(self, market : Market):       
        return market.sell_medicine(1)

class Unempolyed(Profession):

    def work(self, market: Market):

        farmer_pay = market.food_cost * 5
        pharmacist_pay = market.medicine_cost
        plumber_pay = market.plumber_pay()

        job_cance = 85

        if farmer_pay > pharmacist_pay and farmer_pay > plumber_pay:
            r = random.randrange(0, 100)
            if r > job_cance:
                return Farmer
            
        elif pharmacist_pay > plumber_pay:
            r = random.randrange(0, 100)
            if r > job_cance:    
                return Pharmacist
            
        else:
            r = random.randrange(0, 100)
            if r > job_cance:    
                return Plumber

        return Unempolyed
        
