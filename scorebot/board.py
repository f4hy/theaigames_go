import logging
import sb_logic
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
        flist = deque(fstr.replace(';', ',').split(','))
        # logging.info("setting board using {}".format(flist))
        for y in range(self.h):
            for x in range(self.w):
                self.field[(x,y)] = int(flist.popleft())
        # logging.info("field {}".format(self.field))
        # logging.info("board \n{}".format(pprint_field(self.field)))


    def liberties(self, x, y, ID):
        liberty = 0
        for i in stensils.plus((x,y)):
            if self.field[i] == 0 or self.field[i] == ID:
                liberty +=1
        return liberty


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
