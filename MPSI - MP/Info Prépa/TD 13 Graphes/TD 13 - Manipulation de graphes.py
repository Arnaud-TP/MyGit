## Arnaud Capitan MPSI B

## TD - Cours n°12 : Manipulation de graphes

import numpy as np

## I. Représentation et manipulation de graphes :

## Exercice 1. représentation d'un graphe

# 1.1)

Mat_G1 = np.zeros((9,9))
Mat_G2 = np.zeros((5,5))
Mat_G3 = np.zeros((5,5))
Mat_G4 = np.zeros((6,6))

# A partir d'une matrice triangulaire supérieure, on complète le reste de la matrice avec la fonction symetrisation
# On ne s'occupe pas de la diagonale
# M[i,j] = M[j,i]

def symetrisation(Mat): # A partir d'une triangulaire supérieure
    N = len(Mat)
    for lig in range(N):
        for col in range(N):
            Mat[col,lig]=Mat[lig,col]

#On indique uniquement les 1 lorsque i -> j  i <= j

# Arbre G1 (symétrique)
Mat_G1[0] = [0., 1., 1., 1., 0., 0., 0., 0., 0.] #En entier, plus rapide
Mat_G1[1][4] = 1
Mat_G1[1][5] = 1
Mat_G1[3][6] = 1
Mat_G1[5][7] = 1
Mat_G1[5][8] = 1
symetrisation(Mat_G1)

#Graphe G2 non orienté (symétrique)
Mat_G2[0][1]=1
Mat_G2[0][2]=1
Mat_G2[0][4]=1
Mat_G2[1][2]=1
Mat_G2[1][3]=1
Mat_G2[2][3]=1
Mat_G2[2][4]=1
symetrisation(Mat_G2)

#Graphe G3 non orienté pondéré (symétrique)
Mat_G3[0][1]=9
Mat_G3[0][2]=3
Mat_G3[0][4]=7
Mat_G3[1][2]=1
Mat_G3[1][3]=8
Mat_G3[2][3]=4
Mat_G3[2][4]=2
symetrisation(Mat_G3)

#Graphe G4 orienté (non symétrique)
Mat_G4[0] = [0., 0., 1., 1., 0., 0.]
Mat_G4[1] = [0., 0., 0., 1., 1., 0.]
Mat_G4[2] = [0., 1., 0., 0., 0., 1.]
Mat_G4[4][0] = 1

# 1.2)

Voisin_G1 = []
Voisin_G2 = []
Voisin_G3 = []
Voisin_G4 = []

def complete_voisin(Mat,Liste_voisin): #Dans le cas d'un graphe non pondéré (orienté ou non)
    N = len(Mat)
    for lig in range(N):
        Voisin_lig = []
        for col in range(N):
            if Mat[lig,col] != 0:
                Voisin_lig.append(col)
        Liste_voisin.append(Voisin_lig)


def complete_voisin_pondere(Mat,Liste_voisin): #Dans le cas d'un graphe non pondéré (orienté ou non)
    N = len(Mat)
    for lig in range(N):
        Voisin_lig = []
        for col in range(N):
            if Mat[lig,col] != 0:
                Voisin_lig.append([col,Mat[lig,col]])
        Liste_voisin.append(Voisin_lig)

complete_voisin(Mat_G1,Voisin_G1)
complete_voisin(Mat_G2,Voisin_G2)
complete_voisin_pondere(Mat_G3,Voisin_G3)
complete_voisin(Mat_G4,Voisin_G4)

# 1.3)

Dico_G1 = dict()
Dico_G2 = dict()
Dico_G3 = dict()
Dico_G4 = dict()

def tableau_dico(Mat,dico): #Dans le cas d'un graphe non pondéré (orienté ou non)
    N = len(Mat)
    for lig in range(N):
        Voisin_lig = []
        for col in range(N):
            if Mat[lig,col] != 0:
                Voisin_lig.append(col)
        dico[lig] = Voisin_lig


def tableau_dico_pondere(Mat,dico): #Dans le cas d'un graphe non pondéré (orienté ou non)
    N = len(Mat)
    for lig in range(N):
        Voisin_lig = []
        for col in range(N):
            if Mat[lig,col] != 0:
                Voisin_lig.append([col,Mat[lig,col]])
        dico[lig] = Voisin_lig

tableau_dico(Mat_G1,Dico_G1)
tableau_dico(Mat_G2,Dico_G2)
tableau_dico_pondere(Mat_G3,Dico_G3)
tableau_dico(Mat_G4,Dico_G4)

