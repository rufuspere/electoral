#!/usr/bin/env python
# coding: utf-8
# %%
#PARTE 0: ESTABLECER DIRECTORIO DE TRABAJO

# %%
import os 
os.chdir("G:\\dHondt")

# %%
print('Directorio de trabajo: ',os.getcwd())


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
estructura(df0)

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
#df1

df1=pd.concat([dfaux0,dfaux1,dfaux2], axis=1)


# %%
estructura(df1)

# %%
#eliminamos ciertas columnas innecesarias (Censo CERA, Mesas Electorales...)
#para obtener df1

df1 = df1.drop(df1.columns[[ 4,5,6,8,9,10]], axis=1)


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
df1.loc[1][7:20]

# %%
for x in l:
    columna='%'+x
    df1[columna]=df1[x+'Votos']/df1['VOTOS_VÁLIDOS']


# %%
df1.head()


# %%
df1.loc[0]['1Votos':'7Votos']

# %%
#PARTE II: INTRODUCIR GRUPOS

# %%
vot_grupos=['VDERECHA',
'VCENTRO',
'VIZQUIERDA',
'VNACIONALISTAS',
'VOTROS']

# %%
import re
#asignar a cada grupo sus partidos para votos
B=vot_grupos
list_vgroups = {key: None for key in B}
for x in vot_grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==re.sub('V', '', x):
            C.append(str(i)+'Votos')
    #print(x,C)
    list_vgroups[x]=C

# %%
list_vgroups

# %%
grupos=['DERECHA',
'CENTRO',
'IZQUIERDA',
'NACIONALISTAS',
'OTROS']

# %%
new_grupos=dict()
for x in vot_grupos:
    new_grupos[x] = list_groups[x[1:]]

# %%
new_grupos

# %%
#asignar a cada grupo sus partidos para escaños
B=grupos
list_dgroups = {key: None for key in B}
for x in grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    
    for i in df2.loc[2][:]:#nombres de los partidos (1,2,...NPARTIDOS)
        if df2.loc[1][i] ==x:
            C.append(str(i)+'Diputados')
    #print(x,C)
    list_dgroups[x]=C

# %%
list_dgroups

# %%
list_vgroups

# %%
df1 = df1.reindex(columns =df1.columns.tolist() + grupos)
df1 = df1.reindex(columns =df1.columns.tolist() + vot_grupos)
df1 = df1.fillna(0)

# %%
estructura(df1)

# %%
df1.loc[0]['1Votos']

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in vot_grupos:#grupos de partidos
        print(x, f'{df1.loc[j][list_vgroups[x]].sum():,.0f}')
        S=S+df1.loc[j][list_vgroups[x]].sum()
    print('--TOTAL VOTOS ',f'{S:,.0f}')

# %%
#diputados por grupos por provincias
for j in range (N_PROV):#provincias
    print('\n','PROVINCIA',df1.loc[j]['PROVINCIA'].strip(),f'{j:,.0f}','\n')
    S=0
    for x in grupos:#grupos de partidos
        print(x, f'{df1.loc[j][list_dgroups[x]].sum():,.0f}')
        S=S+df1.loc[j][list_dgroups[x]].sum()
    print('--TOTAL DIPUTADOS ',f'{S:,.0f}')

# %%
#votos por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in vot_grupos:#grupos de partidos
        df1.loc[j,x]=df1.loc[j][list_vgroups[x]].sum()

# %%
#diputados por grupos por provincias
for j in range (N_PROV):#provincias
    S=0
    for x in grupos:#grupos de partidos
        df1.loc[j,x]=df1.loc[j][list_dgroups[x]].sum()

# %%
df1=df1.rename(columns=Var)

# %%
estructura(df1)

# %%
df1.loc[0]['%1']

# %%
#PARTE III: ELIMINAR CANDIDATURAS DE <3%

