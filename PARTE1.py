#!/usr/bin/env python
# coding: utf-8
# %%
#PARTE I: IMPORTACIÓN DE DATOS


# %%
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
import pandas as pd
import warnings
#importar datos de las elecciones. Son del Ministerio del Interior adaptados
while True:
    voto=input ('introduce el nombre del fichero de resultados de la votación: ')
    year=input('y el año: ')
    votos=voto+year+'.xlsx'
    try:
        print('nombre del fichero: ',votos)
        df0 = pd.read_excel(votos,header=0)
        break
    except:
        print('no existe')

df0.head()#df0 es el resultado de las elecciones 


# %%
# importar partidos por grupo
parties=input ('introduce el nombre del fichero de partidos: ')
year=input('y el año: ')
party=parties+year+'.xlsx'
    
try:
    print('nombre del fichero: ',party)
    df2 = pd.read_excel(party)
except:
    print('no existe')
df2.head()#df2 es la lista de partidos y grupos 

#genero la lista de claves de partidos
l=[]
for item in df2:
    l.append(str(item))
     


# %%
df2.head()

# %%
party1=set(df2.loc[1])
grupos=list(party1)
party2=pd.Series(df2.columns.values,index=df2.columns.values)
party2=pd.DataFrame(party2)


# %%
#añado a cada partdo un número de identificación que será el usado en adelante
warnings.filterwarnings("ignore")
df2=pd.concat([df2,pd.DataFrame(party2.T)],ignore_index=True).copy()


# %%
party2.T.head()

# %%
df2.head()


# %%
#definimos función que permita conocer la estructura de un DataFrame. Es muy
#necesario para construir Data Frames.
def estructura(my_Frame):
    A=[]
    B=[]
    C=[]
    my_Frame=my_Frame.keys()
    my_List=list(my_Frame)
    for i in range (len(my_List)):
        A.append(my_List[i])
        B.append(i)
    col_list=list(zip(B,A))
   #print('Longitud:',len(col_list),'\n', 'Posición y labels:','\n',col_list)
    return col_list


# %%
estructura(df0)#da una lista de diccionarios donde cada diccionario es un
#número:nombre de columna.


# %%
#creamos dos variables para número de provincias y de partidos
N_PROV=len(df0)
N_PARTIDOS=len(df2.T)
print(N_PROV,N_PARTIDOS)


# %%
#renombramos algunas columnas
df0.rename(columns={'Nombre de Comunidad':'COMUNIDAD','Código de Provincia': 'NPROVINCIA',
'Nombre de Provincia':'PROVINCIA','Total censo electoral': 'CENSO_ELECTORAL',
'Total votantes':'TOTAL_VOTANTES',
'Votos en blanco':'VOTOS_BLANCOS','Votos válidos':'VOTOS_VÁLIDOS','Diputados':'DIPUTADOS',
'Población':'POBLACIÓN','Votos a candidaturas':'VOTOS A CANDIDATURAS',
'Votos nulos':'VOTOS NULOS','Diputados':'DIPUTADOS'},
inplace=True )


# %%
#extraemos las columnas que nos serán necesarias para aplicar el método d'Hondt
W1=[]#datos de provincia y votos de cada partidos
W2=[]#escaños de cada partido
for i in range(0,17):
    W1.append(df0.loc[0].keys()[i])
for i in range(17,151):
    if ('Votos' in df0.loc[0].keys()[i]):
        W1.append(df0.loc[0].keys()[i])
for i in range(17,151):    
    if ('Diputados' in df0.loc[0].keys()[i]):
        W2.append(df0.loc[0].keys()[i])

print(W1)
print(W2)


# %%
Y=[]#nombres de columnas con los votos a cada partido
for x in range(17,84):
    if ('Votos' in W1[x]):
        Y.append(W1[x])


# %%
#modificamos df0 el Data Frame que sirve de base a la asignación de escaño y
#que contiene los datos de circunscripción y los votos y diputados

DF1 = pd.DataFrame(data=None, columns=df0.columns, index=df0.index)
DF2 = pd.DataFrame(data=None, columns=df0.columns, index=df0.index)
for i in range(N_PROV):
    for x in W1:
        DF1.loc[i][x]=df0.loc[i][x]
for i in range(N_PROV):
    for x in W2:
        DF2.loc[i][x]=df0.loc[i][x]
DF1=DF1.dropna(axis=1,how='all')
DF2=DF2.dropna(axis=1,how='all')
df0=pd.concat([DF1,DF2],axis=1)


# %%
estructura(df0)


# %%
#inserto participación por provincia
df0.insert(loc = 13,
          column = '%PARTICIPACIÓN',
          value =df0['TOTAL_VOTANTES']/df0['CENSO_ELECTORAL'])


# %%
df0.loc[30]['%PARTICIPACIÓN']


# %%
dfaux0=df0[W1[0:17]]#datos censales y resumidos por provincia


# %%
W1[17:]#votos


# %%
dfaux1=df0[W1[17:]]

# %%
Var=dict(zip(W1[17:],l))#diccionario que asigna votos a 
#identificación numérica de partido


# %%
Var

# %%
dfaux2=df0[W2[0:]]


# %%
#df0

df1=pd.concat([dfaux0,dfaux1,dfaux2], axis=1)


# %%
estructura(df0)

# %%
#eliminamos ciertas columnas innecesarias (Censo CERA, Mesas Electorales...)
#para obtener df1

df1 = df1.drop(df0.columns[[ 4,5,6,8,9,10]], axis=1)


# %%
estructura(df1)


# %%
#inserto número de partidos
df1.insert(loc = 4,
          column = 'NPARTIDOS',
          value =N_PARTIDOS)


# %%
#partidos con más del 3% de votos
df1.insert(loc = 5,
          column = 'PARTIDOS>3',
          value =0)


# %%
df1.loc[1][:]

# %%
df1.rename(columns=Var, inplace=True)

# %%
for x in l:
    columna='%'+x
    df1[columna]=df1[x]/df1['VOTOS_VÁLIDOS']


# %%
df1.head()

