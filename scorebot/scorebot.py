from random import randint
import logging
import board
import sb_logic


class ScoreBot:

    def __init__(self):
        self.currentboard = None
        self.nmove = 0
        self.points = {}
        self.w = None
        self.h = None

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

    def myid(self, myid):
        self.myid = myid
        if myid == 2:
            self.oppid = 1
        else:
            self.oppid = 2

    def make_move(self, time):
        return self.best_move(self.currentboard, time)

    def best_move(self, board, tleft):
        logging.info("get_move {} {}".format(board, tleft))

        values = self.set_values(board)
        logging.info("values {}".format(values))

        best_moves = [k for k,v in values.iteritems() if v == max(values.values())]

        logging.info("best moves {}".format(best_moves))

        if len(best_moves) < 1:
            logging.error("There are no legal moves?!")

        rm = randint(0, len(best_moves)-1)
        logging.info("rm {}".format(rm))
        return best_moves[rm]

    def set_values(self, board):

        values = {(x,y): 0.0 for x in range(self.w) for y in range(self.h)}

        center_board_value = 0.5

        #priotize the center
        values[(self.h/2,self.w/2)] += center_board_value


        legal_values = {k:v for k,v in values.iteritems() if k in board.legal_moves()}
        return legal_values
