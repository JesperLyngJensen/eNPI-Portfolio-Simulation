import unittest
from typing import List, Tuple

from src.project import Project, SubProject
from src.project_manager import ProjectManager
from src.strategy import traverse_probability_tree, OptimalStrategy
from src.utils.project_utils import (
    calculate_delta_investment,
    find_project_risk_conflicts,
)
from src.year import Year

p1 = Project(
    1,
    [
        SubProject(True, 8, 2),
        SubProject(False, 5, 5),
        SubProject(False, 9, 1),
        SubProject(False, 5, 5),
        SubProject(True, 6, 4),
        SubProject(True, 8, 2),
    ],
)
p2 = Project(
    2,
    [
        SubProject(False, 5, 5),
        SubProject(True, 5, 5),
        SubProject(False, 9, 1),
        SubProject(True, 5, 5),
        SubProject(True, 6, 4),
        SubProject(False, 8, 2),
    ],
)
p3 = Project(
    2,
    [
        SubProject(True, 8, 2),
        SubProject(False, 7, 3),
        SubProject(True, 10, 0),
        SubProject(False, 10, 0),
        SubProject(False, 6, 4),
        SubProject(True, 10, 0),
    ],
)
p4 = Project(
    3,
    [
        SubProject(True, 7, 3),
        SubProject(False, 8, 2),
        SubProject(False, 6, 4),
        SubProject(False, 6, 4),
        SubProject(True, 5, 5),
        SubProject(True, 5, 5),
    ],
)

p5 = Project(
    4,
    [
        SubProject(False, 10, 0),
        SubProject(True, 7, 3),
        SubProject(True, 7, 3),
        SubProject(False, 4, 6),
        SubProject(False, 3, 7),
        SubProject(True, 8, 2),
    ],
)


class OptimalTest(unittest.TestCase):
    def test_cost_1(self):
        s_p = SubProject(False, 5, 5)

        p1 = Project(1, [s_p] * 6)
        projects = [p1] * 3

        res = calculate_delta_investment(projects, 1, 1)

        self.assertEqual(30, res)

    def test_cost_2(self):
        s_p = SubProject(False, 5, 5)

        p1 = Project(1, [s_p] * 6)
        projects = [p1] * 3

        res = calculate_delta_investment(projects, 2, 3)

        self.assertEqual(60, res)

    def test_cost_3(self):
        s_p = SubProject(False, 5, 5)

        p1 = Project(1, [s_p] * 6)
        projects = [p1] * 3

        res = calculate_delta_investment(projects, 5, 6)

        self.assertEqual(60, res)

    def test_cost_4(self):
        s_p = SubProject(False, 5, 5)

        p1 = Project(1, [s_p] * 6)
        projects = [p1] * 3

        res = calculate_delta_investment(projects, 6, 7)

        self.assertEqual(30, res)

    def test_cost_5(self):
        s_p = SubProject(False, 5, 5)

        p1 = Project(1, [s_p] * 6)
        p2 = Project(1, [s_p] * 6)
        projects = [p2, p1, p1]

        projects[0].created_at = 2

        res = calculate_delta_investment(projects, 1, 2)

        self.assertEqual(50, res)


class CalculateExpectedInvestmentTest(unittest.TestCase):

    def test_expected_1(self):
        # expected_investment = 158.91
        expected_investment = 198.2

        funds = [Year(8), Year(8), Year(8), Year(18), Year(38), Year(48)]

        projects = [p1, p2, p3, p4, p5]

        conflicts = find_project_risk_conflicts(
            projects,
            funds,
            4,
        )

        conflict_value_comparison: List[Tuple[int, int, int]] = []

        for conflict in conflicts:
            # (year, existing value, maximum new value)
            conflict_value_comparison.append(
                (
                    conflict[0],
                    calculate_delta_investment([p1, p2, p3, p4], 1, conflict[0]),
                    calculate_delta_investment(projects, 1, conflict[0]),
                )
            )

        calculated_expected = (
            230
            # 180
            - traverse_probability_tree(
                conflicts, None, 4, funds, projects, conflict_value_comparison
            ).expected_loss
        )

        tolerance = 0.6

        self.assertTrue(abs(calculated_expected - expected_investment) <= tolerance)


class AcceptanceTest(unittest.TestCase):
    def test_accept_1(self):
        optimal_manager = ProjectManager([p1, p2, p3, p4], [], [], OptimalStrategy())

        should_accept = optimal_manager.strategy.should_accept_project(
            [Year(18), Year(18), Year(18), Year(28), Year(48), Year(58)],
            optimal_manager.current_projects,
            4,
            p5,
        )
        self.assertFalse(should_accept)
