import random
from profession import Profession, Unempolyed


from dataclasses import dataclass


@dataclass

class Person:
    age: int
    id: int
    profession: Profession = Unempolyed()  
    salary: float = 0
    hunger: int = 0
    food: int = 5
    medicine: int = 0
    working_sink: bool = True
    thirst: int = 0
    sick: bool = False
    money: float = 20

    def tick(self, market) ->  bool:
        
        self.hunger += 1
        self.thirst += 1

        # medicine 
        if self.sick:
            if self.money >= market.medicine_cost:
                market.buy_medicine(self)

        # work        
        elif self.profession.__class__ == Unempolyed:
            self.profession = self.profession.work(market)()

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
        if self.hunger > 3 or self.thirst > 3:
            return True
        

        return False




