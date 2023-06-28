import json
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def generate_responses(message):
    with open("codes.json") as f:
        data = json.load(f)

    final_code = []
    str_to_return = ""
    user_inp = message.lower() if message else ""

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
        highlighted_code = highlight(codeToPrint, PythonLexer(), HtmlFormatter())
        return highlighted_code.replace("\n", "<br>"), True
    elif final_code:
        string = ""
        for i in final_code:
            highlighted_code = highlight(i, PythonLexer(), HtmlFormatter())
            string += highlighted_code.replace("\n", "<br>") + "<br><br>"
        return string, True
    else:
        return str_to_return, False