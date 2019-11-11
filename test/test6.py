#coding=utf-8
from collections import deque
graph = {}
graph["you"] = {"a", "b", "c"}
graph["b"] = {"c", "d"}
graph["a"] = {"e", "f"}
graph["c"] = []
graph["d"] = []
graph["e"] = []
graph["f"] = []

def search(name):
    search_queue = deque()
    search_queue += graph[name]
    searched = []

    while search_queue: #只要队列不为空
        person = search_queue.popleft()
        if person not in searched:
            if person_is_seller(person):
                print person + " is a seller"
                return True
            else:
                search_queue += graph[person]
                searched.append(person)
    return False
def person_is_seller(name):
    return name[-1] == 'd'

print graph
search("you")


