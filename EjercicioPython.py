#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Ejercicio de examen de CyR
Created on Thu Dec 16 10:56:25 2021

@author: mariapereda
"""


#%% Importamos librerías

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities



#%% Creo redes
# redondeo resultados a 4 decimales

#G=nx.barabasi_albert_graph(200,3,seed=1)
#G=nx.barabasi_albert_graph(255,3,seed=2)
#G=nx.barabasi_albert_graph(309,3,seed=3)
G=nx.barabasi_albert_graph(341,3,seed=4)



num_nodes=len(G.nodes())
num_links=len(G.edges())
avg_degree=round(2*num_links/num_nodes,4)
num_componentes=len(list(nx.connected_components(G)))
tamaño_giant_component=max([len(c) for c in nx.connected_components(G)]) # max(nx.connected_components(G), key=len)
avg_clust=round(nx.average_clustering(G),4)

# max(G.degree, key = lambda x : x[1]) #key and value of node of maximum value
#nodo con mayor algo
mydict=dict(G.degree())
max_key = max(mydict, key=mydict.get)
max_value = max(mydict.values())
num_triangles = sum(nx.triangles(G).values())/3 #When computing triangles for the entire graph each triangle is counted three time

communities = greedy_modularity_communities(G) 
len(communities)

# Numero de caminos de longitud 3 entre los nodos 0 y 5
Adj=nx.to_numpy_array(G)
from numpy.linalg import matrix_power
Adj3=matrix_power(Adj,3)
Adj3[0][5]

#print('----------------------------')
#print('Número de nodos:',num_nodes)
#print('Número de enlaces:',num_links)
#print('Grado medio:',avg_degree)
#print('Número de componentes:',num_componentes)
#print('Tamaño de la componente más grande:',tamaño_giant_component)
#print('Coeficiente de clustering medio de la red', avg_clust)
#print('Nodo de mayor grado:',max_key)
#print('Natural cutoff de la red (Kmax):',max_value)
#print('Número de triángulos de la red:',num_triangles)
#print('Número de comunidades de la red:',len(communities))
#print('Número de caminos de longitud 3 del nodo 0 al 5:',Adj3[0][5])

#%%
print('-----Exam 18 enero 2022---------')
print('Número de nodos:',num_nodes)
print('Número de enlaces:',num_links)
print('Grado medio:',avg_degree)
print('Nodo de mayor grado:',max_key)
print('Natural cutoff de la red (Kmax):',max_value)
print('Coeficiente de clustering medio de la red', avg_clust)
print('Número de triángulos de la red:',num_triangles)
print('Número de comunidades de la red:',len(communities))
print('Número de caminos de longitud 3 del nodo 0 al 5:',Adj3[0][5])
print('----------------------------')

#%% Exportar archivo de red 

nx.write_gpickle(G, 'red.pkl')

G=nx.read_gpickle('red.pkl')

#%% Exportar archivo xml moodle



###### Lo del XML aún no funciona #######


from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment
#from ElementTree_pretty import prettify

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, encoding='unicode')
    #rough_string = ElementTree.tostring(elem, encoding='UTF-8) #Python2
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


#%%

top = Element('top')
texto='![CDATA[<p>En este archivo, "<a href="@@PLUGINFILE@@/celegans_n306_sinpesos_A.txt">celegans_n306_sinpesos_A.txt</a>", se describe la red correpondiente a la red neuronal del gusano <b>c elegans</b> mediante la lista de sus de arcos.</p><p><b>1)</b> Descarga y lee el archivo.</p><p><b>2)</b> Responde a estas preguntas utilizando la librería de pyhton llamada networkx.</p><p><span style="font-size: 1rem;">La red tiene {1:NUMERICAL:=297} nodos y {1:NUMERICAL:=2148}&nbsp; aristas.</span><br></p><p><span style="font-size: 1rem;">El grado medio de la red es: {1:NUMERICAL:=14.4:0.1}.</span><br></p><p><span style="font-size: 1rem;">El mayor hub de esta red es el nodo&nbsp; {1:NUMERICAL:=305} que tiene&nbsp; {1:NUMERICAL:=134} vecinos.</span><br></p><p><span style="font-size: 1rem;">El diámetro de la red es {1:NUMERICAL:=5}.</span><br></p><p><span style="font-size: 1rem;">El coeficiente de asortatividad, r, de esta red es&nbsp; {1:NUMERICAL:=-0.16319:0.1}, por lo tanto la red es&nbsp;</span><br></p><p><span style="font-size: 1rem;">{1:MULTICHOICE:=Dissasortative#OK~Assortative#Wrong}.</span><br></p><p>La red tiene {2:NUMERICAL:=153} cliques de tamaño 5.</p><p><b>3)</b> Guarda el código&nbsp; que has utilizado de python en la&nbsp; entrega correspondiente.</p><p><b>Nota</b>: Sólo se puede visitar las web de <i>moodle.upm.es</i> y de la librería networkx (<a href="https://networkx.github.io" target="_blank"><i>https://networkx.github.io</i></a>)</p><p></p>]]'
texto='prueba'

comment = Comment('Generated for PyMOTW')
top.append(comment)

quizz = SubElement(top, 'quizz')
question = SubElement(quizz, 'question', type="cloze")
name_question = SubElement(question, 'name')
text=SubElement(name_question, 'text')
text.text = 'Titulo de la pregunta'
question_text = SubElement(question, 'questiontext', format="html")
text=SubElement(question_text, 'text')
question_text.text=SubElement(question_text, texto)



#child_with_tail = SubElement(top, 'child_with_tail')
#child_with_tail.text = 'This child has regular text.'
#child_with_tail.tail = 'And "tail" text.'

#child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
#child_with_entity_ref.text = 'This & that'

print(prettify(top))
#%%
















