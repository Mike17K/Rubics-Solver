#include <iostream>
#include <vector>
#include <string>

using namespace std;

char R_COLORS[6] = {'w', 'r', 'g', 'o', 'b', 'y'};
string MOVES[18] = {
    "U2", "U'", "U ",
    "D2", "D'", "D ",
    "R2", "R'", "R ",
    "L2", "L'", "L ",
    "F2", "F'", "F ",
    "B2", "B'", "B "};

#define _top 0
#define _left 1
#define _back 2
#define _right 3
#define _front 4
#define _bottom 5

// reference: RELETIONS[top]
int RELATIONS[6][4][2] = {{{_right, 4}, {_front, 6}, {_left, 0}, {_back, 2}},
                          {{_front, 4}, {_bottom, 4}, {_back, 4}, {_top, 4}},
                          {{_right, 6}, {_top, 6}, {_left, 6}, {_bottom, 2}},
                          {{_back, 0}, {_bottom, 0}, {_front, 0}, {_top, 0}},
                          {{_top, 2}, {_right, 2}, {_bottom, 6}, {_left, 2}},
                          {{_right, 0}, {_back, 6}, {_left, 4}, {_front, 2}}};

class Cube
{
public:
    int state[6 * 9] = {0};

    string revert_move_name(string moveName)
    {
        if (moveName[1] == '\'')
            return moveName;
        if (moveName[1] == '2')
            return moveName;
        return moveName + '\'';
    }

    Cube()
    {
        for (int i = 0; i < 6; i++)
        {
            for (int j = 0; j < 9; j++)
            {
                state[i * 9 + j] = i;
            }
        }
    }

    Cube(string code)
    {
        for (int i = 0; i < 54; i++)
        {
            state[i] = ((char)code[i]) - '0';
        }
    }

    std::string code()
    {
        std::string txt;
        for (int i = 0; i < 54; i++)
        {
            txt += state[i] + '0';
        }
        return txt;
    }

    Cube
    copy()
    {
        Cube copy_cube;
        for (int i = 0; i < 6 * 9; i++)
        {
            copy_cube.state[i] = state[i];
        }
        return copy_cube;
    }

    void move(string moveName)
    {
        /* //
        if (moveName.length() > 2)
        {
            for (string move : split(moveName, ' '))
            {
                this->move(move);
            }
            return;
        }
        //*/

        if (moveName.length() == 0)
        {
            return;
        }

        int len = moveName.length();
        if (len == 1)
        {
            moveName += ' ';
        }
        int j = 0;
        for (; j < 18; j++)
        {
            string move = MOVES[j];

            bool logic = true;
            for (int i = 0; i < 2; i++)
            {
                if (move[i] != moveName[i])
                {
                    logic = false;
                }
            }
            if (logic)
            {
                break;
            }
        }

        int side;
        switch (MOVES[j][0])
        {
        case 'U':
            side = _top;
            break;
        case 'L':
            side = _left;
            break;
        case 'B':
            side = _back;
            break;
        case 'R':
            side = _right;
            break;
        case 'F':
            side = _front;
            break;
        case 'D':
            side = _bottom;
            break;

        default:
            break;
        }

        int turns = 1;
        switch (MOVES[j][1])
        {
        case '\'':
            turns = 3;
            break;
        case ' ':
            turns = 1;
            break;
        case '2':
            turns = 2;
            break;

        default:
            break;
        }

        // turn face
        for (int _ = 0; _ < turns; _++)
        {
            int cary1 = state[side * 9 + 6];
            int cary2 = state[side * 9 + 7];

            for (int i = 0; i < 3; i++)
            {
                state[side * 9 + (2 - i) * 2 + 2] = state[side * 9 + (2 - i) * 2];
                state[side * 9 + (2 - i) * 2 + 3] = state[side * 9 + (2 - i) * 2 + 1];
            }
            state[side * 9 + 0] = cary1;
            state[side * 9 + 1] = cary2;
        }

        // turn sides
        for (int _ = 0; _ < turns; _++)
        {

            int cary1 = state[RELATIONS[side][1][0] * 9 + (RELATIONS[side][1][1] + 0) % 8];
            int cary2 = state[RELATIONS[side][1][0] * 9 + (RELATIONS[side][1][1] + 1) % 8];
            int cary3 = state[RELATIONS[side][1][0] * 9 + (RELATIONS[side][1][1] + 2) % 8];

            int *s, *next_s;
            for (int i = 0; i < 3; i++)
            {
                s = RELATIONS[side][(4 - i) % 4];
                next_s = RELATIONS[side][(4 - i + 1) % 4];

                state[next_s[0] * 9 + (next_s[1] + 0) % 8] = state[s[0] * 9 + (s[1] + 0) % 8];
                state[next_s[0] * 9 + (next_s[1] + 1) % 8] = state[s[0] * 9 + (s[1] + 1) % 8];
                state[next_s[0] * 9 + (next_s[1] + 2) % 8] = state[s[0] * 9 + (s[1] + 2) % 8];
            }
            next_s = RELATIONS[side][(4 - 3 + 1) % 4];
            state[next_s[0] * 9 + (next_s[1] + 0) % 8] = cary1;
            state[next_s[0] * 9 + (next_s[1] + 1) % 8] = cary2;
            state[next_s[0] * 9 + (next_s[1] + 2) % 8] = cary3;
        }
    }
};

//
//
//
//
//
//
//
//
//
//
//
//
//
// BFS

#include <queue>
#include <unordered_map>

int BFS(string obj_code, string targetCode, unordered_map<string, pair<string, string>> &history)
{
    Cube obj(obj_code);
    queue<string> node_queue;
    node_queue.push(obj_code);

    while (!node_queue.empty())
    {
        string tmp_code = node_queue.front();
        node_queue.pop();

        Cube tmp(tmp_code);
        for (auto m : MOVES)
        {
            Cube tmp_copy = tmp;
            tmp_copy.move(m);

            if (history.find(tmp_copy.code()) == history.end())
            {
                node_queue.push(tmp_copy.code());
                history[tmp_copy.code()] = make_pair(tmp.code(), m);
                if (history.size() % 10000 == 0)
                {
                    cout << history.size() << endl;
                }
            }

            if (tmp_copy.code() == targetCode)
            {
                return 1;
            }
        }
    }

    return 0;
}

//
//
//
//
//
//
//
//
//
//
//
//
//
//
//

int main()
{
    Cube *a = new Cube();
    Cube *target = new Cube();

    a->move("U ");
    a->move("R ");
    a->move("F ");
    a->move("R ");
    a->move("F ");

    unordered_map<string, pair<string, string>> cube_states;
    int status = BFS(a->code(), target->code(), cube_states);

    cout << a->code() << endl;

    return 1;
}