# 1.4)

# 1.4.a]

def voisins(G,i):
    L=[]
    if isinstance(G, np.ndarray):
        for col in range(len(G)):
            if G[i][col] != 0:
                L.append(col)
        return(L)
    if isinstance(G, list):
        if isinstance(G[0][0], list): #Liste pondérée
            for col in range(len(G[i])):
                L.append(G[i][col][0])
            return(L)
        return(G[i]) #Si non pondéré
    if isinstance(G, dict):
        if isinstance(G[0], list): #Dictionnaire pondéré
            for col in range(len(G[i])):
                L.append(G[i][col])
            return(L)
        return(G[i]) #Si non pondéré
    print("Erreur, type de G invalide")
    return()

assert voisins(Dico_G2,2) == [0,1,3,4]
assert voisins(Mat_G4,0) == [2,3]
assert voisins(Voisin_G1,5) == [1,7,8]

# 1.4.b]

def degre(G,i):
    return(len(voisins(G,i)))

# 1.4.c]

def valeur(G,i,j): #Renvoie la longueur de l'arc séparant les sommets i et j
    if isinstance(G, np.ndarray):
        return(G[i,j])
    if isinstance(G, list):
        if isinstance(G[0][0], list): #Liste pondérée
            return(G[i][G[i].index(j)][1])
        return(1) #Liste non pondérée
    if isinstance(G, dict):
        if isinstance(G[0], list): #Dictionnaire pondéré
            return(G[i][G[i].index(j)][1])
        return(1) #Si non pondéré
    print("Erreur, type de G invalide")
    return()

def longueur(G,L): #L désigne une liste de sommets à emprunter lors d'un chemin
    Total = 0
    while len(L) > 1:
        Sommet_depart = L[0] #On peut partir de la fin, cela aura la même conséquence
        Sommet_arrive = L[1]
        if Sommet_arrive not in voisins(G,Sommet_depart):
            return(-1)
        Total += valeur(G,Sommet_depart,Sommet_arrive)
        L=L[1:]
    return(Total)

## II. Parcours en largeur d'un graphe

#On indiquera le type de représentation utilisée sous la fonction. Exemple :
#
# def maFonction(G):
#    """ type(G) = list """

## Un outil : la file

## Exercice 2 : Opérations de base sur les files

# 2.1)
# On lit la liste dans ce sens : [1,2,3,4,5]

def enfiler(f,e):
    f.append(e)

#Complexité de 1, la commande d'ajout d'un élément en bout de liste existe déjà

# 2.2)
#On supprime et renvoie l'élément en tête de liste

def defiler(f):
    if f == []:
        return("Liste vide : erreur defiler")
    return(f.pop(0))

#Complexité de O(n) sans la vérification de liste vide,
#la commande d'appel d'une valeur à la position 0, nécessite selon le principe de file
#de dépiler toutes les autres valeurs

# 2.3) File avec collections

import collections as co

file = co.deque([]) #File vide
file.appendleft(4) # .append à gauche
file.pop()

def enfiler_deque(f,e):
    f.append(e) #Ajout de l'élément à droite

# 2.4)

def defiler_deque(f,e):
    return(f.popleft()) #Retire l'élément en 1re position de la file et le renvoie

# 2.5)

def fileVide(f):
    if f == []:
        return(True)
    return(False)

## Parcours en largeur d'un arbre à partir d'une file

## Exercice 3 : Parcours en largeur d'un graphe G

# 1)

