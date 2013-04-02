#!/bin/bash

echo "Calculando a Entropia de todos os arquivos TRN..."
find . -name "*trn.csv" -type f | xargs python entropy_all.py > entropias_TRN.txt
echo "Arquivo entropias_TRN_FULL.txt criado"
echo "Calculando a Entropia de todos os arquivos FULL..."
find . -name "*.trn_full.csv" -type f | xargs python entropy_all.py > entropias_TRN_FULL.txt
echo "Arquivo entropias_TRN_FULL.txt criado"
