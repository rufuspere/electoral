# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
#PARTE 0: IMPORTACIÓN DE PAQUETES Y ESTABLECER DIRECTORIO DE TRABAJO
# -

#importar paquetes y definir directorio
import pandas as pd
import numpy as np
import copy
import csv
import os 
import xlrd
import math
import random
import collections
import warnings
import re
os.chdir("G:\HONDT")

# +
#PARTE I: IMPORTACIÓN DE DATOS
# -

#importar datos de las elecciones. Son del Ministerio del Interior adaptados
while True:
    voto=input ('introduce el nombre del fichero de resultados de la votación: ')
    year=input('y el año: ')
    #votos=voto+year+'.xlsx'
    votos=os.path.join('G:\HONDT', voto+year + '.' + 'xlsx')   
    try:
        print('nombre del fichero: ',votos)
        df1 = pd.read_excel(votos,header=0)
        break
    except:
        print('no existe')
df1.head() 

# +
# importar partidos por grupo

parties=input ('introduce el nombre del fichero de partidos: ')
year=input('y el año: ')
party=parties+year+'.xlsx'
    
try:
    print('nombre del fichero: ',party)
    df2 = pd.read_excel(party)
except:
    print('no existe')
df2.head() 

#genero la lista de claves de partidos
l=[]
for item in df2:
    l.append(str(item))
     
# -

df2


#definimos función que permita conocer la estructura de un DataFrame
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


estructura(df1)

N_PROV=len(df1)
N_PARTIDOS=67

df1.rename(columns={'Código de Provincia': 'NPROVINCIA',
'Nombre de Provincia':'PROVINCIA','Total censo electoral': 'CENSO_ELECTORAL',
'Total votantes':'TOTAL_VOTANTES',
'Votos en blanco':'VOTOS_BLANCOS','Votos válidos':'VOTOS_VÁLIDOS','Diputados':'DIPUTADOS',
'Población':'POBLACIÓN','Votos a candidaturas':'VOTOS A CANDIDATURAS',
'Votos nulos':'VOTOS NULOS','Diputados':'DIPUTADOS'},
inplace=True )

# +
W1=[]
W2=[]
for i in range(0,17):
    W1.append(df1.loc[0].keys()[i])
for i in range(17,151):
    if ('Votos' in df1.loc[0].keys()[i]):
        W1.append(df1.loc[0].keys()[i])
for i in range(17,151):    
    if ('Diputados' in df1.loc[0].keys()[i]):
        W2.append(df1.loc[0].keys()[i])

print(W1)
print(W2)
   
# -

Y=[]
for x in range(17,84):
    if ('Votos' in W1[x]):
        Y.append(W1[x])
for x in range(0,67):
    Y[x]=re.sub('Votos', '', Y[x])

DF1 = pd.DataFrame(data=None, columns=df1.columns, index=df1.index)
DF2 = pd.DataFrame(data=None, columns=df1.columns, index=df1.index)
for i in range(N_PROV):
    for x in W1:
        DF1.loc[i][x]=df1.loc[i][x]
for i in range(N_PROV):
    for x in W2:
        DF2.loc[i][x]=df1.loc[i][x]
DF1=DF1.dropna(axis=1,how='all')
DF2=DF2.dropna(axis=1,how='all')
df1=pd.concat([DF1,DF2],axis=1)

df1.fillna(0).head()

estructura(df1)

df1.insert(loc = 13,
          column = '%PARTICIPACIÓN',
          value =df1['TOTAL_VOTANTES']/df1['CENSO_ELECTORAL'])

df1['%PARTICIPACIÓN']=df1['TOTAL_VOTANTES']/df1['CENSO_ELECTORAL']

# +
          
df1.loc[30]['%PARTICIPACIÓN']
# -

Var=dict(zip(W1[17:],Y))

Var

estructura(df1)

dfaux0.head()

dfaux1=df1[W1[17:]]

dfaux1=dfaux1.rename(columns=Var)

dfaux2=df1[W2[0:]]

df1=pd.concat([dfaux0,dfaux1,dfaux2], axis=1)

estructura(df1)

df1 = df1.drop(df1.columns[[ 4,5,6,8,9,10]], axis=1)

estructura(df1)

# +
P=[]
for i in range(78,145):
    if ('Diputados' in df1.loc[0].keys()[i]):
        P.append(df1.loc[0].keys()[i])

print(P)
# -

