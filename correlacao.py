#-*- coding: utf-8 -*-

# Algoritmo para calcular a correlação, erroQuadratoMinimo ou maximaCompressao

import math
import sys
import getopt
import csv
from matplotlib.pylab import *


# media de um vetor x de números
def media(x):
    somatorio = 0.0
    for item in x:
        somatorio += float(item)

    return somatorio / len(x)

# variancia de um vetor x de numeros
def var(x):
    somaQuadratica = 0.0

    for item in x:
        somaQuadratica += float(item)**2

    return somaQuadratica / len(x) - media(x)**2

def covariancia(v1,v2):
    somatorio = 0.0
    for i in range(len(v1)):
        somatorio += float(v1[i]) * float(v2[i])

    return somatorio / len(v1) - media(v1) * media(v2)


def correlacao(v1, v2):
    return covariancia(v1,v2) / math.sqrt(var(v1)*var(v2))

def erroQuadradoMinimo(v1, v2):
    return var(v2) * (1 - correlacao(v1,v2)**2)

def maximaCompressao(v1,v2):
    return var(v1) + var(v2) - math.sqrt((var(v1) + var(v2))**2 - 4*var(v1)*var(v2)*(1 - (correlacao(v1,v2))**2))

# Calcula a transposta da matrix. A coluna i vira a linha i
def transposta(matrix):

    n = len(matrix) # número de linhas
    m = len(matrix[0]) # número de colunas

    # matrix transposta inverte linha por coluna e coluna por linha
    matrixT = [[0 for x in range(n)] for x in range(m)]

    for i in range(n):
        for j in range(m):
            matrixT[j][i] = matrix[i][j]

    return matrixT

def printMatrix(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        for j in range(m):
            print matrix[i][j],
        print


# Matrix com linhas representando os vetor de features e coluna representando a instancia
# Opção 1 -> Correlação
# Opção 2 -> Erro quadrático mínimo
# Opção 3 -> Maxima compressão
def calculaSimilaridade(matrix, opcao):

    # numero de linhas
    n = len(matrix)
    # inicializa a matriz de similaridade NxN onde N é o número de colunas da matriz
    matrixResultado = [[0.0 for x in range(n)] for x in range(n)]
    # para cada linha menos a última
    for i in range(n - 1):
        # para cada linha seguinte até a última
        for j in range(i + 1, n):
            # calculo similaridade entre os vetores

            if opcao == 1: # Matrix simétrica [i][j] = [j][i]
                matrixResultado[i][j] = 1 - abs(correlacao(matrix[i], matrix[j]))
                matrixResultado[j][i] = matrixResultado[i][j]

            elif opcao == 2: # Matrix assimétrica [i][j] != [j][i]
                matrixResultado[i][j] = erroQuadradoMinimo(matrix[i], matrix[j])
                matrixResultado[j][i] = erroQuadradoMinimo(matrix[j], matrix[i])

            elif opcao == 3: # Matrix simétrica [i][j] = [j][i]
                matrixResultado[i][j] = maximaCompressao(matrix[i], matrix[j])
                matrixResultado[j][i] = matrixResultado[i][j]
    return matrixResultado

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
def main(argv=None):
    if argv is None:
        argv = sys.argv

    alg = "" # define o algoritmo a ser usado: 1 - correlação | 2 - Erro quadrático mínimo | 3 - máxima compressão
    matrix = []
    matrixT = []

    # parse a linha de comando
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ha:i:", ["help", "input="])
        except getopt.error, msg:
            raise Usage(msg)

        # processa as opções
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
            if o in ("-a"):
                alg = a
            if o in ("-i", "--input"):
                with open (a, 'rb') as csvfile:
                    cr = csv.reader(csvfile, delimiter=',')
                    for row in cr:
                        matrix.append(row)

                    matrixT = transposta(matrix)

        if alg != "" and matrixT != []:
            matrix = calculaSimilaridade(matrixT[:-1], int(alg))
            printMatrix(matrix)
            matshow(matrix)
            colorbar()
            show(matrix)
        else:
            print 'Uso: python', argv[0], '-i input.arff -a algorithm'


        # processa os argumentos
        for arg in args:
            print 'arg'
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "para ajuda use --help"
        return 2

if __name__ == '__main__':
    sys.exit(main())

