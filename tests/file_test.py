import unittest
from pathlib import Path

from src.data import ManagerResult, Portfolio
from src.file_handling import load_projects_from_file, save_simulation_results_to_excel
from src.project import Project, SubProject
from src.simulation import SimulationResult


class TestImport(unittest.TestCase):

    def test_import(self):
        path = Path("resources", "tests" , "projects_test.xlsx")

        sub_projects1 = [
            SubProject(False, 8, 2),
            SubProject(True, 7, 3),
            SubProject(True, 9, 1),
            SubProject(False, 5, 5),
            SubProject(False, 6, 4),
            SubProject(True, 8, 2),
        ]

        sub_projects2 = [
            SubProject(True, 9, 1),
            SubProject(True, 6, 4),
            SubProject(False, 5, 5),
            SubProject(False, 8, 2),
            SubProject(False, 8, 2),
            SubProject(True, 7, 3),
        ]
        project_1 = Project(0, sub_projects1)
        project_2 = Project(0, sub_projects2)

        imported_projects = load_projects_from_file(path)

        self.assertEqual(project_1, imported_projects[0])
        self.assertEqual(project_2, imported_projects[1])


class TestExport(unittest.TestCase):
    def test_export(self):
        path = Path("resources", "tests", "output_test.xlsx")

        p1 = Portfolio([1, 1], [3, 2])
        p2 = Portfolio([2, 4], [2, 5])
        sim_res = SimulationResult(
            {
                "manager_1": ManagerResult(p1, p1, p2, p1, p1, p2, p2, p1, p1),
                "manager_2": ManagerResult(p2, p2, p2, p1, p1, p2, p2, p1, p1),
                "manager_3": ManagerResult(p2, p1, p2, p1, p1, p2, p1, p2, p2),
            }
        )

        save_simulation_results_to_excel(sim_res, path)

        self.assertTrue(path.is_file())
