import os

num_heuristic_leaf_calls = 0 # The number of times e( n ) is applied at level 3
root_node_heuristic_value = 0 # The value of e( n ) that was brought up to the current node from level 3, with only 1 decimal place
level2_node_heuristic_values = [] # The value of e( n )  that was brought up to all the nodes at level 2, 1 value per line with only 1 decimal place

def flush_to_file(self):
    global num_heuristic_leaf_calls
    global root_node_heuristic_value

    # Write to file
    with open("trace.txt", "a") as f:
        f.write("%i\n" % (num_heuristic_leaf_calls))
        f.write("%f.1\n\n" % (root_node_heuristic_value))
        for value in level2_node_heuristic_values:
            f.write("%f.1\n" % (value))
        f.write("\n")

    # Clear values
    num_heuristic_leaf_calls = 0
    root_node_heuristic_value = 0
    level2_node_heuristic_values.clear()