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
    food_cost: int = 1
    medicine_cost : int = 10

    def buy_food(self, person : Person):
        if person.money > self.food_cost * 5:
            person.money -= self.food_cost * 5
            person.food += 5
        else:
            affordable_food = 