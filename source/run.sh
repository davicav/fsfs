#!/bin/bash

echo "Calculando a Entropia de todos os arquivos CFS..."
find . -name "*.CFS.csv" -type f | xargs python entropy_all.py > entropias_CFS.txt
echo "Arquivo entropias_CFS.txt criado"
echo "Calculando a Entropia de todos os arquivos FULL..."
find . -name "*.FULL.csv" -type f | xargs python entropy_all.py > entropias_FULL.txt
echo "Arquivo entropias_FULL.txt criado"