df1.insert(loc = 4,
          column = 'NPARTIDOS',
          value =N_PARTIDOS)


#partidos con más del 3% de votos
df1.insert(loc = 5,
          column = 'PARTIDOS>3',
          value =0)

estructura(df1)

V=[]
for i in range (N_PROV):
    S=0
    for x in l:

        a=df1.loc[i][x]/df1.loc[i]['VOTOS_VÁLIDOS']
        #
        if (a)>=0.03:
            S=S+1
    print(i,S)
    V.append(S)
    df1.loc[i,'PARTIDOS>3']=V[i]


party1=set(df2.loc[1])
grupos=list(party1)
party2=pd.Series(df2.columns.values,index=df2.columns.values)
party2=pd.DataFrame(party2)

df2

warnings.filterwarnings("ignore")
df2=df2.append(pd.DataFrame(party2.T),ignore_index=True).copy()

df2.head()

# +
#PARTE II: INTRODUCIR GRUPOS
# -

#asignar a cada grupo sus partidos
A=set(df2.loc[1][:])
B=list(A)
list_groups = {key: None for key in B}
for x in B:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==x:
            C.append(str(i))
    #print(x,C)
    list_groups[x]=C

list_groups

vot_grupos=['VDERECHA',
'VCENTRO',
'VIZQUIERDA',
'VNACIONALISTAS',
'VOTROS']


new_grupos=dict()
for x in vot_grupos:
    new_grupos[x] = list_groups[x[1:]]

vot_grupos

list_groups

new_grupos



df3 = df1.reindex(columns =df1.columns.tolist() + grupos)
df3 = df3.fillna(0)

estructura(df3)

df3.loc[0]['IZQUIERDA']

#votos por grupos por provincias
for j in range (len(df3)):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df3.loc[j][new_grupos[x]].sum():,.0f}')
        S=S+df3.loc[j][new_grupos[x]].sum()
    print('--TOTAL VOTOS ',f'{S:,.0f}')


# +
B=[[] for j in range (len(df3))]

for j in range(N_PROV):
    for x in vot_grupos:
        C=df3.loc[j][new_grupos[x]].sum()
        B[j].append(C)
# -

B

df4=df3.copy()
for i in (range(N_PROV)):
    for x in vot_grupos:
        df4.loc[i,x]=B[i][vot_grupos.index(x)]

df4[new_grupos]

df4[list_groups]

for x in l:
    columna='%'+x
    df4[columna]=df4[x]/df4['VOTOS_VÁLIDOS']

# +
#PARTE III: ELIMINAR CANDIDATURAS DE <3%
# -

df5=df4.copy()
for x in l:
    columna='%'+x
    df5[columna]=df5[x]/df5['VOTOS_VÁLIDOS']
    df5[x][df5[columna] < 0.03] = 0

df5.loc[0]['20']

df5.insert(loc = 5,
          column = 'VOTOS_REPARTIR',
          value =df5[l].sum(axis=1))

df5[l].sum(axis=1)

df1[l].sum(axis=1)

# +
#PARTE IV: TABLAS d'HONDT
# -

p=[[] for i in range(N_PROV)]
for j in range(N_PROV):
    c=df5.loc[j,l]
    p[j]=[]
    
    for k in range (1,int(df1.loc[j]['DIPUTADOS'])+1):
        part_voto=c/k
        p[j].append(part_voto)
#p[I][J] es una lista de dimensión N_PROVINCIAS y donde cada elemento de la lista es 
#otra lista de longitud N_PARTIDOSxDIPUTADOS cuyo contenido es el número de votos de 
#cada partido dividido por 1,2,...DIPUTADOS.

df1.loc[0]['DIPUTADOS']

# +
q=[[] for i in range(N_PROV)]
r=[[] for i in range(N_PROV)]
dHondt=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    r[i]=[]
    for j in range(int(df1.loc[i]['DIPUTADOS'])):
        A=p[i][j]
        r[i].append(A.values)
        q[i]=np.array((r[i])).T
        dHondt[i]=pd.DataFrame(q[i])
        
#dHondt es un array que representa la tabla d'Hondt  
# -

estructura(df1)

for i in range(N_PROV):
    print('PROVINCIA: ',df1.loc[i]['PROVINCIA'].strip(),i,'\n',dHondt[i][dHondt[i]>0].dropna(axis=0, how='all', inplace=False))

