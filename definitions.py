from cube import Cube
from BFS import BFS_2, BFS

target = Cube()


m1 = Cube()
m1.move("U R D L2 R'")

cube_states = dict()

status = 0
try:
    status = BFS(m1.code(), target.code(), cube_states)
except:
    print("Different states reached: "+str(len(cube_states.keys())))
print(status)
print("Different states reached: "+str(len(cube_states.keys())))

# decript the solution
m = cube_states[target.code()]
c = Cube(target.code())

movelist = []
prev_node_code = target.code()
while 1:
    move = cube_states[prev_node_code][1]
    prev_node_code = cube_states[prev_node_code][0]

    movelist.append(move)

    if prev_node_code == m1.code():
        break

# movelist.reverse()

print(movelist)
