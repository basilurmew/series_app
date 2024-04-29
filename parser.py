import sympy as sp

def find_open_bracket(string:str, ind:int):
    """Возвращает индекс скобки в строке string,
       являющейся открывающей для скобки на позиции ind"""
    if string[ind] == ")":
        o_br = "("
        cl_br = ")"
    elif string[ind] == "]":
        o_br = "["
        cl_br = "]"
    elif string[ind] == "}":
        o_br = "{"
        cl_br = "}"
    stack = [string[ind]]
    counter = ind - 1
    while len(stack) !=0:
        if string[counter] == o_br:
            stack.pop()
        elif string[counter] == cl_br:
            stack.append(cl_br)
        counter -= 1
    return counter + 1


def find_close_bracket(string:str, ind:int):
    """Возвращает индекс скобки в строке string,
       являющейся закрывающей для скобки на позиции ind"""
    if string[ind] == "(":
        o_br = "("
        cl_br = ")"
    elif string[ind] == "[":
        o_br = "["
        cl_br = "]"
    elif string[ind] == "{":
        o_br = "{"
        cl_br = "}"
    stack = [string[ind]]
    counter = ind + 1
    while len(stack) !=0:
        if string[counter] == cl_br:
            stack.pop()
        elif string[counter] == o_br:
            stack.append(cl_br)
        counter += 1
    return counter - 1


def replace_by_index(string:str, sub:str, ind:int):
    """принимает строку string, подстроку sub и индекс ind
       заменяет символ, находящийся на позиции ind в строке string на sub"""
    string = string[0:ind] + sub + string[ind+1:]
    return string


def add_brackets(s):
    """
    Функция, которая добавляет все необходимые скобки в строке
    Args:
        s (str): изначальная строка
    Returns:
        str: изменненная строка
    """
    numbers = "1234567890"
    alphabet="abcdefghijklmnopqrstuvwxyz"
    s = " " + s.replace(" ", "") + " "
    new_s = ""
    for i in range(1, len(s) - 1):
        if s[i] in numbers + alphabet + "()" and  s[i - 1] not in numbers + alphabet + "()":
            new_s += "("
        new_s += s[i]
        if s[i] in numbers + alphabet + "()" and  s[i + 1] not in numbers + alphabet + "()":
            new_s += ")"
    return new_s


def remove_brackets(string:str):
    """Убирает у строки string ненужные скобки"""
    string = " " + string + " "
    i=0
    first_priorety = "*/^!"
    secondary_priorety = "+-"
    alphabet="abcdefghijklmnopqrstuvwxyz"
    functions = "sintgcosln"
    while i<len(string):
        if string[i]=="(" and string[i-1] not in alphabet:
            cl_br = find_close_bracket(string, i)
            if cl_br == i+2:
                string = replace_by_index(string, "", cl_br)
                string = replace_by_index(string, "", i)
                i-=1
            else:
                if string[i-1] not in first_priorety and string[cl_br+1] not in first_priorety:
                    string = replace_by_index(string, "", cl_br)
                    string = replace_by_index(string, "", i)
                    i-=1
                    
        i+=1
    return string



def insert_by_index(string:str, sub_str:str, ind:int):
    """
    Вставляет строку sub_str в строку str на позицию ind
    """
    if ind >= len(string)-1:
        return string+sub_str
    elif ind>=len(string):
        return string
    elif ind <=0:
        return sub_str+string
    else:
        return string[0:ind] + sub_str + string[ind::]

def str_to_tex(string:str):
    expr = sp.sympify(string)
    latex_str = sp.latex(expr)
    return latex_str


def tex_to_sempy(expr:str):
    # принимает строку в формате латеха, возвращает то, что ест sympy
    res = expr
    res = res.replace("▯", "")
    res = res.replace("\over","/")
    res = res.replace("{", "(")
    res = res.replace("}", ")")
    res = res.replace("\sqrt", "sqrt")
    res = res.replace("^", "**")
    for i in range(0, len(res)):
        if res[i] == "[":
            degree_end = find_close_bracket(res, i)
            degree = res[i+1:degree_end]
            fond_end = find_close_bracket(res, degree_end+1)
            fond = res[degree_end+2 : fond_end]
            res = res[0:i-4] + fond + "**(1/" + degree + ")" + res[fond_end+1:]
            break
    return str(sp.sympify(res))
