import mysql.connector

COLUMN_NAME_INDEX = 0
USER = 'root'
DATABASE = 'nmurad2db'

class SQL():
    @staticmethod
    def query(q):
        # init
        cnx, cursor = SQLTable.init_connection()

        # process
        result = []
        cursor.execute(q)
        for row in cursor:
            result.append(row)

        # clean up
        SQLTable.close_connection(cnx, cursor)

        return result

    @staticmethod
    def parameterized_query(q,parameters):
        # init
        cnx, cursor = SQLTable.init_connection()

        # process
        result = []
        cursor.execute(q,parameters)
        for row in cursor:
            result.append(row)

        # clean up
        SQLTable.close_connection(cnx, cursor)

        return result

    @staticmethod
    def command(c):
        # init
        cnx, cursor = SQLTable.init_connection()

        # execute
        cursor.execute(c)
        cnx.commit()

        # clean up
        SQLTable.close_connection(cnx, cursor)

    @staticmethod
    def init_connection():
        cnx = mysql.connector.connect(user=USER, database=DATABASE)
        cursor = cnx.cursor()
        return (cnx, cursor)

    @staticmethod
    def close_connection(cnx, cursor):
        cnx.close()
        cursor.close()


class SQLTable(SQL):

    def __init__(self, table_name, eoss = ''):
       self.table_name = table_name
       self.end_of_select_statement = eoss

    def query_all(self, end_of_statement=""):
        # init
        cnx, cursor = self.init_connection()
        query = ('SELECT * FROM ' + self.table_name + ' ' + self.end_of_select_statement)
        print("EXECUTING COMMAND: " + query)

        # process
        result = [tuple(self.fields())]
        cursor.execute(query)
        for row in cursor:
            result.append(row)

        # clean up
        self.close_connection(cnx, cursor)

        return result

    def insert(self, values):
        # init
        cnx, cursor = self.init_connection()
        values = self.comma_separate(values)
        command = ("INSERT INTO " + self.table_name +
                 " VALUES(" + values + ")")

        print("EXECUTING COMMAND: " + command)
        cursor.execute(command)

        cnx.commit()

        # clean up
        self.close_connection(cnx, cursor)

    def remove(self, value):
        # init
        cnx, cursor = self.init_connection()
        command = ("DELETE FROM " + self.table_name + " WHERE " + self.table_name + "_id = " + "\'" + value + "\'") 

        print("EXECUTING COMMAND: " + command)
        cursor.execute(command)

        cnx.commit()

        # clean up
        self.close_connection(cnx, cursor)

    def modify(self, pk, values):
        # init
        cnx, cursor = self.init_connection()
        command = ("UPDATE " + self.table_name + " SET " + self.set_statement(values) + " WHERE " + self.table_name + "_id = " + "\'" + pk + "\'")

        print("EXECUTING COMMAND: " + command)
        cursor.execute(command)

        cnx.commit()

        # clean up
        self.close_connection(cnx, cursor)

    def fields(self):
        # init
        cnx, cursor = self.init_connection()
        query = ('SHOW COLUMNS FROM ' + self.table_name)

        # process
        result = []
        cursor.execute(query)
        for row in cursor:
            result.append(row[COLUMN_NAME_INDEX])

        # clean up
        self.close_connection(cnx, cursor)

        return result

    # UTILS

    @staticmethod 
    def comma_separate(values):
        result = ""
        for value in values:
            result +="\'" + value + "\'" + ","
        return result[:-1]

    def equality_condition(self,values):
        result = ""
        for field, value in zip(self.fields(), values):
            if value != "":
                result += field + "=" + value + " AND "
        return result[:-4]

    def set_statement(self,values):
        result = ""
        for field, value in zip(self.fields(), values):
            if value != "":
                result += field + "=" + "\'" + value + "\'" + ","
        return result[:-1]
