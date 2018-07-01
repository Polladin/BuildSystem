
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
        self.cursor.execute("""SELECT * from group_repo where gr_hash='""" + gr_hash + "'")
        rows = self.cursor.fetchall()

        if not rows:
            return None

        if len(rows) != 1:
            raise RuntimeError('ERROR! : More than 1 rows for that commit.')

        # Return [branch_name, nexus_num]
        return [rows[0][1], rows[0][2]]

    def exec_sql_with_commit(self, sql_request):

        try:
            # Execute query
            self.cursor.execute(sql_request)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def create_module_tables(self, modules):

        # Create tables
        for _module in modules:

            # SQL request
            sql_request = 'CREATE TABLE ' + _module + '(' + \
                          '  gr_hash        CHAR(40)    REFERENCES group_repo (gr_hash) PRIMARY KEY NOT NULL, ' + \
                          '  module_hash    CHAR(40)    NOT NULL, ' + \
                          '  branch_name    TEXT        NOT NULL, ' + \
                          '  nexus_num      INT         NOT NULL  ' + \
                          ');'

            self.exec_sql_with_commit(sql_request)

            print('Table created :', _module)

    def create_group_table(self):

        # SQL request
        sql_request = 'CREATE TABLE ' + 'group_repo' + '(' + \
                      '  gr_hash        CHAR(40)    PRIMARY KEY NOT NULL, ' + \
                      '  branch_name    TEXT        NOT NULL, ' + \
                      '  nexus_num      INT         NOT NULL  ' + \
                      ');'

        self.exec_sql_with_commit(sql_request)

        print('Table created : group_repo')

    def drop_tables(self, modules):

        for _module in modules:

            # SQL request
            sql_request = 'DROP TABLE IF EXISTS ' + _module + ';'

            self.exec_sql_with_commit(sql_request)

            print('Dropped table :', _module)

    def allocate_nexus_place(self, module_name, branch_name):

        # Sequence name
        sequence_name = module_name + '_' + branch_name

        # Is sequence already exist for a branch
        if not self._is_sequence_exist(sequence_name):
            self._create_sequence(sequence_name)

        return self._sequence_get_next_val(sequence_name)

    def add_module_build(self, module_name, module_info, group_hash):
        """
        :param module_info: in format {'hash_commit' : ..., 'branch_name': ..., 'nexus_place': ...}
        """

        # SQL request
        sql_request = "INSERT INTO " + module_name + " values ( '" + group_hash + "', " + \
                                                               "'" + module_info['hash_commit'] + "', " + \
                                                               "'" + module_info['branch_name'] + "', " + \
                                                                     str(module_info['nexus_place']) + ");"
        print(sql_request)
        self.exec_sql_with_commit(sql_request)

    def add_group_build(self, module_info):
        """
        :param module_info: in format {'hash_commit' : ..., 'branch_name': ..., 'nexus_place': ...}
        """

        # SQL request
        sql_request = "INSERT INTO group_repo values ( '" + module_info['hash_commit'] + "', " + \
                                                      "'" + module_info['branch_name'] + "', " + \
                                                            str(module_info['nexus_place']) + ");"
        print(sql_request)
        self.exec_sql_with_commit(sql_request)

    def get_modules_info_by_group_commit(self, group_commit, modules):
        """
        :return: {'module_name': (hash, branch_name, nexus_place), ...}
        """


        # Initialize result
        modules_info = {}

        for _module in modules:

            sql_request = "SELECT * from " + _module + " where gr_hash = '" + group_commit + "';"

            self.cursor.execute(sql_request)
            rows = self.cursor.fetchall()

            if rows:
                modules_info[_module] = rows[0][1:]

        return modules_info

    def _is_sequence_exist(self, sequence_name):

        self.cursor.execute('SELECT sequence_name FROM information_schema.sequences;')

        rows = [_row[0] for _row in self.cursor.fetchall()]

        return sequence_name in rows

    def _create_sequence(self, sequence_name):

        sql_request = 'CREATE SEQUENCE ' + sequence_name + ' START 1'

        try:
            # Execute query
            self.cursor.execute(sql_request)
            self.conn.commit()
            print('Sequence created :', sequence_name)
        except Exception as e:
            raise RuntimeError('Do not able to create a SEQUENCE :', e)

    def _sequence_get_next_val(self, sequence_name):

        sql_request = 'SELECT nextval(\'' + sequence_name + '\');'

        self.cursor.execute(sql_request)
        rows = self.cursor.fetchall()

        if not rows:
            raise RuntimeError('SEQUENCE FAILURE : empty answer')

        return rows[0][0]


# db_conn = ConnectionDBPostgres(host='localhost', db_name='DB_1', user='postgres', password='123')
# print(db_conn.sequence_get_next_val('seq_branch_name'))
# db_conn.create_table('common_lib')
# db_conn.is_sequence_exist('seq_branchA_name')

