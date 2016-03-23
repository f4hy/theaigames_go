import logging
from pprint import pprint_field
from collections import deque
from collections import defaultdict
import stensils



class Board(object):

    def __init__(self, w, h):
        f = {(x,y): 0 for x in range(w) for y in range(h)}
        self.field = defaultdict(lambda: 5, f)
        self.w = w
        self.h = h

    def setboard(self, fstr):
        old = self.field
        died = {1: [], 2: []}
        flist = deque(fstr.replace(';', ',').split(','))
        # logging.info("setting board using {}".format(flist))
        for y in range(self.h):
            for x in range(self.w):
                new = int(flist.popleft())
                if old[(x,y)] in [1,2] and new == 0:
                    logging.info("{} {} DIED!!!".format(x,y))
                    died[old[(x,y)]].append((x,y))
                self.field[(x,y)] = new
        # logging.info("field {}".format(self.field))
        # logging.info("board \n{}".format(pprint_field(self.field)))
        return died

    def fieldstring(self):
        return ",".join(str(self.field[(x,y)]) for y in range(self.h)for x in range(self.w) )

    def liberties(self, x, y, ID):
        liberty = 0
        for i in stensils.plus((x,y)):
            if self.field[i] == 0 or self.field[i] == ID:
                liberty +=1
        return liberty

    def fill_liberties(self, x, y):
        target = self.field[(x,y)]
        checked = []
        liberties = []
        filled = [(x,y)]
        dq = deque(stensils.plus((x,y)))

        while len(dq) > 0:
            current = dq.pop()
            checked.append(current)
            if self.field[current] == target:
                filled.append(current)
                dq.extend(i for i in stensils.plus(current) if i not in checked)
            if self.field[current] == 0:
                liberties.append(current)
        return filled, liberties

    def owned(self, x, y):

        target = 0
        checked = []
        edge = None
        filled = [(x,y)]
        dq = deque(stensils.plus((x,y)))

        while len(dq) > 0:
            current = dq.pop()
            checked.append(current)
            if self.field[current] == target:
                filled.append(current)
                dq.extend(i for i in stensils.plus(current) if i not in checked)
            if self.field[current] != 0:
                if edge is None:
                    edge = self.field[current]
                else:
                    if edge != self.field[current]:
                        return None
        return edge



    def is_legal(self, x, y, ID):
        if 0 <= x < self.w:
            if 0 <= y < self.h:
                if self.field[(x,y)] != 0:
                    return False
                if self.liberties(x,y, ID) > 0:
                    return True
        return False

    def legal_moves(self, moveid):
        return [ (x, y) for x in range(self.w) for y in range(self.h) if self.is_legal(x, y, moveid) ]

    def owns(self, spot, playerid):
        x,y = spot
        if 0 <= x < self.w:
            if 0 <= y < self.h:
                return self.field[(x,y)] == playerid
        return False
