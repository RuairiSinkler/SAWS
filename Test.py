
from DatabaseManagement import *

def main() :
    ration_manager = DatabaseManager("rations.db")
    print(ration_manager.get_ration("Minnie"))

if __name__ == "__main__":
    main()
