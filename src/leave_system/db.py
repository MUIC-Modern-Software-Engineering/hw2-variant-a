import abc
import contextlib
from collections.abc import Iterator
from dataclasses import dataclass

import bcrypt
from sqlalchemy import Engine, create_engine
from sqlmodel import Session, select

from leave_system import models


class Database(abc.ABC):

    def engine(self) -> Engine:
        raise NotImplementedError()

    @contextlib.contextmanager
    def session(self) -> Iterator[Session]:
        yield Session(self.engine())

    def create_all_table(self) -> None:
        """Create all tables in the database."""
        models.SQLModel.metadata.create_all(self.engine())

    def create_user_if_not_empty(self) -> None:
        """
        Create two initial users if there are no users in the database.
        """
        with self.session() as session:
            if session.exec(select(models.User)).first() is None:
                session.add(models.User(
                    username='admin',
                    password=bcrypt.hashpw('password'.encode('utf8'), bcrypt.gensalt())
                ))
                session.add(models.User(
                    username='nonadmin',
                    password=bcrypt.hashpw('password'.encode('utf8'), bcrypt.gensalt())
                ))
                session.commit()


@dataclass
class SQLite(Database):
    path: str
    _engine: Engine = None

    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = create_engine(f'sqlite:///{self.path}')
        return self._engine

    @classmethod
    def in_memory(cls):
        return cls(path='')
