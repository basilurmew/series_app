//\sum_{n=1}^{\infty}{}


 		let global_row = document.getElementById('row').textContent;

	//--------------------------------------------------------------------------------------------

 	function find_close_bracket(expr , start_pos, br ){
 		// на вход подается выражение expr в котором нужно найти закрывающую скобку, для скобки, находящейся на позиции start_pos
 		// вид скобки передается в переменную br и может быть "{" , "[" , "(""
 		if (br == "{") cl_br = "}"
 		if (br == "[") cl_br = "]"
 		if (br == "(") cl_br = ")"
 		
		stack = [expr[start_pos]]
		let counter = start_pos + 1
		while(stack.length != 0){
			if(expr[counter] == br){
				stack.push(br)
			}
			if(expr[counter] == cl_br){
				stack.pop()
			}
			counter+=1
		}

		return counter - 1
 	}

 	//------------------------------------------------------------------------------------------------------------
	function find_open_bracket(expr , start_pos, br ){
	 		// вход - выражение expr в котором нужно найти индекс открывающей скобки, для скобки, находящейся на позиции start_pos
	 		// вид скобки передается в переменную br и может быть "}" , "]" , ")"
	 		if (br == "}") o_br = "{"
	 		if (br == "]") o_br = "["
	 		if (br == ")") o_br = "("
	 		
			stack = [expr[start_pos]]
			let counter = start_pos - 1
			while(stack.length != 0){
				if(expr[counter] == br){
					stack.push(br)
				}
				if(expr[counter] == o_br){
					stack.pop()
				}
				counter -=1
			}

			return counter + 1
	 	}


	//------------------------------------------------------------------------------------------------------------


	  function expression_borders(expr, end){
	 	symbols = "+-/*"
	 	digits_alphabet = "1234567890abcdefghijklmnopqrstuvwxyz"
	 	if(end<0) end = 0
	 	if (expr[end] != ")") {
	 		if (expr[end] == "}"){

	 			opn_br = find_open_bracket(expr, end, "}") // индекс открывающей скобки, после которой стоит каретка

	 			if (expr[opn_br-1] == "]"){ // в этом случае это означает, что там находится корень n-ой степени, он выглядит как \sqrt[...]{...}
	 				begin = find_open_bracket(expr, opn_br-1, "]") - 5
	 				return begin
	 			}
	 			else{

	 				if (expr[opn_br- 5] =="\\" )
	 				{

	 					return opn_br-5

	 				}//это будет корень \sqrt{...}

	 				else return opn_br // в этом случае просто надо вернуть то, что в скобках
	 			}
			}
			else{
			if (digits_alphabet.indexOf(expr[end]) !=-1 ){  // сейчас мы будем проверять числа
				begin = end
				while(digits_alphabet.indexOf(expr[begin]) !=-1 && begin>=0){
					begin -=1 // ищем, где начинается число
					console.log(begin)
				}
				return begin + 1
			}
			else {
				if (end == 0 || digits_alphabet.indexOf(expr[end]) == -1 ) return -1 // если поиск идет с начала выражение, либо с мат знака, то выражения нет
	 	
	 		}
	 	}
	 	
		}

	 	else return find_open_bracket(expr, end, ")")  // в данном случае выражением считаем то, что находится в скобках


	}
	 //------------------------------------------------------------------------------------------------------


	 function insert(str, new_sub, pos = global_row.indexOf("▯")){
	 	// заменяет символ строки str на позиции pos на подстроку new_sub
	 	first_part = str.slice(0, pos) 
	 	second_part = str.slice(pos+1)
	 	return first_part + new_sub + second_part
	 }


	 //-------------------------------------------------------------------------------------------------------

	 function move_kurs(expr, elem, pos_end){
	 	//перемещает элемент еlem в выражении expr на позицию pos
	 	pos_begin = expr.indexOf(elem)
	 	if (pos_begin!=-1){ //элемент в принципе должен быть в строке
	 		if(pos_begin < pos_end){
	 			first_part = expr.slice(0,pos_begin) + expr.slice(pos_begin+1, pos_end+1)
	 			console.log(first_part)
	 			second_part = elem + expr.slice(pos_end+1)
	 			console.log(second_part)
	 		}
	 		else{
	 			first_part = expr.slice(0,pos_end) + elem
	 			second_part = expr.slice(pos_end,pos_begin) + expr.slice(pos_begin+1)

	 		}
		}
		return first_part+second_part
	}
	 //-------------------------------------------------------------------------------------------------------

	 function update_global_row(){
	 	// обновляет внешний вид ряда на странице
	 	row.textContent = "\\[" + global_row + "\\] ";
 		console.log(global_row)
 		MathJax.typeset()
 		row_serv.value = global_row
	 }

	 //-------------------------------------------------------------------------------------------------------

 	function add_a_over_b(){
 		kurs_index = global_row.indexOf("▯")
 		if(kurs_index != -1){
 			let numirator_begin = expression_borders(global_row, kurs_index-1)
 			console.log(numirator_begin)
 			if (numirator_begin != -1 && global_row.length !=1){
 				first_part = global_row.slice(0,numirator_begin) + "{{" + global_row.slice(numirator_begin,kurs_index+1)
 				second_part = "}\\over{}}"+global_row.slice(kurs_index+1)
 				global_row = first_part + second_part
 			}

 			else{
 				 if(numirator_begin == -1){ // в этом случае выражения вообще нет и дробь нам надо добавить в то место, где каретка
 				 	first_part = global_row.slice(0,kurs_index) + "{{▯}\\over{}}" 
 					second_part = global_row.slice(kurs_index+1)
 					global_row = first_part + second_part
 				 }
			}

 		}
 		update_global_row()
 	}


 	//----------------------------------------------------------------------------------------------------------
 	
 	function add_a_sqrt(){
 		// каретка оказывается под корнем n-ой степени
 		kurs_index = global_row.indexOf("▯", 0);
 		if(kurs_index!=-1){
 			sqrt_str = "\\sqrt{▯}"
			global_row = insert(global_row, sqrt_str, kurs_index)

		}
 		update_global_row()
 	}


 	//-----------------------------------------------------------------------------------------------------------------------------


 	function add_a_n_sqrt(){
 		// каретка оказывается под корнем n-ой степени
 		kurs_index = global_row.indexOf("▯", 0);
 		if(kurs_index!=-1){
 			sqrt_str = "\\sqrt[n]{▯}"
			global_row = insert(global_row, sqrt_str, kurs_index)

		}
 		update_global_row()
 	}

 	//---------------------------------------------------------------------------------------------------------------


 	function add_a_power(){
 	    digits_alphabet_cl_br = "1234567890abcdefghijklmnopqrstuvwxyz)}"
 		kurs_index = global_row.indexOf("▯")
 		if(kurs_index != -1){
            if(digits_alphabet_cl_br.indexOf(global_row[kurs_index-1])!=-1){
 				 	first_part = global_row.slice(0,kurs_index) + "^{▯}"
 					second_part = global_row.slice(kurs_index+1)
 					global_row = first_part + second_part
 					}
 					update_global_row()
			}

 		}

    //----------------------------------------------------------------------------------------------------------------------------


    function clear_all(){

        global_row = "▯";
        update_global_row();
    }

 	//-----------------------------------------------------------------------------------------------------------------------------------

 	row.addEventListener('mousedown', function(event){
 		//14
 		if(global_row.indexOf("▯", 0) == -1){
 		  let tim = document.getElementById('row') ;
 		  global_row =  "▯"+global_row;
 		  tim.textContent = "\\[" + global_row + "\\]";
 		  update_global_row()
 		}
 	});

   //--------------------------------------------------------------------------------------------------------------------------------------

 	document.addEventListener('keydown', function(event) {
 		 kurs_index = global_row.indexOf("▯", 0);



		 if (event.code == 'ArrowRight' ) {
		 	// перемещает каретку вправо по выражению (не пытайтесь это понять)
		 	if (kurs_index != global_row.length - 1 ){
		 		if(global_row[kurs_index+1] == "}"){
		 			open_br = find_open_bracket(global_row, kurs_index+1, "}")
		 			if(global_row.slice(open_br-5,open_br) == "\\over")
		 				global_row = move_kurs(global_row,"▯", kurs_index+2)
		 			
		 			else{
		 				if (global_row.slice(open_br-5,open_br) == "\\sqrt" || global_row[open_br-1] == "]"  || global_row[open_br-1] == "^")
		 					global_row = move_kurs(global_row,"▯", kurs_index+1)	
		 				else{
		 					if (global_row.slice(kurs_index+2,kurs_index+7) == "\\over")
		 						global_row = move_kurs(global_row,"▯", kurs_index+7)		
		 					}	
		 				}
		 		}

		 		else{
		 			if(global_row.slice(kurs_index+1, kurs_index+6 ) == "\\sqrt")
		 				global_row = move_kurs(global_row, "▯", kurs_index+6)
		 			else{
		 				if (global_row[kurs_index+1] == "]" || global_row[kurs_index+1] == "^" || global_row[kurs_index+1] == "{")
		 					global_row = move_kurs(global_row, "▯", kurs_index+2)
		 				else{
		 					 				
		 						global_row = move_kurs(global_row, "▯", kurs_index+1)
		 				}
		 			}
		 		}

			}
			update_global_row()
		 }
	//----------------------------------------------------------------------------------------------------------------------------------------

		 if (event.code == 'ArrowLeft' ) {
		 	if(kurs_index > 0){
		 		if(global_row[kurs_index-1] =="{" ){
		 			if(global_row[kurs_index-2] == "^" || global_row[kurs_index-2] == "]")
		 				global_row = global_row = move_kurs(global_row,"▯", kurs_index-2)
		 			else{
		 				if (global_row.slice(kurs_index-6, kurs_index-1) == "\\sqrt") 
		 					global_row = global_row = move_kurs(global_row,"▯", kurs_index-6)	
		 				else{
		 					if (global_row.slice(kurs_index-6, kurs_index-1) == "\\over") 
		 						global_row = global_row = move_kurs(global_row,"▯", kurs_index-7)		

		 					else{
			 					if (global_row[kurs_index-2] == "{")  
			 						global_row = move_kurs(global_row,"▯", kurs_index-2)
		 				}
		 					
		 				}
		 			}

		 		}

		 		else{
		 			if(global_row[kurs_index-1] =="}"){
		 				open_br = find_open_bracket(global_row, kurs_index-1, "}")
		 				if (global_row[open_br-1] == "]" || global_row.slice(open_br-5,open_br) == "\\sqrt" || global_row[open_br-1] == "^")
		 					global_row = move_kurs(global_row, "▯", kurs_index-1)
		 				else{
		 					global_row = move_kurs(global_row, "▯", kurs_index-2)
		 				}

		 			}
		 			else{
		 				if( global_row[kurs_index-1] == "[")
		 					global_row = move_kurs(global_row,"▯", kurs_index-6)
		 				else{
		 					global_row = move_kurs(global_row, "▯", kurs_index-1)
		 				}
		 			}

		 		}

		 	}

		 	update_global_row()
		 }

		//-------------------------------------------------------------------------------------------------------------

		if (event.code.slice(0,event.code.length-1) == 'Digit' && event.shiftKey == false && event.ctrlKey == false  ){
			let number = event.code[5]
			let first_part = global_row.slice(0,kurs_index) + number + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}
		if (event.code.slice(0,event.code.length-1) == 'Key' && event.shiftKey == false && event.ctrlKey == false  ){
			let letter = event.code[3]
			let first_part = global_row.slice(0,kurs_index) + letter.toLowerCase() + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}

		

		if (event.code == 'Equal' && event.shiftKey == true) {
			let first_part = global_row.slice(0,kurs_index) + "+" + "▯"   
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}

		if (event.code == 'Minus') {
			let first_part = global_row.slice(0,kurs_index) + "-" + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}
		if (event.code == 'Slash' && event.ctrlKey == false){
			let first_part = global_row.slice(0,kurs_index) + "/" + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}
		if (event.code == 'Digit8' && event.shiftKey == true) {
			let first_part = global_row.slice(0,kurs_index) + "*" + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}
		if (event.code == 'Digit9' && event.shiftKey == true) {
			let first_part = global_row.slice(0,kurs_index) + "(" + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}
		if (event.code == 'Digit0' && event.shiftKey == true) {
			let first_part = global_row.slice(0,kurs_index) + ")" + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}

		if (event.code == 'Digit1' && event.shiftKey == true) {
			let first_part = global_row.slice(0,kurs_index) + "!" + "▯"  
			let second_part = global_row.slice(kurs_index+1)
			global_row = first_part + second_part
			update_global_row()
		}

		if (event.code == 'Digit6' && event.ctrlKey == true) {
			add_a_power()
		}
		if (event.code == 'Slash' && event.ctrlKey == true) {
			add_a_over_b()
		}
		if (event.code == 'Digit2' && event.ctrlKey == true) {
			add_a_sqrt()
		}
	    if (event.code == 'Backspace'){
			if(kurs_index>0){
				if(global_row[kurs_index-1] == "}"){
					open_br == find_open_bracket(global_row, kurs_index-1, "}")
					if(global_row.slice(open_br-5, open_br) == "\\sqrt" || global_row[open_br-1] == "]" || global_row[open_br-1] == "^")
						global_row = move_kurs(global_row,"▯", kurs_index-1)

					else{
						if(global_row[kurs_index-2] == "}")//пропиши, если там будет несколько стрелок
							global_row = move_kurs(global_row,"▯", kurs_index-2)
					}

				}
				//-------------- тут был иф, если перед кареткой стоит }

				else{

					if (global_row[kurs_index-1] == "{") {
						cl_br = find_close_bracket(global_row, kurs_index-1, "{")
						if(global_row[kurs_index-2] == "^"){
							if(cl_br!=kurs_index+1)
								global_row = move_kurs(global_row,"▯", kurs_index-2)
							else{
								first_part = global_row.slice(0,kurs_index-2) + "▯"
								second_part = global_row.slice(kurs_index+2)
								global_row = first_part + second_part
							}

						}
						// теперь, если открывающая скобка принадлежит корню

						else{
							if (global_row.slice(kurs_index-6, kurs_index-1) == "\\sqrt" || global_row[kurs_index-2] == "]") {
								close_br = find_close_bracket(global_row, kurs_index-1, "{")
								begin_sqrt = expression_borders(global_row, close_br)
								first_part = global_row.slice(0, begin_sqrt)
								second_part = global_row.slice(kurs_index, close_br) + global_row.slice(close_br+1)
								console.log( global_row.slice(kurs_index, cl_br))
								global_row = first_part + second_part
							}
							else{
								if(global_row.slice(kurs_index-6, kurs_index-1) == "\\over"){   //случай знаменателя
									if (global_row[kurs_index+1] != "}") {
										global_row = move_kurs(global_row, "▯", kurs_index-7)
									}
									else{ //если знаменатель пустой, то нам надо убрать дробь и оставить только числитель
										open_br = find_open_bracket(global_row, kurs_index-7, "}")
										first_part = global_row.slice(0,open_br-1) + global_row.slice(open_br+1,kurs_index-7) + "▯"
										second_part = global_row.slice(kurs_index+3)
										global_row = first_part + second_part
									}


								}
								else{
									close_br = find_close_bracket(global_row, kurs_index-1, "{")
									if(close_br == kurs_index+1){
										if(global_row[kurs_index+8]=="}"){
											first_part = global_row.slice(0,kurs_index-2) + "▯"
											second_part = global_row.slice(kurs_index+10)
											global_row = first_part+second_part

											}
										else{
											close_br = find_close_bracket(global_row, kurs_index+7, "{")
											first_part = global_row.slice(0,kurs_index-2)
											second_part = "▯"+ global_row.slice(kurs_index+8, close_br)
											global_row = first_part+second_part
										}
									}
								}
							}

						}


						}
						else{
							if(global_row[kurs_index-1] =="[")
								global_row = move_kurs(global_row,"▯", kurs_index-6)
							else
								global_row = insert(global_row,"", kurs_index-1 )
						}

					}



				}


			}
			update_global_row()
		

		 console.log(event.code)
	});