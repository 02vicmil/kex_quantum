from .qiskit_util import Runner, Error, grovers_circuit

# All connected graphs with 5 vertices
# See source/unique_qubit_couplings_find_all_unique_couplings.py, and
#     results/unique_qubit_couplings/unique_couplings.txt 
UNIQUE_5_COUPLINGS = [
    [(0, 1), (0, 2), (0, 3), (0, 4)],
    [(0, 1), (0, 3), (0, 4), (1, 2)],
    [(0, 2), (0, 4), (1, 2), (1, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2)],
    [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3)],
    [(0, 1), (0, 4), (1, 2), (1, 3), (2, 3)],
    [(0, 3), (0, 4), (1, 2), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
    [(0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 3)],
    [(0, 1), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 4), (2, 3)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4)],
    [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
]

GRAPH_DEGREE_ENCODING = ['41111', '32111', '22211', 
                         '42211', '33211', '32221', 
                         '23221', '22222', '43221', 
                         '33222', '33321', '42222', 
                         '33222', '44222', '43331', 
                         '43322', '33332', '44332', 
                         '43333', '44433', '44444']