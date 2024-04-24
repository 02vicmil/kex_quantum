"""
This is kind of a hacky and brute force way to generate all unique quantum couplings for a quantum computer with 5 qubits.
We can consider the qubit coupling as a graph, where edges determine which qubits are coupled.

Requirements:
 - The graphs must be connected
 - They must contain 5 nodes
 - Isomorphic graphs are considered equal(so we dont want two graphs in the solution that are isomorphic)

The code has not been heavily optimized. There probably exists much better ways to achieve the same result!
"""

edge_to_num = dict()
num_to_edge = dict()
index = 0
for i in range(0, 5):
    for j in range(i+1, 5):
        edge_to_num[(i,j)] = index
        edge_to_num[(j,i)] = index
        num_to_edge[index] = (i, j)
        index += 1

def edges_to_number(edges):
    num = 0
    for edge in edges:
        if edge in edge_to_num.keys():
            bit_index = edge_to_num[edge]
            bit_mask = 2 ** bit_index
            num = num | bit_mask
    return num

def number_to_edges(num):
    edges = list()
    for bit_index in range(0, 10):
        bit_mask = 2 ** bit_index
        if bit_mask & num != 0:
            edges.append(num_to_edge[bit_index])
    return edges

# (Can probably be optimized)
def is_connected(edges):
    # Start from node 0 and determine which nodes are connected to it
    touched_nodes = [False] * 5
    touched_nodes[0] = True
    for i in range(0, 5):
        for edge in edges:
            if touched_nodes[edge[0]] or touched_nodes[edge[1]]:
                touched_nodes[edge[0]] = True
                touched_nodes[edge[1]] = True

    # Ensure all nodes are connected to node 0
    for i in range(0, 5):
        if touched_nodes[i] == False:
            return False
    return True

def get_all_possible_edge_mappings():
    all_edge_mappings = list()
    edge_mapping = [0, 1, 2, 3, 4]
    for i in range(0, 5):
        edge_mapping_0 = edge_mapping.copy()
        temp = edge_mapping_0[0]
        edge_mapping_0[0] = edge_mapping_0[i]
        edge_mapping_0[i] = temp
        for i in range(1, 5):
            edge_mapping_1 = edge_mapping_0.copy()
            temp = edge_mapping_1[1]
            edge_mapping_1[1] = edge_mapping_1[i]
            edge_mapping_1[i] = temp
            for i in range(2, 5):
                edge_mapping_2 = edge_mapping_1.copy()
                temp = edge_mapping_2[2]
                edge_mapping_2[2] = edge_mapping_2[i]
                edge_mapping_2[i] = temp
                for i in range(3, 5):
                    edge_mapping_3 = edge_mapping_2.copy()
                    temp = edge_mapping_3[3]
                    edge_mapping_3[3] = edge_mapping_3[i]
                    edge_mapping_3[i] = temp
                    all_edge_mappings.append(edge_mapping_3)
    return all_edge_mappings


# There are 10 edges that can either be there or not there, so there are 2^10 possible combinations
edge_configurations = [True] * 1024

# All the ways we can permutate the nodes
all_edge_mappings = get_all_possible_edge_mappings()

# A list of all unique permutations
unique_couplings = list()

for i in range(0, 1024):
    if(edge_configurations[i] == False):
        # Edge configuration has been disabled because it is isomorf with one of the previous
        continue
    edges = number_to_edges(i)
    if not is_connected(edges):
        # All the nodes must be connected somehow for it to be a valid solution
        continue

    # Found valid candidate!
    # Remove all other isomorphisms
    for mapping in all_edge_mappings:
        new_edges = list()
        for edge in edges:
            new_edge = (mapping[edge[0]], mapping[edge[1]])
            new_edges.append(new_edge)
        new_num = edges_to_number(new_edges)
        edge_configurations[new_num] = False

    unique_couplings.append(edges)

# Print solutions in order of number of edges
index = 1
for i in range(0, 11):
    for c in unique_couplings:
        if len(c) == i:
            print(str(index) + ":  " + str(c))
            index += 1

