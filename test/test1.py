#coding=utf-8
#二分查找
# O(log n)
def binary_serch(list, item):
    low = 0
    high = len(list)-1

    while(low <= high):
        mid = (low + high)/2
        guess = list[mid]

        if guess == item:
            return list[mid]
        if guess > item:
            high = mid -1
        else :
            low = mid + 1

    return None

my_list = [1,3,5,6,34,67,78,9]
print binary_serch(my_list,6)
print binary_serch(my_list,7)