for i in range(N_PROV):
    labels = [x for x in range(1,int(df1.loc[i]['NPARTIDOS'])+1)]
    #print(pd.DataFrame(q[i],index=labels))
    dHondt[i]=pd.DataFrame(q[i],index=labels)

#lista_votos[I] es una lista de longitud N_PROVINCIAS que tiene los valores ordenados de la 
#tabla d'Hondt de cada provincia. Si no existen valores duplicados con lista_votos[I][DIPUTADOS-1]
#en lista_votos[I][>=DIPUTADOS] se eligen los primeros términos hasta DIPUTADOS y se asignan los escaños
#según las veces que aparezca cada partido. Si existen duplicados, se seleccionan aquellos partidos
#que tienen el mismo valor del índice que lista_votos[I][DIPUTADOS-1] y, enre ellos, se eligen al azar
#las candidaturas que deben completar el número de escaños. p.e. si hay DIPUTADOS=6 y 
#lista_votos[I][4]=lista_votos[I][5]=lista_votos[I][6]=lista_votos[I][7]=1000 elegiremos aleatoriamente
#dos de las cuatro empatadas para los dos escaños vacantes.
lista_votos=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    lista_votos[i]=[]
    for j in range(int(df1.loc[i]['DIPUTADOS'])):
        lista_votos[i]=lista_votos[i]+list(p[i][j])
        
        lista_votos[i].sort(reverse=True)

#Exporto d'Hondt 
F=input("¿DESEA EXPORTAR LAS TABLAS d'HONDT? (Y/N)")
if F=='Y' or 'Y'.lower():
    for i in range(N_PROV):
        A=dHondt[i][dHondt[i]>0].dropna(axis=0, how='all') 
        B=pd.DataFrame(lista_votos[i])
        B[B>0].dropna(axis=0, how='all') 
        Name='dHondt'+str(i)
        writer = pd.ExcelWriter(Name+'.xlsx')
        A.to_excel(writer,'dHondt')
        B.to_excel(writer,'lista_votos')
        writer.save()
        writer.close()

# +
#PARTE V: COMPROBAR SI HAY EMPATES
#vemos la lista de los valores repetidos en cada provincia:  repitentes[I] extaídos de lista_votos[I]
repitentes=[[] for i in range(N_PROV) ]
S=0
PR=[]
for i in range(N_PROV):
    D=([x for x in lista_votos[i] if lista_votos[i].count(x) >= 2])
    D.sort(reverse=True)
    
    for j in range(len(D)):
        if D[j]!=0:
            repitentes[i].append(D[j])
            a=repitentes[i][j]
            S=S+1
            PR.append(i)
    if len(repitentes[i])>0:       
        print('provincia: ', df1.loc[i]['PROVINCIA'],i,'\n',repitentes[i])

if S==0:
    print('NO HAY CANDIDATURAS EMPATADAS')
    
else:
    print('Hay candidaturas empatadas en provincias',set(PR))
    Empates=1
# -

#Exporto d'Hondt 
F=input("¿DESEA EXPORTAR LAS TABLAS d'HONDT? (Y/N)")
if F=='Y' or 'Y'.lower():
    for i in range(N_PROV):
        A=dHondt[i][dHondt[i]>0].dropna(axis=0, how='all') 
        B=pd.DataFrame(lista_votos[i])
        B[B>0].dropna(axis=0, how='all') 
        Name='dHondt'+str(i)
        writer = pd.ExcelWriter(Name+'.xlsx')
        A.to_excel(writer,'dHondt')
        B.to_excel(writer,'lista_votos')
        writer.save()
        writer.close()


estructura(df1)

# +
#PARTE VI: SI HAY EMPATES
# -

repeated=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    my_set = {s for s in repitentes[i]}
    repeated[i]=list(my_set)
    repeated[i].sort(reverse=True)
#valores repetidos en cada provincia en la tabla d'Hondt (un solo valor)

#es la función que localiza valores en DataFrame
i,j=np.where(np.isclose(np.array(dHondt[49],dtype=float),91964))
indices=list(zip(i,j))#tupla que da el número de fila y el de columna (f,c) de la tabla d'Hondt
print(indices)
print(dHondt[49][dHondt[49]>0].dropna(axis=0, how='all'))

#defino función que identifica y recopila valores repetidos
from collections import defaultdict
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)#tally es diccionario que asigna a cada valor los índices en que aparece
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)#solo se queda con los índices de valores repetidos
#devuelve un diccionario en el que la key es el elemento de seq y el value es una lista de los índices
#en que aparece


