import unittest

import pandas as pd

from tests.tools.mock_api_client import MockClient
from tests.tools.mocked_client_testcase import MockedClientTestCase
from time_tracking_synchronisation.troi_api.projects import get_all_positions, ProjectState, SUBPOSITION_NAME, \
    SUBPOSITION_ID, SUBPROJECT_NAME, SUBPROJECT_ID, PROJECT_STATE, PROJECT_NAME, PROJECT_ID


class ProjectsTestCase(MockedClientTestCase):
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

    def test_list_projects(self):
        expected_df = pd.DataFrame(
            {
                PROJECT_ID: [2],
                PROJECT_NAME: ["project2"],
                PROJECT_STATE: [ProjectState.open.value],
                SUBPROJECT_ID: [21],
                SUBPROJECT_NAME: ["subproject2"],
                SUBPOSITION_ID: [211],
                SUBPOSITION_NAME: ["position_subproject2"],
            },
            index=[0]
        )
        projects = get_all_positions(client=self.client)
        self.assertEqual(1, projects.shape[0])
        compare = expected_df.compare(projects)
        self.assertTrue(compare.empty)



if __name__ == '__main__':
    unittest.main()
