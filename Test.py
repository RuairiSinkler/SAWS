# import excel.excel_management as ex

# ration_logs_ex = ex.WorksheetManager(".", "ration_logs")
# ration_logs_ex.update_sheets("ration_logs")

# import openpyxl
# import time
# from pathlib import Path

# def get_cell(sheet, column, row):
#   cell_name = "{}{}".format(openpyxl.utils.get_column_letter(column), str(row))
#   return sheet[cell_name]

# dir = "."
# name = "test"
# path = "{}/{}.xlsx".format(dir, name)
# workbook = Path(path)
# if workbook.is_file():
#   workbook = openpyxl.load_workbook(path)
# else:
#   workbook = openpyxl.Workbook()
#   sheet = workbook.active
#   workbook.save(path)
# sheet = workbook.active

# cell = get_cell(sheet, 1, 1)
# cell.value = "test"
# workbook.save(path)

# i = 0
# while(True):
#   print(i)
#   i += 1
#   time.sleep(1)

# class ClassA:

#   def __init__(self):
#     self.test = 0

# class ClassB:

#   def __init__(self, a):
#     self.a = a

# class ClassC:

#   def __init__(self, a):
#     self.a = a

# a0 = ClassA()
# a1 = ClassA()
# a2 = ClassA()
# a3 = ClassA()
# a4 = ClassA()

# a_s = [a0, a1, a2, a3, a4]

# b = ClassB(a_s)
# c = ClassC([a0, a3, a4])

# i = 0
# for a in b.a:
#   a.test = i
#   i += 1

# for a in c.a:
#   print(a.test)

# from pages.page_tools.ingredient import Ingredient
# from pages.page_tools.ration import Ration

# ingredient1 = Ingredient("Wheat", 200, 1, 1, 1, 1, 100)
# ingredient2 = Ingredient("Barley", 300, 1, 1, 1, 1, 1010)

# ration = Ration(1, "Ration 1", "House 1", 1, 2, True, 890321, [ingredient1, ingredient2])

# ration_json = ration.to_json()
# print(ration_json)

# recon_ration = Ration.from_json(ration_json)

# print(recon_ration.to_json())

# ration = Ration(1, "hello")
# ration2 = Ration(2, "hello2")

# ration.add_ingredient(2)
# ration2.add_ingredient(3)

# print(ration.__dict__)
# print(ration2.__dict__)

class Stupid:

  def __init__(self, variable=None):
    if variable is None:
      self.variable = []
    else:
      self.variable = variable

stupid1 = Stupid()
# stupid2 = Stupid()

stupid1.variable.append(1)
stupid2 = Stupid()
# stupid2.variable.append(2)

print(stupid1.variable)
print(stupid2.variable)