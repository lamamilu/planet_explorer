def adql(table, columns, constraints):
     str = "select " + ','.join(columns) + " from " + table

     if len(constraints) > 0:
          str = str + " where " + ' and '.join(constraints)

     print(str)

     str = str + "&format=json"

     return str.replace(" ", "+")