a = [12,424,35,4,46,646,5,67,57,7,578,7]
for i in range(len(a)):
    for j in range(len(a)-1-i):
        if a[j] > a[j+1]:
            a[j],a[j+1] = a[j+1],a[j]
print(a)

a=[1,2,3,4,5,6,7,8,9,10]
def aaa(ls):
    ls[0] = 99
    ls = [100,200,300]


aaa(a)
print(a)

def bbb():
    pass
def ccc():
    pass
c = bbb() or ccc()
print(c)
dict["a"]










