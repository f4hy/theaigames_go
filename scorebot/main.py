#!/usr/bin/env python2
from scorebot import NoGoodMove

def parse_command(instr, bot):

    if instr.startswith('action move'):
        time = int(instr.split(' ')[-1])
        try:
            x, y = bot.make_move(time)
        except NoGoodMove:
            logging.warn("No good move detected, passing")
            return 'pass\n'
        return 'place_move %d %d\n' % (x, y)
    elif instr.startswith('settings timebank'):
        bot.timebank = int(instr.split(' ')[-1])
    elif instr.startswith('settings time_per_move'):
        bot.time_per_move = int(instr.split(' ')[-1])
    elif instr.startswith('settings player_names'):
        bot.players = instr.split(' ')[2:]
    elif instr.startswith('settings your_bot '):
        bot.my_name = instr.split(' ')[-1]
    elif instr.startswith('settings your_botid'):
        myid = int(instr.split(' ')[-1])
        bot.myid = myid
        bot.oppid = 1 if myid == 2 else 2
    elif instr.startswith('settings field_width'):
        bot.setboard_width(int(instr.split(' ')[-1]))
    elif instr.startswith('settings field_height'):
        bot.setboard_height(int(instr.split(' ')[-1]))
    elif instr.startswith('update game round'):
        bot.gameround = (int(instr.split(' ')[-1]))
    elif instr.startswith('update game move'):
        bot.set_movenumb(int(instr.split(' ')[-1]))
    elif instr.startswith('update game field'):
        fstr = instr.split(' ')[-1]
        bot.update_currentboard(fstr)
    elif "points" in instr:
        _, botname, _, points = instr.split(' ')
        bot.points[botname] = int(points)
    else:
        logging.warn("did not parse command correctly! {}".format(instr))
    return ''

if __name__ == '__main__':
    import sys
    from scorebot import ScoreBot
    import logging
    import socket

    if 'f4hy' in socket.gethostname() or 'fahy' in socket.gethostname():
        logging.basicConfig(format='SCOREBOT %(levelname)s: %(message)s', level=logging.DEBUG)
        root = logging.getLogger()
        errfilename = "test"+".err"
        errfilehandler = logging.FileHandler(errfilename, delay=True)
        errfilehandler.setLevel(logging.WARNING)
        formatter = logging.Formatter('SCOREBOT %(levelname)s: %(message)s')
        errfilehandler.setFormatter(formatter)
        root.addHandler(errfilehandler)
        logfilename = "test"+".log"
        logfilehandler = logging.FileHandler(logfilename, delay=True)
        logfilehandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('SCOREBOT %(levelname)s: %(message)s')
        logfilehandler.setFormatter(formatter)
        root.addHandler(logfilehandler)
    else:
        logging.basicConfig(format='SCOREBOT %(levelname)s: %(message)s', level=logging.DEBUG)


    logging.info("starting logging")

    bot = ScoreBot()

    while True:
        try:
            instr = raw_input()
            logging.info("instr {}".format(instr))
        except EOFError as e:
            logging.warn("given EOF exiting")
            sys.stdout.flush()
            exit(-1)
        except Exception as e:
            logging.warn('error reading input {}, {}'.format(e, type(e)))
            sys.stderr.write('error reading input')
            raise e
        outstr = parse_command(instr, bot)
        sys.stdout.write(outstr)
        sys.stdout.flush()
