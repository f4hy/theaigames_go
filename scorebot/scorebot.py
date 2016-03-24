from random import randint
import logging
import board
import stensils
import math
from pprint import print_values
from collections import defaultdict

class NoGoodMove(Exception):
    pass

class ScoreBot:

    def __init__(self):
        self.currentboard = None
        self.nmove = 0
        self.points = {}
        self.w = None
        self.h = None
        self.myid = None
        self.oppid = None
        self.mydead = []
        self.theirdead = []

    def setboard_width(self, w):
        logging.info("setting width {}".format(w))
        self.w = w
        if self.h:
            self.makeboard()

    def setboard_height(self, h):
        logging.info("setting height {}".format(h))
        self.h = h
        if self.w:
            self.makeboard()

    def makeboard(self):
        self.currentboard = board.Board(self.w, self.h)

    def update_currentboard(self, fstring):
        logging.info("updating board")
        dead = self.currentboard.setboard(fstring)
        self.mydead.extend(dead[self.myid])
        self.theirdead.extend(dead[self.oppid])


    def set_movenumb(self, nmove):
        logging.info("N move set to {}".format(nmove))
        self.nmove = nmove

    def make_move(self, time):
        return self.best_move(self.currentboard, time)

    def best_move(self, board, tleft):
        logging.info("get_move {} {}".format(board, tleft))

        values = self.set_values(board)
        # logging.info("values {}".format(values))

        best_moves = [k for k,v in values.iteritems() if v == max(values.values())]

        if max(values.values()) < 0.0:
            logging.warn("best move is negative value, passing")
            logging.warn("values: {}".format(values))
            raise NoGoodMove

        logging.info("best moves {}".format(best_moves))

        if len(best_moves) < 1:
            logging.error("There are no legal moves?!")
            raise NoGoodMove

        rm = randint(0, len(best_moves)-1)
        logging.info("rm {}".format(rm))
        return best_moves[rm]

    def set_values(self, board):

        values = defaultdict(lambda: 0.0)
        owners = defaultdict(lambda: 0)

        whole_board = [(x,y) for x in range(self.w) for y in range(self.h)]

        dot_value = 0.5

        self_neightbor_values = 1.0

        #priotize the dots
        values[(1*self.h/4,1*self.w/4)] += dot_value
        values[(1*self.h/4,2*self.w/4)] += dot_value
        values[(1*self.h/4,3*self.w/4)] += dot_value

        values[(2*self.h/4,1*self.w/4)] += dot_value
        #values[(2*self.h/4,2*self.w/4)] += dot_value
        values[(2*self.h/4,3*self.w/4)] += dot_value

        values[(3*self.h/4,1*self.w/4)] += dot_value
        values[(3*self.h/4,2*self.w/4)] += dot_value
        values[(3*self.h/4,3*self.w/4)] += dot_value


        neightbor_value = {(0,0) : 0.0}
        neightbor_value[(1,0)] = 2.0
        neightbor_value[(0,1)] = 2.0

        neightbor_value[(2,0)] = 3.0
        neightbor_value[(1,1)] = 4.0
        neightbor_value[(0,2)] = 0.0

        neightbor_value[(3,0)] = -2.0
        neightbor_value[(2,1)] = 1.0
        neightbor_value[(1,2)] = -1.0
        neightbor_value[(0,3)] = -2.0

        liberty_value = {0 : -200.0}
        liberty_value[1] = -1.0
        liberty_value[2] = 2.0
        liberty_value[3] = 3.0
        liberty_value[4] = 1.0

        edge_value = -2.5

        kill_value = +11.0
        save_value = +6.0

        mydead_value = -2.0
        theirdead_value = -1.0

        owned_value = -2000.0

        my_lms = board.legal_moves(self.myid)

        eye_value = -2000.00

        #squared people died on we shouldnt play again
        for x,y in self.mydead:
            values[(x,y)] += mydead_value
        for x,y in self.theirdead:
            values[(x,y)] += theirdead_value

        for x,y in my_lms:
            #board edge is bad
            if x == 0 or x == self.w-1 or y == 0 or y == self.h-1:
                values[(x,y)] += edge_value

            # set liberty value
            values[(x,y)] += liberty_value[board.liberties(x,y, self.myid)]

        # kill
        for x,y in (s for s in whole_board if board.field[s] == self.oppid):
            if board.liberties(x,y, self.oppid) == 1:
                for m in stensils.plus((x,y)):
                    values[m] += kill_value

        # save
        for x,y in (s for s in whole_board if board.field[s] == self.myid):
            mylib = board.liberties(x,y, self.myid)
            if mylib in [1,2]:
                for mx,my in stensils.plus((x,y)):
                    if board.liberties(mx,my, self.myid) > mylib:
                        values[(mx,my)] += save_value


        # # save our groups!
        # for x,y in (s for s in whole_board if board.field[s] == self.myid):
        #     filled, libs = board.fill_liberties(x,y)
        #     if len(filled) > 1 and len(libs) == 1:
        #         values[libs[0]] += save_value*len(filled)
        #     else:
        #         for l in libs:
        #             lx,ly = l
        #             if board.liberties(lx,ly, self.myid) > 2:
        #                 values[l] += len(filled)*save_value/len(libs)

        # # dont fill eyes!
        # for x,y in my_lms:
        #     if all(board.field[mx,my] in [self.myid,5] for mx,my in stensils.plus((x,y))):
        #         logging.warn("{} {} is and eye!!!".format(x,y))
        #         exit(-1)
        #         values[(x,y)] += eye_value

        # check owned areas
        if self.gameround > math.sqrt(self.h*self.w):
            logging.info("checking ownership")
            for x,y in my_lms:
                o = board.owned(x,y)
                if o is not None:
                    logging.info("{} owns {}".format(o,(x,y)))
                    owners[(x,y)] = o
                    values[(x,y)] += owned_value


        for x,y in (s for s in whole_board if board.field[s] == self.oppid):
            filled, libs = board.fill_liberties(x,y)
            if len(filled) > 1 and len(libs) == 1:
                values[libs[0]] += kill_value*len(filled)


        print_values(board, values, owners)

        legal_values = {k:v for k,v in values.iteritems() if k in my_lms}
        return legal_values
