def plus(point):
    px, py = point
    return [(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)]


def square(point):
    px, py = point
    return [(px + x, py + y) for x in (-1, 0, 1) for y in (-1, 0, 1)]
