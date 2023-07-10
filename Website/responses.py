import json
from time import sleep

def generate_responses(message):
    with open("codes.json") as f:
        data = json.load(f)

    final_code = []
    str_to_return = ""
    user_inp = message.lower() if message else ""
    sleep(2)
    if len(user_inp) == 0:
        str_to_return = "Please enter a valid input"
    elif user_inp in data:
        final_code += [data[user_inp.lower()]]
    elif len(user_inp) > 1:
        user_inp = user_inp.split(" ")
        for i in user_inp:
            if i in data:
                final_code += [data[i]]
            else:
                str_to_return = "Please enter a valid input"
    else:
        str_to_return = "Please enter a valid input"


    if len(final_code) == 1:
        codeToPrint = final_code[0]
        return codeToPrint, True
    elif final_code:
        string = ""
        for i in final_code:
            string += i
            string += '\n\n'

        return string, True
    else:
        return str_to_return, False