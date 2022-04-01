# to learn
# all list type problems
# Python basics
# tricky python one liners
# Deep python tricks
# data structures in Python
# classes & OOPS
# external libs for datastructures in Python
# https://realpython.com/inner-functions-what-are-they-good-for/
# https://stackabuse.com/python-nested-functions/
# https://treyhunner.com/2019/05/python-builtins-worth-learning/

# z = 0
# def global_test(x):
#     # global need to be declared first and used later
#     # global puts the varibale in global scope. Var can be accessed outside the scope of the function
#     # global lets you MODIFY global variables inside a function 
#     global y
#     # z = z + 1 # this can't happen since z is a global one and we're MODIFYING it locally. ACCESSING a global variable is possible but MODIFYING is not possible without global keyword declaration
#     global z
#     z = z + 1 # now you can MODIFY "z"
#     y = x + 1
#     print(z)
# x=10
# global_test(x)
# print(y)



# dont use global unless necessary coz they're confuisng and hard to debug
# https://www.simplilearn.com/tutorials/python-tutorial/global-variable-in-python
# 
# def a():
#     g=1
#     def b():
#         global g
#         g=2
#     print("Before b() ", g) # 1
#     b()
#     print("After b()", g) # 1: here the o/p is 1 not 2. Why? global keyword changes things only in CURRENT function scope and GLOBAL scope. It doesn't work on intermediate scopes ( here in the scope of a() ).
# a()
# print(" Outside ", g) # 2


# global_weird
# def a():
#     g=1
#     def b():
#         global g
#         g=2
#         def c():
#             global g
#             g=3
#         c()
#         print("c", g) #3
#     b()
#     print("b", g) #1 
# a()
# print("a", g) #3
# explanation below
# When you do g=1 in a() it creates a new LOCAL (only GLOBAL variables can be accessed by global scope) variable to that function. When you do global g in b() and c() it makes g refer to the global variable (which doesn't yet exist when running b). So c, b and the global scope all refer to the same g (which is 3 after running c) while a refers to its local g which never changed and is still 1.
# Changing global to nonlocal will make both prints of c and b to print 3, but now will make a NameError for the last print as there is no g in the global scope.
# Alternatively, adding global g to the start of a, will have all three prints print 3.

# nested functions

# predictable output
# def outer():
#     print("outer-start")
#     def inner():
#         print("inner")
#     inner()
#     print("outer end")
# outer()

# Python closures: an application of nested functions

from ast import comprehension


def adder(how_much):
    def add(input):
        return input + how_much
    # we return a copy off 'add' function which "remembers" the value of "how_much"
    return add
# below two are references to functions. Value of how_much is stored in these functions. When we call them again, they call add()
this_will_add_three = adder(3)
this_will_add_four = adder(4)

print(this_will_add_three(1)) # 4
print(this_will_add_three(2)) # 5

print(this_will_add_four(1)) # 5
print(this_will_add_four(2)) # 6

# nonlocal - this one is liek global but works inside a function

def myfunc1():
  x = "John"
  def myfunc2():
    x = "hello" # this is local to myfunc2
  myfunc2()
  return x

print(myfunc1()) # here o/p: is "John"

def myfunc1():
  x = "John"
  def myfunc2():
    nonlocal x
    x = "hello" # we are accessing the "x" of myfunc1() by making "x" nonlocal
  myfunc2()
  return x

print(myfunc1()) # here o/P is: "hello"

# list comprehension
x = [(1,2),(3,4)]
y = [j for i in x for j in i ] # this is just a nested for loop
# y is [1,2,3,4]
# newlist = [expression for item in iterable if condition == True] (expression could be variable or an expression such as a*a)
x = [1,2,3,4]
# list comprehension is just like range. start from first and ignore the last ( i.e return till last before that)
x[:-1] # show from beginning to -2  ( ignore -1) ==> [1,2,3]
x[-4:] # show from -4 to last ==> [1,2,3,4]
x[-3:-1] # show from -3 to -2 (ignore -1)==> [2,3]
# use append function to add an element to the end of the list