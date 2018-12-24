from os import environ
from cherrypy import expose, quickstart, config
from jinja2 import Environment, PackageLoader
import itertools

from ..database import Database
from ..models import *


class Web:
    def __init__(self) -> None:
        self.index_template = Environment(loader=PackageLoader('app.web', '')).get_template('index.html')
        self.db = Database()

    @expose
    def index(self) -> str:
        users = User.all(self.db)
        problems = {k: list(v) for k, v in itertools.groupby(Problem.all(self.db), lambda p: p.group)}
        groups = list(problems.keys())
        submissions = {(s.user_id, s.problem_id): (s.id, s.score) for s in Submission.all(self.db)}
        return self.index_template.render(groups=groups, problems=problems, users=users, submissions=submissions)

    def start(self) -> None:
        config.update({'server.socket_host': environ['WEB_HOST'], 'server.socket_port': int(environ['WEB_PORT'])})
        quickstart(self)
