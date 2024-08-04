from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple

import troi.client.api
from tests.constant import TROI_PROJECT_RESPONSE_ITEM, TROI_PROJECT_CALC_POSITION_RESPONSE_ITEM


class MockClientError(Exception):
    pass


class ProjectState(Enum):
    closed = "abgeschlossen"
    open = "in Arbeit"


class MockClient(troi.client.api.Client):
    def __init__(self, url: str = "url", username: str = "username", api_token: str = "api_token"):
        self.base_url = url
        self.auth = (username, api_token)
        self.headers = {
            'User-Agent': 'curl/7.58.0',
        }
        self.projects = []
        self.calculation_positions = []

    def setup_add_project(self, id: int = 1, name: str = "project", project_status: ProjectState = ProjectState.open):
        project_template = TROI_PROJECT_RESPONSE_ITEM.copy()
        project_template['Id'] = id
        project_template['Name'] = name
        project_template['Status']['Name'] = project_status.value
        self.projects.append(project_template)

    def setup_add_calc_pos(self, project_id: int = 1, subproject_id: int = 1, subproject_name: str = "subproject1",
                           position_id: int = 1, position_name: str = "calcposition1"):
        calc_pos_template = TROI_PROJECT_CALC_POSITION_RESPONSE_ITEM.copy()
        projects, exception = self.get_project(project_id)
        if len(projects) != 1:
            if exception:
                raise exception
            else:
                raise ValueError(f"Cannot handle zero or multiple entries with Id {project_id}. Found {len(projects)}.")
        calc_pos_template["Project"] = projects[0]
        calc_pos_template["Subproject"]['Id'] = subproject_id
        calc_pos_template["Subproject"]['Name'] = subproject_name
        calc_pos_template['Id'] = position_id
        calc_pos_template['Name'] = position_name
        self.calculation_positions.append(calc_pos_template)

    def list_projects(self, client_id: int) -> Tuple[List[dict], Optional[Exception]]:
        # Fake project listing
        return self.projects, None

    def get_project(self, project_id: int) -> Tuple[List[dict], Optional[Exception]]:
        projects = [project for project in self.projects if project['Id'] == project_id]
        if len(projects) == 0:
            return [], MockClientError("Project with Id {project_id} not found.")
        else:
            return projects, None

    # For simplicity's sake, all other methods also return fake data or None in case of the update and add functions
    def list_calc_pos(self, client_id: int, project_id: int) -> Tuple[List[dict], Optional[Exception]]:
        positions = [position for position in self.projects if position["Project"]['Id'] == project_id]
        if len(positions) == 0:
            return [], MockClientError("No Positions with project Id {project_id} found.")
        else:
            return positions, None

    def list_billing_hours(self, client_id: int, project_id: int, date_from: datetime, date_to: datetime) -> Tuple[
        List[dict], Optional[Exception]]:
        return [], None

    def add_billing_hours(self, client_id: int, user_id: int, task_id: int, date: datetime, hours: float,
                          remark: str) -> Optional[Exception]:
        return None

    def update_billing_hours(self, client_id: int, user_id: int, task_id: int, record_id: int, date: datetime,
                             hours: float, remark: str) -> Optional[Exception]:
        return None