# %%
df3=df1.copy()
for x in l:
    columna='%'+x
    df3[columna]=df3[x]/df3['VOTOS_VÁLIDOS']
    df3[x][df3[columna] < 0.03] = 0

# %%
df3.loc[0]['%2']

# %%
df3.insert(loc = 5,
          column = 'VOTOS_REPARTIR',
          value =df3[l].sum(axis=1))

# %%
df3[l].sum(axis=1)#sumas de votos >3%

# %%
#PARTE IV: TABLAS d'HONDT

# %%
p=[[] for i in range(N_PROV)]
for j in range(N_PROV):
    c=df3.loc[j,l]
    p[j]=[]
    
    for k in range (1,int(df3.loc[j]['DIPUTADOS'])+1):
        part_voto=c/k
        p[j].append(part_voto)
#p[I][J] es una lista de dimensión N_PROVINCIAS y donde cada elemento de la lista es 
#otra lista de longitud N_PARTIDOSxDIPUTADOS cuyo contenido es el número de votos de 
#cada partido dividido por 1,2,...DIPUTADOS.

# %%
df3.loc[30]['DIPUTADOS']

# %%
import numpy as np
q=[[] for i in range(N_PROV)]
r=[[] for i in range(N_PROV)]
dHondt=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    r[i]=[]
    for j in range(int(df3.loc[i]['DIPUTADOS'])):
        A=p[i][j]
        r[i].append(A.values)
        q[i]=np.array((r[i])).T
        dHondt[i]=pd.DataFrame(q[i])
        
#dHondt es un array que representa la tabla d'Hondt  

# %%
estructura(df3)

# %%
for i in range(N_PROV):
    print('PROVINCIA: ',df3.loc[i]['PROVINCIA'].strip(),i,'\n',dHondt[i][dHondt[i]>0].dropna(axis=0, how='all', inplace=False))

# %%
for i in range(N_PROV):
    labels = [x for x in range(1,int(df3.loc[i]['NPARTIDOS'])+1)]
    #print(pd.DataFrame(q[i],index=labels))
    dHondt[i]=pd.DataFrame(q[i],index=labels)

# %%
dHondt[0]

# %%
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
    for j in range(int(df3.loc[i]['DIPUTADOS'])):
        lista_votos[i]=lista_votos[i]+list(p[i][j])
        
        lista_votos[i].sort(reverse=True)

# %%
lista_votos[0]

# %%
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
        writer.close()

# %%
estructura(df3)

# %%
#PARTE V: COMPROBAR SI HAY EMPATES

# %%
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

# %%
#PARTE VI: SI HAY EMPATES

# %%
repeated=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    my_set = {s for s in repitentes[i]}
    repeated[i]=list(my_set)
    repeated[i].sort(reverse=True)
#valores repetidos en cada provincia en la tabla d'Hondt (un solo valor)

# %%
#es la función que localiza valores en DataFrame
i,j=np.where(np.isclose(np.array(dHondt[49],dtype=float),91964))
indices=list(zip(i,j))#tupla que da el número de fila y el de columna (f,c) de la tabla d'Hondt
print(indices)
print(dHondt[49][dHondt[49]>0].dropna(axis=0, how='all'))

# %%
#defino función que identifica y recopila valores repetidos
from collections import defaultdict
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)#tally es diccionario que asigna a cada valor los índices en que aparece
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)#solo se queda con los índices de valores repetidos
#devuelve un diccionario en el que la key es el elemento de seq y el value es una lista de los índices
#en que aparece


# %%
repeat_loc=[[] for i in range(N_PROV)]
for i in range(N_PROV):
    for dup in list_duplicates(lista_votos[i]):
        repeat_loc[i].append(dup)
        repeat_loc[i] = sorted(list_duplicates(lista_votos[i]),reverse=True)
        
#tuplas que asocian key=VALOR repetido con value lista de los ÍNDICES de lista_votos[I]
#en la mayoría de casos es 0 el único valor que se repite

