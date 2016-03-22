import logging

def can_score(sb, team):
    # logging.info("checking if {} can win {}".format(team, sb))

    if won(sb, 1):
        return False
    if won(sb, 2):
        return False

    for loc in range(9):
        if sb[loc] is not 0:
            continue
        new = list(sb)
        new[loc] = team
        if won(new, team):
            return loc
    return False


def won(sb, team):

    horizontals = [sb[i*3:i*3+3] for i in range(3)]
    verticals = [sb[i:9:3] for i in range(3)]
    diags = [sb[0:9:4], sb[2:8:2]]
    #logging.info("h{} v{} d{}".format(horizontals, verticals, diags))
    all3 = horizontals + verticals + diags

    for i in all3:
        if i.count(team) == 3:
            return True

    return False
