from flask import Flask, render_template, request, redirect,url_for
from parser import tex_to_sempy
import sympy as sp
import mysql.connector
import checking, series
from tree_solution import solution_tree
from matan import *
import json
from sign_comparison import *
from game import *
from interactiv_02 import next_dict


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def welcome():
    if request.method == "GET":
        global user, password
        user = " "
        password = "cubikrubik"
        return render_template("login.html")
    if request.method == "POST":
        login = request.form.get('login')
        pas = request.form.get('password')

        if(authenticate_user(login,pas)):

            user = login
            password = pas
            return redirect('/main')
        else:
            return render_template('login.html', mistake = "Неверное имя пользователя или пароль")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "GET":
        global user, password
        user = "free_user"
        password = "cubikrubik"
        return render_template("registration.html")
    else:
        login = request.form.get('login')
        pas = request.form.get('password')
        if (register_user(login, pas)):

            user = login
            password = pas
            return redirect('/main')
        else:
            return render_template("registration.html", mistake = "Пользователь с таким именем уже существует")


@app.route('/main', methods=['POST', 'GET'])
def index():
    if request.method == "POST":

        global getted_row
        global solve_tree
        global ser

        getted_row = request.form.get('row_serv')
        member_n = tex_to_sempy(getted_row)
        check_res = checking.full_check(member_n)

        if(check_res[0]):
            ser = series.Series(sp.sympify(member_n), check_res[1])
            solve_tree, first_input = add_to_db(user, password, ser)
            print(solve_tree)
            if first_input == True:
                return redirect('/main/game')
            else:
                return redirect('/main/secondary_game')
        else:
            return render_template("index.html", mistake = check_res[1])
    else:
        return render_template("index.html", login = user)


@app.route('/main/game', methods=['POST', 'GET'])
def game():
    return render_template("game_of_series.html", getted_series = getted_row.replace("▯", ""), variable = ser.get_str_var(), max_len = len(list(solve_tree.keys())))


@app.route('/main/secondary_game', methods=['POST', 'GET'])
def secondary_game():

    json_elem = list(solve_tree.keys())
    if solve_tree[list(solve_tree.keys())[len(list(solve_tree.keys()))-1]][0] == -1:
        json_elem.append('diverg')
    else:
        json_elem.append('converg')
    signs = json.dumps(json_elem)

    return render_template("secondary_input.html", getted_series = getted_row.replace("▯", ""), variable = ser.get_str_var(), ans = signs)

@app.route('/solve_secondary', methods=['POST', 'GET'])
def solv_sec():
    step = request.data.decode('UTF-8')
    json_element = {"true_answer" : solve_tree[step][0], "intermediate_result" :intermediate_result( solve_tree[step][1],ser )}
    return json.dumps(json_element)



@app.route('/solve', methods=['POST', 'GET'])
def solving():
    step = int(request.data.decode('UTF-8'))
    print("=======================================================")
    print(step)
    print(len(list(solve_tree.keys())))
    if step < len(list(solve_tree.keys())):
        keys_list = list(solve_tree.keys())
        json_element = next_dict(keys_list[step], solve_tree)
        json_element["max_len"] = len(list(solve_tree.keys()))
        return json.dumps(json_element)
    else:
        return redirect('/main/secondary_game')



@app.route('/theory', methods=['POST', 'GET'])
def theory_page():
    """ВАААААААААААДИИИИИИИИИМ
    короче вот тут надо бахнуть функцию, которая в переменные(переменные создай сам) nth_db, harm_db, geom_bd,..., abel_bd --занесет соответственные данные из бд
    текст для каждого признака находится в текстовике theory.txt. Как признаки в текстовике разграничены думаю разберешься. В текст помести единой строкой
    """

    return render_template('theory.html')





if __name__ == "__main__":
    app.run(debug=True)
