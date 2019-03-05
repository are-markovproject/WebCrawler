# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 14:22:35 2019

@author: natch
"""


from bs4 import BeautifulSoup
import os
import csv
import requests
from random import sample
import networkx as nx
import copy
import matplotlib.pyplot as plt

depart="https://www.sorbonne-universite.fr/" #Page de départ


def trouver_prefixe(depart):      #Utiliser cette fonction pour trouver le prefixe d'une page afin de crawler les liens relatifs
    i=1
    while (i<len(depart)-1):
        if (depart[i]=='/' and depart[i-1]!='/' and depart[i+1]!='/'):
            break
        else:
            i+=1
    return depart[:i] #Prefixe sans inclure le / final


def ens_href(s):
    ens=set()
    requete=requests.get(s)
    page=requete.content
    soup=BeautifulSoup(page,"lxml")
    for link in soup.find_all('a'):
        ens.add(link.get('href'))
    return ens
    

def crawler_n_pages_hasard(n,depart):
    D=dict() #Dictionnaire Resultat
    s=depart
    prefixe=trouver_prefixe(depart)  #Url de base à rajouter en prefixe 
    for i in range(n):
        D[s]=ens_href(s)
        s = sample(ens_href(s),1)[0]   #Choisis un élément au hasard parmis les URL de la page
        if s[0]=='/': #Si on tombe sur un lien relatif, on lui rajoute le prefixe du site 
            s=prefixe+s  
        elif (prefixe!=s[0:len(prefixe)] or len(prefixe)>len(s)):  #Si on tombe sur un lien absolu : tant qu'on reste sur le même site on utilisera le même prefixe par la suite
            prefixe=trouver_prefixe(s)  #Sinon on le change
    return D

def crawler_total_n_pages(n,depart):
    """Crawl toutes les pages croisées sur n 'générations' """
    D=dict() #Dictionnaire Résultat
    i=n
    temp_lien=""#Variable textuelle temporaire 
    D[depart]=ens_href(depart) #On initialise le dictionnaire avec les liens disponibles sur la page de départ
    prefixe=trouver_prefixe(depart)
    while i!=0:
        Dtemp=copy.deepcopy(D)  #On ne peut pas modifier un dicitonnaire tout en itérant sur ses éléments donc on effectue une iteration sur une copie du ditionnaire
        for (page,ens_liens) in Dtemp.items(): #On crawl chaque lien qu'on trouve sur la page
            prefixe=trouver_prefixe(page) #On met à jour le prefixe
            for lien in ens_liens:
                if type(lien)==str:
                    if len(lien)!=0:
                        if lien[0]=='/': #Si on tombe sur un lien relatif, on lui rajoute le prefixe du site 
                            temp_lien=prefixe+lien
                        elif lien[0]!='h': #Si on tombe sur un lien relatif ne contenant pas de / à son début
                            temp_lien=prefixe+'/'+lien
                        else:           #Si on tombe sur un lien absolu
                            temp_lien=lien
                        if temp_lien not in D:
                            D[temp_lien]=ens_href(temp_lien) #On créer une nouvelle entrée dans le dictionnaire en 
        i=i-1
    print(len(D))
    return D

#def dessiner_graphe(n,depart):  
    #"""Fonction qui permet la creation d'un graphe représentant la portion du web crawlée"""
    #Graphe=nx.DiGraph()
    #D=crawler_total_n_pages(n,depart)
    
    #for (page,ens_liens) in D.items():
        #for lien in ens_liens:
            
            
        
        
    
    



    
    
            
            
        
        
        