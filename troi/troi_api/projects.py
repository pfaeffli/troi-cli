from enum import Enum
from typing import Optional, Union

import pandas as pd

from troi.troi_api.api import Client

TROI_PROJECT_NAME = "Name"
TROI_PROJECT_STATE_NAME = "Name"
TROI_PROJECT_ID = "Id"
TROI_SUBPROJECT_ID = "Id"
TROI_SUBPROJECT_NAME = "Name"
TROI_SUBPOSITION_ID = "Id"
TROI_SUBPOSITION_NAME = "Name"

CLIENT_ID = "client_id"
PROJECT_ID = "project_id"
PROJECT_NAME = "project_name"
PROJECT_STATE = "project_state"
SUBPROJECT_ID = "subproject_id"
SUBPROJECT_NAME = "subproject_name"
SUBPOSITION_ID = "task_id"
SUBPOSITION_NAME = "subposition_name"


def _to_project_dataframe(content: Union[list, dict]) -> pd.DataFrame:
    if isinstance(content, list):
        df = pd.DataFrame([pd.Series(r) for r in content])
    else:
        df = pd.Series(content).to_frame().T
    df[PROJECT_STATE] = df.Status.apply(lambda s: s[TROI_PROJECT_STATE_NAME])
    projects = df.loc[:, [TROI_PROJECT_ID, TROI_PROJECT_NAME, PROJECT_STATE]]
    return projects.loc[projects.loc[:, PROJECT_STATE] != ProjectState.closed.value, :].rename(columns={
        TROI_PROJECT_ID: PROJECT_ID,
        TROI_PROJECT_NAME: PROJECT_NAME,
    })

def get_project(client: Client, project_id:int) -> pd.DataFrame:
    content, error = client.get_project(project_id=project_id)
    if content is None:
        raise error
    return _to_project_dataframe(content)


def get_projects(client: Client, client_id: int) -> pd.DataFrame:
    content, error = client.list_projects(client_id=client_id)
    if content is None:
        raise error
    return _to_project_dataframe(content)


def _get_subpositions(client: Client, project_id: int, client_id: int) -> pd.DataFrame:
    content, error = client.list_calc_pos(client_id, project_id)
    if content is None:
        raise error

    df = pd.DataFrame([pd.Series(r) for r in content])

    df[PROJECT_ID] = df.Project.apply(lambda p: p[TROI_PROJECT_ID])
    df[SUBPROJECT_ID] = df.Subproject.apply(lambda p: p[TROI_SUBPROJECT_ID])
    df[SUBPROJECT_NAME] = df.Subproject.apply(lambda p: p[TROI_SUBPROJECT_NAME])
    df = df.rename(columns={TROI_SUBPOSITION_ID: SUBPOSITION_ID, TROI_SUBPOSITION_NAME: SUBPOSITION_NAME})
    return df.loc[:, [PROJECT_ID, SUBPROJECT_ID, SUBPROJECT_NAME, SUBPOSITION_ID, SUBPOSITION_NAME]]


def get_all_positions(client: Client, client_id: int, project_id: Optional[int] = None) -> pd.DataFrame:
    subpositions = []
    if project_id:
        projects = get_project(client, project_id=project_id)
        subpositions.append(_get_subpositions(client, project_id=project_id, client_id=client_id))
    else:
        # Load all projects
        projects = get_projects(client, client_id=client_id)
        for _, project in projects.iterrows():
            subpositions.append(_get_subpositions(client, project_id=project[PROJECT_ID], client_id=client_id))

    project_subpositions = pd.concat(subpositions)
    projects = projects.merge(project_subpositions, on=PROJECT_ID)
    return projects


class ProjectState(Enum):
    closed = "abgeschlossen"
    open = "in Arbeit"
