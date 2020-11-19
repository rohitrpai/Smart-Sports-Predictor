from injector import inject
from Flask_APIS.Database import DatabaseBase
class MyService:
    @inject
    def __init__(self, db: DatabaseBase):
        print(f"DatabaseBase instance is {db}")
        self.db = db
    def get_data(self):
        return self.db.get()
    def get_db_cursor(self):
        return self.db.setup_cursor()
    def get_sql_instance(self):
        return self.db.setup_sql_instance()