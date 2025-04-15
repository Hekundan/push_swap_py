def get_sorted(to_sort):
    to_return = []
    for i in range(len(to_sort)):
        to_return.append(0)
        for j in to_sort:
            if j < to_sort[i]:
                to_return[i]+=1
    return to_return

