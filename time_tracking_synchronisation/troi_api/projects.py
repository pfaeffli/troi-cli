from enum import Enum

import pandas as pd

from time_tracking_synchronisation.troi_api.api import Client

TROI_PROJECT_NAME = "Name"
TROI_PROJECT_STATE_NAME = "Name"
TROI_PROJECT_ID = "Id"
TROI_SUBPROJECT_ID = "Id"
TROI_SUBPROJECT_NAME = "Name"
TROI_SUBPOSITION_ID = "Id"
TROI_SUBPOSITION_NAME = "Name"

PROJECT_ID = "project_id"
PROJECT_NAME = "project_name"
PROJECT_STATE = "project_state"
SUBPROJECT_ID = "subproject_id"
SUBPROJECT_NAME = "subproject_name"
SUBPOSITION_ID = "subposition_id"
SUBPOSITION_NAME = "subposition_name"


def _get_projects(client: Client) -> pd.DataFrame:
    content, error = client.list_projects(client_id=3)

    df = pd.DataFrame([pd.Series(r) for r in content])
    df[PROJECT_STATE] = df.Status.apply(lambda s: s[TROI_PROJECT_STATE_NAME])
    df.head(1)
    projects = df.loc[:, [TROI_PROJECT_ID, TROI_PROJECT_NAME, PROJECT_STATE]]
    return projects.loc[projects.loc[:, PROJECT_STATE] != ProjectState.closed.value, :].rename(columns={
        TROI_PROJECT_ID: PROJECT_ID,
        TROI_PROJECT_NAME: PROJECT_NAME,
    })


def _get_subpositions(client: Client, project: pd.Series) -> pd.DataFrame:
    content, exception = client.list_calc_pos(3, project[PROJECT_ID])
    df = pd.DataFrame([pd.Series(r) for r in content])

    df[PROJECT_ID] = df.Project.apply(lambda p: p[TROI_PROJECT_ID])
    df[SUBPROJECT_ID] = df.Subproject.apply(lambda p: p[TROI_SUBPROJECT_ID])
    df[SUBPROJECT_NAME] = df.Subproject.apply(lambda p: p[TROI_SUBPROJECT_NAME])
    df = df.rename(columns={TROI_SUBPOSITION_ID: SUBPOSITION_ID, TROI_SUBPOSITION_NAME: SUBPOSITION_NAME})
    return df.loc[:, [PROJECT_ID, SUBPROJECT_ID, SUBPROJECT_NAME, SUBPOSITION_ID, SUBPOSITION_NAME]]


def get_all_positions(client: Client) -> pd.DataFrame:
    projects = _get_projects(client)
    subpositions = []
    for _, project in projects.iterrows():
        subpositions.append(_get_subpositions(client, project))

    project_subpositions = pd.concat(subpositions)
    projects = projects.merge(project_subpositions, on=PROJECT_ID)
    return projects


class ProjectState(Enum):
    closed = "abgeschlossen"
    open = "in Arbeit"
