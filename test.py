import pyparsing

j = -360
i = -640
Xs = []
Ys = []

while i < 640:
    Xs.append(i)
    i+=5
    while j < 360:
        Ys.append(j)
        j += 5

#print (Xs)
#print (Ys)
FieldX = []
FieldY = []

for x in Xs:
    if x == 0:
        x = 1
    x_dist = -x
    #FieldX.append(float((100 * 5500)/(x_dist**2)))
    FieldY.append(-x)


for y in Ys:
    if y == 0:
        y = 1
    y_dist = -y
    #FieldY.append(float((100 * 5500)/(y_dist**2)))
    FieldX.append(y)

print (FieldX)
