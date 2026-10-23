import json

def adql(table, columns, constraints):
     str = "select " + ','.join(columns) + " from " + table

     if len(constraints) > 0:
          str = str + " where " + ' and '.join(constraints)

     print(str)

     str = str + "&format=json"

     return str.replace(" ", "+")

def convert_speed(value):
     # values -51 to 49
     value += 1
     if value >= 1:
          return value
     else:
          return 1.05**-value


def update_planets(planets):
     with open("planets.json", "w") as f:
          json.dump(planets, f, indent=5)