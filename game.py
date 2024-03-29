from series import *
from sign_comparison import *
from parser import str_to_tex


def solve_series_by_sign(ser: Series, sign: str):
    if sign == "Необходимое условие":
        return nth_test(ser)
    elif sign == "Радикальный признак Коши":
        return is_cauchy_test(ser)
    elif sign == "Признак Даламбера":
        return is_dalamber_test(ser)
    elif sign == "Признак Раабе":
        return is_raabe_test(ser)
    elif sign == "Признак Бертрана":
        return is_bertran_test(ser)
    # elif sign == ""


def intermediate_result(expr:list, ser:Series):
    res = expr[0]
    for i in range(1, len(expr ) - 1):
        res += "= \\lim\\limits_{" + ser.get_str_var() + "\\to\\infty}" + "({" + str_to_tex(expr[i])+"})"
    return res + "=" + expr[-1] + "\\]"