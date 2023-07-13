'''
El Juego de la Vida - Conway

~Adaptado por Óscar Mirás~

REGLAS

% 1) Cualquier célula viva con menos de dos vecinas muere.
% 2) Cualquier célula viva con más de cuatro vecinas muere.
% 3) Cualquier célula viva con dos e tres vecinas sigue viva en la siguiente generación.
% 4) Cualquier célula muerta con exactamente tres vecinas vivas, se convierte en una célula viva.


'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randint
from functools import reduce
from math import floor


'''
INICIALIZACIÓN DE LA MALLA

'''


def crear_mundo(M, N):
    # Crea una matriz de tamaño MxN con células muertas.
    mundo = np.zeros((M, N))
    return mundo

def inicializar_mundo(mundo):
    # Agrega células vivas aleatoriamente al mundo.
    M, N = mundo.shape #Forma rápida de tomar las dimensiones de la matriz creada con numpy (np).
    for i in range(M):
        for j in range(N):
            mundo[i, j] = randint(0, 1)
    return mundo

def contar_células_vivas(mundo):
    M, N = mundo.shape
    contador = reduce(lambda x,y: x+y, [mundo[i][j] for i in range(M) for j in range(N) if mundo[i][j] == 1])
    return int(contador)

def calcular_vecinos(mundo):
    # Calcula el número de vecinos vivos de cada célula.
    M, N = mundo.shape
    vecinos = np.zeros((M, N))
    for i in range(1, M-1):
        for j in range(1, N-1):
            # Suma los valores de las 8 células vecinas.
            vecinos[i, j] = np.sum(mundo[i-1:i+2, j-1:j+2]) - mundo[i, j] #No contamos el caso de la propia celda.
    return vecinos


def actualizar_mundo(mundo, vecinos):
    # Actualiza el mundo según las reglas del juego.
    M, N = mundo.shape
    for i in range(1, M-1):
        for j in range(1, N-1):
            if mundo[i, j] == 1 and (vecinos[i, j] < 2 or vecinos[i, j] > 3): # (CASOS 1 y 2) Si vecinos es menor que 2 o mayor que 3 [...]
                mundo[i, j] = 0 #[...] la célula muere.
            elif mundo[i, j] == 0 and vecinos[i, j] == 3: # (CASO 4) Si es una célula muerta y tiene 3 vecinas "vivas", se vuelve viva.
                mundo[i, j] = 1
            # (CASO 3) Se obvia el caso en el que vecinos[i,j] sea == 2 o vecinos[i,j] sea == 3, ya que la célula se mantendría viva.
    return mundo


def restringir_malla(mundo):
    M, N = mundo.shape
    submalla = mundo[floor(M/3) : floor((2*M)/3), floor(N/3) : floor((2*N)/3)] #Restringimos la malla imprimible a un tamaño menor.
    return submalla
    

matriz = crear_mundo(50, 50) #Creamos un mundo matriz/malla 30 x 30 lleno de "0s".
inicializar_mundo(matriz) #Repartimos células vivas por la malla.

plt.imshow(matriz, cmap="gray") #Toma colores para representar imágenes (cmap es el "mapa de colores"). 
plt.title("Malla inicial (aleatoria)")
plt.show() #Enseñamos la malla previa a la animación en sí.



'''
EL JUEGO DE LA VIDA - ANIMACIÓN 

'''

# Función de actualización para la animación.
def update(frame):
    global matriz
    M,N = matriz.shape
    vecinos = calcular_vecinos(matriz)
    matriz = actualizar_mundo(matriz, vecinos)
    número_células_vivas = contar_células_vivas(matriz)
    submalla = restringir_malla(matriz)
    plt.clf() #Borras las figuras de antes continuadamente frame tras frame para que no se superpongan.
    plt.imshow(matriz, cmap="gray")
    plt.title("Generación {}".format(frame)) #Plot del Número de Generación.
    plt.figtext(0.006, 0.035, "Nº Células Vivas: {}".format(número_células_vivas)) #Plot del Número de Células vivas.
    plt.figtext(0.001, 0, "Tamaño de Malla: {}".format(M * N)) #Plot del Número de Células vivas.


# Crear la animación y mostrarla.
fig, ax = plt.subplots() #Se crea figura (fig) y conjunto de ejes vacío en esa figura (ax).
ani = FuncAnimation(fig, update, frames=range(1, 2000), repeat=False, interval = 2) #Si disminuímos interval, podemos aumentar los frame/s.
plt.show()

print("\nSimulación finalizada con éxito. La vida siempre se abre camino...")




