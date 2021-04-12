#Primero Importamos las librerias que se estarán utilizando.
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

#Seteamos las variables y leemos los CSV para hacer un Pronostico de Temperatura.
df=pd.read_csv('/content/MaunaLoaDailyTemps.csv',index_col='DATE'   ,parse_dates=True)
df=df.dropna()
print('Shape of data',df.shape)
df.head()
df

#Realizamos trazabilidad de losd datos. Con esto podremos predecir la temperatura de promedio.
df['AvgTemp'].plot(figsize=(12,5))

#Realizamos pruebas de estadística fija para verificar si los datos son estacionarios o no.

def ad_test(dataset):
	dftest = adfuller(dataset, autolag = 'AIC')
	print("1. ADF : ",dftest[0])
	print("2. P-Value : ", dftest[1])
	print("3. Num Of Lags : ", dftest[2])
	print("4. Num Of Observations Used For ADF Regression:",      dftest[3])
	print("5. Critical Values :")
	for key, val in dftest[4].items():
		print("\t",key, ": ", val)
adf_test(df['AvgTemp'])

#Se define el Modelo ARIMA. Este realizará el modelo automaticamente, gracias a la librería: pmdarima.
stepwise_fit = auto_arima(df['AvgTemp'], trace=True,
suppress_warnings=True)

#Dividimos los conjuntos de datos en las secciones de entrenamiento y prueba, y realizamos predicciones sobre
#los datos de prueba.
print(df.shape)
train=df.iloc[:-30]
test=df.iloc[-30:]
print(train.shape,test.shape)

#En este punto se crea el modelo ARIMA Automaticamente.
model=ARIMA(train['AvgTemp'],order=(1,0,5))
model=model.fit()
model.summary()

#Aquí se ecnontrarán los modelos de prueba y podremos realizar una predicción de tempreratura
#sobre los datos de prueba. Estos se podrán comparar a las predicciones con datos reales.
start=len(train)
end=len(train)+len(test)-1
pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
pred.plot(legend=True)
test['AvgTemp'].plot(legend=True)

#Con esto podremos verificar y asegurarnos de que el modelo esta bien o mal hecho.
test['AvgTemp'].mean()
rmse=sqrt(mean_squared_error(pred,test['AvgTemp']))
print(rmse)

#https://ichi.pro/es/pronostico-de-temperatura-con-el-modelo-arima-en-python-73096807304019