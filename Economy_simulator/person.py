import random
from profession import Profession, Unempolyed, Plumber

from dataclasses import dataclass

# single entity withing the society
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
    home_owning = False



    sickness_chance = 20
    

    # returns true if the person is gonna die 
    def tick(self, market) ->  bool:
        
        self.hunger += 1
        self.thirst += 1
        self.age += 1

        # medicine 
        if self.sick:
            if self.money >= market.medicine_cost:
                market.buy_medicine(self)

        # work        
        elif self.profession.__class__ == Unempolyed:
            self.profession = self.profession.work(market)()

        else:       
            self.money += self.profession.work(market)

        # can get sick     
        if random.choice(range(self.sickness_chance)) == 1:
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
        
        if not self.home_owning:
            if self.money > market.housing_price:
                self.home_owning = market.buy_house(self)

        # check death
        if self.hunger > 3 or self.thirst > 3:
            return True
        
        
        
        return False

    def is_plumber(self) -> bool:
        if self.profession.__class__ == Plumber:
           return True
        return False        



