from src.data import SimulationResult, Portfolio, ManagerResult
from src.project import Project
from src.project_manager import ProjectManager
from src.year import Year


class Simulation:
    projects: list[Project]
    years: list[Year]
    iteration_limit: int
    managers: dict[str, ProjectManager]

    def __init__(
        self,
        years: list[Year],
        iterations: int,
        managers: dict[str, ProjectManager],
        projects: list[Project],
    ):

        self.years = years
        self.iteration_limit = iterations
        self.managers = managers
        self.projects = projects

    def reset_managers(self):
        for manager in self.managers.values():
            manager.reset_manager()

    def run_simulation(self) -> SimulationResult:
        """
        Run the configured simulation.
        :return: The functions will return a dictionary holding each manager and their respective simulation results.
        Each simulation result consists of all iteration of the simulation, which is a list of integers.
        """
        simulation_results: SimulationResult = SimulationResult({})

        # Setup managers for result

        for manager_name in self.managers.keys():
            simulation_results.managers[manager_name] = ManagerResult(
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
                Portfolio([], []),
            )

        for iteration in range(self.iteration_limit):
            simulation_results.add_iteration_result(self.run_iteration())

        return simulation_results

    def run_iteration(self) -> dict[str, Portfolio]:
        """
        Runs an iteration of simulation.
        :return: This functions returns a list of values each manager generated after every year.
        """
        self.reset_managers()

        manager_results: dict[str, Portfolio] = {}

        for manager_name, manager in self.managers.items():
            manager_results[manager_name] = manager.run(self.years, self.projects)

        assert len(self.managers) == len(manager_results)

        return manager_results
