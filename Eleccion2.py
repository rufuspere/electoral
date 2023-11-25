# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
#Eleccion2: importa funciones que pueden ser útiles para analizar 
#resultados

# %%
import funciones as aux

# %%
print ("ESTA ES LA LISTA DE FUNCIONES EN EL MÓDULO 'funciones'")
print("--1)Identificar partido:\n    partido(codigo)")
print('--2) Listar nombre, índice, código y comunidad de una provincia:\n     provincia(x)')
print('--3) Lista de votos y escaños por provincia:\n     Resumen_Prov(dataFrame)')
print('--4) Lista de votos por grupo político:\n     Votos_y_Escaños_Grupos(dataFrame)')
print('--5) Lista de votos y escaños por CA:\n     Votos_y_Diputados(Com)')
print('--6) Lista de votos y escaños por provincia:\n     VotEscaño_Prov(dataFrame,x)')
print('--7) Comunidades con sus provincias:\n     Com_Aut()')

# %%
aux.provincia(1)

# %%
