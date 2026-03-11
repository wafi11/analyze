import time

def difference_list_and_dict():
    t1 = time.time()
    my_list = []
    for i in range(1000000):
        my_list.append(int(i//(2**(1/2))))
    t2 = time.time()
    print("Time taken to create List:", t2-t1, "seconds")
    print(my_list)

    t1 = time.time()
    my_dict = {}
    for i in range(1000000):
        my_dict[int(i//(2**(1/2)))] = i

    t2 = time.time()
    print("Time taken to create Dictionary:", t2-t1, "seconds")
    print(my_dict)
