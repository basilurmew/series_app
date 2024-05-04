import time
import mysql.connector
import ast
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
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, expression VARCHAR(255) UNIQUE, nth LONGTEXT, geom LONGTEXT, harm LONGTEXT,integral LONGTEXT, bertran LONGTEXT, raabe LONGTEXT, gauss LONGTEXT, dalamber LONGTEXT, cauchy LONGTEXT, abs LONGTEXT, leibniz LONGTEXT, abel LONGTEXT, dirichlet LONGTEXT)")

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
                'abs': str([None, []]),
                'leibniz': str([None, []]),
                'abel': str([None, []]),
                'dirichlet': str([None, []]),
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

# #Пример использования:
# start1 = time.perf_counter()
# create_user_table()
# username = "player1"
# password = "sdfhdsfhdska"
# register_user(username,password)
# add_to_db(username, password, Series(sp.sympify("1/n**2"), "n"))
# print(time.perf_counter()-start1)

def theory():
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="lolkek2004",
        auth_plugin='mysql_native_password',
        database="series"
    )
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE IF NOT EXISTS theory (id INT AUTO_INCREMENT PRIMARY KEY, attribute VARCHAR(255), latex_representation TEXT, description TEXT)")
    try:
        mycursor.execute("SELECT COUNT(*) FROM theory")
        result = mycursor.fetchone()
        if result[0] > 0:
            print("Таблица уже содержит данные")
        else:
            sign = ["Необходимое условие", "Обобщенный гармонический ряд","Геометрический ряд ряд",
                    "Радикальный признак  Коши","Признак  Даламбера","Признак  Куммера","Признак  Раабе",
                    "Признак  Бертрана","Интегральный признак Коши","Признак  Гаусса",
                    "Признак  Лейбница","Признак Дирихле","Признак Абеля"]
            latex = [
                [r"[\\sum_{n=1}^{\infty}{a_n}\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{a_n} = 0\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{a_n} \\neq 0\\]"],

                [r"[\\sum_{n=1}^{\infty}{ {1}\\over{n^\\alpha} }\\]",
                 r"[\\alpha > 1 \\]",
                 r"[\\alpha \\leq 1 \\]"],

                [r"[\\sum_{n=1}^{\infty}{q^n}\\]",
                 r"[q < 1 \\]",
                 r"[q \\geq 1 \\]"],

                [r"[\\alpha = \\lim\\limits_{n\\to\\infty}{\\sqrt[n]{a_n}}\\]",
                 r"[\\alpha < 1 \\]",
                 r"[\\alpha > 1 \\]",
                 r"[\\alpha = 1 \\]"],

                [r"[\\lim\\limits_{n\\to\\infty}{ {a_{n+1}}\\over{a_n} } > 1\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{ {a_{n+1}}\\over{a_n} } < 1\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{ {a_{n+1}}\\over{a_n} } = 1\\]"],

                [r"[K_n := c_n {{a_n}\\over{a_{n+1}}} - c_{n+1}\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{K_n} = K\\]",
                 r"[K > 0 \\]",
                 r"[K < 0 \\]"],

                [r"[R_n = n ( { {a_n}\\over{a_{n+1} } } - 1)\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{R_n} = R\\]",
                 r"[R > 1 \\]",
                 r"[R < 1 \\]"],

                [r"[B_n = \\ln{n} (n ({{a_n}\\over{a_{n+1}}} - 1) - 1)\\]",
                 r"[\\lim\\limits_{n\\to\\infty}{B_n} = B\\]",
                 r"[B > 1 \\]",
                 r"[B < 1 \\]"],

                [r"[\\int_{1}^{+\\infty} f(x) dx\\]"],

                [r"[{{a_n}\\over{a_{n+1}}}\\]",
                 r"[{{a_n}\\over{a_{n+1}}} = \\lambda + {{\\mu}\\over{n}} + O({ {1}\\over{n^{1+\\nu}}}), n \\xrightarrow{} \\infty\\]",
                 r"[\\lambda > 1\\]",
                 r"[\\lambda < 1\\]",
                 r"[\\lambda = 1\\]",
                 r"[\\mu > 1\\]",
                 r"[\\mu\\leq 1\\]"],

                [r"[\\sum_{n=1}^{\infty}{{(-1)^{(n-1)}}{a_n}}\\]",
                 r"[\\lvert\\sum_{k=n}^{\infty}{{(-1)^{(k-1)}}{a_k}}\\rvert\\leq a_n\\]"],

                [r"[\\sum_{n=1}^{\infty}{ {a_n}{b_n} }\\]",
                 r"[\\sum_{n=1}^{\infty}{{a_n}{b_n} }\\]"],
                [r"\((a_n)_{n=1}^{\infty}\)",
                 r"\(\sum_{n=1}^{\infty}{b_n}\)",
                 r"\(\sum_{n=1}^{\infty}{ {a_n}{b_n} }\)"]
            ]

            info=[r"Если ряд \(\sum_{n=1}^{\infty}{a_n}\) сходится, то выполняется следующее условие:  \(\lim\limits_{n\to\infty}{a_n} = 0\) \[\]Ряд рсходится, если выполняется следующее условие   \(\lim\limits_{n\to\infty}{a_n} \neq 0\)",
                         r"Обобщенным гармоническим называют ряд вида: \(\sum_{n=1}^{\infty}{ {1}\over{n^\alpha} }\) \[ \]Этот ряд сходится в случае, если: \( \alpha > 1 \) \[ \]И расходится, если: \(\alpha \leq 1 \)",
                         r"Геометрическим называют ряд вида:\(\sum_{n=1}^{\infty}{q^n}\) \[ \]Который расходится, если: \(q < 1 \) \[ \]И сходится, если: \(q \geq 1 \)",
                         r"Дан ряд \(\sum_{n=1}^{\infty}{a_n}\) \[ \]Пусть существует предел\(\alpha = \lim\limits_{n\to\infty}{\sqrt[n]{a_n}}\)Тогда ряд сходится, если\(\alpha < 1 \) \[ \]Расходится, если\(\alpha > 1 \) \[ \]И может как сходится, так и расходится, если\(\alpha = 1 \), в этом случае требуется дополнительное исследование",
                         r"Дан ряд \(\sum_{n=1}^{\infty}{a_n}\) \[\]Если \(\lim\limits_{n\to\infty}{ {a_{n+1}}\over{a_n} } > 1\), то ряд расходится\[ \]Если \(\lim\limits_{n\to\infty}{ {a_{n+1}}\over{a_n} } < 1\), то ряд сходится \[ \]Если \(\lim\limits_{n\to\infty}{ {a_{n+1}}\over{a_n} } < 1\), то ряд сходится\[ \]Если \(\lim\limits_{n\to\infty}{ {a_{n+1}}\over{a_n} } = 1\), то ряд может как сходится так и расходится",
                         r"\[(с_n)_{n=1}^{\infty}\]\[\sum_{n=1}^{\infty}{{1}\over{c_n} }\]\[\sum_{n=1}^{\infty}{a_n}\]\[(K_n)_{n=1}^{\infty}\]\[K_n := c_n { {a_n}\over{a_{n+1} } } - c_{n+1}\]\[\lim\limits_{n\to\infty}{K_n} = K\]Если \(K > 0 \), то ряд сходитсяЕсли \(K < 0 \), то ряд рассходится",
                         r"\[\sum_{n=1}^{\infty}{a_n}\]\[(R_n)_{n=1}^{\infty}\]\[R_n = n ( { {a_n}\over{a_{n+1} } } - 1)\]\[\lim\limits_{n\to\infty}{R_n} = R\]Если \(R > 1 \), то ряд сходитсяЕсли \(R < 1 \), то ряд рассходится",
                         r"\[\sum_{n=1}^{\infty}{a_n}\]\[(B_n)_{n=1}^{\infty}\]\[B_n = \ln{n} (n ( { {a_n}\over{a_{n+1} } } - 1) - 1)\]Пусть существет предел \(\lim\limits_{n\to\infty}{B_n} = B\) \[ \]Если \(B > 1 \), то ряд сходится \[ \]Если \(B < 1 \), то ряд расходится",
                         r"\[f:[1, +\infty) -> \mathbb{R}_{+}\]\[\sum_{n=1}^{\infty}{f(n)}\]Если интеграл \(\int_{1}^{+\infty} f(x) dx\) сходится, то сходится и исходный ряд.В противном случае ряд расходится",
                         r"\[\sum_{n=1}^{\infty}{a_n}\]\[{ {a_n }\over{a_{n+1} } }\]\[{ {a_n}\over{a_{n+1} } } = \lambda + { {\mu}\over{n} }  + O({ {1}\over{n^{1+\nu} } }), n \xrightarrow{} \infty\]\[\lambda > 1\]\[\lambda < 1\]\[\lambda = 1\]\\[\mu > 1\]\[\mu \leq 1\]",
                         r"\[(a_n)_{n=1}^{\infty}\]\[\lim\limits_{n\to\infty}{a_n} = 0\]Если исходный ряд можно представить в виде \(\sum_{n=1}^{\infty}{ {(-1)^{ (n-1)} }{a_n} }\) и\(\lvert \sum_{k=n}^{\infty}{ {(-1)^{(k-1)} }{a_k} } \rvert \leq a_n\), то ряд сходится",
                         r"Если последовательность \((a_n)_{n=1}^{\infty}\) ограничена и ряд\(\sum_{n=1}^{\infty}{b_n}\) сходится, то сходится и ряд\(\sum_{n=1}^{\infty}{ {a_n}{b_n} }\)",
                         r"Если последовательность \((a_n)_{n=1}^{\infty}\) сходится к нулю и последовательность частичных сумм ряда\(\sum_{n=1}^{\infty}{b_n}\) ограничена, то ряд\(\sum_{n=1}^{\infty}{ {a_n}{b_n} }\) сходится"
                         ]

            for i in range(len(latex)):
                sql = "INSERT INTO theory (attribute, latex_representation, description) VALUES (%s, %s, %s)"
                val = (sign[i], ', '.join(latex[i]), info[i])
                mycursor.execute(sql, val)

            db.commit()

            print("Данные успешно вставлены.")

    except mysql.connector.Error as err:
        print("Error creating table:", err)

    finally:
        db.close()

theory()