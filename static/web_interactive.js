


 let current_step;
        let step = 0;
        next_step_gen()

        async function next_step_gen(){
            let promise = await fetch('/solve',{
            'method': 'POST',
            'body':step
            });
            let serv_answer = await promise.json();
            current_step = {
                question: serv_answer["question"],
                true_actor_answer :  serv_answer["true_actor_answer"],
                false_actor_answer : serv_answer["false_actor_answer"],
                intermediate_result: serv_answer["intermediate_result"],
                true_answer: serv_answer["true_answer"],
                sign:serv_answer["sign"],
                vars_of_answers: serv_answer["vars_of_answers"]
            }
           console.log(current_step["vars_of_answers"])
           hide_and_show(current_step['sign'])
           document.getElementById("question").textContent = current_step['question']
           document.getElementById('buttons').style.display = "flex"
           document.getElementById('question').style.display = "flex"
           document.getElementById('go').style.display = "none"
           document.getElementById('intermediate_result').style.display = "none"
           step+=1
        }



        function try_to_ask_sign_3(ans){
            if(ans == current_step['true_answer']){

                document.getElementById('intermediate_result').textContent = current_step['intermediate_result']
                document.getElementById('answer').textContent = current_step['true_actor_answer']
                document.getElementById('intermediate_result').style.display = "flex"
                document.getElementById('buttons').style.display = "none"
                document.getElementById('question').style.display = "none"
                if (ans != 1 && ans != -1)
                    document.getElementById('go').style.display = 'flex';
                MathJax.typeset()
            }
            else{
                document.getElementById('answer').textContent = current_step['false_actor_answer']
            }
        }

       function try_to_ask_sign(sign){
            if(sign == current_step['sign']){

                 hide_and_show('probably')
                 document.getElementById('answer').textContent = "Вы выбрали верный признак";
                 document.getElementById('question').textContent = "Что покажет выбранный вами признак в этом случае?";
                 document.getElementById(current_step['sign']).style.display = "none"
               }else{
                document.getElementById('answer').textContent = current_step['false_actor_answer']
            }
        }

        function put_variants_of_answers(sign){
            document.getElementById("converg").textContent = current_step['vars_of_answers'][0]
            document.getElementById("not_work").textContent = current_step['vars_of_answers'][1]
            document.getElementById("diverg").textContent = current_step['vars_of_answers'][2]

        }


        function hide_and_show(sign){
            if (sign == 'nth'){
                put_variants_of_answers(sign)
                document.getElementById('tf_nw').style.display = 'none'
                document.getElementById('signs').style.display = 'none'
                document.getElementById('tf').style.display = 'flex'
            } else
                if(sign == 'harm' || sign == 'geom' || sign == 'probably'){
                put_variants_of_answers(sign)
                document.getElementById('tf_nw').style.display = 'flex'
                document.getElementById('signs').style.display = 'none'
                document.getElementById('tf').style.display = 'none'
            }

            else{
                document.getElementById('tf_nw').style.display = 'none'
                document.getElementById('signs').style.display = 'flex'
                document.getElementById('tf').style.display = 'none'
            }

        }