# %%
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


# %%
locations
#donde la lista está vacía, no hay coeficientes d'Hondt duplicados.
#donde no está vacía muestra el rango [MIN,MAX] en el que se encuentran los coeficientes empatados y
#el intervalo siempre ha de cubrir el valor del número de diputados asignados a la provincia.

# %%
for i in range(N_PROV):
    if list(locations[i]):
        print(df1.loc[i]['PROVINCIA'].strip(),i,locations[i],'N_DIPUTADOS',int(df1.loc[i]['DIPUTADOS']))
#nos da el índice mínimo  y el máximo que comprende el número de DIPUTADOS


# %%
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

s=[(i,df3.loc[i]['PROVINCIA'].strip()) for i in range(N_PROV)]
n_rep1=list(zip(s,n_rep))       
#n_rep1 asocia para cada provincia el número de veces a elegir al azar

# %%
S=0
for i in range(N_PROV):
    
    if n_rep1[i][1]>0:
        print(n_rep1[i])
        S=S+1
if S==0:
    print('No hay sorteo')

# %%
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

# %%
alea30

# %%
counts30 = alea30['alea'].value_counts().to_dict()
counts49 = alea49['alea'].value_counts().to_dict()
counts30 = dict(sorted(counts30.items()))
counts49 = dict(sorted(counts49.items()))

# %%
counts30 

# %%
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


# %%
#función que cuenta el número de diputados que cada partido obtiene en función del orden en tabla dHondt
def CountFrequency(my_list):
    count = {}
    for i in my_list:
        count[i] = count.get(i, 0) + 1
    return count


# %%
#es el método para localizar en d'Hondt los valores de los coeficientes de la tabla
M=np.array(dHondt[0],dtype=float)
i,j=np.where(np.isclose(M,39036))

# %%
i,j
#devuelve una tupla

# %%
#provincias sin empates
dipus=[[] for k in range(N_PROV)]
num_part=[]
elements_count=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus[k]=[]
    if n_rep[k]==0:
        for x in lista_votos[k][0:int(df3.loc[k]['DIPUTADOS'])]:
            M=np.array(dHondt[k],dtype=float)
            i,j=np.where(np.isclose(M,x))
            dipus[k].append(i[0]+1)
        a=CountFrequency(dipus[k])
        elements_count[k].append(a)
    num_part.append(elements_count[k])    
# el diccionario elements_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k
    print(k,elements_count[k])

# %%
n_rep

# %%
#lista de candidaturas que recibirán diputados ordenadas según la regla d'Hondt
for i in range (N_PROV):
    print(df1.loc[i]['PROVINCIA'],dipus[i])

# %%
#añado columnas para guardar los escaños de cada candidatura
for k in range(N_PROV):
    for x in l:
        columna='DIPUTADOS'+x
        df3.loc[k,columna]=0

# %%
#Asigno diputados a provincias donde no hay empates
df4=df3.copy()
for k in range(N_PROV):
    print('PROV ',k)
    if n_rep[k]==0:#si no hay duplicados en la provincia n_rep[k]==0
        for x in l:
            columna='DIPUTADOS'+x
            try:
                
                df4.loc[k,columna]=(elements_count[k][0][int(x)])
                print('PARTIDO',int(x),'DIPUS ', elements_count[k][0][int(x)])
            except:
                continue
df4 = df4.fillna(0)

# %%
df4.head()

# %%
#listo los votos por grupo en cada provincia descontados los partidos con menos del 3%
df5=df4.copy()
for k in range(N_PROV):
    print('\n','PROVINCIA: ',df1.loc[k]['PROVINCIA'].strip(),k)
    print('EN BLANCO',f"{df5.loc[k]['VOTOS_BLANCOS']:,.0f}")
    S=0
    for x in grupos:
        print(x, f"{df5.loc[k][list_groups[x]].sum():,.0f}")
        S=S+df5.loc[k][list_groups[x]].sum()
    print('---TOTALES NO EN BLANCO:',f"{S:,.0f}")

