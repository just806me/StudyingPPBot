from os import environ
from cherrypy import expose, quickstart, config
from jinja2 import Environment, PackageLoader
from ..database import Database
from ..models import *


class Web:
    def __init__(self) -> None:
        self.index_template = Environment(loader=PackageLoader(
            'app.web', '')).get_template('index.html')
        self.db = Database()

    @expose
    def index(self) -> str:
        users = User.all(self.db)

        problems = Problem.all(self.db)
        p = dict()
        g = set()
        for problem in problems:
            if problem.group in p:
                p[problem.group].append(problem.id)
            else:
                p[problem.group] = [problem.id]
            g.add(problem.group)

        submissions = Submission.all(self.db)
        s = dict()
        for submission in submissions:
            s[(submission.user_id, submission.problem_id)] = (
                submission.id, submission.score)

        return self.index_template.render(groups=g, problems=p, users=users, submissions=s)

    def start(self) -> None:
        config.update({'server.socket_host': environ['WEB_HOST'], 'server.socket_port': int(
            environ['WEB_PORT'])})
        quickstart(self)
