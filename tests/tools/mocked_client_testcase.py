import unittest

from tests.tools.mock_api_client import MockClient
from troi.troi_api.projects import ProjectState


class MockedClientTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MockClient()
        self.client.setup_add_project(id=1, name="project1", project_status=ProjectState.closed)
        self.client.setup_add_project(id=2, name="project2", project_status=ProjectState.open)
        self.client.setup_add_calc_pos(
            project_id=1,
            subproject_id=11,
            subproject_name="subproject1",
            position_id=111,
            position_name="position_subproject1"
        )
        self.client.setup_add_calc_pos(
            project_id=2,
            subproject_id=21,
            subproject_name="subproject2",
            position_id=211,
            position_name="position_subproject2"
        )