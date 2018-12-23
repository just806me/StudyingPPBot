from os import environ
from cherrypy import expose, quickstart, config
from jinja2 import Environment, PackageLoader
from ..database import Database
from ..models import *


class Web:
    def __init__(self) -> None:
        self.index_template = Environment(loader=PackageLoader('app.web', '')).get_template('index.html')
        self.db = Database()

    @expose
    def index(self) -> str:
        problems = Problem.all(self.db)
        users = User.all(self.db)
        submissions = Submission.all(self.db)
        return self.index_template.render(problems=problems, users=users, submissions=submissions)

    def start(self) -> None:
        config.update({'server.socket_host': environ['WEB_HOST'], 'server.socket_port': int(environ['WEB_PORT'])})
        quickstart(self)
