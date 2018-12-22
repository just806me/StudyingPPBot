from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from ..database import Database


@dataclass
class Problem:
    id: int
    group: int

    @staticmethod
    def create(db: Database, id: int, group: int) -> Problem:
        cursor = db.cursor()
        cursor.execute('INSERT INTO "problems" ("id", "group") VALUES (?, ?)', (id, group))
        db.commit()
        return Problem(id, group)

    @staticmethod
    def find(db: Database, id: int) -> Optional[Problem]:
        cursor = db.cursor()
        cursor.execute('SELECT "id", "group" FROM "problems" WHERE "id" = ?', (id,))
        values = cursor.fetchone()
        return None if values is None else Problem(*values)
