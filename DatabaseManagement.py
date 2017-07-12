
import sqlite3

class DatabaseManager :

    def __init__(self, database_name) :
        self.database_name = database_name

    def insert(self, table, values) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        values_string = "\"" + values[0] + "\""
        for i in range(1, len(values)) :
            values_string += ", \"" + values[i] + "\""
        print(table)
        print(values_string)
        execution = "INSERT INTO %s VALUES (%s);" % (table, values_string)
        print(execution)
        cursor.execute(execution)

        connect.close()
        


