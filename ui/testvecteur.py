from kivy.vector import Vector


a = [-1, -5]
b = [0, -3]
c = [2,1]
ab = Vector(b)-Vector(a)
ac = Vector(c)-Vector(b)
r = ab.x*ac.y - ab.y*ac.x
print(ab, ac, r)