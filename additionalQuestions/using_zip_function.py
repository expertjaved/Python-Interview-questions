# The zip function in python is a nifty tool for combining multiple iterables into a single
# iterable of tuples.It takes in two or more iterables as arguments and returns an iterator 
#that generates tuples containing elements from each iterable , paired together

numbers =[1,2,3]
letters =['a','b','c'] 
result = zip(numbers,letters)
#now lets print the result
for item in result:
 print(item)
 #output
 #(1,'a')
 #(2,'b')
 #(3,'c')
 