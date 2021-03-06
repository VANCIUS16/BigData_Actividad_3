# importamos las librerías que necesitamos
from sklearn.datasets import load_iris # datos de iris
from sklearn.tree import DecisionTreeClassifier # árbol de decisión para clasificación

iris = load_iris()
print(iris.DESCR) # información sobre del conjunto de datos iris

# lo más relevante es:
#    :Number of Instances: 150 (50 in each of three classes)
#    :Number of Attributes: 4 numeric, predictive attributes and the class
#    :Attribute Information:
#        - sepal length in cm
#        - sepal width in cm
#        - petal length in cm
#        - petal width in cm
#        - class:
#                - Iris-Setosa
#                - Iris-Versicolour
#                - Iris-Virginica

# veamos 4 filas donde ocurre un cambio de clase
print(iris.data[48:52,:])

# da el resultado
# [[5.3 3.7 1.5 0.2]
#  [5.  3.3 1.4 0.2]
#  [7.  3.2 4.7 1.4]
#  [6.4 3.2 4.5 1.5]]

# para la variable a predecir también hacemos lo mismo
print(iris.target[48:52])

# La clase 0 es Iris-Setosa, la 1 es Iris-Versicolor y la 2 es Iris-Virginica
# [0 0 1 1]

# Vamos a crear y entrenar un árbol de decisión para clasificar los datos de Iris
tree = DecisionTreeClassifier(max_depth=2, random_state=42) # vamos a usar un árbol de profundidad 2
tree.fit(iris.data, iris.target) # entrenamiento del árbol

# podemos usar el método predict para obtener predicciones
print( tree.predict(iris.data[47:53]) )

# resulta en
# [0 0 0 1 1 1]

# si queremos saber las probabilidades podemos usar el método predict_proba
print( tree.predict_proba(iris.data[47:53]) )

# la primera clase (Setosa) es la primera columna, la segunda clase en la segunda, etc..
# este es el resultado:
# [[1.         0.         0.        ]
#  [1.         0.         0.        ]
#  [1.         0.         0.        ]
#  [0.         0.90740741 0.09259259]
#  [0.         0.90740741 0.09259259]
#  [0.         0.90740741 0.09259259]]

#https://www.iartificial.net/arboles-de-decision-con-ejemplos-en-python/