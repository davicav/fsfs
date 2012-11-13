fsfs
====

Feature Selection Using Feature Similarity

Este projeto é de uma cadeira do mestrado baseado no documento Unsupervised Feature Selection.pdf
O objetivo é escolher um subconjunto de features para o aprendizado de máquina baseada em métricas
de maneira não supervisionada. Isto é, não temos as classes para classificar as features. Após visto
como se comportam as features em relação às outras de acordo com cada uma das 3 métricas abordadas no
capítulo (correlação, erro quadrático e índice de informação máxima) e escolhido o subconjunto,
é necessário análisar as escolhas feitas utilizando uma outra métrica, conhecida como entropia.

Este projeto apresenta dois códigos-fontes:

  fsfs.py - onde é feito os cálculos das métricas e visualizada uma matrix de similaridades
  entro.py - onde é feita a análise da escolha das features

Não é abordado aqui como fazer a escolha. Você analisa os dados e faz suas escolhas, podendo verificar
a "pureza" dos dados a partir do índice de entropia.