from profession import Profession, Student, Farmer, Plumber
from society import Society

class Person:
    def __init__(self, age, profession : Profession ):
        self.age = age
        self.profession = profession
        self.salary = profession.salary 
        self.hunger = 0
        self.thirst = 0 
        self.sick = False
        self.money = 500

    def tick(self, society : Society):
        self.profession.work(society)
