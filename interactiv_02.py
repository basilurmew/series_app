from parser import str_to_tex


q_d = {"nth": "Выполняется ли необходимое условие сходимости?",   "geom": "Сходится ли данный ряд как геометрический?",
       "harm": "Сходится ли данный ряд как обобщенный гармонический?",
        "dalamber":"Какой признак на данном этапе самый подходящий?",
          "cauchy":"Какой признак на данном этапе самый подходящий?","raabe":"Какой признак на данном этапе самый подходящий?",
          "bertran":"Какой признак на данном этапе самый подходящий?", "gauss":"Какой признак на данном этапе самый подходящий?",
          "integral":"Какой признак на данном этапе самый подходящий?"}
a_d = {"nth":["Необходимое условие не выполняется.Данный ряд расходится.", "Необходимое условие выполняется, думаем дальше.", ""],
            "geom":["Данный ряд расходится как геометрический.", "Данный ряд не является геометрическим.", "Данный ряд сходится как геометрический."],
            "harm":["Данный ряд расходится как обобщенный гармонический.","Данный ряд не является обобщенным гармоническим.","Данный ряд сходится как обобщенный гармонический."],
            "dalamber": ["Данный ряд расходится по признаку Даламбера","Признак Даламбера не работает. Думаем дальше.", "Данный ряд сходится по признаку Даламбера."],
            "cauchy":["Данный ряд расходится по Радикальному признаку Коши.","Данный признак ничиго не может сказать о сходимости данного ряда.Думаем дальше.","Данный ряд сходится по Радикальному признаку Коши."],
            "raabe":["Данный ряд расходится по признаку Раабе.","Данный признак ничего не может сказать о сходимости данного ряда.Думаем дальше.","Данный ряд сходится по признаку Раабе."],
            "bertran":["Данный ряд расходится по признаку Бертрана", "Признак Бертрана не работает, думаем дальше.", "Данный ряд сходится по признаку Бертрана"],
            "integral":["Данный ряд расходится по интегральному признаку.","Для данного ряда не выполнены условия интегрального признака.","Данный ряд сходится по интегральному признаку Коши."],
            "gauss":["Данный ряд сходится по признаку Гаусса.","","Данный ряд расходится по призаку Гаусса."]}
bin_ans = "Вы ошиблись, подумайте и попробуйте снова."
sign_ans = "Вы ошиблись, выбранный вами признак не подходит."
sign_list = ["dalamber","raabe", "cauchy", "bertran", "gauss", "integral"]

def next_dict(current_key, tree):
    res = {}
    if current_key == "nth":
        res["question"] = q_d[current_key]
        res["false_actor_answer"] = bin_ans
        res["intermediate_result"] = tree[current_key][1]
        if tree[current_key][0] == 0:
            res["true_actor_answer"] = a_d[current_key][1]
            res["true_answer"] = 0
        else:
            res["true_actor_answer"] = a_d[current_key][0]
            res["true_answer"] = -1


    elif current_key == "geom":
        res["question"] = q_d[current_key]
        res["false_actor_answer"] = bin_ans
        res["intermediate_result"] = tree[current_key][1]
        if tree[current_key][0] == 0:
            res["true_actor_answer"] = a_d[current_key][1]
            res["true_answer"] = 0
        elif tree[current_key][0] == -1:
            res["true_actor_answer"] = a_d[current_key][0]
            res["true_answer"] = -1

        elif tree[current_key][0] == 1:
            res["true_actor_answer"] = a_d[current_key][2]
            res["true_answer"] = 1



    elif current_key == "harm":
        res["question"] = q_d[current_key]
        res["false_actor_answer"] = bin_ans
        res["intermediate_result"] = tree[current_key][1]
        if tree[current_key][0] == 0:
            res["true_actor_answer"] = a_d[current_key][1]
            res["true_answer"] = 0
        elif tree[current_key][0] == -1:
            res["true_actor_answer"] = a_d[current_key][0]
            res["true_answer"] = -1

        elif tree[current_key][0] == 1:
            res["true_actor_answer"] = a_d[current_key][2]
            res["true_answer"] = 1

    elif current_key in sign_list:
        res["question"] = q_d[current_key]
        res["false_actor_answer"] = sign_ans
        res["intermediate_result"] = tree[current_key][1]
        if tree[current_key][0] == 0:
            res["true_actor_answer"] = a_d[current_key][1]
            res["true_answer"] = 0
        elif tree[current_key][0] == -1:
            res["true_actor_answer"] = a_d[current_key][0]
            res["true_answer"] = -1

        elif tree[current_key][0] == 1:
            res["true_actor_answer"] = a_d[current_key][2]
            res["true_answer"] = 1
    if len(res["intermediate_result"])>0:
        inter_res = res["intermediate_result"][0]
        for i in range(1,len(res["intermediate_result"])):
            inter_res+= " = " + str_to_tex(res["intermediate_result"][i])

        inter_res += " \]"
    else:
        inter_res = ""
    res["intermediate_result"] = inter_res
    res["sign"] = current_key
    return res