"""
Pour le graphe G1 :

Initialisation
F=[0] visite = [0]

F vide ? Non
1e itération :

On regarde les voisins du premier élément de F, dont on retire l'élément F=[],
-> Le 1er élément est 0 : voisins(G1,0) = [1,2,3]
1 n'est pas dans visite, on l'ajoute dans visite et dans F
2 n'est pas dans visite, on l'ajoute dans visite et dans F
3 ...
F = [1,2,3] visite = [0,1,2,3]

F vide ? Non
2e itération :

On regarde les voisins de 1, F = [2,3]
voisins(G1,1) = [0,4,5]
0 est dans la liste visite
4 n'est pas dans la liste visite
5 n'est pas dans la liste visite, on les ajoute à F
F = [2,3,4,5] visite = [0,1,2,3,4,5]

F vide ? Non
3e itération :

On regarde les voisins de 2, F = [3,4,5]
voisins(G1,2) = [0]
0 est dans la liste visite
F = [3,4,5] visite = [0,1,2,3,4,5]

F vide ? Non
3e itération :

On regarde les voisins de 3, F = [4,5]
voisins(G1,3) = [0,6]
0 est dans la liste visite
6 n'est pas dans la liste visite, on l'ajoute
F = [4,5,6] visite = [0,1,2,3,4,5,6]

F vide ? Non
4e itération :

On regarde les voisins de 4, F = [5,6]
voisins(G1,4) = [1]
1 est dans la liste visite
F=[5,6] visite = [0,1,2,3,4,5,6]


F vide ? Non
5e itération :

On regarde les voisins de 5, F = [6]
voisins(G1,5) = [7,8]
7 et 8 ne sont pas dans la liste visite
F=[6,7,8] visite = [0,1,2,3,4,5,6,7,8]

F vide ? Non
6e itération :

On regarde les voisins de 6, F = [7,8]
voisins(G1,6) = [3]
3 est dans la liste visite
F=[7,8] visite = [0,1,2,3,4,5,6,7,8]

F vide ? Non
7e itération :

On regarde les voisins de 7, F = [8]
voisins(G1,7) = [5]
5 est dans la liste visite
F=[8] visite = [0,1,2,3,4,5,6,7,8]

F vide ? Non
8e itération :

On regarde les voisins de 8, F = []
voisins(G1,8) = [5]
5 est dans la liste visite
F=[] visite = [0,1,2,3,4,5,6,7,8]

F vide ? Oui !
Fin (on renvoie l'une des listes ?)

"""


"""
Pour le graphe G2 :

Initialisation
F=[0] visite = [0]

F vide ? Non
1e itération :

On regarde les voisins du premier élément de F, dont on retire l'élément F=[],
-> Le 1er élément est 0 : voisins(G2,0) = [1,2,4]
1 n'est pas dans visite, on l'ajoute dans visite et dans F
2 n'est pas dans visite, on l'ajoute dans visite et dans F
4 ...
F = [1,2,4] visite = [0,1,2,4]

F vide ? Non
2e itération :

On regarde les voisins de 1, F = [2,4]
voisins(G2,1) = [0,2,3]
0 est dans la liste visite
2 est dans la liste visite
3 n'est pas dans la liste visite, on l'ajoute à F
F = [2,4,3] visite = [0,1,2,4,3]

F vide ? Non
3e itération :

On regarde les voisins de 2, F = [4,3]
voisins(G2,2) = [0,1,3,4]
0 est dans la liste visite
1 est dans la liste visite
3 ...
4 ...
F = [4,3] visite = [0,1,2,4,3]

F vide ? Non
3e itération :

On regarde les voisins de 4, F = [3]
voisins(G2,2) = [0,2]
0 est dans la liste visite
2 est dans la liste visite
F = [3] visite = [0,1,2,4,3]

F vide ? Non
4e itération :

On regarde les voisins de 3, F = []
voisins(G2,3) = [1,2]
1 est dans la liste visite
2 est dans la liste visite
F=[] visite = [0,1,2,4,3]

F vide ? Oui !
Fin (on renvoie l'une des listes ?)

"""

# 3.2)

def parcoursLargeur(G,debut):
    F=co.deque([debut])
    visite=[debut]
    while (len(F) != 0):
        sommet = F.popleft()
        voisins_sommet = voisins(G,sommet)
        if len(voisins_sommet) != 0:
            if isinstance(voisins_sommet[0],list): #Dans le cas d'un graphe pondéré, les sommets sont [nom, valeur]
                L=[]
                for elem in voisins_sommet :
                    L.append(elem[0]) #On récupère juste le nom des sommets
                voisins_sommet = L
        for elem in voisins_sommet :
            if elem not in visite :
                F.append(elem)
                visite.append(elem)
    return(visite)

# 3.3) On teste chaque type sur chaque graphe

assert parcoursLargeur(Mat_G1,0) == [0,1,2,3,4,5,6,7,8]
assert parcoursLargeur(Dico_G2,0) == [0,1,2,4,3] #Sur les exemples ci-dessus
assert parcoursLargeur(Voisin_G3,0) == [0,1,2,4,3] # Le même que précédent
assert parcoursLargeur(Mat_G4,4) == [4,0,2,3,1,5]

## Test de connexité d'un graphe

## Exercice 4 :

# 4.1)

