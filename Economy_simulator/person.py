import random
from profession import Profession, Unempolyed, Plumber, Cook, Student, Farmer, Pharmacist, Construction

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
    home_owning: bool = False



    sickness_chance = 20
    

    # returns true if the person is gonna die 
    def tick(self, market) ->  bool:
        
        self.hunger += 1
        self.thirst += 1
        self.age += 1

        # graduation chance for students
        if isinstance(self.profession, Student) and random.random() < 0.001:
            self.profession = Unempolyed()

        # medicine 
        if self.sick:
            if self.money >= market.medicine_cost:
                market.buy_medicine(self)

        # work        
        elif isinstance(self.profession, Unempolyed):
            self.profession = self.profession.work(market)()

        elif isinstance(self.profession, Cook):
            self.money += market.cook_turn(self, self.profession)

        else:       
            self.money += self.profession.work(market)

        # can get sick     
        if random.choice(range(self.sickness_chance)) == 1:
            self.sick = True

        meal_bought = False
        if random.random() < 0.05 and self.money >= market.meal_cost:
            meal_bought = market.buy_meal(self)

        # eat
        if meal_bought:
            pass
        elif self.food > 0:
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
            bought_home = market.buy_house(self)
            if not bought_home:
                market.collect_rent(self)

        # check death
        if self.hunger > 3 or self.thirst > 3:
            return True
        
        
        
        return False

    def is_plumber(self) -> bool:
        if self.profession.__class__ == Plumber:
           return True
        return False        



