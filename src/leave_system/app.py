from __future__ import annotations

import datetime
from typing import Annotated, List

from fastapi import FastAPI, Request, Form
from starlette.templating import _TemplateResponse

from leave_system.app_engine import LeaveSystemEngine, get_leave_system_engine, LeaveSystemEngineDep
from leave_system.models import LeaveRequest
from leave_system.services.auth import UserSessionDep, UserSession

app = FastAPI()


@app.on_event("startup")
def create_all():
    leave_system_engine = app.dependency_overrides.get(get_leave_system_engine, get_leave_system_engine)()
    leave_system_engine.database.create_all_table()
    leave_system_engine.database.create_user_if_not_empty()


@app.get("/")
def index(request: Request, user: UserSessionDep, lse: LeaveSystemEngineDep):
    return render_page(request, user, lse)


@app.post("/add_leave")
def add_leave(request: Request, user: UserSessionDep, lse: LeaveSystemEngineDep,
              date: Annotated[datetime.date, Form()], reason: Annotated[str, Form()]):
    lse.leave_request_service.add_leave_request(user.user_id, date, reason)
    return render_page(request, user, lse)


def render_page(request: Request, user: UserSession, lse: LeaveSystemEngine) -> _TemplateResponse:
    service = lse.leave_request_service
    all_leave_requests: List[LeaveRequest] = service.get_all_leave_requests()
    my_leave_requests: List[LeaveRequest] = service.get_own_leave_requests(user.user_id)
    return lse.templates.TemplateResponse(request, "leave_request.jinja2",
                                          context=dict(
                                              all_leave_requests=all_leave_requests,
                                              my_leave_requests=my_leave_requests
                                          ))
