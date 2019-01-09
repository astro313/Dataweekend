'''

n     n/2    n%2
1      0      1

2      1      0
1      0      1

4      2      0
2      1      0
1      0      1


'''



def decimal2binary(n):
    if n == 0:
        return '0'
    else:
        # attaching the str of (n%2) to front of the str(n%2)
        return decimal2binary(n/2) + str(n%2)


print decimal2binary(0)
print decimal2binary(1)
print decimal2binary(4)
