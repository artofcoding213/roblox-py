a = [
    (2, 3, 4),
    (1, 0, 0),
]

b = [
    (0, 1000),
    (1, 100),
    (0, 10),
]

out = a @ b # [(3, 2340), (0, 1000)]
assert out[0][0] == 3
assert out[0][1] == 2340
assert out[1][0] == 0
assert out[1][1] == 1000

try:
    a = [ (1, 2) ]
    b = [ (1, 2) ]
    out = a@b

    print("should've errored with incompatible matrix sizes")
except:
    pass