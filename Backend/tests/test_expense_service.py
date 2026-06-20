import asyncio
import os
from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/test")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")

from services import expense_service


def test_get_expense_returns_expense_and_splits(monkeypatch):
    group_id = uuid4()
    expense_id = uuid4()
    current_user_id = uuid4()
    split_id = uuid4()

    expense = SimpleNamespace(
        id=expense_id,
        group_id=group_id,
        paid_by=current_user_id,
        title="Dinner",
        amount=Decimal("42.50"),
        split_type="equal",
        created_at=datetime.now(timezone.utc),
    )
    split = SimpleNamespace(
        id=split_id,
        expense_id=expense_id,
        user_id=current_user_id,
        amount=Decimal("42.50"),
    )

    class FakeExpenseRepository:
        def __init__(self, db):
            pass

        async def get_by_id(self, requested_expense_id):
            assert requested_expense_id == expense_id
            return expense

        async def get_splits(self, requested_expense_id):
            assert requested_expense_id == expense_id
            return [split]

    class FakeGroupMemberRepository:
        def __init__(self, db):
            pass

        async def is_member(self, requested_user_id, requested_group_id):
            assert requested_user_id == current_user_id
            assert requested_group_id == group_id
            return True

    monkeypatch.setattr(expense_service, "ExpenseRepository", FakeExpenseRepository)
    monkeypatch.setattr(
        expense_service, "GroupMemberRepository", FakeGroupMemberRepository
    )

    response = asyncio.run(
        expense_service.get_expense(expense_id, group_id, current_user_id, db=object())
    )

    assert response.message == "Expense fetched successfully"
    assert response.data["expense"].id == expense_id
    assert response.data["expense"].title == "Dinner"
    assert len(response.data["splits"]) == 1
    assert response.data["splits"][0].id == split_id
