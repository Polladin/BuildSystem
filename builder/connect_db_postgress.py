
import psycopg2


class ConnectionDBPostgres:

    def __init__(self, host, db_name, user, password):

        # Create connection string
        connect_str = 'dbname=' + db_name + \
                      ' user=' + user + \
                      ' host=' + host + \
                      ' password=' + password

        try:
            # Connect to DB
            self.conn = psycopg2.connect(connect_str)

            # Create a psycopg2 cursor that can execute queries
            self.cursor = self.conn.cursor()

        except Exception as e:
            print('Connection to DB:' + db_name + ' failed.')
            print(e)
            raise RuntimeError()

    def is_group_built(self, gr_hash):

        # Select from DB
        self.cursor.execute("""SELECT * from group_repo where id='""" + gr_hash + "'")
        rows = self.cursor.fetchall()

        print(rows)

        if not rows:
            return None
        else:
            if len(rows) != 1:
                raise RuntimeError('ERROR! : More than 1 rows for that commit.')
            # Return [branch_name, nexus_num]
            return [rows[0][1], rows[0][2]]

    def get_

    def create_table(self, new_module_name):

        # SQL request
        sql_request = 'CREATE TABLE ' + new_module_name + '(' + \
                      '  gr_hash        CHAR(40)    REFERENCES group_repo (id) PRIMARY KEY NOT NULL, ' + \
                      '  branch_name    TEXT        NOT NULL, ' + \
                      '  nexus_num      INT         NOT NULL  ' + \
                      ');'

        try:
            # Execute query
            self.cursor.execute(sql_request)
            self.conn.commit()
            print('Table Created')
        except Exception as e:
            print(e)


db_conn = ConnectionDBPostgres(host='localhost', db_name='DB_1', user='postgres', password='123')
db_conn.create_table('common_lib')
