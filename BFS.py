from cube import Cube
import queue


def BFS(obj_code, targetCode, history={}):
    ''' obj: .MOVES:list .code():str .move(str:.MOVES[i]) '''

    node_queue = queue.Queue()
    node_queue.put(obj_code)

    while not node_queue.empty():
        tmp_code = node_queue.get()

        obj = Cube(tmp_code)
        for m in obj.MOVES:
            tmp = obj.copy()
            tmp.move(m)

            if tmp.code() not in history.keys():
                node_queue.put(tmp.code())
                history[tmp.code()] = [obj.code(), m]
                if len(history.keys()) % 1000 == 0:
                    print(len(history.keys()))

            if tmp.code() == targetCode:
                return 1


def BFS_2():
    pass
