
import sqlite3

class DatabaseManager :

    def __init__(self, database_name) :
        self.database_name = database_name
        self.connect = sqlite3.connect(self.database_name)

    def insert(self, table, values) :
        cursor = self.get_cursor()

        values_string = "\"" + values[0] + "\""
        for i in range(1, len(values)) :
            values_string += ", \"" + values[i] + "\""
        print(table)
        print(values_string)
        execution = "INSERT INTO %s VALUES (%s);" % (table, values_string)
        print(execution)
        cursor.execute(execution)

        self.close_connection()

    def get_cursor(self) :
        cursor = self.connect.cursor()
        return cursor

    def close_connection(self) :
        self.connect.close()


