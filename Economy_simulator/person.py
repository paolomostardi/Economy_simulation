import random
from profession import Profession, Unempolyed


from dataclasses import dataclass


@dataclass
class Person:
    age: int
    profession: Profession = Unempolyed()  
    salary: float = 0
    hunger: int = 0
    food: int = 5
    medicine: int = 0
    working_sink: bool = True
    thirst: int = 0
    sick: bool = False
    money: float = 500

    def tick(self, market) ->  bool:
        
        # medicine 
        if self.sick:
            if self.money >= market.medicine_cost:
                market.buy_medicine(self)

        # work        
        else:  
            self.money += self.profession.work(market)
            if random.choice(range(20)) == 1:
                self.sick = True

        # eat
        if self.food > 0:
            self.food -= 1
            self.hunger = 0
        elif self.money > 0:
            market.buy_food(self)
            if self.food > 0:
                self.food -= 1
                self.hunger = 0

        # drink        
        if self.working_sink:
            self.thirst = 0
            if random.choice(range(20)) == 1:
                self.working_sink = False
            
        elif self.money > 0:
            market.hire_plumber(self)
            if self.working_sink:
                self.thirst = 0
        
        # check death
        if self.hunger > 2 or self.thirst > 2:
            return True
        
        return False




