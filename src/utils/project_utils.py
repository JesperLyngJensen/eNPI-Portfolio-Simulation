from itertools import chain, combinations
from typing import List, Tuple

from src.project import Project
from src.utils.constants import SUB_PROJECT_COST, NO_VIABLE_SOLUTION
from src.year import Year


def find_optimal_closures(
    deficit: int, current_projects: List[Project], current_year: int
) -> List[Project]:
    assert deficit < 0

    projects_powerset: List[List[Project]] = powerset(current_projects)

    viable_solutions: List[Tuple[int, List[Project]]] = (
        []
    )  # All lists of projects in this set must have a salvageable cost greater or equal to the deficit

    for i, projects in enumerate(projects_powerset):
        salvageable_cost = 0

        for project in projects:
            if project_is_active(project, current_year):
                salvageable_cost += project.get_current_sub_project(
                    current_year
                ).salvageable_cost

        if deficit + salvageable_cost >= 0:
            viable_solutions.append((i, projects))

    least_valued_combination: Tuple[int, int] = (
        NO_VIABLE_SOLUTION,
        1000,
    )  # [index in the powerset list, total value of projects ]

    for solution in viable_solutions:
        total_value = 0

        for project in solution[1]:
            total_value += project.get_current_value(current_year)

        if total_value < least_valued_combination[1]:
            least_valued_combination = (solution[0], total_value)

    if least_valued_combination[0] == -1:
        return []

    return projects_powerset[least_valued_combination[0]]


def powerset(projects: List[Project]) -> List[List[Project]]:
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(projects)

    collection: List[List[Project]] = []
    for projects in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)):
        collection.append(projects)

    return collection


def find_project_risk_conflicts(
    projects: List[Project], funds: List[Year], current_year: int
) -> List[
    Tuple[int, int]
]:  # Type is (year of conflict, number of risk elements for year)
    conflicts = []

    for year in range(1, 10):
        risk_count = 0

        if year < current_year:
            continue

        for project in projects:
            if not project_is_active(project, year):
                continue
            if project.get_current_sub_project(year).has_risk:
                risk_count += 1

        if funds[year - current_year].allocated_funds < risk_count * 6:
            conflicts.append((year, risk_count))

    return conflicts


def calculate_delta_investment(
    projects: List[Project],
    starting_year: int,
    current_year: int,
) -> int:
    new_value = 0

    for year in range(starting_year, current_year + 1):
        for project in projects:
            if not project_is_active(project, year):
                continue
            new_value += SUB_PROJECT_COST

    return new_value


def project_is_active(project: Project, current_year: int) -> bool:
    current_sub_project = current_year - project.created_at

    return 0 <= current_sub_project < 6
