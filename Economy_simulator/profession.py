from society import Society


class Profession():
    def __init__(self, salary):
        self.salary = salary
    
    def work(self, society : Society):
        return self.salary

class Student(Profession):
    def __init__(self):
        salary = 0
        super().__init__(salary)
    pass
    
class Farmer(Profession):
    
    def tick(self, society : Society):       

        society.total_food += 5
        return society.market.price_of_food 
    
class Plumber(Profession, society : Society):
    pass

class Pharmacist(Profession):
    pass

class Unempolyed(Profession):
    pass