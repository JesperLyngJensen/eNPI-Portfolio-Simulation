import unittest

from src.project import SubProject, Project
from src.project_manager import ProjectManager
from src.strategy import GreedyStrategy, MinusOneStrategy
from src.year import Year


class TestSellOptimal(unittest.TestCase):
    def test_sell_1(self):
        test_manager = ProjectManager([], [], [], GreedyStrategy())

        p1 = [
            SubProject(False, 0, 10),
            SubProject(True, 0, 10),
            SubProject(True, 0, 10),
            SubProject(False, 0, 10),
            SubProject(False, 0, 10),
            SubProject(True, 0, 10),
        ]

        p2 = [
            SubProject(True, 0, 10),
            SubProject(True, 0, 10),
            SubProject(False, 0, 10),
            SubProject(False, 0, 10),
            SubProject(False, 0, 10),
            SubProject(True, 0, 10),
        ]

        high_value_project = Project(1, p1)

        low_value_project = Project(4, p2)

        test_manager.current_projects = [high_value_project, low_value_project]

        test_manager.reacquire_deficit_value(
            -3,
            5,
            [
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
            ],
        )

        print(
            "\ncurrent project length: "
            + str(len(test_manager.current_projects))
            + "\ndiscarded project length: "
            + str(len(test_manager.discarded_projects))
        )

        self.assertEqual(test_manager.current_projects, [high_value_project])
        self.assertEqual(test_manager.discarded_projects, [low_value_project])

    def test_sell_2(self):
        manager = ProjectManager([], [], [], MinusOneStrategy())

        p1 = [
            SubProject(False, 0, 10),
            SubProject(True, 0, 10),
            SubProject(True, 0, 10),
            SubProject(True, 0, 10),
            SubProject(False, 0, 10),
            SubProject(True, 0, 10),
        ]

        p2 = [
            SubProject(True, 0, 10),
            SubProject(False, 0, 10),
            SubProject(False, 0, 10),
            SubProject(False, 0, 10),
            SubProject(False, 0, 10),
            SubProject(True, 0, 10),
        ]

        high_value_project = Project(1, p1)

        low_value_project = Project(4, p2)

        manager.current_projects = [high_value_project, low_value_project]

        deficit_return = manager.reacquire_deficit_value(
            -15,
            5,
            [
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
                Year(20),
            ],
        )

        print(
            "\ncurrent project length: "
            + str(len(manager.current_projects))
            + "\ndiscarded project length: "
            + str(len(manager.discarded_projects))
        )

        self.assertEqual(manager.current_projects, [])
        self.assertEqual(
            manager.discarded_projects, [high_value_project, low_value_project]
        )
        self.assertEqual(deficit_return, 5)
