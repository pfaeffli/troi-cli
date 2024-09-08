import copy
from datetime import datetime
from typing import List, Optional, Tuple

import troi.troi_api as client
import troi.troi_api.projects as const_projects
from tests.constant import TROI_PROJECT_RESPONSE_ITEM, TROI_PROJECT_CALC_POSITION_RESPONSE_ITEM, TROI_BILLING_HOURS
from troi.troi_api.api import create_billing_hour_payload, TROI_BILLING_HOUR_RECORD_ID, \
    TROI_BILLING_HOUR_DISPLAY_PATH


class MockClientError(Exception):
    pass


def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, dict):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class MockClient(client.api.Client):
    def __init__(self, url: str = "url", username: str = "username", api_token: str = "api_token"):
        self.base_url = url
        self.auth = (username, api_token)
        self.headers = {
            'User-Agent': 'curl/7.58.0',
        }
        self.projects = []
        self.calculation_positions = []
        self.billing_hours = []
        self.added_billing_hours = []
        self.updated_billing_hours = []
        self.error = None

    def setup_add_project(self, id: int = 1, name: str = "project",
                          project_status: const_projects.ProjectState = const_projects.ProjectState.open):
        project_template = copy.deepcopy(TROI_PROJECT_RESPONSE_ITEM)
        project_template[const_projects.TROI_PROJECT_ID] = id
        project_template[const_projects.TROI_PROJECT_NAME] = name
        project_template['Status'][const_projects.TROI_PROJECT_STATE_NAME] = project_status.value
        self.projects.append(project_template)

    def setup_add_calc_pos(self, project_id: int = 1, subproject_id: int = 1, subproject_name: str = "subproject1",
                           position_id: int = 1, position_name: str = "calcposition1"):
        calc_pos_template = copy.deepcopy(TROI_PROJECT_CALC_POSITION_RESPONSE_ITEM)
        projects, exception = self.get_project(project_id)
        if len(projects) != 1:
            if exception:
                raise exception
            else:
                raise ValueError(f"Cannot handle zero or multiple entries with Id {project_id}. Found {len(projects)}.")
        calc_pos_template["Project"] = projects[0]
        calc_pos_template["Subproject"][const_projects.TROI_SUBPROJECT_ID] = subproject_id
        calc_pos_template["Subproject"][const_projects.TROI_SUBPROJECT_NAME] = subproject_name
        calc_pos_template[const_projects.TROI_SUBPOSITION_ID] = position_id
        calc_pos_template[const_projects.TROI_SUBPOSITION_NAME] = position_name
        self.calculation_positions.append(calc_pos_template)

    def setup_billing_hours(self,
                            record_id: Optional[int] = None,
                            client_id: int = 3,
                            user_id: int = 1,
                            display_path: str = "project / subproject / position",
                            project_id: int = 1,
                            position_id: int = 111,
                            date: datetime = datetime(2024, 1, 1),
                            hours: float = 1.0,
                            remark: str = "work"):
        billing_hour_template = copy.deepcopy(TROI_BILLING_HOURS)
        update = create_billing_hour_payload(client_id=client_id, user_id=user_id, postion_id=position_id, date=date, hours=hours,
                                             remark=remark)
        billing_hour_template = deep_update(billing_hour_template, update)
        if record_id is None:
            record_id = len(self.billing_hours)
        billing_hour_template[TROI_BILLING_HOUR_RECORD_ID] = record_id
        billing_hour_template[TROI_BILLING_HOUR_DISPLAY_PATH] = display_path
        self.billing_hours.append(billing_hour_template)

    def set_error(self, error: Exception):
        self.error = error

    def list_projects(self, client_id: int) -> Tuple[List[dict], Optional[Exception]]:
        if self.error:
            return [], self.error
        # Fake project listing
        return self.projects, None

    def get_project(self, project_id: int) -> Tuple[List[dict], Optional[Exception]]:
        if self.error:
            return [], self.error
        projects = [project for project in self.projects if project['Id'] == project_id]
        if len(projects) == 0:
            return [], MockClientError(f"Project with Id {project_id} not found.")
        else:
            return projects, None

    # For simplicity's sake, all other methods also return fake data or None in case of the update and add functions
    def list_calc_pos(self, client_id: int, project_id: int) -> Tuple[List[dict], Optional[Exception]]:
        if self.error:
            return [], self.error
        positions = [position for position in self.calculation_positions if
                     position["Project"][const_projects.TROI_PROJECT_ID] == project_id]
        if len(positions) == 0:
            return [], MockClientError(f"No Positions with project Id {project_id} found.")
        else:
            return positions, None

    def list_billing_hours(self, client_id: int, project_id: int, date_from: datetime, date_to: datetime) -> Tuple[
        List[dict], Optional[Exception]]:
        if self.error:
            return [], self.error

        if len(self.billing_hours) == 0:
            return [], MockClientError("No billing hours added. Use setup_billing_hours().")
        else:
            return self.billing_hours, None

    def add_billing_hours(self, client_id: int, user_id: int, task_id: int, date: datetime, hours: float,
                          remark: str) -> Optional[Exception]:
        self.added_billing_hours.append(
            create_billing_hour_payload(client_id=client_id, user_id=user_id, postion_id=task_id, date=date, hours=hours,
                                        remark=remark)
        )
        if self.error:
            return self.error
        return None

    def update_billing_hours(self, client_id: int, user_id: int, task_id: int, record_id: int, date: datetime,
                             hours: float, remark: str) -> Optional[Exception]:
        self.updated_billing_hours.append(
            create_billing_hour_payload(client_id=client_id, user_id=user_id, postion_id=task_id, date=date,
                                        hours=hours,
                                        remark=remark)
        )
        if self.error:
            return self.error
        return None
