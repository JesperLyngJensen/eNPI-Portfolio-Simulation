import random
from abc import abstractmethod, ABC
from copy import deepcopy
from typing import override, List, Tuple

from src.probability import get_risk_distribution, ProjectConflict, TreeTraversalResult
from src.project import Project
from src.risk import NORMAL_RISK_VALUES
from src.utils.project_utils import (
    find_project_risk_conflicts,
    calculate_delta_investment,
)

from src.utils.constants import SUB_PROJECT_COST, PROJECT_LENGTH

from src.year import Year


def get_risk_cost() -> int:
    """
    This algorithm gives a random risk value, which can either be from the 'NORMAL_RISK_VALUES' or
    'VOLATILE_RISK_VALUES'
    :return: The Integer risk cost.
    """

    return random.choice(NORMAL_RISK_VALUES)


class ProjectStrategy(ABC):
    @abstractmethod
    def should_accept_project(
        self,
        available_funds: list[Year],
        current_projects: list[Project],
        current_year: int,
        new_project: Project,
    ) -> bool:
        """
        This is the algorithm for deciding if a project should be accepted by a project manager, if true, then it will accept the project.
        :param current_year: The current year for the project_manager.
        :param available_funds: These are funds from the current year and forward until the end, this should already have accounted for currently owned projects.
        :param current_projects: The current projects, used for risk calculation.
        :param new_project: The new project that can be accepted or rejected.
        :return: The boolean indicating if the project should be accepted (True) or rejected (False).
        """
        raise NotImplementedError("Subclasses must implement this method")


class GreedyStrategy(ProjectStrategy):
    @override
    def should_accept_project(
        self,
        available_funds: list[Year],
        current_projects: list[Project],
        current_year: int,
        new_project: Project,
    ) -> bool:
        for count, funds in enumerate(available_funds):
            if count >= len(new_project.sub_projects):
                break
            elif funds.allocated_funds < SUB_PROJECT_COST:
                return False

        return True


class MinusOneStrategy(ProjectStrategy):
    @override
    def should_accept_project(
        self,
        available_funds: list[Year],
        current_projects: list[Project],
        current_year: int,
        new_project: Project,
    ) -> bool:
        for count, funds in enumerate(available_funds):
            if count >= len(new_project.sub_projects):
                break
            elif funds.allocated_funds < SUB_PROJECT_COST * 2:
                return False

        return True


class OptimalStrategy(ProjectStrategy):
    @override
    def should_accept_project(
        self,
        available_funds: list[Year],
        current_projects: list[Project],
        current_year: int,
        new_project: Project,
    ) -> bool:
        # First check that there are funds for the new project

        for count, funds in enumerate(available_funds):
            if count >= PROJECT_LENGTH:
                break
            elif funds.allocated_funds < SUB_PROJECT_COST:
                return False

        # Add the new project to the projects_copy to run the simulation on.

        fund_copy = deepcopy(available_funds)
        projects_copy = list(current_projects)

        projects_copy.append(new_project)
        project_end = PROJECT_LENGTH
        if project_end > len(fund_copy):
            project_end = len(fund_copy)

        for j in range(0, project_end):
            fund_copy[j].allocated_funds -= SUB_PROJECT_COST

        # Calculate the conflicting years.
        conflict_years = find_project_risk_conflicts(
            projects_copy, fund_copy, current_year
        )

        # For each conflict year calculate the existing value, and maximum value after accepting new project

        # (year, existing investment, maximum new value)
        conflict_value_comparison: List[Tuple[int, int, int]] = []

        for conflict in conflict_years:
            # (year, existing value, maximum new value)
            conflict_value_comparison.append(
                (
                    conflict[0],
                    calculate_delta_investment(current_projects, 1, conflict[0]),
                    calculate_delta_investment(projects_copy, 1, conflict[0]),
                )
            )
        # We have now detected the years with possible conflicts.

        if len(conflict_years) == 0:
            return True

        (existing_return, expected_return) = calculate_expected_investment(
            conflict_years,
            current_year,
            projects_copy,
            fund_copy,
            conflict_value_comparison,
        )

        if expected_return < existing_return:
            return False
        else:
            return True


def calculate_expected_investment(
    conflict_years: List[Tuple[int, int]],
    current_year: int,
    projects: List[Project],
    funds: List[Year],
    value_comparison: List[Tuple[int, int, int]],
) -> Tuple[float, float]:
    """
    This function unwraps the TreeTraversalResult.
    """
    result = traverse_probability_tree(
        conflict_years, None, current_year, funds, projects, value_comparison
    )

    return float(result.existing_return), (
        result.expected_return - result.expected_loss
    )


def traverse_probability_tree(
    next_conflicts: List[Tuple[int, int]],
    chance_to_proceed: float | None,
    current_year: int,
    funds: List[Year],
    projects: List[Project],
    value_comparison: List[Tuple[int, int, int]],
) -> TreeTraversalResult:

    assert len(next_conflicts) > 0

    current_conflict = next_conflicts[0]
    fund_index = current_conflict[0] - current_year
    conflicts: List[ProjectConflict] = []

    risk_probability = get_risk_distribution(current_conflict[1])

    new_chance_to_proceed: float = 0.0

    for risk in risk_probability:
        risk_percentage: float
        if chance_to_proceed is None:
            risk_percentage = risk[0]
        else:
            risk_percentage = chance_to_proceed * risk[0]

        deficit = funds[fund_index].allocated_funds - risk[1]

        if deficit < 0:
            conflicts.append(
                ProjectConflict(deficit, risk_percentage, current_conflict[0])
            )
        else:
            new_chance_to_proceed += risk_percentage

    expected_loss = 0.0

    assert new_chance_to_proceed is not None

    for conflict in conflicts:
        expected_loss += conflict.calculate_expected_loss(projects)

    current_existing_return = 0
    current_maximum_return = 0.0

    if len(next_conflicts) > 1:
        traversel_result = traverse_probability_tree(
            next_conflicts[1:],
            new_chance_to_proceed,
            current_year,
            funds,
            projects,
            value_comparison,
        )

        expected_loss += traversel_result.expected_loss
        current_existing_return = traversel_result.existing_return
        current_maximum_return = traversel_result.expected_return

    for c_year, existing, maximum in value_comparison:
        if c_year == current_conflict[0]:
            current_existing_return = existing
            current_maximum_return = maximum

    assert current_existing_return != 0

    return TreeTraversalResult(
        int(current_existing_return), current_maximum_return, expected_loss
    )
