hi = 'hi'
assert hi[0:1] == 'h'
assert hi[1:2] == 'i'
assert hi[0:2] == 'hi'
assert hi[0:-1] == 'hi'

l = [1, 2, 3]
assert l[0:1] == [1]
assert l[0:2] == [1, 2]
assert l[0:3] == [1, 2, 3]
assert l[-2:-1] == [3]