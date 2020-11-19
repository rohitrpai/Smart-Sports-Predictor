from flask_injector import request
from injector import singleton
from Flask_APIS.Database import DatabaseBase, MySqlDatabase
from Flask_APIS.Service import MyService
def configure(binder):
    binder.bind(MyService, to=MyService, scope=request)
    binder.bind(DatabaseBase, to=MySqlDatabase, scope=request)