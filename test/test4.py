#coding=utf-8
#快速排序
def quicksort(arr):
    if len(arr) < 2:
        return arr
    else:
        pivot = arr[0]
        less = []
        greater = []
        for i in arr[1:]:
            if i <= pivot:
                less.append(i)
            else:
                greater.append(i)

        return quicksort(less) + [pivot] + quicksort(greater)

print quicksort([1,5,3,8,12,57,4,5])