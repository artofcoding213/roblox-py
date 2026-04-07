assert isinstance([1, 2, 3], list)
assert isinstance({'foo': 'bar'}, dict)

class a():
    descend_a = True

    def __init__(self):
        self.x = 'hello'

class b(a):
    descend_b = True
    
    def __init__(self):
        assert super().descend_a == True

        super().__init__()
        assert self.x == 'hello'

assert issubclass(b, a)

c = b()
assert isinstance(c, b)
assert isinstance(c, a)
assert c.descend_a
assert c.descend_b