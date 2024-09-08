from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class Generic:
    data: dict


@dataclass
class Project:
    ExternalDescription: str
    Id: int
    InternalDescription: str
    Name: str
    Number: str
    Path: str
    ProjectFolderId: int
    ProjectTypes: List[Any]
    Team: Any
    Id1: int


@dataclass
class CalcPosEmbedded:
    ClassName: str
    ETag: Optional[Any]
    Id: int
    IsDeleted: bool
    IsFavorite: bool
    IsPrintable: bool
    Name: Optional[Any]
    ParentPath: str
    Path: str
    ReeCpId: int
    ReeDate: Optional[Any]
    ReeEmployeeId: int
    ReeProjectId: int
    ReeQuantity: int
    ReeServiceId: int
    ReeSubProjectId: int
    Type: str
    Id1: int


@dataclass
class CalculationPosition:
    AccountId: int
    CostCenterId: int
    DisplayPath: str
    ExternalDescription: str
    Id: int
    Name: str
    Path: str
    Id1: int


@dataclass
class BillingHour:
    ActualHours: int
    ClassName: str
    Date: str
    DisplayPath: str
    ETag: str
    Id: int
    IsApproved: bool
    IsBillable: bool
    IsBilled: bool
    IsDeleted: bool
    IsInvoiced: bool
    Path: str
    Quantity: float
    Remark: str
    DocumentComputedTotalNet: int
    Id1: int
    # Employee: Employee            # Needs to be defined
    # CalculationPosition: CalculationPosition  # Needs to be defined
    # Client: ClientType             # Needs to be defined


@dataclass
class BillingHourRequest:
    CalculationPositionID: int
    UserId: int
    Hours: int
    Date: str
    Description: str


@dataclass
class Employee:
    ClassName: str
    ETag: Optional[Any]
    Id: int
    IsDeleted: bool
    IsFavorite: bool
    IsPrintable: bool
    Name: Optional[Any]
    ParentPath: str
    Path: str
    ReeCpId: int
    ReeDate: Optional[Any]
    ReeEmployeeId: int
    ReeProjectId: int
    ReeQuantity: int
    ReeServiceId: int
    ReeSubProjectId: int
    Type: str
    Id1: int


@dataclass
class ClientType:
    Type: str
    Name: str
    IsFavorite: bool
    IsPrintable: bool
    ParentPath: Optional[Any]
    ReeEmployeeId: int
    ReeCpId: int
    ReeSubProjectId: int
    ReeProjectId: int
    ReeQuantity: int
    ReeDate: Optional[Any]
    ReeServiceId: int
    Id: int
    Id1: int
    Path: str
    ETag: str
    IsDeleted: bool
    ClassName: str
