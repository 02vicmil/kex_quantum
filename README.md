# kex_quantum
Welcome to the project page for our candidate project. The projects purpose is to examine how qubit couplings affect the performance of grovers algorithm.

![alt text](/resources/grover_circuit.png)


## Getting stared
### Installing dependencies
Make sure you have python installed, version > 3.9

Install packages required by running:
`pip install -r requirements.txt`

NOTE: We have used windows10 and windows11 during the development of this project, we have not tested it on other platforms.

## Running experiments and examples
First, make sure your current working directory is the same as this `README.md`.

Running the experiments can be done using the following command:
```
python -m source.experiments.EXPERIMENT_NAME
```
where `EXPERIMENT_NAME` is one of the experiments in `source/experiments` (except `run_all.py`, and `grid_positions.py`)

To run an example, run:
```
python -m source.examples.EXAMPLE_NAME
```
where `EXAMPLE_NAME` is one of the experiments in `source/examples`.

## Project structure

### Source
Here you can find all the source files used throughout the project. Read source/README.md for more info

### Results
Here you can find the results that were generated. This includes for example
- The performance of the different qubit couplings for 5 qubit circuit when running grover one step
- The performance of different fake providers when running grover one step
- All possible qubit couplings for 5 qubits

### Resources
Here you can find images used for the readme files