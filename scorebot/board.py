import logging
import sb_logic
from pprint import pprint_field
from collections import deque

class Board(object):

    def __init__(self, w, h):
        self.field = {(x,y): 0 for x in range(w) for y in range(h)}
        self.w = w
        self.h = h

    def setboard(self, fstr):
        flist = deque(fstr.replace(';', ',').split(','))
        logging.info("setting board using {}".format(flist))
        for y in range(self.h):
            for x in range(self.w):
                self.field[(x,y)] = int(flist.popleft())
        logging.info("field {}".format(self.field))
        logging.info("board \n{}".format(pprint_field(self.field)))


    def is_legal(self, x, y):
        if 0 <= x < self.w:
            if 0 <= y < self.h:
                return self.field[(x,y)] == 0
        return False

    def legal_moves(self):
        return [ (x, y) for x in range(self.w) for y in range(self.h) if self.is_legal(x, y) ]

    def owns(self, spot, playerid):
        x,y = spot
        if 0 <= x < self.w:
            if 0 <= y < self.h:
                return self.field[(x,y)] == playerid
        return False
