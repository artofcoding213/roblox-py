def myrange(num):
    curr = 1

    while curr <= num:
        yield curr*2
        curr += 1

myrange_num = 4
myrange_exp = [2, 4, 6, 8]

# note: enumerate() does nothing here. maybe make generators emit an iterator?
for i, x in enumerate(myrange(myrange_num)):
    assert myrange_exp[i] == x

yieldstr_exp = ['h', 'i', ' ', 'm', 'o', 'm']

def yieldstr():
    yield 'h'
    yield 'i'
    yield ' '
    yield 'm'
    yield 'o'
    yield 'm'

for i, x in enumerate(yieldstr()):
    assert yieldstr_exp[i] == x