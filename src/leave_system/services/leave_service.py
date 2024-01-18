import datetime
from dataclasses import dataclass

from pydantic import BaseModel
from sqlmodel import select

from leave_system.db import Database
from leave_system.models import LeaveRequest


class LeaveRequestCreateParam(BaseModel):
    date: datetime.date
    reason: str


@dataclass
class LeaveRequestService:
    db: Database

    def add_leave_request(self, user_id: int, date: datetime.date, reason: str) -> LeaveRequest:
        with self.db.session() as session:
            request = LeaveRequest(
                user_id=user_id,
                date=date,
                reason=reason,
            )
            session.add(request)
            session.commit()
            return request

    def get_all_leave_requests(self) -> list[LeaveRequest]:
        with self.db.session() as session:
            query = select(LeaveRequest)
            rows = session.exec(query).all()
            return [r for r in rows]

    def get_own_leave_requests(self, user_id: int) -> list[LeaveRequest]:
        with self.db.session() as session:
            rows = session.exec(select(LeaveRequest).where(LeaveRequest.user_id == user_id)).all()
            ret = [r for r in rows]
        return ret
