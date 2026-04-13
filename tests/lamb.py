x = lambda *args, **kwargs: args[0] + args[1] + kwargs.get('c')
assert x(1, 2, c=3) == 6

y = lambda *args: x(*args, c=3)
assert y(1, 2) == 6