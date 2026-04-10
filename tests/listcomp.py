l = [3 for x in range(3)]
assert l[0] == 3 and l[1] == 3 and l[2] == 3

# [(4, 4, 4), (4, 4, 4), (4, 4, 4)]
l = [[x+1 for x in l] for x in l]
assert l[0][0] == 4 and l[0][1] == 4

l = [[1, 2], [3, 4]]
l2 = [[x+1, y+1] for [x, y] in l]
assert l2[0] == [2, 3] and l2[1] == [4, 5]