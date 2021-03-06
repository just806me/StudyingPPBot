from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

from ..database import Database


@dataclass
class User:
    id: int
    name: str
    username: str
    deleted_at: Optional[int] = None

    @staticmethod
    def create(db: Database, id: int, name: str, username: str) -> User:
        cursor = db.cursor()
        cursor.execute('INSERT INTO "users" ("id", "name", "username") VALUES (?, ?, ?)', (id, name, username.casefold()))
        db.commit()
        return User(id, name, username)

    @staticmethod
    def find(db: Database, id: int, with_deleted: bool = False) -> Optional[User]:
        sql = 'SELECT "id", "name", "username", "deleted_at" FROM "users" WHERE "id" = ?'
        if not with_deleted:
            sql += ' AND "deleted_at" IS NULL'
        cursor = db.cursor()
        cursor.execute(sql, (id,))
        values = cursor.fetchone()
        return None if values is None else User(*values)

    @staticmethod
    def all(db: Database, with_deleted: bool = False) -> List[User]:
        sql = 'SELECT "id", "name", "username", "deleted_at" FROM "users"'
        if not with_deleted:
            sql += ' WHERE "deleted_at" IS NULL'
        cursor = db.cursor()
        cursor.execute(sql)
        return [User(*values) for values in cursor.fetchall()]
