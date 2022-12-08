import random
import time
import copy
from itertools import combinations

class TabuSearch:
    route = []
    iteration = 200
    tabu_length = 10
    tabu_list = []
    
    def __init__(self, distance_list) -> None:
        self.distance_list = distance_list
    
    # Step1: Initial Path
    def initial_route(self,number):
        route = list(range(number))
        random.shuffle(route)
        cost = self.calculate_cost(route)

        return route, cost

    # Step2: Calculate cost 
    def calculate_cost(self, route):
        cost = 0

        for i, element in enumerate(route):
            if(i < (len(route)-1)):
                cost += self.distance_list[element][route[i+1]]
            else:
                cost += self.distance_list[element][route[0]]

        return cost  

    # Step3: Swap between index1 and index2
    def swap(self,route,index1, index2):
        swap_route = copy.deepcopy(route)
        
        swap_route[index1] = route[index2]
        swap_route[index2] = route[index1]

        return swap_route

    def is_in_tabu_list(self,route):
        neighborhoods = copy.deepcopy(route)
        for i in combinations(neighborhoods, 2):
            if i not in self.tabu_list:
                return False
            else:
                return True
    def empty_tabu_list(self,tabu_list):
        self.tabu_list = []

    def add_tabu_list(self,tabu):
        self.tabu_list.append(tabu)
    
    # Step4: Define tabu search
    def tabu_search(self, route):
        results = []
        tabu = [] 
        best_candidate = copy.deepcopy(route)
        
        results.append(route)

        while(self.iteration):
            # Tabu list is full
            if len(self.tabu_list) > self.tabu_length:
               self.tabu_list = []
            
            neighborhoods = copy.deepcopy(route)
            for i in combinations(neighborhoods, 2):
                # Swap positions between s0 and s1   
                current_candidate = self.swap(neighborhoods,i[0],i[1])
                if self.calculate_cost(current_candidate) < self.calculate_cost(best_candidate):
                    if (not self.is_in_tabu_list(neighborhoods)):
                        best_candidate = current_candidate
                        tabu = i
                        # Add to tabu list
                        self.add_tabu_list(tabu)
                                      
            # Find best route
            if self.calculate_cost(best_candidate) < self.calculate_cost(route):
                route = best_candidate

            results.append(best_candidate)

            # Number of iterations
            self.iteration -= 1 

        return route, results

if __name__ == "__main__":
    number_city = 5
    # Step5: define 2D List
    distance_list = [[0.0000, 11.8658, 14.0778, 4.2337, 1.4596], 
                        [11.8658, 0.0000, 10.2788, 6.3823, 13.3265], 
                        [14.0778, 10.2788, 0.0000, 4.0575, 17.2087], 
                        [4.2337, 6.3823, 4.0575, 0.0000, 28.0986], 
                        [1.4596, 13.3265, 17.2087, 28.0986, 0.0000]]
    
    ts = TabuSearch(distance_list)

    route, initial_cost = ts.initial_route(number_city)
    print('initial route: ', route)
    print('initial route cost: ', initial_cost)

    t = time.time()
    #ts.tabu_search(route, initial_cost)
    best_route, routes = ts.tabu_search(route) 
    t = time.time() - t

    print('Best route:', best_route)
    print('best distance:', ts.calculate_cost(best_route))
    print('Time Spent: ', t)


'''
    def tabu_search(self,route, initial_cost):
        optimal_cost = 0
        temp_cost = 0
        count = 0
        optimal_cost = initial_cost
        
        while count < 50:
            swaped_route = self.swap(route)
            #print('after swapped', swaped_route)
            temp_cost = self.calculate_cost(swaped_route)
            #print('new route cost', temp_cost)
            if(temp_cost < optimal_cost):
                optimal_cost = temp_cost
            count += 1
        print('Optimal:', optimal_cost)
    '''