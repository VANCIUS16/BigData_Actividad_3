 
#def loadDataSet():
#    '''
# Asumiendo que la comisaría tiene un total de 5 productos a la venta
 # Este método construye 4 registros de transacciones (dataSet)
#    '''
#    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
 
 
def createC1(dataSet):
    '''
         Este método consiste en obtener un conjunto de elementos con 1 elemento, es decir, un conjunto de elementos.
    '''
         C1 = [] # Conjunto de elementos con 1 elemento (conjunto de elementos poco frecuente, porque no se ha comparado con el soporte mínimo)
    for transaction in dataSet:
        for item in transaction:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
         return map (frozenset, C1) #Convertir C1 de una lista de Python a un conjunto invariante (frozenset, una estructura de datos en Python)
 
 
def scanD(D, Ck, minSupport):
    '''
         Donde D es el conjunto de datos completo (una colección de todos los registros de transacciones).
         Ck es un conjunto candidato de tamaño k (que contiene k elementos). Por ejemplo, si contiene un elemento, entonces Ck es C1, y así sucesivamente.
         minSupport es el soporte mínimo establecido.
         Este método se utiliza para filtrar los conjuntos de elementos frecuentes más grandes que minupport
    '''
         ssCnt = {} #Almacenar todos los elementos combinados aleatoriamente (1 conjunto de elementos, 2 conjuntos de elementos, etc.) y el número de ocurrencias de un subconjunto de registros de transacciones
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0) + 1
    numItems = float(len(D))
         retList = [] #retList es el conjunto de elementos frecuentes que se encuentra en Ck (el soporte es mayor que minSupport)
         supportData = {} #supportData registra el soporte de cada conjunto de elementos frecuentes
    for key in ssCnt:
        if support >= minSupport:
            retList.insert(0, key)
            supportData[key] = support
    return retList, supportData
 
 
def aprioriGen(Lk, k):
    '''
         Esta función genera un conjunto de elementos candidatos C (k + 1) a través de la lista de conjuntos de elementos frecuentes Lk y el número de conjuntos de elementos k.
         Todos los conjuntos binomiales formados por la combinación libre de un conjunto de elementos, si el primer elemento de dos conjuntos binomiales es igual, se generan tres conjuntos de elementos.
         Tenga en cuenta que en el proceso de generación, cada conjunto de elementos se ordena primero por elemento y luego se comparan dos conjuntos de elementos cada vez.
         Los dos elementos se combinan solo cuando los primeros elementos k-1 son iguales. Esto se hace porque la función no fusiona las colecciones en pares.
         No todos los conjuntos generados de esa manera tienen k + 1 elementos.
         Bajo la premisa de que el número de elementos restringidos es k + 1, solo cuando los primeros k-1 elementos son iguales y el último elemento es diferente, la combinación puede ser el nuevo conjunto de elementos candidatos requerido.
    '''
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
                         # Cuando los primeros elementos k-2 sean iguales, combine los dos conjuntos
                         L1 = lista (Lk [i]) [: k-2] #Convierte el conjunto en una lista y toma rodajas. Por ejemplo, el conjunto ([1,3]) se convierte en una lista y se convierte en [1,3]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                                 retList.append (Lk [i] | Lk [j]) # Encuentra la unión del conjunto y agrégala a retList
    return retList
 
 
def apriori(dataSet,minSupport=0.5):
    '''
         Función total
    '''
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L,supportData


import apriori
def generateRules(L, supportData, minConfident=0.5):
    '''
         Esta función es la función principal y llama a las otras dos funciones. Las otras dos funciones son rulesFromConseq () y calcConf (), que se utilizan para generar conjuntos de reglas candidatos y evaluar reglas (calcular el soporte), respectivamente.
         La función generateRules () tiene 3 parámetros:
         Lista de conjuntos de elementos frecuentes L, soporte de diccionario Datos que contienen los datos de soporte de conjuntos de elementos frecuentes, umbral mínimo de credibilidad minConf.
         Al final de la función, se genera una bigRuleList que contiene una lista de reglas de credibilidad, que se puede ordenar en función de la credibilidad más adelante.
         L y supportData son exactamente la salida de la función apriori ().
         Esta función atraviesa cada conjunto de elementos frecuentes en L y construye una lista H1 que contiene solo un conjunto de elementos para cada conjunto de elementos frecuentes.
         La i en el código indica el número de elementos contenidos en el conjunto de elementos frecuentes actual,
         freqSet es el conjunto de elementos frecuentes que se atraviesa actualmente (recuerde que la estructura organizativa de L es organizar los conjuntos de elementos frecuentes con el mismo número de elementos en listas y luego formar una lista grande de cada lista, por lo que para recorrer los conjuntos de elementos frecuentes en L, necesita Use un bucle de dos capas).
    '''
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
                         H1 = [frozenset ([item]) for item in freqSet] # Por ejemplo, para freqSet (conjunto de elementos frecuentes) frozenset ([a, b, c,…]), el valor de H1 es [a, b, c,…] ( A, b, c, etc.en la lista son tipos de conjuntos congelados)
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConfident)
    return bigRuleList
 
 
 
def calcConf(freqSet, H, supportData, brl, minConfident=0.5):
    '''
         Evaluar conjuntos de reglas candidatos
         Calcule la credibilidad de la regla y encuentre la regla que cumpla con el requisito mínimo de credibilidad.
         La función devuelve una lista de reglas que cumplen con los requisitos mínimos de credibilidad y agrega esta lista de reglas a bigRuleList de la función principal (a través del parámetro brl).
         El valor de retorno prunedH contiene la parte derecha de la lista de reglas. Este valor se usará en la siguiente función rulesFromConseq ().
    '''
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConfident:
            print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH
 
 
def rulesFromConseq(freqSet, H, supportData, brl, minConfident=0.5):
    '''
         Genere conjuntos de reglas candidatas, por ejemplo, {2,3} genera reglas candidatas {2} ➞ {3}, {3} ➞ {2}.
         Genere el conjunto de reglas candidatas del siguiente nivel de acuerdo con el conjunto de reglas candidatas actual H
         Genere más reglas de asociación a partir del conjunto de elementos inicial.
         Esta función tiene dos parámetros: FreqSet de elementos frecuentes, que puede aparecer en la lista de elementos H a la derecha de la regla.
         Los parámetros restantes: supportData guarda el soporte del conjunto de elementos, brl guarda las reglas de asociación generadas y minConf es lo mismo que la función principal.
         La función primero calcula el tamaño del conjunto de elementos frecuentes m en H. A continuación, compruebe si el conjunto de elementos frecuentes es lo suficientemente grande como para eliminar un subconjunto de tamaño m.
    Si es posible, retírelo. Utilice la función aprioriGen () para generar una combinación no repetida de elementos en H, y el resultado se guarda en Hmp1, que también es la lista H para la siguiente iteración.
    '''
    m = len(H[0])
         while (len (freqSet)> m): # Juzgue la longitud> m, entonces se puede obtener la credibilidad de H
        H = calcConf(freqSet, H, supportData, brl, minConfident)
                 if (len (H)> 1): # Determine si hay un elemento con una credibilidad mayor que el umbral después de que se calcula la credibilidad para generar la siguiente capa de H
            H = apriori.aprioriGen(H, m + 1)
            m +=1
                 else: # No se puede continuar generando el siguiente nivel de reglas de asociación de candidatos, salga del ciclo antes
            break

#https://programmerclick.com/article/8103986113/