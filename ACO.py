import warnings
import numpy as np
from numpy import inf

#Ignore divide by zero warning 
warnings.simplefilter("ignore")

#Adjacency list of graph
d = np.array([[0, 10, 12, 11, 14]
             ,[10, 0, 13, 15, 8]
             ,[12, 13, 0, 9, 14]
             ,[11, 15, 9, 0, 16]
             ,[14, 8, 14, 16, 0]])

iteration = 100
#Number of ants
m = 5
#Number of vertices
n = 5

#Init Parameters
e = 0.5          #Evaporation Rate
alpha = 1        #Pheromone Factor
beta = 2         #Path Factor

#Calculate Path Factor as 1/Path Length
visibility = 1 / d
visibility[visibility == inf] = 0
#Init pheromone to 0.1 on each path
pheromone = 0.1 * np.ones((m, n))
#Init Route eg: A -> B -> C -> A
route = np.ones((m, n + 1))

for _ in range(iteration):
    #Initial node for each ant = 1
    route[:, 0] = 1
    for ant in range(m):
        temp_visibility = np.array(visibility)
        for vertex in range(n - 1):
            cur_loc = int(route[ant, vertex] - 1)            
            temp_visibility[:, cur_loc] = 0
            p_feature = np.power(pheromone[cur_loc, :], beta)
            v_feature = np.power(temp_visibility[cur_loc, :], alpha)
            combine_feature = np.multiply(p_feature, v_feature)
            total = np.sum(combine_feature)
            probs = combine_feature / total
            cum_prob = np.cumsum(probs)
            r = np.random.random_sample()
            #Roulette Selection of next vertex 
            next_vertex = np.nonzero(cum_prob > r)[0][0] + 1
            route[ant, vertex + 1] = next_vertex
        #Last Vertex left to traverse
        next_vertex = list(set([i for i in range(1, n + 1)]) - set(route[ant, :-2]))[0]
        route[ant, -2] = next_vertex

    route_opt = np.array(route)
    dist_cost = np.zeros((m, 1))
    for ant in range(m):        
        s = 0
        for vertex in range(n):
            #Total distance of routes
            s = s + d[int(route_opt[ant, vertex]) - 1, int(route_opt[ant, (vertex + 1) % n]) - 1]
        #Total distance traversed by ant i
        dist_cost[ant] = s
    
    min_dist = dist_cost[np.argmin(dist_cost)]
    best_route = route[np.argmin(dist_cost), :]

    #Evaporation of pheromones
    pheromone = (1 - e) * pheromone
    #Add pheromone proportional to ant's path length
    for ant in range(m):
        for vertex in range(n - 1):
            dt = 1 / dist_cost[ant]
            pheromone[int(route_opt[ant, vertex]) - 1, int(route_opt[ant, vertex + 1]) - 1] = pheromone[int(route_opt[ant, vertex]) - 1, int(route_opt[ant, vertex + 1]) - 1] + dt   

#Set float precision to 4 before printing
formatter = "{:.4f}".format
np.set_printoptions(formatter = {'float_kind' : formatter})
print('ROUTES : \n', route_opt)
print()
print('PHEROMONES : \n', pheromone)
print()
print('BEST ROUTE : \n', best_route)
print('ROUTE LENGTH : ', min_dist[0])
