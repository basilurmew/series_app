from flask import Flask, render_template, request, redirect
from parser import tex_to_sempy
import sympy as sp
import checking, series
import json
from sign_comparison import *
from game import *

app = Flask(__name__)



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        global getted_row
        global ser
        getted_row = request.form.get('row_serv')
        member_n = tex_to_sempy(getted_row)
        check_res = checking.full_check(member_n)

        if(check_res[0]):
            ser = series.Series(sp.sympify(member_n), check_res[1])
            return redirect('/main/game')
        else:
            return render_template("index.html", res = check_res[1])


    else:
        return render_template("index.html" )


@app.route('/main/game', methods=['POST', 'GET'])
def game():
    if request.method == "POST":
        way = request.form.get('way') # считываем, какую кнопку нажал пользователь
        pr_res = solve_series_by_sign(ser, way) # считаем, выбранный признак, для нашего ряда
        res = pr_res.get_res()# В зависимости от того, что дал нам признак - гененрируем строку ответа
        return render_template("game_of_series.html", getted_series = getted_row.replace("▯", ""), res = res, intermediate_result = intermediate_result(pr_res.get_steps(), ser))
    else:
        return render_template("game_of_series.html", getted_series = getted_row.replace("▯", ""))


if __name__ == "__main__":
    app.run(debug=True)
