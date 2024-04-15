import mysql.connector
import sympy as sp
# hello world
def add_to_db(expr_str):
    db = mysql.connector.connect(
        host="Vadick",
        user='andrey',
        password="1234567899",
        database="series"
    )

    mycursor = db.cursor()

    # mycursor.execute("CREATE DATABASE IF NOT EXISTS series")

    # mycursor.execute("DROP TABLE IF EXISTS mytable")

    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS mytable (id INT AUTO_INCREMENT PRIMARY KEY, expression VARCHAR(255) UNIQUE)")

    try:  # Проверяем, есть ли уже такая запись в таблице
        sql_check_duplicate = "SELECT id FROM mytable WHERE expression = %s"
        val_check_duplicate = (expr_str,)
        mycursor.execute(sql_check_duplicate, val_check_duplicate)
        existing_row = mycursor.fetchone()
        if existing_row is None:  # Если запись не найдена
            # Добавляем новую запись с увеличением id
            sql_insert_new_row = "INSERT INTO mytable (expression) VALUES (%s)"
            val_insert_new_row = (expr_str,)
            mycursor.execute(sql_insert_new_row, val_insert_new_row)
            db.commit()
            last_insert_id = mycursor.lastrowid
            print("Выражение успешно добавлено в базу данных. ID новой записи:", last_insert_id)
        else:
            print("Ряд уже существует в базе данных. ID:", existing_row[0])
    except mysql.connector.IntegrityError as e:
        print("Ошибка: Дубликат ряда. Ряд не был добавлен в базу данных.")
        print("Error:", e)

    db.commit()
    db.close()

