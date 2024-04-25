sign_list = ["dalamber","raabe", "cauchy", "bertran", "gauss", "integral"]

a_d = {"nth":["Необходимое условие не выполняется.Данный ряд расходится.", "Необходимое условие выполняется, думаем дальше.", ""],
            "geom":["Данный ряд расходится как геометрический.", "Данный ряд не является геометрическим.", "Данный ряд сходится как геометрический."],
            "harm":["Данный ряд расходится как обобщенный гармонический.","Данный ряд не является обобщенным гармоническим.","Данный ряд сходится как обобщенный гармонический."],
            "dalamber": ["Данный ряд расходится по признаку Даламбера","Признак Даламбера не работает. Думаем дальше.", "Данный ряд сходится по признаку Даламбера."],
            "cauchy":["Данный ряд расходится по Радикальному признаку Коши.","Данный признак ничиго не может сказать о сходимости данного ряда.Думаем дальше.","Данный ряд сходится по Радикальному признаку Коши."],
            "raabe":["Данный ряд расходится по признаку Раабе.","Данный признак ничего не может сказать о сходимости данного ряда.Думаем дальше.","Данный ряд сходится по признаку Раабе."],
            "bertran":["Данный ряд расходится по признаку Бертрана", "Признак Бертрана не работает, думаем дальше.", "Данный ряд сходится по признаку Бертрана"],
            "integral":["Данный ряд расходится по интегральному признаку.","Для данного ряда не выполнены условия интегрального признака.","Данный ряд сходится по интегральному признаку Коши."],
            "gauss":["Данный ряд сходится по признаку Гаусса.","","Данный ряд расходится по призаку Гаусса."]}
bin_ans = "Атата, неа, подумай лучше."
sign_ans = "Не, этот признак не подходит, подумай и выбери другой."

vars_of_answers = {
    "nth":["Выполняется", "Не выполняется"],
    "geom" : ["Сходится", "Таковым не является", "Расходится"],
    "harm":["Сходится", "Таковым не является", "Расходится"],
    "dalamber":["Сходится", "Не сработает", "Расходится"]
    ,"raabe":["Сходится", "Не сработает", "Расходится"]
    , "cauchy":["Сходится", "Не сработает", "Расходится"]
    , "bertran":["Сходится", "Не сработает", "Расходится"]
    ,"gauss":["Сходится", "Не сработает", "Расходится"]
    ,"integral":["Сходится", "Не удовлетворяет условиям", "Расходится"]
}