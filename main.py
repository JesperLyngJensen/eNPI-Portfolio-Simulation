from pathlib import Path

from config import (
    ITERATIONS,
    INPUT_FILE_NAME,
    OUTPUT_FILE_NAME,
)

from src.project_manager import ProjectManager
from src.simulation import Simulation
from src.strategy import (
    GreedyStrategy,
    MinusOneStrategy,
    OptimalStrategy,
)
from src.year import STANDARD_YEARS
import src.file_handling as fh


INPUT_FILE_PATH = Path("resources", INPUT_FILE_NAME)
OUTPUT_FILE_PATH = Path("resources", OUTPUT_FILE_NAME)


if __name__ == "__main__":

    # Define the manager strategies that will be used in the simulation.
    managers = {
        "greedy_manager": ProjectManager([], [], [], GreedyStrategy()),
        "minus_one_manager": ProjectManager([], [], [], MinusOneStrategy()),
        "optimal_manager": ProjectManager([], [], [], OptimalStrategy()),
    }
    # Load the projects from a file.
    projects = fh.load_projects_from_file(INPUT_FILE_PATH)

    # Setup the simulation that will be ran.
    simulation = Simulation(STANDARD_YEARS, ITERATIONS, managers, projects)

    print("Loaded simulation!")

    # Run the simulation and collect the resulting data in simulation_result
    simulation_result = simulation.run_simulation()

    print("Simulation finished!")

    # Save the simulation_result to the output Excel file.
    fh.save_simulation_results_to_excel(simulation_result, OUTPUT_FILE_PATH)

    print("Simulation saved to file: " + str(OUTPUT_FILE_PATH))
