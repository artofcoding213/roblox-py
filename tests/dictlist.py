d = { 'hello': 'world' }
d.foo = 'bar'

assert d.hello == 'world'
assert d.foo == 'bar'

# we're doing stricter checks on lists because i just added a new list() std entry
# to support 0-based indexing,
# and i'm assuming the dict() implementation was well-tested

l = [1, 2]
l.append(3)

assert 1 in l
assert 2 in l
assert 3 in l

assert l[0] == 1
assert l[1] == 2
assert l[2] == 3
assert len(l) == 3

assert l.pop() == 3
assert len(l) == 2

# l = [1, 2] again :)

l.insert(0, 5)
assert l[0] == 5

# l = [5, 1, 2]
l.reverse()

assert l[0] == 2
assert l[1] == 1
assert l[2] == 5

assert l == [2, 1, 5]
assert l != [6, 7, 8]
assert 2 in l
assert 67 not in l

l.sort()
assert l == [5, 2, 1]

words = ["apple", "kiwi", "banana"]
words.sort(key=len)
assert words == ["banana", "apple", "kiwi"]

expected_i = 0
for i, word in enumerate(words):
    assert i == expected_i
    assert words[expected_i] == word
    expected_i += 1

# tuples are readonly lists under the hood
t = (1, 2)
assert t[0] == 1
assert t[1] == 2

try:
    t.append(67)
    print("this should error: tuples are readonly")
except:
    pass