import random
import statistics

"""
1 - natural resource 
2 - buyer 
3 - excavator 
"""

class Resource:
    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates
        self.amount = random.randint(2,20)
        self.value = random.uniform(0.7, 2.0)
class Excavator:
    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates
        self.list_of_actions = ['resource hunt','selling resource']
        self.current_action = 0
        self.resource_amount = 0
        self.money = 300
        self.current_resource_value = 0

    def next_action(self):
        if self.current_action == 0:
            self.current_action = 1
        elif self.current_action == 1:
            self.current_action = 0

class Buyer:
    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates
        self.price = random.randint(2,20)
        self.ticks_from_selling = 0

    def increase_price(self):
        self.price += 1

    def reset_ticks_from_selling(self):
        self.ticks_from_selling = 0

class Simulation:
    def __init__(self, size) -> None:
        matrix = []

        for n in range(size):
            matrix.append([])
            for i in range(size):
                matrix[n].append(0)
        self.tick_counter = 0
        self.size = size - 1
        self.matrix = matrix
        self.resource_array : list[Resource] = []
        self.excavator_array : list[Excavator] = []
        self.buyer_array : list[Buyer] = []
        self.left_move = (-1, 0)
        self.right_move = (1, 0)
        self.up_move = (0, 1)
        self.down_move = (0, -1)
        self.fuel_cost = 1
        self.generate_resources(size)
        self.generate_excavators(size // 5)
        self.generate_buyers(size // 10)

    def print_grid(self):
        for row in self.matrix:
            print(row)

    def random_pick(self):
        x = random.randint(0, self.size)
        y = random.randint(0, self.size)
        return x, y

    def generate_resources(self, amount):
        for i in range(amount):
            x, y = self.random_pick()
            if self.matrix[x][y] == 0:
                self.matrix[x][y] = 1
                self.resource_array.append(Resource([x, y]))

    def generate_excavators(self, amount):
        for i in range(amount):
            x, y = self.random_pick()
            if self.matrix[x][y] == 0:
                self.matrix[x][y] = 3
                self.excavator_array.append(Excavator([x, y]))

    def generate_buyers(self, amount):
        for i in range(amount):
            x, y = self.random_pick()
            if self.matrix[x][y] == 0:
                self.matrix[x][y] = 2
                self.buyer_array.append(Buyer([x, y]))

    def excavator_action(self):
        for excavator in self.excavator_array:
            if excavator.current_action == 0:
                best_resource = self.find_best_resource(excavator)
                if best_resource is None:
                    continue
                direction = self.find_directions_given_two_coordinates(excavator.coordinates, best_resource.coordinates)
                if direction == 0: # excavator is on the resource 
                    best_resource.amount -= 1
                    excavator.current_resource_value = best_resource.value
                    if best_resource.amount == 0:
                        self.resource_array.remove(best_resource)
                        self.matrix[best_resource.coordinates[0]][best_resource.coordinates[1]] = 0
                    excavator.next_action()
                    continue
                self.move_excavator(direction, excavator)   

            if excavator.current_action == 1:
                best_buyer = self.find_best_buyer(excavator)
                if best_buyer is None:
                    continue
                direction = self.find_directions_given_two_coordinates(excavator.coordinates, best_buyer.coordinates)
                if direction == 0:
                    self.excavator_buyer_transaction(excavator,best_buyer)
                    excavator.next_action()
                    continue
                self.move_excavator(direction, excavator)             

    def get_coordinates_of_closest_resource(self, excavator_coordinates):
        distance = self.size
        coordinates = 0
        for resource in self.resource_array:
            current_distance = distance_between_points(excavator_coordinates, resource.coordinates)
            if current_distance < distance:
                distance = current_distance
                coordinates = resource.coordinates
        return coordinates
    
    def get_coordinates_of_closest_buyer(self, excavator_coordinates):
        distance = self.size
        coordinates = 0
        for buyer in self.buyer_array:
            current_distance = distance_between_points(excavator_coordinates, buyer.coordinates)
            if current_distance < distance:
                distance = current_distance
                coordinates = buyer.coordinates
        return coordinates

    def find_best_resource(self, excavator :Excavator):
        best_value = 0
        best_resource = None
        for resource in self.resource_array:
            for buyer in self.buyer_array:
                distance_excavator_resource = distance_between_points(excavator.coordinates,resource.coordinates)
                distance_resuorce_buyer = distance_between_points(resource.coordinates,buyer.coordinates)
                value = (buyer.price * resource.value) - (distance_excavator_resource + distance_resuorce_buyer * self.fuel_cost) 
                if value > best_value:
                    best_value = value
                    best_resource = resource
        
        return best_resource

    # finds the best buyer with the cost of fuel and the amount of money the buyer buys for 
    def find_best_buyer(self,excavator :Excavator):
        best_value = 0 
        buyer = None
        for buyer in self.buyer_array:
            distance_excavator_buyer = distance_between_points(excavator.coordinates,buyer.coordinates)
            value = (buyer.price * excavator.current_resource_value) - (distance_excavator_buyer * self.fuel_cost)
            if value > best_value:
                best_value = value
                best_buyer = buyer
        if best_value != 0:        
            return best_buyer
    
    def excavator_buyer_transaction(self,excavator, buyer):
        if buyer:
            buyer.ticks_from_selling = 0 
            excavator.money += int(buyer.price * excavator.current_resource_value
)
    def find_buyer_given_coordinates(self,buyer_coordinates):
        for buyer in self.buyer_array:
            print(buyer_coordinates, buyer.coordinates)
            if buyer_coordinates == buyer.coordinates:
                return buyer
        return None
    
    def find_directions_given_two_coordinates(self, coordinate1, coordinate2):
        if coordinate1[0] > coordinate2[0]:
            return self.left_move
        if coordinate1[0] < coordinate2[0]:
            return self.right_move
        if coordinate1[1] > coordinate2[1]:
            return self.down_move
        if coordinate1[1] < coordinate2[1]:
            return self.up_move
        return 0

    def move_excavator(self, direction, excavator):
        x, y = excavator.coordinates
        x_new, y_new = x + direction[0], y + direction[1]
        self.matrix[x][y] -= 3
        excavator.coordinates = [x_new, y_new]
        self.matrix[x_new][y_new] += 3
        excavator.money -= 1
        if excavator.money < 0:
            self.excavator_array.remove(excavator)
            self.matrix[x_new][y_new] -= 3
    def buyer_action(self):

        for buyer in self.buyer_array:
            if buyer.ticks_from_selling > 30:
                buyer.price += 1
            buyer.ticks_from_selling += 1

    def tick(self):
        self.excavator_action()
        self.buyer_action()
        self.tick_counter += 1
        if self.tick_counter % 100 == 0:
            self.generate_resources(2)
        if self.tick_counter % 30 == 0:
            self.fuel_cost = statistics.mean(buyer.price for buyer in self.buyer_array) // self.size


def distance_between_points(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
