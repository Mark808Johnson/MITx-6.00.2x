###########################
# 6.00.2x Problem Set 1: Space Cows 

import time
from ps1_partition import get_partitions

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # cow_dict = {k: v for k, v in sorted(cows.items(), key=lambda item: item[1], reverse=True)}  # dictionary in order
    sorted_cows = sorted(cows.items(), key=lambda kv: kv[1], reverse=True) #Creates ordered list of cows (tuples, in descending weight order)
    list_of_trips = []  # Total list of trips
    while len(sorted_cows) > 0:
        new_trip = []
        trip_limit = limit
        copy_sorted_cows = sorted_cows.copy()
        for cow in sorted_cows:
            if trip_limit - cow[1] >= 0:
                new_trip.append(cow[0])
                trip_limit -= cow[1]
                copy_sorted_cows.remove(cow) #remove cow from copy_sorted_cows
            else:
                continue
        list_of_trips.append(new_trip)
        sorted_cows = copy_sorted_cows
    return list_of_trips

# Problem 2
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # partitions = []
    # for partition in (get_partitions(cows)):
    #     partitions.append(partition)  # Creates list of all partitions
    partitions = [partition for partition in (get_partitions(cows))]
    min_trip_len = len(cows)
    for partition in partitions:
        legit_trip = True
        for load in partition:
            weight = 0
            for cow in load:
                weight += cows[cow]
            if weight > limit:
                legit_trip = False
                break
        if legit_trip and len(partition) <= min_trip_len:
                min_trip_len, min_trip = len(partition), partition
    return min_trip


print(brute_force_cow_transport({'Boo': 20, 'Horns': 25, 'MooMoo': 50, 'Milkshake': 40, 'Miss Bella': 25, 'Lotus': 40}, 100))
print(brute_force_cow_transport({'Daisy': 50, 'Buttercup': 72, 'Betsy': 65}, 75))
print(brute_force_cow_transport({'Starlight': 54, 'Luna': 41, 'Betsy': 39, 'Buttercup': 11}, 145))

# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows("ps1_cow_data.txt")
    limit = 10
    start_time = time.time()
    Greedy_result = greedy_cow_transport(cows, limit)
    print("Result of greedy algorithm is: \n ,", Greedy_result, "\n with minimum ", len(Greedy_result),
          " trips needed")
    print("Time taken: --- {}s seconds ---".format(time.time() - start_time))

    print("________________")

    Brute_force_result = brute_force_cow_transport(cows, limit)
    print("Result of brute force algorithm is: \n ,", Brute_force_result, "\n with minimum ", len(Brute_force_result),
          " trips needed")
    print("Time taken: --- {}s seconds ---".format(time.time() - start_time))


    # print("Greedy algorithm returns minimum trip of ", len(greedy_cow_transport(cows)))

"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

compare_cow_transport_algorithms()

