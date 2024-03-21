from market import Market


class Profession():
    def __init__(self, salary = 0):
        self.salary = salary
    
    def work(self, market : Market) -> int:
        return self.salary

class Student(Profession):
    def work(self, market : Market) -> int:
        return market.food_cost


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
    pass