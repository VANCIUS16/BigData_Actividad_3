#Primero se realizan los import de las librerias que se estará utilizando
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sb
%matplotlib inline

#Realizamos lectura de los archivos CSV
dataframe = pd.read_csv(r"usuarios_win_mac_lin.csv")
dataframe.head()

#Asiganmos un nombre al método y lo mandamos llamar para recibir un poco de información
#de estadistica básica. Media, Desviación Estándar, Mínimo y Máximo.
dataframe.describe()

#Analizamos cuántos resultados de cada tipo usando la función 'groupby' 
print(dataframe.groupby('clase').size())

#VISUALIZACIÓN DE DATOS
#Visualizaremos mediante diferentes gráficas como:
#Acciones, Duración, Páginas, Valor
dataframe.drop(['clase'],1).hist()
plt.show() 

#Procedemos a interrelacionar las entradas de pares, para ver como se concentran linealmente
#las salidas de usuarios por colores.
sb.pairplot(dataframe.dropna(), hue='clase',size=4,vars=["duracion", "paginas","acciones","valor"],kind='reg')

#CREANDO MODELOS DE REGRESIÓN LOGÍSTICA
#cargamos las variables de 4 columnas de entrada en X excluyendo la columna “clase” con el método drop().
#Agregamos la columna “clase” en la variable y. 
#Ejecutamos X.shape para comprobar la dimensión de nuestra matriz con datos de entrada de 170 registros por 4 columnas.	
X = np.array(dataframe.drop(['clase'],1))
y = np.array(dataframe['clase'])
X.shape

#Creamos el modelo y hacemos que se ajuste (fit) al conjunto de entradas X y salidas ‘y’.
model = linear_model.LogisticRegression()
model.fit(X,y)

#Clasificamos todo nuestro conjunto de entradas X utilizando el método “predict(X)” y
#revisamos algunas de sus salidas y vemos que coincide con las salidas reales del archivo csv.
predictions = model.predict(X)
print(predictions)[0:5]

#Confirmamos cuan bueno fue el modelo utilizando model.score().
#Nos devuelve la precisión media de las predicciones, en nuestro caso del 77%.
model.score(X,y)

#VALIDACIÓN
#Subdividimos los datos de entrada en forma aleatoria utilizando 80% de registros para
#entrenamiento y 20% para validar.
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, y, test_size=validation_size, random_state=seed)

#Volvemos a compilar el modelo de Regresión Logística pero esta vez sólo con 80%
#de los datos de entrada y calculamos el nuevo scoring que ahora nos da 74%.
name='Logistic Regression'
kfold = model_selection.KFold(n_splits=10, random_state=seed)
cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring='accuracy')
msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
print(msg)

#Ahora se realizan las predicciones.
predictions = model.predict(X_validation)
print(accuracy_score(Y_validation, predictions))

#REPORTE DE RESULTADOS
print(confusion_matrix(Y_validation, predictions))

#Reporte de clasificación con nuestro conjunto de Validación.
print(classification_report(Y_validation, predictions))

#CLASIFICACIÓN O PREDICCIÓN DE NUEVOS VALORES 	
X_new = pd.DataFrame({'duracion': [10], 'paginas': [3], 'acciones': [5], 'valor': [9]})
model.predict(X_new)

#https://www.aprendemachinelearning.com/regresion-logistica-con-python-paso-a-paso/