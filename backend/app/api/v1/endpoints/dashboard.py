from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardSummary, MonthlyOrderCount, RoleCount
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_summary(db)


@router.get("/sales-by-month", response_model=list[MonthlyOrderCount])
def sales_by_month(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_sales_count_by_month(db)


@router.get("/users-by-role", response_model=list[RoleCount])
def users_by_role(
    db: Session = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return dashboard_service.get_users_by_role(db)
