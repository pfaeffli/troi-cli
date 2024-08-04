import pandas as pd

from troi.client.api import Client

TROI_PROJECTNAME = "Name"

TROI_PROJECTID = "Id"

PROJECTSTATE = "project_state"


def _get_projects(client: Client) -> pd.DataFrame:
    content, error = client.list_projects(client_id=3)

    df = pd.DataFrame([pd.Series(r) for r in content])
    df[PROJECTSTATE] = df.Status.apply(lambda s: s[TROI_PROJECTNAME])
    df.head(1)
    projects = df.loc[:, [TROI_PROJECTID, TROI_PROJECTNAME, PROJECTSTATE]]
    return projects.loc[projects.Projectstate != "abgeschlossen", :].rename(columns={TROI_PROJECTID: "ProjectId"})


def _get_subpositions(client: Client, project: pd.Series) -> pd.DataFrame:
    content, exception = client.list_calc_pos(3, project["Id"])
    df = pd.DataFrame([pd.Series(r) for r in content])

    df["ProjectId"] = df.Project.apply(lambda p: p["Id"])
    df["SubprojectId"] = df.Subproject.apply(lambda p: p["Id"])
    df["SubprojectName"] = df.Subproject.apply(lambda p: p["Name"])
    return df.loc[:, ["ProjectId", "SubprojectId", "SubprojectName", "Id", "Name"]].rename(
        columns={"Id": "PositionId", "Name": "PositionName"})


def get_all_positions(client: Client) -> pd.DataFrame:
    projects = _get_projects(client)
    subpositions = []
    for _, project in projects.iterrows():
        subpositions.append(_get_subpositions(client, project))

    project_subpositions = pd.concat(subpositions)
    projects = projects.merge(project_subpositions, on="ProjectId")
    return projects
