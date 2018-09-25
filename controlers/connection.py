from psycopg2 import connect, OperationalError


def create_connection(db_name):
    username = "aleksandrasandor"
    passwd = "1987lukas"
    hostname = "127.0.0.1"  # lub "localhost"
    cnx = None
    try:
        cnx = connect(user=username, password=passwd, host=hostname, database=db_name)
        cnx.autocommit = True #informacja o tym, że to jest transakcja
        print("Połączenie udane.")
    except OperationalError as error:
        print("Nieudane połączenie.")
    return cnx

def execute_sql(cnx, sql_file):
    cursor = cnx.cursor()
    result = []
    file = open(sql_file, "r")
    sql_text = file.read()
    file.close()

    sqlCommands = sql_text.split(";")
    print(sqlCommands)

    for command in sqlCommands:
        if command == "": continue
        try:
            cursor.execute(command)
            #result.append(cursor.fetchall())
            result.append({"query": command, "result": cursor.fetchall()})
        except Exception as e:
            print(e)

    cursor.close()
    return result

#pojedyncze zapytanie sql
def execute_single_sql(cnx, command):
    cursor = cnx.cursor()

    result = None
    try:
        cursor.execute(command)
        result = cursor.fetchall()
    except Exception as e:
        print(e)

    cursor.close()
    return result

if __name__ == "__main__":
    connection = create_connection("users_db")  #tu nazwa bazy
    results = execute_sql(connection, "create_base.sql") #tu nazwa pliku, w którym tworzymy zapytanie sql

    for result in results:
        print(result)

    connection.close()