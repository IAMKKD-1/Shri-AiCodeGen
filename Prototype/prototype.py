import time
import json

with open("codes.json") as f:
    data = json.load(f)

final_code = []

user_inp = input("Enter the program to generate: ")
user_inp = user_inp.lower()
if len(user_inp) == 0:
    print("Please enter a valid input")
elif user_inp in data:
    final_code += [data[user_inp.lower()]]
elif len(user_inp) > 1:
    user_inp = user_inp.split(" ")
    for i in user_inp:
        if i in data:
            final_code += [data[i]]
else:
    print("Please enter a valid input")


if len(final_code) == 1:
    codeToPrint = final_code[0]
    for i in codeToPrint:
        print(i, end="")
        time.sleep(0.05)
else:
    for i in final_code:
        codeToPrint = i
        for j in codeToPrint:
            print(j, end="")
            time.sleep(0.07)
        print("\n") 