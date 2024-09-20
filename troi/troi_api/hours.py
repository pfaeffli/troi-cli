from datetime import datetime
from typing import Optional, List

import pandas as pd

import troi.troi_api.api as constants
import troi.troi_api.projects as proj_constants
from troi.troi_api.api import Client

BILLING_HOUR_RECORD_ID = "record_id"
BILLING_HOUR_DISPLAY_PATH = "display_path"
BILLING_HOUR_EMPLOYEE_ID = "user_id"
BILLING_HOUR_DATE = "billing_date"
BILLING_HOUR_QUANTITY = "quantity"
BILLING_HOUR_TAGS = "tags"
BILLING_HOUR_ANNOTATION = "annotation"


def get_billing_hours(
        client: Client,
        project_id: int,
        date_from: datetime,
        date_to: Optional[datetime] = None,
        client_id: int = None,
        user_id: Optional[int] = None,
        position_id: Optional[int] = None,
) -> pd.DataFrame:
    content, error = client.list_billing_hours(
        client_id=client_id,
        project_id=project_id,
        date_from=date_from,
        date_to=date_to if date_to else datetime.now(),
    )
    if content is None:
        raise error

    df = pd.DataFrame([pd.Series(r) for r in content])
    if df.empty:
        return df

    df[proj_constants.SUBPOSITION_ID] = df[constants.TROI_BILLING_HOUR_CALCULATION_POSITION].apply(lambda x: x[
        constants.TROI_BILLING_HOUR_CALCULATION_POSITION_ID])

    df[BILLING_HOUR_RECORD_ID] = df[constants.TROI_BILLING_HOUR_RECORD_ID]
    df[BILLING_HOUR_DISPLAY_PATH] = df[constants.TROI_BILLING_HOUR_DISPLAY_PATH]
    df[BILLING_HOUR_EMPLOYEE_ID] = df[constants.TROI_BILLING_HOUR_EMPLOYEE].apply(
        lambda x: x[constants.TROI_BILLING_HOUR_EMPLOYEE_ID])
    df[BILLING_HOUR_DATE] = pd.to_datetime(df[constants.TROI_BILLING_HOUR_DATE])
    df[BILLING_HOUR_QUANTITY] = df[constants.TROI_BILLING_HOUR_QUANTITY]
    tags_annotation = df[constants.TROI_BILLING_HOUR_REMARK].apply(
        lambda x: str(x).split('@', maxsplit=1) if x is not None else ("", ""))
    df[BILLING_HOUR_TAGS] = tags_annotation.apply(lambda x: str(x[0]).strip() if x is not None else "")
    df[BILLING_HOUR_ANNOTATION] = tags_annotation.apply(lambda x: x[1] if len(x) > 1 else "")
    reduced_df = df.loc[:,
                 [BILLING_HOUR_RECORD_ID, BILLING_HOUR_DISPLAY_PATH, proj_constants.SUBPOSITION_ID,
                  BILLING_HOUR_EMPLOYEE_ID, BILLING_HOUR_DATE, BILLING_HOUR_QUANTITY,
                  BILLING_HOUR_TAGS, BILLING_HOUR_ANNOTATION]]
    filter_cond = [True] * reduced_df.shape[0]
    if user_id:
        filter_cond = filter_cond & (reduced_df[BILLING_HOUR_EMPLOYEE_ID] == user_id)
    if position_id:
        filter_cond = filter_cond & (reduced_df[proj_constants.SUBPOSITION_ID] == position_id)
    return reduced_df.loc[filter_cond, :]


def get_remark(tags: List[str] = None,
               annotation: str = None):
    remark = ""
    if tags:
        remark += ", ".join(tags)

    if annotation:
        if len(remark) > 0:
            remark += " "
        remark += f"@{annotation}"
    return remark


def add_billing_entry(
        client: Client,
        task_id: int,
        date: datetime,
        hours: float,
        user_id: int,
        tags: List[str] = None,
        annotation: str = None,
        client_id: int = 3,
):
    error = client.add_billing_hours(client_id=client_id,
                                     user_id=user_id,
                                     task_id=task_id,
                                     date=date,
                                     hours=hours,
                                     remark=get_remark(tags, annotation))
    if error is not None:
        raise error


def update_billing_entry(
        client: Client,
        client_id: int,
        record_id: int,
        date: datetime,
        hours: float,
        user_id: int,
        task_id: int,
        tags: List[str] = None,
        annotation: str = None,
):
    error = client.update_billing_hours(
        client_id=client_id,
        user_id=user_id,
        task_id=task_id,
        record_id=record_id,
        date=date,
        hours=hours,
        remark=get_remark(tags, annotation))
    if error is not None:
        raise error
