from typing import Optional, List
from dataclasses import dataclass
import requests

from ..database import Database
from ..models import *
from . import resources

EOLYMP_URL = 'https://www.e-olymp.com/ru/submissions/%s'


class EOlimpParser:
    def __init__(self, submission_id: int, user: User, db: Database):
        self.submission_id = submission_id
        self.user = user
        self.db = db
        self.errors = []
        self.score = None
        self.problem_id = None
        self.username = None
        self.fetched = False

    def __fetch_json__(self) -> None:
        response = requests.get(EOLYMP_URL % self.submission_id, headers={
                                'X-Requested-With': 'XMLHttpRequest'})
        if not response.ok:
            return
        json = response.json()
        self.score = int(round(json['report']['accepted'] * 100.0))
        self.problem_id = json['problem']['id']
        self.username = json['user']['username'].casefold()
        self.fetched = True

    def __validate__(self) -> None:
        self.errors.clear()
        if not self.fetched:
            self.errors.append(resources.CREATE_SUBMISSION_ERROR_CANNOT_FETCH)
        elif Problem.find(self.db, self.problem_id) is None:
            self.errors.append(
                resources.CREATE_SUBMISSION_ERROR_PROBLEM_NOT_FOUND % self.problem_id)
        elif self.user.username != self.username:
            self.errors.append(resources.CREATE_SUBMISSION_ERROR_USERNAME_INVALID % (
                self.user.username, self.username))
        elif Submission.find(self.db, self.submission_id) is not None:
            self.errors.append(
                resources.CREATE_SUBMISSION_ERROR_SUBMISSION_EXISTS % self.submission_id)

    def execute(self) -> None:
        self.__fetch_json__()
        self.__validate__()

    def create_submission(self) -> Submission:
        return Submission.create(self.db, self.submission_id, self.user.id, self.problem_id, self.score)
