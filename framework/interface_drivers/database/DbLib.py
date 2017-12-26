import cx_Oracle


class Oracle(object):
    def __init__(self, connection_model):
        """
        :param connection_model: object of DbConnectionModel
        :type connection_model: DbConnectionModel
        """
        connection_model = '{user}/{password}@{host}:{port}/{sid}'.format(user=connection_model.user,
                                                                          password=connection_model.password,
                                                                          host=connection_model.host,
                                                                          port=connection_model.port,
                                                                          sid=connection_model.sid)
        try:
            self.connect = cx_Oracle.connect(connection_model)
            self.cursor = self.connect.cursor()
        except Exception as e:
            raise e

    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
        except Exception as e:
            raise e

    def select(self, query):
        """
        execute query to db, results will be saved in self.cursor
        :param query: query that should be executed
        :return: Dict of query results
        """
        try:
            self.cursor.fetchall()
        except Exception:
            pass
        self.cursor.execute(query)
        return self.rows_to_dict_list()

    def execute_command(self, query):
        """
        execute query to db, and commit changes
        :param query: query that should be executed
        """
        self.cursor.execute(query)
        self.connect.commit()
        return self

    def rows_to_dict_list(self):
        columns = [str(i[0]).lower() for i in self.cursor.description]
        return [dict(zip(columns, row)) for loop, row in enumerate(self.cursor)]
