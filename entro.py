import math
import csv
import getopt
import sys

# input: the list of features of i and j and info about the matrix
# return: distancy between i and j
def dist(i, j, m_info):
    len_cols = m_info['len_cols']
    maxf = m_info['maxf']
    minf = m_info['minf']

    dist = 0
    for l in range(len_cols):
        dist += ((float(i[l]) - float(j[l]))/(maxf[l]-minf[l]))**2

    return math.sqrt(dist)

# input: the list of features of i and j and info about the matrix
# return: similiraty of the attributes i and j
def sim(i, j, m_info):
    alfa = -math.log(0.5) / 0.3 # missing the " / avg(dist)"

    return math.exp(-alfa*dist(i, j, m_info))

# input: list of attributes with a list of features
# [[f1,f2,f3],[f1,f2,f3],[f1,f2,f3],[f1,f2,f3]]
#
# return: dictionary with information about the matrix
def get_info(m):
    len_rows = len(m)
    len_cols = len(m[0])

    minf = [sys.float_info.max for row in range(len_cols)]
    maxf = [sys.float_info.min for row in range(len_cols)]

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

# input: list of attributes with a list of features
# [[f1,f2,f3],[f1,f2,f3],[f1,f2,f3],[f1,f2,f3]]
#
# return: entropy of the attributes set
def entropy(m):
    m_info = get_info(m)
    len_rows = m_info['len_rows']
    entropy = 0

    for i in range(len_rows):
        for j in range(len_rows):
            sim_ij = sim(m[i], m[j], m_info)
            print "sim_ij = %f" % sim_ij
            print "alsdfjalsdkj"
            entropy += (sim_ij*math.log(sim_ij) + (1-sim_ij)*math.log(1-sim_ij))

    return -entr

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
                print "Uso:" , argv[0], "input"
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
        print >>sys.stderr, err.msg
        print >>sys.stderr, "Para ajuda -h ou --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())