#devuelve el rango de las posiciones de lista_votos en que se repite el valor que ha de ser asignado
#a un partido aleatoriamente ya que el coeficiente de d'Hondt es el mismo para varios partidos.
locations=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    for j in range (len(repeat_loc[i])):
        a=min([x for x in repeat_loc[i][j][1]])
        b=max([x for x in repeat_loc[i][j][1]])
        if(b>=df1.loc[i]['DIPUTADOS'] and a<=df1.loc[i]['DIPUTADOS']):
            #print(i,df1.loc[i]['PROVINCIA'].strip(),j,b>=df1.loc[i]['DIPUTADOS'] and a<=df1.loc[i]['DIPUTADOS'])
            print(i,df1.loc[i]['PROVINCIA'].strip(),'Escaños a sortear',j,'entre las candidaturas',repeat_loc[i][j][1])
            print('Mínimo',min([x for x in repeat_loc[i][j][1]]),'Máximo', max([x for x in repeat_loc[i][j][1]]))
            
            locations[i].append(a)
            locations[i].append(b)


locations
#donde la lista está vacía, no hay coeficientes d'Hondt duplicados.
#donde no está vacía muestra el rango [MIN,MAX] en el que se encuentran los coeficientes empatados y
#el intervalo siempre ha de cubrir el valor del número de diputados asignados a la provincia.

for i in range(N_PROV):
    if list(locations[i]):
        print(df1.loc[i]['PROVINCIA'].strip(),i,locations[i],'N_DIPUTADOS',int(df1.loc[i]['DIPUTADOS']))
#nos da el índice mínimo  y el máximo que comprende el número de DIPUTADOS


# +
#el número de veces que se ha de elegir al azar en cada provincia
n_rep=[]
pr_alea=[]
for i in range(N_PROV):
    try:
        n=(+int(df1.loc[i]['DIPUTADOS'])-min(locations[i]))
        print('PROVINCIA ',df1.loc[i]['PROVINCIA'].strip(),i,' SELECCIONES ALEATORIAS ',n)
        n_rep.append(n)
        pr_alea.append(i)
    except:
        n_rep.append(0)

s=[(i,df5.loc[i]['PROVINCIA'].strip()) for i in range(N_PROV)]
n_rep1=list(zip(s,n_rep))       
#n_rep1 asocia para cada provincia el número de veces a elegir al azar
# -

S=0
for i in range(N_PROV):
    
    if n_rep1[i][1]>0:
        print(n_rep1[i])
        S=S+1
if S==0:
    print('No hay sorteo')

# +
#comprobación del muestreo
M=[[] for o in range(N_PROV)]
for o in range(N_PROV):
    try:
        m=[i for i in range(min(locations[o]),max(locations[o]))]
        M[o].append(m)
        print('POSICIONES DE DUPLICADOS: ','PROVINCIA',o,M[o])
    except:
        continue
N=[[] for o in range(N_PROV)]
for i in range(100):
    
    for k in pr_alea:
        for j in range(len(M[k])):    
            r=random.sample(M[k][j], int(df1.loc[k]['DIPUTADOS'])-min(locations[k]))
            r.sort()
            
            #print ('pasada',i+1,'provincia',k,'muestra',r)
            N[k].append(r)
        
alea49 = pd.DataFrame(N[49], columns = ['alea'])
alea30=[elem for sublist in N[30] for elem in sublist]
alea30 = pd.DataFrame(alea30, columns = ['alea'])
# -

alea30

counts30 = alea30['alea'].value_counts().to_dict()
counts49 = alea49['alea'].value_counts().to_dict()
counts30 = dict(sorted(counts30.items()))
counts49 = dict(sorted(counts49.items()))

counts30 

#provincias con y sin duplicados
S1=0
S2=0
for i in range(N_PROV):
    if n_rep[i]==0:
        #print('\n','SIN DUPLICADOS','\n')
        #print('PROVINCIA ',i,'\n',dHondt[i],'\n')
        S1=S1+1
    else:
        # dHondt con duplicados
        if max(locations[i])+1-min(locations[i])<=df1.loc[0]['NPARTIDOS']:
            print('PROVINCIA CON DUPLICADOS',df1.loc[i]['PROVINCIA'].strip(),i,'\n','NÚMERO DE PARTIDOS EMPATADOS ',
                  max(locations[i])+1-min(locations[i]))
            S2=S2+1
