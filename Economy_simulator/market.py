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
    plumbing_provided : int = 0

    medicine_history = [20]
    food_history = [20]
    plumbing_history = [20]
    
    food_cost: int = 1
    medicine_cost : int = 10
    plumbing_cost : int = 15

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
            self.food_consumed += 5
        else:
            affordable_food = person.money // self.food_cost
            person.money -= affordable_food * self.food_cost
            person.food += affordable_food
            self.total_food -= affordable_food
            self.food_consumed += affordable_food
        
    def hire_plumber(self, person ):
        if person.is_plumber():
            person.working_sink = True
            return
        
        if person.money > 0:

            try:
                plumber = self.plumbers.pop(0)
                plumber.money += self.plumbing_cost
                person.money -= self.plumbing_cost
                person.working_sink = True
                self.plumbers.append(plumber)
                self.plumbing_provided += 1
                print('plumbing provided')
                
            except IndexError:
                print('plumbing error')
                print(self.plumbers)

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
            self.medicine_consumed += 1

    def remove_plumber(self, id: int):
        for i in self.plumbers:
            if i.id == id:
                self.plumbers.remove(i)
                return

    def plumber_pay(self):
        if self.plumbing_provided == 0:
            return 0
        pay = (self.plumbing_provided / len(self.plumbers)) * self.plumbing_cost
        print(pay)
        return pay        

        

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
        elif self.food_consumed < self.food_produced:
            if self.food_cost > 1:
                self.food_cost -=1
        if self.medicine_consumed > self.medicine_produced:
            self.medicine_cost += 1 
        elif self.medicine_consumed < self.medicine_produced:
            if self.medicine_cost > 1:
                self.medicine_cost -=1

        if self.plumbing_provided < len(self.plumbers):
            if self.plumbing_cost > 1:
                self.plumbing_cost -= 1
        elif self.plumbing_provided > len(self.plumbers):   
            self.plumbing_cost += 1 
        
        return True
    
    # resets counters of production 
    def reset_production(self):
        self.food_history.append(self.food_consumed)
        self.medicine_history.append(self.medicine_consumed)
        self.plumbing_history.append(self.plumbing_provided)

        print('TOTAL FOOD CONSUMED')
        print(self.food_consumed)

        self.food_consumed = 0
        self.food_produced = 0
        self.medicine_consumed = 0
        self.medicine_produced = 0
        self.plumbing_provided = 0
        
    