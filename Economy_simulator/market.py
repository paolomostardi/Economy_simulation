from dataclasses import dataclass, field
# class that keeps track of all the changes in the market
# a society could have more markets 

@dataclass
class Market:
    total_food: int = 100
    total_medicine: int = 20
    plumbers: list = field(default_factory=list)

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

    def buy_food(self, person ):
        
        if self.total_food <= 0:
            return

        if person.money > self.food_cost * 5:
            person.money -= self.food_cost * 5
            self.total_food -= 5
            person.food += 5
        else:
            affordable_food = person.money // self.food_cost
            person.money -= affordable_food * self.food_cost
            person.food += affordable_food
            self.total_food -= affordable_food
        
    def hire_plumber(self, person ):
        if person.money > self.plumbing_cost:
            plumber = self.plumbers.pop(0)
            plumber.money += self.plumbing_cost
            person.money -= self.plumbing_cost
            self.plumbers.append(plumber)

    def sell_medicine(self, amount : int) -> int: 
        self.medicine_produced += amount
        self.total_medicine += amount
        return amount * self.medicine_cost

    def buy_medicine(self, person ):
        if self.total_medicine < 1:
            return
        if person.money > self.medicine_cost:
            person.money -= self.medicine_cost
            person.sick = False
            self.total_medicine -= 1

    # tf fix boiler plate

    def print_infos(self):

        print('--------------------------------')

        print( 'total_food: ', self.total_food) 
        print('total_medicine', self.total_medicine)
        print('total plumbers', len(self.plumbers))

        print('food_produced ', self.food_produced)
        print('medicine produced', self.medicine_produced)

        print('food_consumed', self.food_consumed)
        print('medicine_consumed', self.medicine_consumed)
        
        print('food_cost', self.food_cost)
        print('medicine_cost', self.medicine_cost)
        print('plumbing_cost', self.plumbing_cost)

    def update_prices(self):

        if self.food_consumed > self.food_produced:
            self.food_cost += 1
        elif self.food_consumed < self.food_produced * 2:
            self.food_cost -=1
        if self.medicine_consumed > self.medicine_produced:
            self.medicine_produced += 1 
        return True
    
    # resets counters of production 
    def reset_production(self):
        self.food_consumed = 0
        self.food_produced = 0
        self.medicine_consumed = 0
        self.medicine_produced = 0
        
    