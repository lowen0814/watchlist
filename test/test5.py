#coding=utf-8
voted = {} #等同于 voted = dict()
def check_voter(name):
    if voted.get(name):
        print name + " ,he has voted,kick them out"
    else:
        voted[name] = True
        print name + " ,let him vote"

check_voter("tom")
check_voter("lucus")
check_voter("tom")

