from dataclasses import dataclass
from typing import List, Tuple

from src.project import Project
from src.utils.project_utils import calculate_delta_investment, find_optimal_closures

#   RISK_{x} defines the probability of getting a certain outcome with x-amount of risk elements
#   where the data is stored as a tuple with the data: (probability, outcome)


RISK_1: List[Tuple[float, int]] = [(0.33, 0), (0.33, 3), (0.33, 6)]

RISK_2: List[Tuple[float, int]] = [
    (0.1089, 0),
    (0.2178, 3),
    (0.333, 6),
    (0.2178, 9),
    (0.1089, 12),
]

RISK_3: List[Tuple[float, int]] = [
    (0.037, 0),
    (0.111, 3),
    (0.222, 6),
    (0.260, 9),
    (0.222, 12),
    (0.111, 15),
    (0.037, 18),
]

RISK_4: List[Tuple[float, int]] = [
    (0.012, 0),
    (0.049, 3),
    (0.124, 6),
    (0.197, 9),
    (0.235, 12),
    (0.197, 15),
    (0.124, 18),
    (0.049, 21),
    (0.012, 24),
]

RISK_5: List[Tuple[float, int]] = [
    (0.00411522633744856, 0),
    (0.020576131687242802, 3),
    (0.0617283950617284, 6),
    (0.1234567901234568, 9),
    (0.1851851851851852, 12),
    (0.20987654320987656, 15),
    (0.1851851851851852, 18),
    (0.1234567901234568, 21),
    (0.0617283950617284, 24),
    (0.020576131687242802, 27),
    (0.00411522633744856, 30),
]


def get_risk_distribution(risk_elements: int) -> List[Tuple[float, int]]:
    match risk_elements:
        case 1:
            return RISK_1
        case 2:
            return RISK_2
        case 3:
            return RISK_3
        case 4:
            return RISK_4
        case 5:
            return RISK_5

    # This currently limits the yearly funds that can be given, as more funds could result in 6 risk_elements,
    # which can be handled if another case for 6 risk_elements is added and so on.
    # In the current simulation 6 is not possible.
    raise ValueError(
        f"Risk elements can only be between 1 to 5, given risk elements: {risk_elements}"
    )


@dataclass
class ProjectConflict:
    deficit: int
    adjusted_probability: float
    conflict_year: int

    def __init__(self, deficit: int, adjusted_probability: float, conflict_year: int):
        self.deficit = deficit
        self.adjusted_probability = adjusted_probability
        self.conflict_year = conflict_year

    def calculate_expected_loss(self, projects: List[Project]) -> float:
        value = calculate_delta_investment(projects, 1, self.conflict_year)
        temp_projects = list(projects)
        closures = find_optimal_closures(self.deficit, projects, self.conflict_year)

        for closure in closures:
            temp_projects.remove(closure)

        loss = value - calculate_delta_investment(temp_projects, 1, self.conflict_year)

        return float(loss) * self.adjusted_probability


@dataclass
class TreeTraversalResult:
    existing_return: float
    expected_return: float
    expected_loss: float

    def __init__(
        self, existing_return: int, expected_return: float, expected_loss: float
    ):
        self.existing_return = existing_return
        self.expected_return = expected_return
        self.expected_loss = expected_loss
