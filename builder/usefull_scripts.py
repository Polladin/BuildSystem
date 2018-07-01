
import json

from build_system.builder.connect_db_postgress import ConnectionDBPostgres


class InitializeDB:

    def __init__(self):

        self.db_conn = ConnectionDBPostgres(host='localhost', db_name='DB_1', user='postgres', password='123')
        self.modules = [_module.strip() for _module in open('storage/modules.txt').readline().strip().split(',')]

    def create_module_tables(self):

        # Create tables
        self.db_conn.create_group_table()
        self.db_conn.create_module_tables(self.modules)

    def drop_module_tables(self):

        # Create tables
        repos = self.modules
        repos.append('group_repo')
        self.db_conn.drop_tables(repos)


# Create module tables
InitializeDB().create_module_tables()
# InitializeDB().drop_module_tables()
