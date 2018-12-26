from os import environ
from typing import List
from cherrypy import expose, quickstart, config
from jinja2 import Environment, PackageLoader
import itertools

from ..database import Database
from ..models import *


class Web:
    def __init__(self) -> None:
        self.index_template = Environment(loader=PackageLoader('app.web', '')).get_template('index.html')
        self.db = Database()

    def __get_marks__(self) -> List[tuple]:
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT
                "users"."id",
                "problems"."group",
                0.12 * AVG(COALESCE("submissions"."score", 0))
            FROM
                "problems"
            LEFT JOIN
                "users"
            LEFT JOIN
                "submissions"
            ON
                "submissions"."problem_id" = "problems"."id"
            AND
                "submissions"."user_id" = "users"."id"
            GROUP BY
                "users"."id",
                "problems"."group"
        ''')
        return cursor.fetchall()

    @expose
    def index(self) -> str:
        users = User.all(self.db)
        problems = {k: list(v) for k, v in itertools.groupby(Problem.all(self.db), lambda p: p.group)}
        groups = list(problems.keys())
        submissions = {(s.user_id, s.problem_id): (s.id, s.score) for s in Submission.all(self.db)}
        marks = {(m[0], m[1]): m[2] for m in self.__get_marks__()}
        params = {'groups': groups, 'problems': problems, 'users': users, 'submissions': submissions, 'marks': marks}
        return self.index_template.render(params)

    def start(self) -> None:
        config.update({'server.socket_host': environ['WEB_HOST'], 'server.socket_port': int(environ['WEB_PORT'])})
        quickstart(self)
