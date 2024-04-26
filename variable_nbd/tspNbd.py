import random, time, json, os
import numpy as np

# random will help in shaking, aka leaving the nbd
# to have a chance for a better solution
# json for formatting
# os for
# numpy cuz we doing array manipulation
# 
# function definitions

# tour_dist : inp is the tour, list ig
# and of course, a dist matrix (adjacency matrix)

def tour_dist(tour, adja_matrix):
    tour_rolled = np.roll(tour, -1) #shift r to l the tour list
    return np.sum(adja_matrix[tour, tour_rolled])

def two_opt(tour, i, j): #heuristic which cuts the graph and joins criss-cross the two edge for enw path
    tour2 = np.concatenate((tour[:i], tour[i:j+1][::-1], tour[j+1:]))
    return tour2

def three_opt(tour, i, j, k):
    tour3 = np.concatenate((tour[:i], tour[j:k], tour[i:j], tour[k:]))
    return tour3
# three_opt takes three cut parts and re-joins them to form a new one

def local_search(tour, adja_matrix, operator):
    better_sol_found = True
    og_dist = tour_dist(tour, adja_matrix)

    while better_sol_found:
        better_sol_found = False 
        for i in range(1, len(tour) -1):
            for j in range(i+1, len(tour)):
                if j-i == 1: continue 
                new_tour = operator(tour, i, j)
                new_dist = tour_dist(new_tour, adja_matrix)
                if new_dist < og_dist:
                    tour = new_tour
                    og_dist = new_dist
                    better_sol_found = True

    return tour

def shaking(tour, k):
    new_tour = tour.copy()
    for _ in range(k):
        i, j = sorted(random.sample(range(1, len(tour)-1), 2))
        new_tour = two_opt(new_tour, i, j)
    return new_tour

def vns(tour, adja_matrix, k_max=500, operator=two_opt):
    k = 1
    total_explore_time =0
    total_exploit_time =0
    while k <= k_max:
        time_start = time.time()
        k_tour = shaking(tour, k)
        time_end = time.time()
        total_explore_time += time_end - time_start
        new_tour = local_search(k_tour, adja_matrix, operator)
        time_end = time.time()
        total_exploit_time += time_end - time_start

        if tour_dist(new_tour, adja_matrix) < tour_dist(tour, adja_matrix):
            tour = new_tour
            k = 1
        else:
            k += 1
        
    return tour, total_explore_time, total_exploit_time