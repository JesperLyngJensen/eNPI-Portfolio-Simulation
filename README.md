# eNPI-Portfolio-Simulation
Python code for the article 'Optimizing Capitally Constrained Portfolios: A Structural Risk Approach

## Description

The simulation models a project portfolio operating under strict capital constraints. Its purpose is to demonstrate the mechanism of Structural Value Loss—the irreversible destruction of value in long-term, illiquid projects caused by a capital deficit—and to test the performance of different management strategies in mitigating this risk.

The model simulates three distinct strategies over several iterations:

- Greedy Strategy: A baseline that maximizes investment without regard for future risk.
- Minus One Strategy: A simple heuristic that maintains a static capital buffer.
- Optimal Strategy: A predictive strategy that uses the eNPI (estimated Net Present Investment) framework to dynamically optimize the portfolio's resilience and output.

## Installing and running the simulation

To run this simulation, you will need Python installed, the script was only tested on Python version 3.13,
but older versions may work. The simulation can be ran by using the ```uv``` package manager or by manually installing the required Python libraries that are listed in the requirements.txt file.
1. Clone or download this repository.
2. Navigate to the project's root directory in your terminal.

### Using uv

3. Download the nescessary packages and run the script: ```uv run main.py```

### Manual download

3. install required packages (preferably in a virtual environment): ```pip install -r requirements.txt```

4. The simulation is executed by running the main.py script from the project's root directory. ```python main.py```

## Configuration
It is possible to configure the amount of iterations in the config.py file, 1000 is recommended and is the default for fast execution, 10000 is recommended to get a larger dataset. More iterations will simply take more time to complete.

In the same config.py file it is also possible to change both input and output file names if desired.

## Input Data

The simulation requires an input file named projects.xlsx located in a resources subfolder. This file is required to contain a sheet named "projects".
The "projects" sheet defines the available projects for the simulation. Each row specifies a project's annual Sunk Cost, Salvageable Cost, and whether a given year is a "risk-year".
Currently it is only allowed to include between 1 and 100 projects in the sheet.

## Output

The simulation will produce an Excel file named project_results.xlsx in the resources folder. This file contains the raw, iteration-by-iteration results for both the final portfolio value and the final cash surplus for each of the three strategies, across all iterations.
