# this was an old bug i had to patch

class test():
    def x(self):
        # 'i' wasn't local here, took me forever to fix it
        i = 'foo'

test().x()
assert i == None

# same thing here
def foo(x):
    x = 'foo'
    y = 'hello'

foo('bar')
assert x == None and y == None