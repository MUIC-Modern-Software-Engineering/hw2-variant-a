# In this file, you will see that testing sometimes require
# dark magic to make sure that the test is isolated
# from each other and from other environment (ex prod).
from datetime import date

import pytest
from sqlmodel import select
from starlette.testclient import TestClient

from leave_system import models
from leave_system.app import app
from leave_system.app_engine import LeaveSystemEngine, get_leave_system_engine
from leave_system.db import SQLite


def create_test_lse() -> LeaveSystemEngine:
    lse = LeaveSystemEngine.with_db(SQLite.in_memory())
    lse.database.create_all_table()
    lse.database.create_user_if_not_empty()
    return lse


@pytest.fixture(scope='function')
def lse():
    return create_test_lse()


@pytest.fixture(scope='function')
def client(lse: LeaveSystemEngine) -> TestClient:
    app.dependency_overrides[get_leave_system_engine] = create_test_lse
    return TestClient(app)


class TestEngine:
    def test_add_leave_request(self, lse: LeaveSystemEngine):
        # this way we can test engine separately from http call stack
        lse.leave_request_service.add_leave_request(1, date(2020, 8, 1), 'reason')
        assert len(lse.leave_request_service.get_all_leave_requests()) == 1

    def test_add_another_leave_request(self, lse: LeaveSystemEngine):
        # this is to show that all we did is to isolate test
        # you get a fresh db everytime
        lse.leave_request_service.add_leave_request(1, date(2020, 8, 2), 'reason2')
        assert len(lse.leave_request_service.get_all_leave_requests()) == 1  # this is still 1 not 2

    def test_there_are_2_users(self, lse: LeaveSystemEngine):
        with lse.database.session() as session:
            assert len(session.exec(select(models.User)).all()) == 2


class TestApp:
    def test_auth(self, client: TestClient):
        response = client.get('/', auth=('admin', 'password'))

        assert response.status_code == 200
        assert b'Leave System' in response.content

    def test_bad_auth(self, client):
        response = client.get('/', auth=('admin', 'wrong_password'))
        assert response.status_code == 401
