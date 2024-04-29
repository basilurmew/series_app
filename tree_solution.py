from sign_comparison import *from tree_form import *from series import Seriesdef bertarn_branch(s, d):    """    Функция, которая реализует блок ветку дерева, корнем которого является признак Бертрана    Args:        s(Series): числовой ряд        d(dict): словарь решения    Returns:    """    bertran = is_bertran_test(s)    d["bertran"] = [bertran.get_ans(), bertran.get_steps()]    if bertran.get_ans() == 1:        #print("Данный ряд сходится по признаку Бертрана")        return d    elif bertran.get_ans() == -1:        #print("Данный ряд расходится по признаку Бертрана")        return d    else:        #print("Признак Бертрана не помог определить сходимость/расходимость ряда, поэтому попробуем использовать признак Гаусса")        gauss = is_gauss_test(s)        d["gauss"] = [gauss.get_ans(), gauss.get_steps()]        if gauss.get_ans() == 1:            #print("Данный ряд сходится по признаку Гаусса")            return d        elif gauss.get_ans() == -1:            #print("Данный ряд расходится по признаку Гаусса")            return d        else:            #print("Что-то пошло не так и мы не определили сходится ли ряд")            return ddef cauchy_branch(s, d):    """    Функция, которая реализует ветку дерева, корнем которого является Радикальный признак Коши    Args:        s(Series): числовой ряд        d(dict): словарь решений    Returns:    """    cauchy = is_cauchy_test(s)    d["cauchy"] = [cauchy.get_ans(), cauchy.get_steps()]    if cauchy.get_ans() == -1:        #print("Данный ряд расходится по Радикальному признаку Коши")        return d    elif cauchy.get_ans() == 1:        #print("Данный ряд сходится по Радикальному признаку Коши")        return d    else:        #print("Радикальный признак не помог определить сходимость/расходимость ряда")        #print("Поэтому давайте проверим содержит ли общий член ряда логарифм")        if is_log(s.get_expr()):            #print("Общий член ряда содержит логарифм, поэтому проверим является ли общий член ряда подходящим "             #     "для Интегрального признака Коши")            integral = is_integral_test(s)            d["integral"] = [integral.get_ans(), integral.get_steps()]            if integral.get_ans() == 1:                #print("Данный ряд сходится по Интегральному признаку Коши")                return d            elif integral.get_ans() == -1:                #print("Данный ряд расходится по Интегральному признаку Коши")                return d            else:                return bertarn_branch(s, d)        else:            #print("Общий член ряда не содержит логарифм, поэтому попробуем использовать признак Раабе")            raabe = is_raabe_test(s)            d["raabe"] = [raabe.get_ans(), raabe.get_steps()]            if raabe.get_ans() == 1:                #print("Данный ряд сходится по признаку Раабе")                return d            elif raabe.get_ans() == -1:                #print("Данный ряд расходится по признаку Раабе")                return d            else:                #print("Признак Раабе не помог определить сходитсь/расходисть ряда, поэтому будем использовать признак Бертрана")                return bertarn_branch(s,d)def left_tree(s, d):    """    Фукнция, которая реализует левый блок дерева решений    Args:        s(Series): числовой ряд        d(dict): словарь решений    Returns:    """    #print("Проверим сходится ли ряд как обобщенный гармонический")    harm = is_harmonic_test(s)    d["harm"] = [harm.get_ans(), harm.get_steps()]    if harm.get_ans() == -1:        #print("Данный ряд расходится как обобщенный гармонический")        return d    elif harm.get_ans() == 1:        #print("Данный ряд сходится как обобщенный гармонический")        return d    else:        #print("Данный ряд не является обобщенным гармоническим, поэтому давайте думать дальше")        #print("Давайте проверим содержит ли общий член ряда факториал")        if is_factorial(s.get_expr()):            #print("Общий член ряда содержит факториал, поэтому попробуем использовать признак Даламбера")            dalamber = is_dalamber_test(s)            d["dalamber"] = [dalamber.get_ans(), dalamber.get_steps()]            if dalamber.get_ans() == 1:                #print("Данный ряд сходится по признаку Даламбера")                return d            elif dalamber.get_ans() == -1:                #print("Данный ряд расходится по признаку Даламбера")                return d            else:                #print("Признак Даламбера не помог определить сходимость/расходимость ряда")                #print("Поэтому попробуем использовать Радикальный призрак Коши")                return cauchy_branch(s, d)        else:            #print("Общий член ряда не содержит факториал, поэтому попробуем использовать Радикальный признак Коши")            return cauchy_branch(s, d)def solution_tree(s):    """    Функция, которая является деревом решений    Args:        s(Series): числовой ряд    Returns:        dict: словарь, у которого ключ - признак, значение - спискок(информация о сходимости        а также промежуточные результаты)    """    #print буду выводить пока что для себя    d = dict()    #print("Проверка выполения необходимого условия сходимости ряда")    nth = nth_test(s)    d["nth"] = [nth.get_ans(), nth.get_steps()]    if nth.get_ans() == 0:        #print("Необходимое условие выполняется, поэтому давайте думать дальше")        #print("Давайте проверим является ли данный ряд геометрическим")        geom = is_geometric_test(s)        d["geom"] = [geom.get_ans(),geom.get_steps()]        if geom.get_ans() == -1:            #print("Данный ряд расходится, как геометрический, так как q >= 1")            return d        elif geom.get_ans() == 1:            #print("Данный ряд сходится, как геометрический, так как q < 1")            return d        else:            #print("Данный ряд не является геометрическим, поэтому давайте думать дальше")            #print("Проверим, является ли данный ряд положительным")            if is_positive(s):                #print("Данный ряд положительный")                return left_tree(s, d)            else:                #print("Данный ряд неположительный")                #print("Пока что в разработке правая ветка дерева")                return d    else:        #print("Необходимое условие не выполняется, данный ряд расходится")        return d#s = sp.sympify("5**(n - 1)/ n!")#s = sp.sympify("ln(n/(n - 1)) **(3/2) /(sqrt(n) - sqrt(n - 1))")#s = sp.sympify("n!* exp(n) / n**(n + 2)")#s = sp.sympify("1/(n*ln(n)**4)")# s = sp.sympify("1/(2*n + 3)**(7/6)")