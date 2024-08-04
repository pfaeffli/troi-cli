import unittest

import pandas as pd
from troi.projects import get_all_positions

from tests.tools.MockApiClient import MockClient, ProjectState


class ProjectsTestCase(unittest.TestCase):
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

    def test_list_projects(self):
        expected_df = pd.DataFrame(
            {

            }
        )
        projects = self.client.list_projects(client_id=1)
        self.assertEqual(len(projects), 1)



if __name__ == '__main__':
    unittest.main()
