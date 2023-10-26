# %%
#PARTE 0: ESTABLECER DIRECTORIO DE TRABAJO

# %%
import os 
print(os.chdir("G:\\Hondt"))

# %%
print('Directorio de trabajo: ',os.getcwd())


# %%
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
import pandas as pd
import warnings
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
while True:
    voto=input ('introduce el nombre del fichero de resultados de la votación: ')
        votos=voto+year+'.xlsx'
    try:
        print('nombre del fichero: ',votos)
        df0 = pd.read_excel(votos,header=0)
        break
    except:
        print('no existe')

df0.head()#df0 es el resultado de las elecciones 
