from tree_solution import solution_tree
from series import Series
import sympy as sp
from parser import str_to_tex
from text_for_interactiv.questions import q_d
from text_for_interactiv.answers import *






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
    res["vars_of_answers"] = vars_of_answers[current_key]
    return res
