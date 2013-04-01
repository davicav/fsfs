import math
import csv
import getopt
import sys
from os.path import basename


def dist(i, j, m_info):
    """
    :param i: i's feature list
    :param j: j's feature list
    :param m_info:
    :return: distance between the data points 'i' and 'j'
    :rtype : float
    """
    len_cols = m_info['len_cols']
    maxf = m_info['maxf']
    minf = m_info['minf']

    dist = 0.0
    # for each feature get the distance of the points
    for l in range(len_cols):
        dist += ((float(i[l]) - float(j[l])) / (maxf[l] - minf[l])) ** 2

    return math.sqrt(dist)


def sim(i, j, dm, dm_avg):
    """
    :param i: point i
    :param j: point j
    :param dm: matrix with the distance between the points
    :param dm_avg: average distance between data points computed over the entire data set
    :return: similarity of the data points 'i' and 'j'
    :rtype : float
    """
    alfa = -math.log(0.5) / dm_avg

    return math.exp(-alfa * dm[i][j])


def get_info(m):
    """
    :param m: list of attributes with a list of features
    :return: dictionary with the min and max values to every feature
    :rtype : dict
    """
    len_rows = len(m)
    len_cols = len(m[0])

    minf = [sys.float_info.max for col in range(len_cols)]
    maxf = [sys.float_info.min for col in range(len_cols)]

    for col in range(len_cols):
        for row in range(len_rows):
            cur = float(m[row][col])
            if cur < minf[col]:
                minf[col] = cur
            if cur > maxf[col]:
                maxf[col] = cur

    info = {
        'len_rows': len_rows,
        'len_cols': len_cols,
        'minf': minf,
        'maxf': maxf,
    }
    return info


def get_distance_matrix(m, m_info):
    """
    :param m: list of attributes with a list of features
    :return: matrix with the distances between the attributes along all the features direction
    :rtype : list, float
    """
    # init the distance matrix
    dm = [[0.0 for j in range(len(m))] for i in range(len(m))]

    dm_sum_total = 0.0
    dm_count = 0
    # calculate the distances while i < j. dist(i , j) = dist(j, i)
    for i in range(len(m)):
        for j in range(i + 1, len(m)):
            dm[i][j] = dist(m[i], m[j], m_info)
            dm[j][i] = dm[i][j]

            # calculate the average sum between the attributes
            dm_sum_total += dm[i][j]
            dm_count += 1

    dm_avg = dm_sum_total / dm_count

    return dm, dm_avg


def entropy(m):
    """
    :param m: list of attributes with a list of features
    :return: entropy of the attributes set
    :rtype : float
    """
    m_info = get_info(m)
    len_rows = m_info['len_rows']
    distance_matrix, dm_avg = get_distance_matrix(m, m_info)
    entropy = 0.0

    for i in range(len_rows):
        for j in range(i + 1, len_rows):
            sim_ij = sim(i, j, distance_matrix, dm_avg)
            if sim_ij == 1:  # i and j are equal
                continue

            entropy += (sim_ij * math.log(sim_ij) + (1 - sim_ij) * math.log(1 - sim_ij))

    return -entropy

###############################################################################
class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    if argv == None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)

        for o, a in opts:
            if o in ("-h", "--help"):
                print "Uso:", argv[0], "input"
                return 0

        if not args:
            raise Usage("Sem argumentos")
        total = 0
        for arg in args:
            matrix = []
            with open(arg, 'rb') as csvfile:
                cr = csv.reader(csvfile, delimiter=',')
                for row in cr:
                    matrix.append(row[:-1])

            ent = entropy(matrix)
            print "Entropy of %s = %f" % (basename(arg), ent)

            total += ent
        print "Media of entropy = %f" % (total / len(args))
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "Para ajuda -h ou --help"
        return 2


if __name__ == '__main__':
    sys.exit(main())
