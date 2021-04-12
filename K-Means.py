#Procedemos a importar todas las librerías que se estrán utilizando.
from sklearn.cluster import KMeans

#Cada acción tiene su propio rango. Se tiene que agrupar las acciones por el comportamiento de sus ganancia,
#en vez del precio en el mercado.

#Se calcula el rendimiento de cada acción desde el inicio.
start = stocks.iloc[0]               
returns = (stocks - start) / start   

#Realizamos un clustering con los datos. Instruimos a kmeans a usar 8 grupos. K=8.
kmeans = KMeans(n_clusters=8, random_state=42) 
kmeans.fit(dow_returns.T);

#Muestra de los resultados
'''
Cluster 0: 
    - American Express Co (AXP)
    - General Electric (GE)
    - Goldman Sachs Group (GS)
    - Coca-Cola Company (The) (KO)
    - McDonalds Corp. (MCD)
    - Pfizer Inc. (PFE)
    - Procter & Gamble (PG)
    - United Technologies (UTX)
    - Verizon Communications (VZ)
    - Wal-Mart Stores (WMT)
Cluster 1:
    - Apple Inc. (AAPL)
    - 3M Company (MMM)
Cluster 2:
    - United Health Group Inc. (UNH) 
Cluster 3:
    - Caterpillar Inc. (CAT)
    - Chevron Corp. (CVX)
    - International Business Machines (IBM)
    - Exxon Mobil Corp. (XOM)
Cluster 4:
    - Home Depot (HD)
    - Microsoft Corp. (MSFT)
    - Visa Inc. (V) 
Cluster 5:
    - Cisco Systems (CSCO)
    - Intel Corp. (INTC)
    - Johnson & Johnson (JNJ)
    - JPMorgan Chase & Co. (JPM)
    - Merck & Co. (MRK)
    - The Travelers Companies Inc. (TRV)
Cluster 6:
    - The Walt Disney Company (DIS)
    - Nike (NKE)
Cluster 7:
    - Boeing Company (BA)
'''

#https://www.iartificial.net/clustering-agrupamiento-kmeans-ejemplos-en-python/