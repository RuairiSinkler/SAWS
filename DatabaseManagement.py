import sqlite3


class DatabaseManager:
    def __init__(self, database_name):
        self.database_name = database_name

    # Inserts given values into a given table
    def insert(self, table, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        print(table)
        print(values)
        execution = "INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(table)
        print(execution)
        cursor.execute(execution, values)
        connect.commit()

        connect.close()

    # Specifically inserts values into the rations table
    def insert_ration(self, values):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(ration_id)+1 FROM rations")
        ration_id = cursor.fetchone()[0]
        if ration_id is None:
            ration_id = 0
        # print(ration_id)
        connect.close()
        values.insert(0, ration_id)

        # Perform Validation on the values inserted to go into the rations database
        all_ok = isinstance(values[1], str) and values[1]
        for i in range(2, 10):
            if (i == 8):
                all_ok = all_ok and isinstance(values[i], float)
            else:
                all_ok = all_ok and isinstance(values[i], int)

        # If all is ok then insert otherwise raise an exception
        if all_ok:
            self.insert("rations", values)
        else:
            raise (IOError)

    def update_ration(self, values):
        # Perform Validation on the values inserted to go into the rations database
        all_ok = isinstance(values[1], str) and values[1]
        for i in range(2, 10):
            if (i == 8):
                all_ok = all_ok and isinstance(values[i], float)
            else:
                all_ok = all_ok and isinstance(values[i], int)

        # If all is ok then insert otherwise raise an exception
        if all_ok:
            ration_id = values.pop(0)
            values.append(ration_id)

            connect = sqlite3.connect(self.database_name)
            cursor = connect.cursor()

            execution = "UPDATE rations SET ration_name = ?, " \
                        "wheat = ?, barley = ?, soya = ?, " \
                        "limestone = ?, soya_oil = ?, arbocell = ?," \
                        "methionine = ?, premix = ? " \
                        "WHERE ration_id = ?"

            cursor.execute(execution, values)
            connect.commit()

            connect.close()
        else:
            raise (IOError)

    def get_ration(self, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(ration)
        execution = "SELECT * FROM rations WHERE ration_id = ?"
        # print(execution)
        cursor.execute(execution, (ration_id,))

        result = cursor.fetchall()[0]

        connect.close()

        return result

    def get_all_rations(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(ration)
        execution = "SELECT *  FROM rations"
        # print(execution)
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()

        return result

    def get_assignment(self, house_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT rations.ration_id FROM house_rations " \
                    "JOIN houses ON house_rations.house_id = houses.house_id " \
                    "JOIN rations ON house_rations.ration_id = rations.ration_id " \
                    "WHERE houses.house_id = ?"
        # print(execution)
        cursor.execute(execution, (str(house_id),))

        result = cursor.fetchall()[0][0]

        connect.close()
        # print(result)
        return result

    def get_assignments(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT houses.house_id, house_name, rations.ration_id, ration_name, batch_number " \
                    "FROM house_rations " \
                    "JOIN houses ON house_rations.house_id = houses.house_id " \
                    "JOIN rations ON house_rations.ration_id = rations.ration_id"
        # print(execution)
        cursor.execute(execution)

        result = cursor.fetchall()

        connect.close()
        # print(result)
        return result

    def check_ration_assignment(self, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(value_id)
        execution = "SELECT house_id FROM house_rations WHERE ration_id = ?"
        # print(execution)
        cursor.execute(execution, (ration_id,))
        for house in cursor.fetchall():
            self.assign_ration(house[0], 0)

        connect.close()

    def update_id(self, old_id, new_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(house_id)
        # print(ration_id)
        execution = "UPDATE rations SET ration_id = ? WHERE ration_id = ?"
        # print(execution)
        cursor.execute(execution, (str(new_id), str(old_id),))
        connect.commit()
        execution = "UPDATE house_rations SET ration_id = ? WHERE ration_id = ?"
        # print(execution)
        cursor.execute(execution, (str(new_id), str(old_id),))
        connect.commit()

        connect.close()

    def delete_ration(self, value_id):
        self.check_ration_assignment(value_id)
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(value_id)
        execution = "DELETE FROM rations WHERE ration_id = ?"
        # print(execution)
        cursor.execute(execution, (value_id,))
        connect.commit()

        for id in range(int(value_id) + 1, self.get_max_ration_id() + 1):
            self.update_id(id, id - 1)

        connect.close()

    def assign_ration(self, house_id, ration_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        # print(house_id)
        # print(ration_id)
        execution = "UPDATE house_rations SET ration_id = ? WHERE house_id = ?"
        # print(execution)
        cursor.execute(execution, (str(ration_id), str(house_id),))
        connect.commit()

        connect.close()

    def get_max_ration_id(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT max(ration_id) FROM rations"
        cursor.execute(execution)

        result = cursor.fetchall()[0][0]

        connect.close()

        return result

    def get_house_name(self, house_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT house_name FROM houses WHERE house_id = ?"
        cursor.execute(execution, (house_id, ))

        result = cursor.fetchall()[0][0]

        connect.close()

        return result

    def get_house_batch_number(self, house_id):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT batch_number FROM houses WHERE house_id = ?"
        cursor.execute(execution, (house_id,))

        result = cursor.fetchall()[0][0]

        connect.close()

        return result

    def change_batch(self, house_id, batch_number):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "UPDATE houses SET batch_number = ? WHERE house_id = ?"
        cursor.execute(execution, (str(batch_number), str(house_id),))
        connect.commit()

        connect.close()

    def get_max_house_id(self):
        connect = sqlite3.connect(self.database_name)
        cursor = connect.cursor()

        execution = "SELECT max(house_id) FROM houses"
        cursor.execute(execution)

        result = cursor.fetchall()[0][0]

        connect.close()

        return result
