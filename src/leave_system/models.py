import datetime

from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str = Field()
    leave_requests: list["LeaveRequest"] = Relationship(back_populates="user",
                                                        sa_relationship_kwargs={"lazy": "selectin"})


class LeaveRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User = Relationship(back_populates="leave_requests", sa_relationship_kwargs={"lazy": "selectin"})
    date: datetime.date
    reason: str
