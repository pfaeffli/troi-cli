from datetime import datetime


def create_billing_hour_payload(client_id: int, user_id: int, task_id: int, date: datetime, hours: float,
                                remark: str) -> dict:
    billing_hour = {
        "Date": date.strftime("%Y-%m-%d"),
        "Quantity": hours,
        "Remark": remark,
        "Employee": {
            "Id": user_id,
            "Path": f"/employees/{user_id}"
        },
        "CalculationPosition": {
            "Id": task_id,
            "Path": f"/calculationPositions/{task_id}"
        },
        "Client": {
            "Id": client_id,
            "Id1": client_id,
            "Path": f"/clients/{client_id}"
        }
    }
    return billing_hour
