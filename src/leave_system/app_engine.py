from dataclasses import dataclass
from os.path import join, dirname
from typing import Annotated

from fastapi import Depends
from starlette.templating import Jinja2Templates

from leave_system.db import Database, SQLite
from leave_system.services.leave_service import LeaveRequestService


@dataclass
class LeaveSystemEngine:
    database: Database
    templates: Jinja2Templates
    leave_request_service: LeaveRequestService

    @classmethod
    def with_db(cls, db: Database):
        return cls(
            database=db,
            templates=Jinja2Templates(directory=join(dirname(__file__), "templates")),
            leave_request_service=LeaveRequestService(db)
        )


def get_leave_system_engine() -> LeaveSystemEngine:
    return LeaveSystemEngine.with_db(SQLite(path="hello.db"))


LeaveSystemEngineDep = Annotated[LeaveSystemEngine, Depends(get_leave_system_engine)]
