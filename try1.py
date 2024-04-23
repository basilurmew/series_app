from flask import Flask, render_template, request, redirect
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
        return render_template("welcome.html")


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
            solve_tree = solution_tree(ser)
            #add_to_db(ser.get_str_expr())
            return redirect('/main/game')
        else:
            return render_template("index.html", mistake = check_res[1])
    else:
        return render_template("index.html" )


@app.route('/main/game', methods=['POST', 'GET'])
def game():
    if request.method == "GET":
        return render_template("game_of_series.html", getted_series = getted_row.replace("▯", ""), variable = ser.get_str_var() )




@app.route('/solve', methods=['POST', 'GET'])
def solving():
    step = int(request.data.decode('UTF-8'))
    keys_list = list(solve_tree.keys())
    json_element = next_dict(keys_list[step], solve_tree)
    return json.dumps(json_element)



if __name__ == "__main__":
    app.run(debug=True)
