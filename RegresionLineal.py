#Realizamos las importaciones de las libreias que utilizaremos.
import numpy as np #Librería numérica
import matplotlib.pyplot as plt # Para crear gráficos con matplotlib
from sklearn.linear_model import LinearRegression #Regresión Lineal con scikit-learn
%matplotlib inline #Este es especificamente para realizar gráficos dentro de un jupyter notebook

#Creamos una Función que nos dara numeros aleatorios y los retornará.
def f(x):  # función f(x) = 0.1*x + 1.25 + 0.2*Ruido_Gaussiano
    np.random.seed(42) # para poder reproducirlo
    y = 0.1*x + 1.25 + 0.2*np.random.randn(x.shape[0])
    return y

#Se generan valores entre 0 a 20 con intervalos de 0.5, y estos se calculan dentro de la 
#funcion f.
x = np.arange(0, 20, 0.5)
y = f(x)

# Realizamos un gráfico de los datos que se han generado y este se imprime.
plt.scatter(x,y,label='data', color='blue')
plt.title('Datos');

#https://www.iartificial.net/regresion-lineal-con-ejemplos-en-python/#Datos_de_ejemplo