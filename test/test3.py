#coding=utf-8
#递归
def countdown (i):
    print i
    if i <= 1:
        return
    else:
        countdown(i-1)

#countdown(5)

def factorial (i):
    if i == 1:
        return 1
    else:
        return i * factorial(i-1)

print factorial(5)