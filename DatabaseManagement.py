
import sqlite3

class DatabaseManager :

    def __init__(self, database_name) :
        self.database_name = database_name

    # Inserts given values into a given table
    def insert(self, table, values) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        values_string = "\"" + values[0] + "\""
        for i in range(1, len(values)) :
            values_string += ", \"" + values[i] + "\""
        print(table)
        print(values_string)
        execution = "INSERT INTO %s VALUES (%s)" % (table, values_string)
        print(execution)
        cursor.execute(execution)

        connect.close()

    # Specifically inserts values into the rations table
    def insert_ration(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        ration_id = cursor.execute("SELECT MAX(ration_id)+1 FROM rations")
        connect.close()
        values.insert(0, ration_id)

        # Perform Validation on the values inserted to go into the rations database
        all_ok = isinstance(values[1], str) and values[1]
        for i in range(2, 10):
            all_ok = all_ok and isinstance(values[i], int)

        # If all is ok then insert otherwise raise an exception
        if all_ok:
            self.insert("ration.db", values)
        else:
            raise (IOError)

    def delete_ration(self, value_id) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        print(value_id)
        execution = "DELETE FROM rations WHERE ration_id = %s" % (value_id)
        print(execution)
        cursor.execute(execution)

        connect.close()


