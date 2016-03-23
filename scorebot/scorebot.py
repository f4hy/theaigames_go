from random import randint
import logging
import board
import sb_logic

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
        logging.info("values {}".format(values))

        best_moves = [k for k,v in values.iteritems() if v == max(values.values())]

        if max(values.values()) < 0.0:
            logging.warn("best move is negative value, passing")
            raise NoGoodMove

        logging.info("best moves {}".format(best_moves))

        if len(best_moves) < 1:
            logging.error("There are no legal moves?!")
            raise NoGoodMove

        rm = randint(0, len(best_moves)-1)
        logging.info("rm {}".format(rm))
        return best_moves[rm]

    def set_values(self, board):

        values = {(x,y): 0.0 for x in range(self.w) for y in range(self.h)}

        dot_value = 10.0

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

        logging.info("WTF {}".format(values))

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

        neightbor_value[(4,0)] = -200.0
        neightbor_value[(3,1)] = -200.0
        neightbor_value[(2,2)] = -200.0
        neightbor_value[(1,3)] = -200.0
        neightbor_value[(0,4)] = -200.0

        def plus_stensil(point):
            px, py = point
            return [(px + 1, py), (px - 1, py), (px, py - 1), (px, py - 1)]


        def square_stensil(point):
            px, py = point
            return [(px + x, py + y) for x in (-1, 0, 1) for y in (-1, 0, 1)]

        # #play near ourselves
        # for spot, v in self.currentboard.field.iteritems():
        #     logging.info("{}, {}".format(spot, v))
        #     logging.info("{}, {}".format(v, self.myid))
        #     if v == self.myid:
        #         for s in square_stensil(spot):
        #             values[s] += self_neightbor_values

        #consider neightbors
        for spot, v in self.currentboard.field.iteritems():
            if v == 0:
                mynbs = 0
                theirnbs = 0
                for s in plus_stensil(spot):
                    if self.currentboard.owns(s,self.myid):
                        mynbs += 1
                    if self.currentboard.owns(s,self.oppid):
                        theirnbs += 1
                values[spot] += neightbor_value[(mynbs,theirnbs)]


        self.print_values(values)

        legal_values = {k:v for k,v in values.iteritems() if k in board.legal_moves()}
        return legal_values

    def print_values(self, values):
        boardstring = "board and values:\n"
        def fp(x,y):
            field = self.currentboard.field[(x,y)]
            if field == self.myid:
                return "M"
            if field == self.oppid:
                return "E"
            return "{}".format(field)

        def fv(x,y):
            v = values[(x,y)]
            logging.info("{},{},{}".format(x,y,v))
            if v < 0:
                return "N"
            if v > 9:
                return "+"
            if v == 0:
                return '.'
            return "{:d}".format(int(v))


        for x in range(self.w):
            for y in range(self.h):
                f = fp(x,y)
                if f == '0':
                    boardstring += fv(x,y)
                else:
                    boardstring += f
            boardstring += "\n"
        # logging.info(boardstring.replace('0','.'))
        logging.info(boardstring)
        return
