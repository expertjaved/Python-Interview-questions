#list =[1,2,3,1,2,4] . find unique list for example [1234]


my_list = [1, 2, 3, 1, 2, 4]
unique_list = []
for elem in my_list:
    if elem not in unique_list:
        unique_list.append(elem)

print(unique_list)

#we can program in another way as well by using set() function
#my_list = [1, 2, 3, 1, 2, 4]
#unique_list = list(set(my_list))

#print(unique_list)
# understood it 