from dataclasses import dataclass

from src.utils.constants import SUB_PROJECT_VALUE


@dataclass
class SubProject:
    has_risk: bool
    sunk_cost: int
    salvageable_cost: int

    def __init__(self, has_risk: bool, sunk_cost: int, salvageable_cost: int):
        self.has_risk = has_risk
        self.sunk_cost = sunk_cost
        self.salvageable_cost = salvageable_cost


@dataclass
class Project:
    created_at: int  # the year which the project was created
    sub_projects: list[
        SubProject
    ]  # Should always have 6, but python does not have arrays

    def get_current_value(self, current_year: int) -> int:
        assert current_year >= self.created_at

        return (current_year - (self.created_at - 1)) * SUB_PROJECT_VALUE

    def get_current_sub_project(self, current_year: int) -> SubProject:
        return self.sub_projects[current_year - self.created_at]
