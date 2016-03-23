from random import randint
import logging
import board
import sb_logic
import stensils
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
        self.currentboard.setboard(fstring)


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

        whole_board = [(x,y) for x in range(self.w) for y in range(self.h)]

        dot_value = 3.0

        self_neightbor_values = 1.0

        #priotize the dots
        values[(1*self.h/4,1*self.w/4)] += dot_value
        values[(1*self.h/4,2*self.w/4)] += dot_value
        values[(1*self.h/4,3*self.w/4)] += dot_value

        values[(2*self.h/4,1*self.w/4)] += dot_value
        values[(2*self.h/4,2*self.w/4)] += dot_value
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

        my_lms = board.legal_moves(self.myid)

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




        # for spot, v in self.currentboard.field.iteritems():
        #     if v == 0:
        #         mynbs = 0
        #         theirnbs = 0
        #         for s in stensil.plus(spot):
        #             if self.currentboard.owns(s,self.myid):
        #                 mynbs += 1
        #             if self.currentboard.owns(s,self.oppid):
        #                 theirnbs += 1
        #         values[spot] += neightbor_value[(mynbs,theirnbs)]




        self.print_values(values, board)

        legal_values = {k:v for k,v in values.iteritems() if k in my_lms}
        return legal_values

    def print_values(self, values, board):
        boardstring = "board and values:\n"
        def fp(x,y):
            field = board.field[(x,y)]
            if field == self.myid:
                return "M"
            if field == self.oppid:
                return "E"
            return "{}".format(field)

        def fv(x,y):
            v = values[(x,y)]
            if v < 0:
                return "N"
            if v > 9:
                return "+"
            if v == 0:
                return '.'
            return "{:d}".format(int(v))

        def fl(x,y, ID):
            l = board.liberties(x,y, ID)
            if l < 0:
                return "N"
            if l > 9:
                return "+"
            if l == 0:
                return '.'
            return "{:d}".format(int(l))



        for y in range(self.h):
            for x in range(self.w):
                f = fp(x,y)
                if f == '0':
                    boardstring += fv(x,y)
                else:
                    boardstring += f
            boardstring += "|   |"
            for x in range(self.w):
                boardstring += fl(x,y,self.myid)
            boardstring += "|   |"
            for x in range(self.w):
                boardstring += fl(x,y,self.oppid)


            boardstring += "\n"
        # logging.info(boardstring.replace('0','.'))
        logging.info(boardstring)
        return
