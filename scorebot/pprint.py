import logging

def pprint_field(field):
    # pstr = ""
    # for y1 in range(3):
    #     for y2 in range(3):
    #         for j in range(3):
    #             i = (y1*9+y2*3+j)
    #             pstr += "".join(map(str, field[i*3:(i+1)*3]))
    #             pstr += "|"
    #         pstr += "\n"
    #     pstr += "---+---+---\n"
    # return pstr.strip()
    return field

def print_values(board, values, owners):
    boardstring = "board and values:\n"

    logging.info("{}".format(owners))
    w = board.w
    h = board.h
    def fp(x,y):
        field = board.field[(x,y)]
        if field == 1:
            return "x"
        if field == 2:
            return "+"
        if field == 0:
            return "."
        return "{}".format(field)

    def fv(x,y):
        v = values[(x,y)]
        if v < 0:
            return "N"
        if v > 9:
            return "*"
        if v == 0:
            return '.'
        return "{:d}".format(int(v))

    def fo(x,y):
        o = owners[(x,y)]
        return "{:d}".format(int(o))


    def fl(x,y, ID):
        l = board.liberties(x,y, ID)
        if l < 0:
            return "N"
        if l > 9:
            return "+"
        if l == 0:
            return '.'
        return "{:d}".format(int(l))



    for y in range(h):
        boardstring += "|   |"
        for x in range(w):
            boardstring += fp(x,y)
        boardstring += "|   |"
        for x in range(w):
            f = fp(x,y)
            if f == '.':
                boardstring += fv(x,y)
            else:
                boardstring += f
        boardstring += "|   |"
        for x in range(w):
            boardstring += fo(x,y)
        boardstring += "|   |"
        for x in range(w):
            boardstring += fl(x,y,1)


        boardstring += "\n"
    # logging.info(boardstring.replace('0','.'))
    logging.info(boardstring)
    return