print('\n','NÚMERO DE PROVINCIAS SIN DUPLICADOS',S1,'\n','NÚMERO DE PROVINCIAS CON DUPLICADOS',S2)


#función que cuenta el número de diputados que cada partido obtiene en función del orden en tabla dHondt
def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count


#es el método para localizar en d'Hondt los valores de los coeficientes de la tabla
M=np.array(dHondt[0],dtype=float)
i,j=np.where(np.isclose(M,39036))

i,j
#devuelve una tupla

#provincias sin empates
dipus=[[] for k in range(N_PROV)]
num_part=[]
elements_count=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus[k]=[]
    if n_rep[k]==0:
        for x in lista_votos[k][0:int(df5.loc[k]['DIPUTADOS'])]:
            M=np.array(dHondt[k],dtype=float)
            i,j=np.where(np.isclose(M,x))
            dipus[k].append(i[0]+1)
        a=CountFrequency(dipus[k])
        elements_count[k].append(a)
    num_part.append(elements_count[k])    
# el diccionario elements_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k
    print(k,elements_count[k])

n_rep

#lista de candidaturas que recibirán diputados ordenadas según la regla d'Hondt
for i in range (N_PROV):
    print(df1.loc[i]['PROVINCIA'],dipus[i])

#añado columnas para guardar los escaños de cada candidatura
for k in range(N_PROV):
    for x in l:
        columna='DIPUTADOS'+x
        df5.loc[k,columna]=0

#Asigno diputados a provincias donde no hay empates
df6=df5.copy()
for k in range(N_PROV):
    if n_rep[k]==0:#si no hay duplicados en la provincia n_rep[k]==0
        for x in l:
            columna='DIPUTADOS'+x
            try:
                
                df6.loc[k,columna]=(elements_count[k][0][int(x)])
                print('PROV ',k,'PARTIDO',int(x),'DIPUS ', elements_count[k][0][int(x)])
            except:
                continue
df6 = df6.fillna(0)

df6.head()

#listo los votos por grupo en cada provincia descontados los partidos con menos del 3%
df7=df6.copy()
for k in range(N_PROV):
    print('\n','PROVINCIA: ',df1.loc[k]['PROVINCIA'].strip(),k,'\n','EN BLANCO',
         df7.loc[k]['VOTOS_BLANCOS'])
    S=0
    for x in grupos:
        print(x, df7.loc[k][list_groups[x]].sum())
        S=S+df7.loc[k][list_groups[x]].sum()
    print('TOTALES NO EN BLANCO:',S)

#lista de provincias sin empates
nemp=[]
for k in range(N_PROV):
    if n_rep[k]==0:
        nemp.append(df1.loc[k]['PROVINCIA'].strip())
emp=[]
#lista de provincias con empates
for k in range(N_PROV):
    if n_rep[k]!=0:
        emp.append(df1.loc[k]['PROVINCIA'].strip())


#provincias con empates
dipus1=[[] for k in range(N_PROV)]
elements_count1=[[] for k in range(N_PROV)]
loto=[]
dipus2=[[] for k in range(N_PROV)]
dipus3=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus1[k]=[]
    if n_rep[k]!=0:
        
        E=set(lista_votos[k][0:int(df6.loc[k]['DIPUTADOS'])])
        F=list(E)
        F.sort(reverse=True)
        for x in F:#coeficientes d'Hondt a considerar
            M=np.array(dHondt[k],dtype=float)
            i,j=np.where(np.isclose(M,x))
            v=list(zip(i+1,j))
            print(k,x,v,i[0])
            dipus1[k].append(v)
            flat_list = [item for sublist in dipus1[k][:] for item in sublist]
            dipus2[k]= [item for item in flat_list[:min(locations[k])]]
            dipus3[k]=[item for item in flat_list[min(locations[k]):]]


dipus2[30]#contiene las tuplas (partido-1,Índice-1) que ya se han asignado

dipus3[30]#contiene las tuplas (partido,Índice-1) que han de asignarse por sorteo

for i in range(len(dipus3[30])):
    print (dipus3[30][i][0]+1)

#asignación por sorteo
dipus4=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    try:
        w=int(df6.loc[k]['DIPUTADOS'])-min(locations[k])
        print(w)
        r=random.sample(dipus3[k][:], w)
        print(k,r)
        dipus3[k]=(dipus2[k]+r)
        for i in range(len(dipus3[k])):
            dipus4[k].append(dipus3[k][i][0])
    except:
        continue


