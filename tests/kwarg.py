def param_overload(x, **kwargs):
    assert x == 'x'
param_overload(x='x')

# lune environments dont have `game` so __name__ == nil
if __name__ == None:
    def param_overloadfail(x):
        assert x == None
    param_overloadfail(x='x')
else:
    print("the above code is a feature only provided by roblox-py, cannot do it with python")

def f(depth, **kwargs):
    if depth > 10:
        return
    
    assert kwargs.get('hi') == 'hi'
    
    kwargs['depth'] += 1
    f(**kwargs)

f(depth=0, **{'hi': 'hi'})