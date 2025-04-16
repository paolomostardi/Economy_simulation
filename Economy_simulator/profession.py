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
    
class Construction(Profession):
    housing_counter = 0 
    def work(self, market: Market):
        if self.housing_counter == market.housing_building_time:
            self.housing_counter = 0            
            return market.build_house()
        else:
            self.housing_counter += 1
            return 0
        
# unemployed has a job_cance to do become the profession that is most payed
class Unempolyed(Profession):

    def work(self, market: Market):

        farmer_pay = market.food_cost * 5
        pharmacist_pay = market.medicine_cost
        plumber_pay = market.plumber_pay()
        construction_pay = market.construction_pay()

        pays = [farmer_pay,pharmacist_pay,plumber_pay,construction_pay]

        job_cance = 85
        r = random.randrange(0, 100)

        if r > job_cance:        
            if farmer_pay ==  max(pays):
                return Farmer
                
            elif pharmacist_pay ==  max(pays):
                return Pharmacist

            elif construction_pay == max(pays):
                return Construction    
        
            else:
                r = random.randrange(0, 100)
                return Plumber

        return Unempolyed
        
