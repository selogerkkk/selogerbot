import numpy as np
import cv2

# Carregando a imagem de referência
imagem_referencia = cv2.imread('ref.png')

# Convertendo a imagem de referência para escala de cinza
imagem_referencia_gray = cv2.cvtColor(imagem_referencia, cv2.COLOR_BGR2GRAY)

# Definindo os valores de intensidade para estrela e quadrado
intensidade_estrela = 255
intensidade_quadrado = 0

# Definindo o limite inferior de intensidade para considerar como quadrado
limite_inferior = 100

# Obtendo as dimensões do grid
altura_grid, largura_grid = 5, 5

# Redimensionando a imagem de referência para o tamanho do grid
imagem_referencia_resized = cv2.resize(imagem_referencia_gray, (largura_grid, altura_grid))

# Criando o grid
grid = np.zeros((altura_grid, largura_grid), dtype=int)
posicoes_estrelas = []
for i in range(altura_grid):
    for j in range(largura_grid):
        if imagem_referencia_resized[i, j] > limite_inferior:
            grid[i, j] = intensidade_estrela
            posicoes_estrelas.append((i, j))

        else:
            grid[i, j] = intensidade_quadrado

for i in range(altura_grid):
    for j in range(largura_grid):
        if grid[i, j] == intensidade_estrela:
            print("⭐️", end='')
        else:
            print("⬛️", end='')
    print()
    
# Exibindo as posições das estrelas
print("Posições das estrelas:")
for posicao in posicoes_estrelas:
    print(posicao)
