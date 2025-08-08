import random
from copy import deepcopy
from dataclasses import dataclass

from src.data import Portfolio
from src.project import Project
from src.strategy import ProjectStrategy
from src.strategy import get_risk_cost
from src.utils.constants import SUB_PROJECT_VALUE, SUB_PROJECT_COST, PROJECT_LENGTH
from src.utils.project_utils import find_optimal_closures
from src.year import Year


@dataclass
class ProjectManager:
    current_projects: list[Project]
    completed_projects: list[Project]
    discarded_projects: list[Project]
    strategy: ProjectStrategy

    def reset_manager(self):
        self.current_projects.clear()
        self.completed_projects.clear()
        self.discarded_projects.clear()

    def calculate_current_value(self, current_year) -> int:
        valuation = 0

        for project in self.current_projects:
            finished_work_years = current_year - (project.created_at - 1)
            assert (
                finished_work_years > 0
            )  # This function should only be run after each year is finished, but before the next is started

            valuation += finished_work_years * SUB_PROJECT_VALUE

        valuation += len(self.completed_projects) * (SUB_PROJECT_VALUE * PROJECT_LENGTH)
        return valuation

    def reacquire_deficit_value(
        self, deficit: int, current_year: int, available_funds: list[Year]
    ) -> int:
        """
        :param available_funds: the fund list, which is used to reacquire funds for future years.
        :param deficit: The deficit to afford the current projects.
        :param current_year: The current year for the project manager.
        :return: Returns the excess cash, which should be added to the cash of the portfolio.
        """

        optimal_closures = find_optimal_closures(
            deficit, self.current_projects, current_year
        )

        if len(optimal_closures) == 0:
            close_projects(self, self.current_projects, current_year, available_funds)
            assert len(self.current_projects) == 0
            return 0

        # A viable solution exists, only close the projects in least_valued_combination.
        remaining_funds = deficit

        for project in optimal_closures:
            remaining_funds += project.get_current_sub_project(
                current_year
            ).salvageable_cost

        assert remaining_funds >= 0

        close_projects(
            self,
            optimal_closures,
            current_year,
            available_funds,
        )

        return remaining_funds

    def run(
        self,
        funds_per_year: list[Year],
        new_projects: list[Project],
    ) -> Portfolio:
        """
        Runs the simulation on a single manager for 1 iteration, also said as one round.
        """

        available_funds: list[Year] = deepcopy(funds_per_year)
        years = len(available_funds)

        portfolio = Portfolio([0] * years, [0] * years)
        for i in range(years):
            current_year = i + 1

            # Step 1: Given the available funds, run strategy and accept projects until returns false
            run_strategy(self, new_projects, i + 1, available_funds)
            # Step 2: Run the risk calculations for the current year
            risk_cost = 0
            for project in self.current_projects:
                current_sub_project = project.get_current_sub_project(current_year)
                if current_sub_project.has_risk:
                    risk_cost += get_risk_cost()

            # Step 3: Calculate if there is a deficit and reacquire value if there is.
            possible_deficit = available_funds[i].allocated_funds - risk_cost
            current_year_cash = 0

            if possible_deficit < 0:
                deficit_return = self.reacquire_deficit_value(
                    possible_deficit, current_year, available_funds
                )

                if deficit_return > 0:
                    current_year_cash = deficit_return
            else:
                current_year_cash = possible_deficit

            # Step 4: Remove any finished projects in current_projects
            projects_to_finish: list[Project] = []
            for project in self.current_projects:
                if (current_year - project.created_at) >= 5:
                    projects_to_finish.append(project)

            for project in projects_to_finish:
                self.completed_projects.append(
                    self.current_projects.pop(self.current_projects.index(project))
                )

            # Step 5: accumulate cash in portfolio, and calculate value for current year in portfolio.
            for year_count in range(i, years):
                portfolio.cash[year_count] += current_year_cash

            portfolio.value[i] = self.calculate_current_value(current_year)

        return portfolio


def run_strategy(
    project_manager: ProjectManager,
    new_projects: list[Project],
    current_year: int,
    available_funds: list[Year],
):
    while True:
        new_project = deepcopy(random.choice(new_projects))
        new_project.created_at = current_year

        should_accept = project_manager.strategy.should_accept_project(
            available_funds[current_year - 1 :],
            project_manager.current_projects,
            current_year,
            new_project,
        )
        if not should_accept:
            break

        project_manager.current_projects.append(new_project)
        project_start = current_year - 1  # zero indexed
        project_end = project_start + PROJECT_LENGTH
        if project_end > len(available_funds):
            project_end = len(available_funds)

        for j in range(project_start, project_end):
            available_funds[j].allocated_funds -= SUB_PROJECT_COST


def close_projects(
    project_manager: ProjectManager,
    projects_to_close: list[Project],
    current_year: int,
    available_funds: list[Year],
):
    updated_current_projects = []
    for project in project_manager.current_projects:
        if project in projects_to_close:
            # This project is being discarded. Add its funds back.
            project_manager.discarded_projects.append(project)
            sub_project_index = current_year - project.created_at
            if sub_project_index <= 5:
                for i in range(sub_project_index, PROJECT_LENGTH):
                    index = (project.created_at - 1) + i
                    if index < len(available_funds):
                        available_funds[index].allocated_funds += SUB_PROJECT_COST
        else:
            # This project is being kept.
            updated_current_projects.append(project)

    project_manager.current_projects = updated_current_projects
