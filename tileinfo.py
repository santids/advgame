"""Different functions that provide information about a tiletype indicated by a number"""
from display import colors

def color(tile):
    d = {0:colors.gray6,1:colors.black,2:colors.cyan6}
    if tile in d:
        return d[tile]
    else:
        return colors.brown7
def isobstacle(tile):
    d = [1]
    return tile in d


if __name__ == '__main__':
    print color(0)
    print isobstacle(1)
    print isobstacle(2)
