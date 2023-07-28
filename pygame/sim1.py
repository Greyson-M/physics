
grav = 9.8      #m/s^2
masskg = 60.0     #kg
ivel = 3.5      #m/s
iheight = 5.0   #m

fvelM = 0       #m/s
fheight = "?"      #m

mass = masskg * grav    #N

#1/2mv^2 + mgh = mgh
#1/2v^2 + gh = gh

velsq = ivel**2
dvel = velsq * 0.5
gh = grav*iheight
initial_work = dvel + gh

print (initial_work)

#initial_work = gh
hf = initial_work/grav
print (hf)
