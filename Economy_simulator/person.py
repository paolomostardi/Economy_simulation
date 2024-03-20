from profession import Profession, Unempolyed
from society import Society

from dataclasses import dataclass

@dataclass
class Person:
    age: int
    profession: Profession = Unempolyed()  
    salary: float
    hunger: int = 0
    food: int = 5
    working_sink: bool = True
    thirst: int = 0
    sick: bool = False
    money: float = 500

    def tick(self, society: Society):
        
        # eat
        if self.food > 0:
            self.food -= 1
            self.hunger = 0
        elif self.money > 0:
            society.market.buy_food(self)
            if self.food > 0:
                self.food -= 1
                self.hunger = 0

        # drink
        
        if self.working_sink:
            self.thirst = 0
            
        elif self.money > 0:
            society.market.hire_plumber(self)
            if self.working_sink:
                self.thirst = 0


        

        


        self.profession.work(society)
