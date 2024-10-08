from datetime import datetime
from typing import List, Optional, Tuple, Union

import requests
from requests.auth import HTTPBasicAuth


class Client:
    def __init__(self, url: str, username: str, api_token: str):
        self.base_url = url
        self.auth = HTTPBasicAuth(username, api_token)
        self.headers = {
            'User-Agent': 'curl/7.58.0',  # Adjust the version accordingly
        }

    def _request(self, method: str, endpoint: str, params: Optional[dict] = None,
                 json_payload: Optional[dict] = None) -> Tuple[Optional[Union[List[dict], dict]], Optional[Exception]]:
        url = self.base_url + endpoint
        try:
            response = requests.request(method, url, headers=self.headers, auth=self.auth, params=params,
                                        json=json_payload)
            response.raise_for_status()
            return response.json(), None
        except Exception as e:
            return None, e

    def list_projects(self, client_id: int) -> tuple[list[dict], Exception | None]:
        endpoint = "/projects"
        values = {"clientId": client_id}
        return self._request("GET", endpoint, params=values)

    def get_project(self, project_id: int) -> tuple[dict, Exception | None]:
        endpoint = f"/projects/{project_id}"
        return self._request("GET", endpoint)

    def list_calc_pos(self, client_id: int, project_id: int) -> tuple[list[dict], Exception | None]:
        endpoint = "/calculationPositions"
        values = {"clientId": client_id, "projectId": project_id}
        return self._request("GET", endpoint, params=values)

    def list_billing_hours(self, client_id: int, project_id: int, date_from: datetime, date_to: datetime) -> tuple[
        list[dict], Exception | None]:
        endpoint = "/billings/hours"
        values = {
            "clientId": client_id,
            "projectId": project_id,
            "startDate": date_from.strftime("%Y%m%d"),
            "endDate": date_to.strftime("%Y%m%d")}
        return self._request("GET", endpoint, params=values)

    def add_billing_hours(self, client_id: int, user_id: int, task_id: int, date: datetime, hours: float,
                          remark: str) -> Optional[Exception]:
        endpoint = "/billings/hours"
        data = create_billing_hour_payload(client_id, user_id, task_id, date, hours, remark)
        _, e = self._request("POST", endpoint, json_payload=data)
        return e

    def update_billing_hours(self, client_id: int, user_id: int, task_id: int, record_id: int, date: datetime,
                             hours: float, remark: str) -> Optional[Exception]:
        endpoint = f"/billings/hours/{record_id}"
        data = create_billing_hour_payload(client_id, user_id, task_id, date, hours, remark)
        _, e = self._request("PUT", endpoint, json_payload=data)
        return e


TROI_BILLING_HOUR_CALCULATION_POSITION = "CalculationPosition"
TROI_BILLING_HOUR_CALCULATION_POSITION_ID = "Id"
TROI_BILLING_HOUR_CALCULATION_POSITION_PATH = "Path"
TROI_CLIENT = "Client"
TROI_CLIENT_ID = "Id"
TROI_CLIENT_PATH = "Path"
TROI_BILLING_HOUR_RECORD_ID = "Id"
TROI_BILLING_HOUR_DISPLAY_PATH = "DisplayPath"
TROI_BILLING_HOUR_DATE = "Date"
TROI_BILLING_HOUR_EMPLOYEE = "Employee"
TROI_BILLING_HOUR_EMPLOYEE_ID = "Id"
TROI_BILLING_HOUR_EMPLOYEE_PATH = "Path"
TROI_BILLING_HOUR_QUANTITY = "Quantity"
TROI_BILLING_HOUR_REMARK = "Remark"


def create_billing_hour_payload(client_id: int, user_id: int, postion_id: int, date: datetime, hours: float,
                                remark: str) -> dict:
    billing_hour = {
        TROI_BILLING_HOUR_DATE: date.strftime("%Y-%m-%d"),
        TROI_BILLING_HOUR_QUANTITY: hours,
        TROI_BILLING_HOUR_REMARK: remark,
        TROI_BILLING_HOUR_EMPLOYEE: {
            TROI_BILLING_HOUR_EMPLOYEE_ID: user_id,
            TROI_BILLING_HOUR_EMPLOYEE_PATH: f"/employees/{user_id}"
        },
        TROI_BILLING_HOUR_CALCULATION_POSITION: {
            TROI_BILLING_HOUR_CALCULATION_POSITION_ID: postion_id,
            TROI_BILLING_HOUR_CALCULATION_POSITION_PATH: f"/calculationPositions/{postion_id}"
        },
        TROI_CLIENT: {
            TROI_CLIENT_ID: client_id,
            "Id1": client_id,
            TROI_CLIENT_PATH: f"/clients/{client_id}"
        }
    }
    return billing_hour
