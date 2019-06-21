#[1,2,2,3,4]任意长度
e=input("请输入任意长度的数：1,2,2,3,4")
list=e.split(',')
print(list)
num1=[int(i) for i in list]
num1.sort()
print(num1)
print(len(num1))
he1=0
he2=0
for x in range(len(num1)):
    for y in range(len(num1)-x):
        he1 += num1[y]
    for z in range(len(num1)-x,len(num1)):
        he2 += num1[z]
    if he2 >= he1:
        for a in range(0,z):
            print(num1[a])
        print("------------------")
        for b in range(z,len(num1)):
            print(num1[b])
        break