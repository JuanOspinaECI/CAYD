import numpy as np
import matplotlib.pyplot as plt
import sys
import math
import random

QAM_tam = 8
#sqr_tam = int(math.sqrt(QAM_tam))
sqr_tam = 8
#Función para generar vector aletaorio
#tam: es el numero de bloques a generar (8 bits cada uno)
#Retorna una matriz con vectores de 8 bits aletorios (0-1)
def bits_ran(tam):
  bloques = []
  for k in range(0,tam):
    bloque = []
    for j in range(0,QAM_tam):
      bloque += [random.randint(0, 1)]
    bloques += [bloque]
  return bloques

# Funcion para convertir de lista de binario a decimal
# El parametro bits es un vector de n bits (int 0 - 1)
# La funcion retorna el numero decimal (int)
def conv_bin_dec(bits):
  contador = 0
  suma = 0
  for k in bits: 
    suma += k*2**(contador)
    contador += 1
  return suma

#Creación de vectores y diccionario de modulación (tabla de verdad)

#Creación vectores A Y B 
# A: son las magnitudes del eje x
# B: son las magnitudes del eje y
# La modulación 256QAM cada cuadrante tendra 8 magnitudes en x y 8 en y
# La modulación 64QAM cada cuadrante tendra 4 magnitudes en x y 4 en y
# La modulación 16QAM cada cuadrante tendra 2 magnitudes en x y 2 en y
# Se generan vectores multiplos de 0.25 que hacen referencia a las diferetnes magnitudes de x y (senwt y coswt)

#Tipo de modulacion
print("Elija tipo de modulacion")
print("1. 16-QAM")
print("2. 64-QAM")
print("3. 256-QAM")
MOD = int(input())

if MOD == 1:
    QAM_tam = 4
    sqr_tam = 2
elif MOD == 2:
    QAM_tam = 6
    sqr_tam = 4
elif MOD == 3:
    QAM_tam = 8
    sqr_tam = 8
A = []
B = []
for j in range(1,sqr_tam+1):
  A += [0.25*j]
  B += [0.25*j]


#Creación de tablas de verdad de Amplitud y Fase
#Seran tablas de 0-15/63/255, donde estaran orgnizados según la posicion 
Amplitud = []
Fase = []


for j in range(0,sqr_tam):
  for k in range(0,sqr_tam):
    # Cuadrante 1
    Amplitud += [math.sqrt(A[j]**2+B[k]**2)]
    Fase += [math.atan(B[k]/A[j])]
    # Cuadrante 2
    Amplitud += [math.sqrt(A[j]**2+B[k]**2)]
    Fase += [math.pi - math.atan(B[k]/A[j])]
    # Cuadrante 3
    Amplitud += [math.sqrt(A[j]**2+B[k]**2)]
    Fase += [math.pi + math.atan(B[k]/A[j])]
    # Cuadrante 4
    Amplitud += [math.sqrt(A[j]**2+B[k]**2)]
    Fase += [2*math.pi - math.atan(B[k]/A[j])]

#Ver vectores de amplitu y Fase
#print(Amplitud)
#print(Fase)



#Pedir datos al usuario 

num = int(input("Ingrese numero de bloques de (bits)"))
frec_portadora = int(input("Ingrese frecuencia de portadora en Hz"))

#Generar bloques de vectores aleatorios con la funcion bits_ran(num)
bloques_bin = bits_ran(num)

#Generar bloques en formato decimal y señales seno
bloques_dec = [] #Vector para almacenar el valor en decimal de cada bloque (no se utiliza en el procesamiento de datos)

#Vector de tiempo (Vector correspondiente a todos los bloques generados)
t_full=np.linspace(0,1/frec_portadora*num, num = 100*num)

signal = []
cons_x = []
cons_y = []

for k in range(0,num):
  #Convertir bloques a decimal
  decimal = conv_bin_dec(bloques_bin[k])
  bloques_dec += [decimal]
  #Mostrar el bloque de bits en binario y su respectiva amplitud y fase
  print(bloques_bin[k], "Amplitud", Amplitud[decimal], "Fase",int(Fase[decimal]*180/np.pi) )
  cons_x += [Amplitud[decimal]*np.cos(Fase[decimal])]
  cons_y +=[Amplitud[decimal]*np.sin(Fase[decimal])]
  #Generar señale seno por cada bloque
  t = np.linspace(1/frec_portadora*k,1/frec_portadora*(k+1), num = 100)
  signal += [Amplitud[decimal] * np.sin(frec_portadora * 2.0 * np.pi * t + Fase[decimal])]
#print(bloques_dec)


#Concatenar señales seno generadas 
if num == 1:
  signal_2 = signal[0]
for k in range(1,num):
  if k == 1:
    signal_2 = np.concatenate((signal[k-1],signal[k]))
    #print(len(signal_2))
  else:
    signal_2 = np.concatenate((signal_2,signal[k]))
    #print(len(signal_2))

#print(signal_2)
plt.plot(t_full,signal_2)
plt.show()


plt.plot(cons_x,cons_y,'bo')
plt.show()
