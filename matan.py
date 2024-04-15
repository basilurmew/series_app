import mysql.connector
import ast
import sympy as sp
from tree_solution import *
def add_to_db(s):
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lolkek2004",
        auth_plugin='mysql_native_password',
        database="series"
    )

    expr_str = s.get_str_expr()

    mycursor = db.cursor()

    #mycursor.execute("CREATE DATABASE IF NOT EXISTS series")

    #mycursor.execute("DROP TABLE IF EXISTS test")

    mycursor.execute("CREATE TABLE IF NOT EXISTS test (id INT AUTO_INCREMENT PRIMARY KEY, expression VARCHAR(255) UNIQUE, nth LONGTEXT, bertran LONGTEXT, raabe LONGTEXT, gauss LONGTEXT, dalamber LONGTEXT,cauchy LONGTEXT, geom LONGTEXT, harm LONGTEXT, integral LONGTEXT)")

    try:
        # Проверяем, есть ли уже такая запись в таблице
        sql_check_duplicate = "SELECT id FROM test WHERE expression = %s"
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
            sql_insert_new_row = f"INSERT INTO test ({columns}) VALUES ({', '.join(['%s'] * len(values))})"
            # val_insert_new_row[]
            mycursor.execute(sql_insert_new_row, values)
            #здесь поступает вычиления ряда

            check = solution_tree(s)

            for key, value in check.items():
                # Формируем SQL-запрос для обновления значения
                sql_update = f"UPDATE test SET {key} = %s WHERE expression = %s"
                val_update = (str(value),expr_str)
                mycursor.execute(sql_update, val_update)

            db.commit()
            mycursor.execute("SELECT LAST_INSERT_ID()")
            last_insert_id = mycursor.fetchone()[0]
            print("Выражение успешно добавлено в базу данных. ID новой записи:", last_insert_id)
        else:
            print("Ряд уже существует в базе данных. ID:", existing_row[0])
            new_check = {}
            # Получаем список столбцов таблицы
            mycursor.execute("SHOW COLUMNS FROM test")
            columns = [column[0] for column in mycursor.fetchall()]
            for column in columns[2:]:
                # Получаем значение текущего столбца для существующей записи
                sql_get_value = f"SELECT {column} FROM test WHERE expression = %s"
                val_get_value = (expr_str,)
                mycursor.execute(sql_get_value, val_get_value)
                value = mycursor.fetchone()[0]

                # Проверяем значение столбца
                if value != str([None, []]):
                    # Добавляем в словарь new_check
                    new_check[column] = ast.literal_eval(value)

            print("new_check:", new_check)


    except mysql.connector.IntegrityError as e:
        print("Ошибка: Дубликат ряда. Ряд не был добавлен в базу данных.")
        print("Error:", e)


    db.commit()
    db.close()

