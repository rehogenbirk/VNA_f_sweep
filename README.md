# VNA_f_sweep

Python code used to do measurements with Agilent PNA Network Analyzer E8361C (VNA) and process the incoming data.

## Modules

### vna_functions
Contains functions that send SCPI commands to VNA using the PyVISA library.
For SCPI commands used, see the documentation inside Keysight Command Expert

### sweep_functions
Contains functions for performing the steps of taking a frequency sweep measurement
Implemented in VNA_f_sweep script

### data_analysis
Functions for processing the measurement data
