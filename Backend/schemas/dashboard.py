from pydantic import BaseModel

from schemas.expense_split import ExpenseResponse
from schemas.groups import GroupResponse
from schemas.user import UserResponse


class GroupDashBoardResponse(BaseModel):
    group: GroupResponse
    expense: list[ExpenseResponse]


class DashBoard(BaseModel):
    user: UserResponse
    groups: list[GroupDashBoardResponse]
