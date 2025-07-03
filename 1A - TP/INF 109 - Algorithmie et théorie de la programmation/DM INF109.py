import random as rd
import time

## Exercice 1

# 1)

MAX1 = 10 #Maximum de grains de chaque couleur

def init_liste(max):
    nB = rd.randint(1,max) #Nombre de grains blancs
    nN = rd.randint(1,max) #Nombre de grains noirs
    L = []
    for i in range(nB):
        L.append("B")
    for i in range(nN):
        L.append("N")
    return(L)

def proc(L):
    m = len(L)
    if m < 2:
        print("Moins de 2 elements dans la liste")
        return(L)
    a = rd.randint(0,m-1) #Génération des deux positions aléatoires
    b = rd.randint(0,m-1)
    while a == b:
        b = rd.randint(0,m-1) #On s'assure qu'on ne pointe pas sur le même grain
    if a > b: #Permet de faite la commande lignes 34-35
        a,b = b,a
    A = L[a] #Récupération des couleurs des grains
    B = L[b]
    if A == B: #Les grains sont de même couleur
        L.pop(a)
        L.pop(b-1)
        L.append("N")
    else :
        L.pop() #Les grains noirs sont à droite

def simulation_1():      
    Liste = init_liste(MAX1)
    while(len(Liste)>1):
        print(Liste)
        proc(Liste)
        time.sleep(1)
    print(Liste)
    print("Fin de la simulation")

# 2)
"""
On sait que :
    Le nombre de grains diminue de 1 à chaque itération
    Le processus s'exécute tant que la boîte a au moins 2 grains
    La boîte a un nombre fini de grains
On a donc une suite d'entiers (le nombre de grains) strictement décroissante qui va finir par atteindre la valeur 1
L'algorithme termine
"""

# 3)
"""


"""

## Exercice 2 :

#1)

## Exercice 4 :

#1)

class Box():
    def __init__(self,m):
        self.nut = [ x for x in range(m)]
        rd.shuffle(self.nut)
        self.bolt = [ x for x in range(m)]
        rd.shuffle(self.bolt)
    def screw(self, n, b):
        if self.nut[n] < self.bolt[b]:
            return -1 # Ecrou trop étroit
        if self.nut[n] == self.bolt[b]:
            return 0 # Ecrou et vis s'ajustent
        if self.nut[n] > self.bolt[b]:
            return 1 # Ecrou trop lâche

N = 100
box = Box(N)

def assemble(): # Un écrou assemblé sur une vis n'est plus testé
    d = dict()
    L = [i for i in range(N)]
    for i in range(N):
        for j in L:
            if box.screw(i,j) == 0:
                d[i]=j
                L.remove(j) # Une fois qu'on a trouvé l'écrou correspondant, il ne sert à rien de le retester pour les autres vis
                break
    return(d)

def assemble2(): # Un écrou assemblé sur une vis est testé pour les autres vis
    d = dict()
    for i in range(N):
        for j in range(N):
            if box.screw(i,j) == 0:
                d[i]=j
                break
    return(d) #Complexité en n² au pire

assert assemble() == assemble2()

# 2)
#
# Le mélange des deux listes permet de considérer que la première reste triée, et que suelement la deuxième est mélangée
# Dans le pire des cas, le test box.screw(i,j) de la fonction assemble s'exécute n(n+1)/2 fois 
#    Cela se produit quand la liste des écrous triée dans l'ordre décroissant (tous les écrous restants sont testés avant de trouver le bon)
#
# Dans le meilleur des cas, le test box.screw(i,j) de la fonction assemble s'exécute n fois
#    Cela se produit quand la liste des écrous est triée dans l'ordre croissant (tous les tests fonctionnent)
#
# 3)
#
# 