from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from ..database import Database


@dataclass
class Submission:
    id: int
    user_id: int
    problem_id: int
    score: float

    @staticmethod
    def create(db: Database, id: int, user_id: int, problem_id: int, score: float) -> Submission:
        cursor = db.cursor()
        cursor.execute('INSERT INTO "submissions" ("id", "user_id", "problem_id", "score") VALUES (?, ?, ?, ?)',
                       (id, user_id, problem_id, score))
        db.commit()
        return Submission(id, user_id, problem_id, score)

    @staticmethod
    def find(db: Database, id: int) -> Optional[Submission]:
        cursor = db.cursor()
        cursor.execute('SELECT "id", "user_id", "problem_id", "score" FROM "submissions" WHERE id = ?', (id,))
        values = cursor.fetchone()
        return None if values is None else Submission(*values)