# %%
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


# %%
#provincias con empates
dipus1=[[] for k in range(N_PROV)]
elements_count1=[[] for k in range(N_PROV)]
loto=[]
dipus2=[[] for k in range(N_PROV)]
dipus3=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    dipus1[k]=[]
    if n_rep[k]!=0:
        
        E=set(lista_votos[k][0:int(df4.loc[k]['DIPUTADOS'])])
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


# %%
dipus2[30]#contiene las tuplas (partido-1,Índice-1) que ya se han asignado

# %%
dipus3[30]#contiene las tuplas (partido,Índice-1) que han de asignarse por sorteo

# %%
for i in range(len(dipus3[30])):
    print (dipus3[30][i][0]+1)

# %%
#asignación por sorteo
dipus4=[[] for k in range(N_PROV)]
for k in range(N_PROV):
    try:
        w=int(df4.loc[k]['DIPUTADOS'])-min(locations[k])
        print(w)
        r=random.sample(dipus3[k][:], w)
        print(k,r)
        dipus3[k]=(dipus2[k]+r)
        for i in range(len(dipus3[k])):
            dipus4[k].append(dipus3[k][i][0])
    except:
        continue


# %%
dipus4[30]

# %%
elements_count1=[[] for k in range(N_PROV)]
for k in pr_alea:
    a=CountFrequency(dipus4[k])
    elements_count1[k].append(a)
    print(k,elements_count1[k][0])
# el diccionario elements1_count[k] nos da el par (PARTIDO, ESCAÑOS) para cada PROVINCIA k

# %%
#Asigno diputados a provincias donde hay empates
df5=df4.copy()
for k in pr_alea:
    for x in l:
        columna='DIPUTADOS'+x
        try:
            df5.loc[k,columna]=(elements_count1[k][0][int(x)])
            print('PROV ',k,'PARTIDO',int(x),'DIPUS ', elements_count[k][0][int(x)])
        except:
            continue
df5 = df5.fillna(0)

# %%
estructura(df5)

# %%
#PARTE VII: ASIGNACIÓN DE ESCAÑOS DEFINITIVA

# %%
estructura(df5)

# %%
#compruebo los escaños por provincia
for i in range(N_PROV):
    print(i,df5.loc[i]['PROVINCIA'],f"{df5.loc[i][220:287].sum():,.0f}")

# %%
estructura(df5)

# %%
#asignar a cada grupo sus diputados
df6=df5.copy()
B=list(df6.loc[2][220:287].keys())
new_list_groups = {key: None for key in grupos}
for x in grupos:#nombres de los grupos (CENTRO, DERECHA,...)
    C=[]
    for i in list_groups[x]:
        if B[int(i)-1][9:] ==str(i):
            print(B[int(i)-1][9:])
            C.append(B[int(i)-1])
            #print(x,C)
    new_list_groups[x]=C


# %%
list(df5.loc[2][220:287].keys())

# %%
#votos por grupo político

for k in range(N_PROV):
    for x in grupos:
        columna=x
        df6.loc[k,columna]=df6.loc[k][new_list_groups[x]].sum()
                

# %%
df6.loc[0,'DERECHA']

# %%
list_groups

# %%
df7=df6.copy()
import warnings
warnings.filterwarnings("ignore")
for k in range(N_PROV):
    for x in grupos:
        df7.loc[k][x]=df7.loc[k][new_list_groups[x]].sum()
        print(f"{df7.loc[k][x]:,.0f}")
        print(f"{df7.loc[k][new_list_groups[x]].sum():,.0f}")
df7 = df7.fillna(0)


# %%
new_list_groups

# %%
df7.loc[0]['DERECHA']

# %%
estructura(df7)

# %%
