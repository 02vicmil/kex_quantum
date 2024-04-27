import os, pathlib
from .. import grovers_circuit, Runner, Error, UNIQUE_5_COUPLINGS

## Default parameters
NUM_QUBITS = 3
NUM_STATES = 2**NUM_QUBITS
SHOTS      = 1000

def get_directory_in_results(directory: str):
    parent_directory = pathlib.Path(__file__).parents[0]
    path = os.path.join(parent_directory, f"../../results/{directory}")
    if not os.path.exists(path):
        os.makedirs(path)
    return path
