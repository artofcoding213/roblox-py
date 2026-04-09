with (x := 5) as y:
    assert x == 5
    assert y == 5

def f(z):
    assert z['var']['var'] == 67

f({
    'var': {
        'var': (z := 67),
    }
})

assert z == 67