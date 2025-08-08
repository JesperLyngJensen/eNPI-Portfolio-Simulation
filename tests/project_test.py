import unittest

from src.project import Project
from src.utils.project_utils import project_is_active

project_1 = Project(1, [])
project_2 = Project(6, [])


class ProjectTest(unittest.TestCase):

    def test_active_1(self):

        res = project_is_active(project_1, 1)

        self.assertEqual(True, res)

    def test_active_2(self):

        res = project_is_active(project_1, 7)

        self.assertEqual(False, res)

    def test_active_3(self):

        res = project_is_active(project_1, 6)

        self.assertEqual(True, res)

    def test_active_4(self):

        res = project_is_active(project_2, 9)

        self.assertEqual(True, res)
