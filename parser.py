def find_open_bracket(string:str, ind:int):
    """Возвращает индекс скобки в строке string,
       являющейся открывающей для скобки на позиции ind"""
    if string[ind] == ")":
        o_br = "("
        cl_br = "]"
    elif string[ind] == "]":
        o_br = "["
        cl_br = "]"
    stack = [string[ind]]
    counter = ind - 1
    while len(stack) !=0:
        if string[counter] == o_br:
            stack.pop()
        elif string[counter] == o_br:
            stack.append(cl_br)
        counter -= 1
    return counter + 1

def replace_by_index(string:str, sub:str, ind:int):
    """принимает строку string, подстроку sub и индекс ind
       заменяет символ, находящийся на позиции ind в строке string на sub"""
    string = string[0:ind] + sub + string[ind+1:]
    return string




def find_close_bracket(string:str, ind:int):
    """Возвращает индекс скобки в строке string,
       являющейся закрывающей для скобки на позиции ind"""
    if string[ind] == "(":
        o_br = "("
        cl_br = ")"
    elif string[ind] == "[":
        o_br = "["
        cl_br = "]"
    stack = [string[ind]]
    counter = ind + 1
    while len(stack) !=0:
        if string[counter] == cl_br:
            stack.pop()
        elif string[counter] == o_br:
            stack.append(cl_br)
        counter += 1
    return counter - 1


def str_to_tex(string:str):
    string = string.replace("**", "^")
    for i in range(0,len(string)):
        if string[i:i+4] == "sqrt":
            if string[i+4] =="(":
                cls = find_close_bracket(string,i+4)
                string = replace_by_index(string, "}", cls)
                string = replace_by_index(string, "{", i+4)
    string = string.replace("(", "{")
    string = string.replace(")", "}")
    string = string.replace("sqrt", "\sqrt")
    string = string.replace("/", "\over ")
    return "{" + string + "}"

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
    return res

