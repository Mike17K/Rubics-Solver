from cube import Cube

m1 = Cube()
m2 = Cube()

m1.move("R U2")
m2.move("R U2 L L'")

m1.show()
m2.show()

print(m1.code() == m2.code())
