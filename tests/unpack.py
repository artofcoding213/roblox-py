l = [1, 2]

x, y = l
assert x == 1 and y == 2

def f():
    return 1, 2, 3

m, n, o = f()
assert m == 1 and n == 2 and o == 3

try:
    # this is a python semantic, not a luau one, as x = 1, y = 2 in luau
    x, y = [1, 2, 3]
    print("this should error: not unpacking enough values")
except:
    pass

# test of for loop unpacking
nested = [[1, 2], [3, 4]]

for i, [a, b] in enumerate(nested):
    if i == 0:
        assert a == 1 and b == 2
    else:
        assert a == 3 and b == 4