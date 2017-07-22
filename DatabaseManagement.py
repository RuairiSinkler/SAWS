
import sqlite3

class DatabaseManager :

    def __init__(self, database_name) :
        self.database_name = database_name

    # Inserts given values into a given table
    def insert(self, table, values) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        values_string = str(values[0])
        for i in range(1, len(values)) :
            if isinstance(values[i], int) :
                values_string += ", " + str(values[i])
            else :
                values_string += ", \"" + values[i] + "\""
        #print(table)
        #print(values_string)
        execution = "INSERT INTO {} VALUES ({})".format(table, values_string)
        #print(execution)
        cursor.execute(execution)
        connect.commit()

        connect.close()

    # Specifically inserts values into the rations table
    def insert_ration(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(ration_id)+1 FROM rations")
        ration_id = cursor.fetchone()[0]
        if ration_id is None :
            ration_id = 0
        #print(ration_id)
        connect.close()
        values.insert(0, ration_id)

        # Perform Validation on the values inserted to go into the rations database
        all_ok = isinstance(values[1], str) and values[1]
        for i in range(2, 10):
            all_ok = all_ok and isinstance(values[i], int)

        # If all is ok then insert otherwise raise an exception
        if all_ok:
            self.insert("rations", values)
        else:
            raise (IOError)

    def get_ration(self, ration_id) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(ration)
        execution = "SELECT *  FROM rations WHERE ration_id = {}".format(ration_id)
        # print(execution)
        cursor.execute(execution)

        result = cursor.fetchall()[0]

        connect.close()

        return result

    def get_all_rations(self) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(ration)
        execution = "SELECT *  FROM rations"
        # print(execution)
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()

        return result

    def get_assignments(self) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT house_id, house_name, ration_id, ration_name FROM house_rations " \
                    "JOIN houses ON house_rations.house_id = houses.house_id " \
                    "JOIN rations ON house_rations.ration_id = rations.ration_id"
        # print(execution)
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()
        #print(result)
        return result

    def delete_ration(self, value_id) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        #print(value_id)
        execution = "DELETE FROM rations WHERE ration_id = {}".format(value_id)
        #print(execution)
        cursor.execute(execution)
        connect.commit()

        connect.close()

    def assign_ration(self, house_id, ration_id) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        #print(house_id)
        #print(ration_id)
        execution = "UPDATE house_rations SET ration_id = {} WHERE house_id = {}".format(str(ration_id), str(house_id))
        #print(execution)
        cursor.execute(execution)
        connect.commit()

        connect.close()

    def get_max_ration_id(self) :
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT max(ration_id) FROM rations"
        cursor.execute(execution)

        result = cursor.fetchall()[0][0]

        connect.close()

        return result

    def get_max_house_id(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT max(house_id) FROM houses"
        cursor.execute(execution)

        result = cursor.fetchall()[0][0]

        connect.close()

        return result