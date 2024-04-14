from flask import Flask, render_template, request, redirect
from parser import tex_to_sempy
import sympy as sp
import mysql.connector
import checking, series
from matan import *
import json
from sign_comparison import *
from game import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def welcome():
    if request.method == "GET":
        return render_template("welcome.html")
@app.route('/main', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        global getted_row
        global ser
        getted_row = request.form.get('row_serv')
        member_n = tex_to_sempy(getted_row)
        check_res = checking.full_check(member_n)

        if(check_res[0]):
            ser = series.Series(sp.sympify(member_n), check_res[1])
            #add_to_db(ser.get_str_expr())
            return redirect('/main/game')
        else:
            return render_template("index.html", mistake = check_res[1])


    else:
        return render_template("index.html" )


@app.route('/main/game', methods=['POST', 'GET'])
def game():
    if request.method == "GET":
        return render_template("game_of_series.html", getted_series = getted_row.replace("▯", ""))

@app.route('/solve', methods=['POST', 'GET'])
def solving():
    way =request.data.decode('UTF-8')
    pr_res = solve_series_by_sign(ser, way)
    json_element = {}
    json_element["passed"] = pr_res.get_ans()
    print(pr_res.get_steps())
    json_element["intermediate_result"] = intermediate_result(pr_res.get_steps(),ser)
    print(intermediate_result(pr_res.get_steps(),ser))
    json_element["answer"] = pr_res.get_res()
    return json.dumps(json_element)



if __name__ == "__main__":
    app.run(debug=True)
