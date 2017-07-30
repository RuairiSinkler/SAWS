from DatabaseManagement import *


def main():
    print([1, 2, 3] == [1, 2, 3])
    print([1, 2, 3] == [3, 2, 1])
    ration_manager = DatabaseManager("rations.db")
    print(ration_manager.get_ration("Minnie"))


if __name__ == "__main__":
    main()