dipus4[30]

elements_count1=[[] for k in range(N_PROV)]
for k in pr_alea:
    a=CountFrequency(dipus4[k])
    elements_count1[k].append(a)
    print(k,elements_count1[k][0])
# el diccionario elements1_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k

#Asigno diputados a provincias donde hay empates
df7=df6.copy()
for k in pr_alea:
    for x in l:
        columna='DIPUTADOS'+x
        try:
            df7.loc[k,columna]=(elements_count1[k][0][int(x)])
            print('PROV ',k,'PARTIDO',int(x),'DIPUS ', elements_count[k][0][int(x)])
        except:
            continue
df7 = df7.fillna(0)

estructura(df7)

# +
#PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA
# -

#compruebo los escaños por provincia
for i in range(N_PROV):
    print(i,df7.loc[i]['PROVINCIA'],f"{df7.loc[i][292:359].sum():,.0f}")

estructura(df7)

#asignar a cada grupo sus diputados
df8=df7.copy()
B=list(df8.loc[2][292:359].keys())
new_list_groups = {key: None for key in grupos}
for x in grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    for i in list_groups[x]:
        if B[int(i)-1][9:] ==str(i):
            print(B[int(i)-1][9:])
            C.append(B[int(i)-1])
            #print(x,C)
    new_list_groups[x]=C


list(df7.loc[2][292:359].keys())

# +
#votos por grupo político

for k in range(N_PROV):
    for x in grupos:
        columna=x
        df8.loc[k,columna]=df8.loc[k][new_list_groups[x]].sum()
                
# -

df8.loc[0,'VDERECHA']

list_groups

df9=df8.copy()
import warnings
warnings.filterwarnings("ignore")
for k in range(N_PROV):
    for x in grupos:
        df9.loc[k][x]=df9.loc[k][new_list_groups[x]].sum()
        print(df9.loc[k][x])
        print(df9.loc[k][new_list_groups[x]].sum())
df9 = df9.fillna(0)


new_list_groups

df9.loc[0]['VDERECHA']

estructura(df9)

# ###PARTE VIII: LISTADOS DE COMPROBACIÓN Y ARCHIVO DE SALIDA EXCEL

list(df9.keys()[222:289])[0][9:]

# +
#VOTOS POR PROVINCIA Y PARTIDO

print("\033[4m" + 'LISTADO DE VOTOS POR PROVINCIA A PARTIDOS'.center(80) + "\033[0m",'\n')
for k in range(N_PROV):
    print('\n','Provincia ',k, df1.loc[k]['PROVINCIA'].strip())
    for j in l:
        if int(df9.loc[k][j])!=0:
            print('Votos al partido: ',j, int(df9.loc[k][j]))
# -

#ESCAÑOS POR PROVINCIA Y GRUPO POLÍTICO
print("\033[4m" + 'LISTADO DE ESCAÑOS POR PROVINCIA A GRUPOS POLÍTICOS'.center(80) + "\033[0m",'\n')
for k in range(N_PROV):
    print('\n','Provincia: ',k,df1.loc[k]['PROVINCIA'].strip())
        
    for j in range(215,220):
        
        if df9.loc[k][j]!=0:
            print('Escaños por grupo: ', df9.loc[0].keys()[j],' ',f"{df9.loc[k][j]:,.0f}")

estructura(df9)

df10=df9.copy()
A=[x for x in range(0,14)]
B=[x for x in range(81,148)]
C=[x for x in range(215,225)]
D=[x for x in range(292,359)]
columnas=A+B+C+D

df9.loc[0][columnas]

new_cols=[]
for i in columnas:
    new_cols.append(df9.loc[0].keys()[i])
df10=df10[new_cols]

estructura(df10)

a=list(df10.keys())
b=a[14:81]

df10[b].sum(axis=1)

estructura(df10)

a=list(df10.keys())
b=a[86:]
df10[b].sum(axis=1)

df11=df10.copy()
df11 = df11.loc[:, df11.any()]
#solo columnas que no son totas nulas

estructura(df11)

Name=input('Nombre de archivo Excel de salida:')
salida=Name+'.xlsx'

writer = pd.ExcelWriter(salida)
df1.to_excel(writer,'datos ministerio')
df11.to_excel(writer,'resultados')
writer.save()
writer.close()

# +
#PARTE IX: DESAPARECER PARTIDOS Y REASIGNAR VOTOS
# -

estructura(df8)


