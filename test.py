#!/usr/bin/env python2
import os
import sys
from subprocess import Popen, PIPE, STDOUT
import argparse


def main(options):
    # Get robots who are fighting (player1, player2)
    bot1, bot2 = get_bots(options)
    # Simulate game init input
    h, w = 9, 9
    send_init('1', bot1, h, w)
    send_init('2', bot2, h, w)
    round_num = 1
    move = 1
    field = ','.join(['0'] * h*w)
    print_board(field, h, w, round_num, '')
    win1 = win2 = 0
    while win1 + win2 < options.games:
        for bot_id, bot in [('1', bot1), ('2', bot2)]:
            # Wait for any key
            if not options.nowait:
                raw_input()
            # Send inputs to bot
            move = send_update(bot, round_num, move, field)
            # Update macroboard and game field
            if move == "pass":
                pass
            else:
                field = update_field(field, move, str(bot_id), h, w)
            print_board(field, h, w, round_num, move)
            round_num += 1



def get_bots(options):
    root = os.path.dirname(os.path.realpath(__file__))
    files = os.listdir(root)
    bots = [f for f in files
            if os.path.isdir(os.path.join(root, f)) and f != '.git']

    bot_list = '\n'.join(
        ['{}. {}'.format(i, bot) for i, bot in enumerate(bots)])

    if options.bot1 is None:
        bot1_name = bots[int(raw_input(
            'Choose Player 1:\n' + bot_list + '\n\n> '))]
    else:
        bot1_name = bots[options.bot1]
    if options.bot2 is None:
        bot2_name = bots[int(raw_input(
            'Choose Player 2:\n' + bot_list + '\n\n> '))]
    else:
        bot2_name = bots[options.bot2]

    with open("bot1.log",'w') as bot1log:
        bot1 = Popen(['python2', 'main.py'],
                     cwd=os.path.join(root, bot1_name),
                     stdout=PIPE,
                     stdin=PIPE,
                     stderr=bot1log)
    with open("bot2.log",'w') as bot2log:
        bot2 = Popen(['python2', 'main.py'],
                     cwd=os.path.join(root, bot2_name),
                     stdout=PIPE,
                     stdin=PIPE,
                     stderr=bot2log)

    return bot1, bot2


def send_init(bot_id, bot, h, w):
    init_input = (
        'settings timebank 10000\n'
        'settings time_per_move 500\n'
        'settings player_names player1,player2\n'
        'settings your_bot player{bot_id}\n'
        'settings your_botid {bot_id}\n'
        'settings field_width {width}\n'
        'settings field_height {height}\n'.format(bot_id=bot_id, width=w, height=h))

    bot.stdin.write(init_input)


def send_update(bot, round_num, move, field):
    update_input = (
        'update game round {round}\n'
        'update game move {move}\n'
        'update game field {field}\n'
        'action move 10000\n'.format(
            round=round_num,
            move=move,
            field=field))

    bot.stdin.write(update_input)
    out = bot.stdout.readline().strip()
    print 'bot output: ' + repr(out)
    return out


def update_field(field, move, bot_id, h, w):
    col, row = move.split(' ')[1:3]
    arr = field.split(',')
    index = int(row) * w + int(col)
    if arr[index] != '0':
        raise RuntimeError(
            'Square {col} {row} already occupied by {occ}.'.format(
                col=col, row=row, occ=arr[index]))

    arr[index] = bot_id
    return ','.join(arr)




def print_board(field, h, w, round_num, move):
    field = field.replace('0', ' ')
    a = field.split(',')
    msg = ''
    for i in range(0, w*h, w):
        msg += "".join(a[i:i+w])
        msg += "\n"

    sys.stderr.write("\x1b[2J\x1b[H")  # clear screen
    msg += '\nRound {} \nfield: {}\nmove: {}\n'.format(
        round_num, field, move)

    sys.stdout.write(msg)


def is_winner(macroboard):

    return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run bots")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument("-n", "--nowait", action="store_true",
                        help="don't wait")
    parser.add_argument("-g", "--games", type=int, default=1)
    parser.add_argument("-b1", "--bot1", type=int, default=None)
    parser.add_argument("-b2", "--bot2", type=int, default=None)

    args = parser.parse_args()

    wins = {'1': 0, '2':0}
    for i in range(args.games):
        winner = main(args)
        wins[winner] += 1

    print wins
