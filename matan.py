import mysql.connector
import ast
import sympy as sp
from tree_solution import *
from passlib.hash import sha256_crypt
def create_user_table():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lolkek2004",
        auth_plugin='mysql_native_password',
        database="series"
    )
    mycursor = db.cursor()

    try:
        # Создание таблицы пользователей, если она еще не существует
        mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) UNIQUE, password VARCHAR(255))")
        db.commit()
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
    finally:
        db.close()

def register_user(username, password):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lolkek2004",
        auth_plugin='mysql_native_password',
        database="series"
    )
    mycursor = db.cursor()

    hashed_password = sha256_crypt.hash(password)

    try:
        # Проверяем, существует ли пользователь с таким именем
        mycursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        existing_user = mycursor.fetchone()
        if existing_user:
            print("Пользователь с таким именем уже существует.")
            return False

        # Создаем пользователя
        mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        db.commit()
        print(f"Пользователь '{username}' успешно создан.")
        return True
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        db.close()

def authenticate_user(username, password):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lolkek2004",
        auth_plugin='mysql_native_password',
        database="series"
    )
    mycursor = db.cursor()

    try:
        mycursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = mycursor.fetchone()
        if user and sha256_crypt.verify(password, user[1]): # Проверяем хешированный пароль из базы данных
            print(f"Пользователь '{username}' успешно аутентифицирован.")
            return True
        else:
            print("Неверное имя пользователя или пароль.")
            return False
    except mysql.connector.Error as err:
        print(f"Ошибка: {err}")
        return False
    finally:
        db.close()


def add_to_db(username, password, s):
    if not authenticate_user(username, password):
        return
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lolkek2004",
        auth_plugin='mysql_native_password',
        database="series"
    )

    mycursor = db.cursor()

    try:

        expr_str = s.get_str_expr()

        table_name = f"{username}"
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, expression VARCHAR(255) UNIQUE, nth LONGTEXT, bertran LONGTEXT, raabe LONGTEXT, gauss LONGTEXT, dalamber LONGTEXT, cauchy LONGTEXT, geom LONGTEXT, harm LONGTEXT, integral LONGTEXT)")

        # Проверяем, есть ли уже такая запись в таблице
        sql_check_duplicate = f"SELECT id FROM {table_name} WHERE expression = %s"
        val_check_duplicate = (expr_str,)
        mycursor.execute(sql_check_duplicate, val_check_duplicate)
        existing_row = mycursor.fetchone()

        if existing_row is None:  # Если запись не найдена
            # Создаем словарь с данными для вставки в базу данных
            data_dict = {
                'expression': expr_str,
                'nth': str([None, []]),
                'geom': str([None, []]),
                'harm': str([None, []]),
                'integral': str([None, []]),
                'bertran': str([None, []]),
                'raabe': str([None, []]),
                'gauss': str([None, []]),
                'dalamber': str([None, []]),
                'cauchy': str([None, []]),
            }

            # Получаем список ключей и значений словаря
            columns = ', '.join(data_dict.keys())
            values = tuple(data_dict.values())
            # Создаем SQL-запрос с использованием параметров %s
            sql_insert_new_row = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['%s'] * len(values))})"
            mycursor.execute(sql_insert_new_row, values)

            # Здесь происходят вычисления ряда
            check = solution_tree(s)

            for key, value in check.items():
                # Формируем SQL-запрос для обновления значения
                sql_update = f"UPDATE {table_name} SET {key} = %s WHERE expression = %s"
                val_update = (str(value), expr_str)
                mycursor.execute(sql_update, val_update)

            db.commit()
            mycursor.execute("SELECT LAST_INSERT_ID()")
            last_insert_id = mycursor.fetchone()[0]
            print("Выражение успешно добавлено в базу данных. ID новой записи:", last_insert_id)
            return check
        else:
            print("Ряд уже существует в базе данных. ID:", existing_row[0])
            new_check = {}
            # Получаем список столбцов таблицы
            mycursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in mycursor.fetchall()]
            for column in columns[2:]:
                # Получаем значение текущего столбца для существующей записи
                sql_get_value = f"SELECT {column} FROM {table_name} WHERE expression = %s"
                val_get_value = (expr_str,)
                mycursor.execute(sql_get_value, val_get_value)
                value = mycursor.fetchone()[0]

                # Проверяем значение столбца
                if value != str([None, []]):
                    # Добавляем в словарь new_check
                    new_check[column] = ast.literal_eval(value)

            print("new_check:", new_check) # АНДРЮХА ВОТ ТУТ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return new_check
    except mysql.connector.IntegrityError as e:
        print("Ошибка: Дубликат ряда. Ряд не был добавлен в базу данных.")
        print("Error:", e)
    finally:
        db.close()

#Пример использования:
create_user_table()
username = "kush"
password = "avtomat_po_kripte"
register_user(username,password)
add_to_db(username, password, Series(sp.sympify("1/n**4"), "n"))
