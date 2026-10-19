import json

def adql(table, columns, constraints):
     str = "select " + ','.join(columns) + " from " + table

     if len(constraints) > 0:
          str = str + " where " + ' and '.join(constraints)

     print(str)

     str = str + "&format=json"

     return str.replace(" ", "+")

def convert_speed(value):
    if value < -10:
        return 0.2 * 10 ** ((value + 10) / 40)
    elif value < 0:
        return 5 ** (value / 10)
    elif value <= 10:
        return 5 ** (value / 10)
    else:
        return 5 * 10 ** ((value - 10) / 40)


def update_planets(planets):
     with open("planets.json", "w") as f:
          json.dump(planets, f, indent=5)