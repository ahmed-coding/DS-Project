import string
import random


def generit_random_code():
    list_code = string.digits
    lenth = len(list_code)
    count = 0
    code = ''
    while count <= 3:
        index = random.randint(0, lenth-1)
        code += list_code[index]
        count += 1
    # print(len(str(int(code))))
    if len(str(int(code))) != 4:
        generit_random_code()
    return int(code)
