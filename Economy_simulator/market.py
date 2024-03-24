from dataclasses import dataclass
from person import Person

# class that keeps track of all the changes in the market

@dataclass
class Market:
    total_food: int = 100
    total_medicine: int = 20
    available_plumbers: list[Person] = []
    food_produced : int = 0
    medicine_produced: int = 0
    food_consumed : int = 0
    medicine_consumed : int = 0
    food_cost: int = 1
    medicine_cost : int = 10
    plumbing_cost : int = 20

    def sell_food(self, amount : int):
        self.food_produced += amount
        self.total_food += amount
        return amount * self.food_cost

    def buy_food(self, person : Person):
        
        if person.money > self.food_cost * 5:
            person.money -= self.food_cost * 5
            self.total_food -= 5
            person.food += 5
        else:
            affordable_food = person.money // self.food_cost
            person.money -= affordable_food * self.food_cost
            person.food += affordable_food
            self.total_food -= affordable_food
        
    def hire_plumber(self, person : Person):
        if person


    def sell_medicine(self, amount : int) -> int: 
        self.medicine_produced += amount
        self.total_medicine += amount
        return amount * self.medicine_cost



    def buy_medicine(self, person : Person):
        self.
        pass


    def update_prices(self):
        return 