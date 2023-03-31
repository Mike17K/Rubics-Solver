import numpy as np
import random


class Cube:
    def reverce_move_name(moveName):
        if len(moveName) == 1:
            return moveName+"'"
        if len(moveName) == 2:
            if moveName[1] == '2':
                return moveName
            return moveName[0]

    MOVES = [
        "U2", "U'", "U",
        "D2", "D'", "D",
        "R2", "R'", "R",
        "L2", "L'", "L",
        "F2", "F'", "F",
        "B2", "B'", "B"
    ]

    COLORS = {'w': 0, 'r': 1, 'g': 2, 'o': 3, 'b': 4, 'y': 5}
    R_COLORS = {'0': 'w', '1': 'r', '2': 'g', '3': 'o', '4': 'b', '5': 'y'}
    SIDES = {
        'top': 0,
        'left': 1,
        'back': 2,
        'right': 3,
        'front': 4,
        'bottom': 5
    }

    # this table stores the around sides of each side and their ofset for the top layer
    RELATIONS = {
        'top': {'right': 4, 'front': 6, 'left': 0, 'back': 2},
        'left': {'front': 4, 'bottom': 4, 'back': 4, 'top': 4},
        'back': {'right': 6, 'top': 6, 'left': 6, 'bottom': 2},
        'right': {'back': 0, 'bottom': 0, 'front': 0, 'top': 0},
        'front': {'top': 2, 'right': 2, 'bottom': 6, 'left': 2},
        'bottom': {'right': 0, 'back': 6, 'left': 4, 'front': 2}
    }

    def __init__(self, code=""):
        self.state = np.array(
            [i for i in range(6) for _ in range(9)]
        )

        if code != "":
            for i in range(len(code)):
                self.state[i] = int(code[i])

    def copy(self):
        return Cube(self.code())

    def code(self):
        # returns the decripted unique code of the state
        txt = ""
        for i in self.state:
            txt += str(i)
        return txt

    def scramble(self, text=""):
        if text == "":
            # from random pool of moves pick some and execute
            moves = []
            for _ in range(10):
                m = random.choice(Cube.MOVES)
                moves.append(m)
                self.move(m)
            return " ".join(moves)

        for move in text.split(" "):
            self.move(move)

    def move(self, moveName):
        # if multiple moves
        if len(moveName) > 2:
            for move in moveName.split(" "):
                self.move(move)
                # print(f"Sub Move:{move}")
                # self.show()
            return
        if moveName in ['']:
            # rotate cube or middle moves
            return

        if moveName not in Cube.MOVES:
            return 1

        side = None
        if moveName[0] == "U":
            side = 'top'
        if moveName[0] == "L":
            side = 'left'
        if moveName[0] == "B":
            side = 'back'
        if moveName[0] == "R":
            side = 'right'
        if moveName[0] == "F":
            side = 'front'
        if moveName[0] == "D":
            side = 'bottom'

        turns = 1
        if (len(moveName) == 2):
            if moveName[1] == '2':
                turns = 2
            elif moveName[1] == "'":
                turns = 3

        # turn face <--fix-->
        for _ in range(turns):
            cary1 = self.state[Cube.SIDES[side]*9 + 6]
            cary2 = self.state[Cube.SIDES[side]*9 + 7]

            for i in range(3):
                self.state[Cube.SIDES[side]*9 + (2-i) *
                           2+2] = self.state[Cube.SIDES[side]*9 + (2-i)*2]
                self.state[Cube.SIDES[side]*9 + (2-i)*2 +
                           3] = self.state[Cube.SIDES[side]*9 + (2-i)*2+1]

            self.state[Cube.SIDES[side]*9 + 0] = cary1
            self.state[Cube.SIDES[side]*9 + 1] = cary2

        # turn sides
        for _ in range(turns):
            sides = [i for i in Cube.RELATIONS[side].items()]
            cary1 = self.state[Cube.SIDES[sides[1][0]]*9+(sides[1][1]+0) % 8]
            cary2 = self.state[Cube.SIDES[sides[1][0]]*9+(sides[1][1]+1) % 8]
            cary3 = self.state[Cube.SIDES[sides[1][0]]*9+(sides[1][1]+2) % 8]
            for i in range(len(sides)-1):
                s = sides[(4-i) % 4]  # ex. ('left', 2)
                next_s = sides[(4-i+1) % 4]  # ex. ('left', 2)

                self.state[Cube.SIDES[next_s[0]]*9 +
                           (next_s[1] + 0) % 8] = self.state[Cube.SIDES[s[0]]*9+(s[1]+0) % 8]
                self.state[Cube.SIDES[next_s[0]]*9 +
                           (next_s[1] + 1) % 8] = self.state[Cube.SIDES[s[0]]*9+(s[1]+1) % 8]
                self.state[Cube.SIDES[next_s[0]]*9 +
                           (next_s[1] + 2) % 8] = self.state[Cube.SIDES[s[0]]*9+(s[1]+2) % 8]
            next_s = sides[(4-3+1) % 4]  # ex. ('left', 2)
            self.state[Cube.SIDES[next_s[0]]*9+(next_s[1]+0) % 8] = cary1
            self.state[Cube.SIDES[next_s[0]]*9+(next_s[1]+1) % 8] = cary2
            self.state[Cube.SIDES[next_s[0]]*9+(next_s[1]+2) % 8] = cary3

    def show(self):
        # 'top': 0,
        # 'left': 1,
        # 'back': 2,
        # 'right': 3,
        # 'front': 4,
        # 'bottom': 5
        p = self.state

        txt = ""

        txt += f"    {p[27]}{p[28]}{p[29]}" + '\n'
        txt += f"    {p[34]}{p[35]}{p[30]}" + '\n'
        txt += f"    {p[33]}{p[32]}{p[31]}" + '\n'
        txt += f"{p[18]}{p[19]}{p[20]} {p[0]}{p[1]}{p[2]} {p[36]}{p[37]}{p[38]} {p[45]}{p[46]}{p[47]}" + '\n'
        txt += f"{p[25]}{p[26]}{p[21]} {p[7]}{p[8]}{p[3]} {p[43]}{p[44]}{p[39]} {p[52]}{p[53]}{p[48]}" + '\n'
        txt += f"{p[24]}{p[23]}{p[22]} {p[6]}{p[5]}{p[4]} {p[42]}{p[41]}{p[40]} {p[51]}{p[50]}{p[49]}" + '\n'
        txt += f"    {p[9]}{p[10]}{p[11]}" + '\n'
        txt += f"    {p[16]}{p[17]}{p[12]}" + '\n'
        txt += f"    {p[15]}{p[14]}{p[13]}" + '\n'

        for key, value in Cube.R_COLORS.items():
            txt = txt.replace(key, value)

        print(txt)

        return txt
