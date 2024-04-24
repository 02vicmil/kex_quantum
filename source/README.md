# Source
This folder contains all the source the files contained in the project. The folder is split into multiple parts described below.

## unique_qubit_couplings
Generate all possible 5 qubit couplings that are non-isomorphic. 

## qiskit_util
Contains some utility functions to run qiskit and implementation of grover, this includes 
- A wrapper to run quantum algorithms
- Implementation of Grovers algorithm

## grover_util_mcz
Implementation of grover's algoritm, without any ancilla bits. 

(MCZ stands for Multi-Controlled Z, which is a special quantum gate)

## grover_util_mcz_anc
Implementation of grover's algoritm, with ancilla bits. 

Ancilla bits means that the ciruit uses more qubits. The ancilla qubits are used when implementing large controlled not gates, central for implementing the oracle. They are not strictly necessary for the implementation, but using them can lead to improved performance and less noise.

(MCZ stands for Multi-Controlled Z, which is a special quantum gate)