import math
import csv
import getopt
import sys


def dist(i, j, m_info):
    """
    :param i: list of features of 'i'
    :param j: list of features of 'j'
    :param m_info: dictionary with the matrix information about min and max values of all features
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


def sim(i, j, m_info):
    """
    :param i: list of features of 'i'
    :param j: list of features of 'j'
    :param m_info: dictionary with the matrix information about min and max values of all features
    :return: similarity of the data points 'i' and 'j'
    :rtype : float
    """
    alfa = -math.log(0.5) / 0.3  # missing the " / avg(dist)"

    return math.exp(-alfa * dist(i, j, m_info))


# input: list of a list of features of attributes
# [[f1,f2,f3],[f1,f2,f3],[f1,f2,f3],[f1,f2,f3]]
#
# return: dictionary with information about the matrix
def get_info(m):
    """
    :param m: list of attributes with a list of features
    :return: dictionary with the matrix information about min and max values of all features
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


def get_distance_matrix(m):
    """
    :param m: list of attributes with a list of features
    :return: matrix with the distances between the attributes along all the features direction
    :rtype : list
    """
    # init the distance matrix
    dm = [[0.0 for j in range(len(m))] for i in range(len(m))]

    m_info = get_info(m)
    # calculate the distances while i < j. dist(i , j) = dist(j, i)
    for i in range(len(m)):
        for j in range(i + 1, len(m)):
            dm[i][j] = dist(m[i], m[j], m_info)

    return dm


def entropy(m):
    """
    :rtype : float
    :param m: list of attributes with a list of features 
    :return: entropy of the attributes set
    """
    m_info = get_info(m)
    len_rows = m_info['len_rows']
    distance_matrix = get_distance_matrix(m)
    entropy = 0.0

    for i in range(len_rows):
        for j in range(i + 1, len_rows):
            if m[i] != m[j]:
                sim_ij = sim(m[i], m[j], m_info)
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
        for arg in args:
            matrix = []
            with open(arg, 'rb') as csvfile:
                cr = csv.reader(csvfile, delimiter=',')
                for row in cr:
                    matrix.append(row[:-1])

            print "Entropy of %s = %f" % (arg, entropy(matrix))

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "Para ajuda -h ou --help"
        return 2


if __name__ == '__main__':
    sys.exit(main())