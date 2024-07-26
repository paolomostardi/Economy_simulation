from society import Society
import matplotlib.pyplot as plt
import tkinter as tk

class GraphicInterface:

    def __init__(self, society : Society) -> None:
        self.society = society

    def main(self):
        plt.bar(x = ['Medicine Price  ', 'Food Price'] , height=[self.society.market.medicine_cost, self.society.market.food_cost] )
        plt.show()
    