#Dans le cas d'un graphe non orienté, un seul parcours convient. On ne traitera pas le cas du graphe orienté
#Dans les cas du graphe orienté, il faudrait vérifier chaque point

def estConnexe(G):
    return(len(G) == len(parcoursLargeur(G,0))) #Le nombre de sommets du graphe est égal au nombre de sommets visités

# 4.2)

assert estConnexe(Mat_G1) == True
assert estConnexe(Voisin_G2) == True
assert estConnexe(Dico_G3) == True
assert estConnexe(Mat_G4) == True #En partant de 0

# 4.3)

#Le graphe G5 n'est pas connexe, il est composé de deux triangles non reliés (1,3,5) et (0,2,4)
# Preuve par utilisation de la fonction :

Mat_G5 = np.zeros((6,6))
for i in range (len(Mat_G5)):
    for j in range (len(Mat_G5)):
        if (i + j)%2 == 0: # Soit deux nombres pairs, soit deux nombres impairs
            Mat_G5[i,j]=1

assert estConnexe(Mat_G5) == False

## Détection de circuit dans un graphe orienté et de cycle dans un graphe non orienté

## Exercice 5 : Cas du graphe orienté

# 5.1)

def circuitSommet(G,debut):
    F=co.deque([debut])
    visite=[debut]
    while (len(F) != 0):
        sommet = F.popleft()
        voisins_sommet = voisins(G,sommet)
        if len(voisins_sommet) != 0:
            if isinstance(voisins_sommet[0],list): #Dans le cas d'un graphe pondéré, les sommets sont [nom, valeur]
                L=[]
                for elem in voisins_sommet :
                    L.append(elem[0]) #On récupère juste le nom des sommets
                voisins_sommet = L
        for elem in voisins_sommet :
            if elem == debut : #On modifie cette ligne pour vérifier si l'un des sommets est celui du début
                return(True)
            if elem not in visite :
                F.append(elem)
                visite.append(elem)
    return(False)

# 5.2)

def admetCircuit(G):
    for i in range (len(G)):
        if circuitSommet(G,i):
            return(True)
    return(False)

assert admetCircuit(Mat_G4) == True

## Exercice 6 :

# 6.1)
## Cette fonction trouve un cycle en partant du sommet du début, mais pas nécessairement incluant le sommet de départ

def cycleSommet(G,debut):
    F = co.deque([debut])
    visite = [debut]
    pere=[]
    for i in range (len(G)):
        pere.append([])
    while (len(F) != 0):
        sommet = F.popleft()
        voisins_sommet = voisins(G,sommet)
        if len(voisins_sommet) != 0:
            if isinstance(voisins_sommet[0],list): #Dans le cas d'un graphe pondéré, les sommets sont [nom, valeur]
                L=[]
                for elem in voisins_sommet :
                    L.append(elem[0]) #On récupère juste le nom des sommets
                voisins_sommet = L
        for elem in voisins_sommet :
            if elem in visite : # S'il a déjà été visité
                if elem not in pere[sommet]: # S'il n'est pas le père de s
                    return(True) # Il y a un cycle
            if elem not in visite :
                pere[elem].append(sommet)
                visite.append(elem)
                F.append(elem)
    return(False)

#On définit les 2 matrices en exemple pour vérifier, nommées G6 et G7

Mat_G6 = np.zeros((5,5))
Mat_G6[0,4] = 1
Mat_G6[1,2] = 1
Mat_G6[1,4] = 1
Mat_G6[2,4] = 1
Mat_G6[3,4] = 1
symetrisation(Mat_G6)

assert cycleSommet(Mat_G6,1) == True
assert cycleSommet(Mat_G6,3) == True # En partant de 3, il trouve le cylce 1-2-4-1

Mat_G7 = np.zeros((5,5))
Mat_G7[0,4] = 1
Mat_G7[1,2] = 1
Mat_G7[1,4] = 1
Mat_G7[3,4] = 1
symetrisation(Mat_G7)
assert cycleSommet(Mat_G7,1) == False
assert cycleSommet(Mat_G7,3) == False

def admetCycle(G):
    for i in range(len(G)):
        if cycleSommet(G,i):
            return(True)
    return(False)

assert admetCycle(Mat_G1) == False #Le graohe G1 n'admet pas de cycle
assert admetCycle(Voisin_G2) == True
assert admetCycle(Dico_G3) == True
assert admetCycle(Mat_G7) == False




