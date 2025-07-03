## Les algorithmes de tri
#Arnaud Capitan MPSI B

## On compte le nombre de COMPARAISONS

## Exercice 0 :

#Question 0.0)

import random as rd
import matplotlib.pyplot as plt

a=3
b=12
n=10
Alea=lambda a,b,n : [rd.randint(a,b) for i in range (n)]
#Création d'une fonction de paramètres a,b,n qui crée une liste de n éléments contenant des entiers aléatoires entre a et b
listeAbscisse=Alea(a,b,n)
listeOrdonnee=Alea(a,b,n)
plt.plot(listeAbscisse,listeOrdonnee, linestyle=' ', marker='.', color='r')

#Question 0.1)

def nuage(tri, nombreTests, longs_n, couleur,k):
    abscisse=[]
    ordonnee=[]
    for element in longs_n: #Pour chaque élément de la liste de longueur
        for i in range (nombreTests): #On crée une liste pour chaque nombre de tests
            liste=Alea(1,element,element) #Elements entre 1 et n pour n éléments
            cout=tri(liste) #On renvoie le coût une fois la liste triée
            abscisse.append(element) #On ajoute l'abscisse
            ordonnee.append(cout/(element**k)) #On ajoute l'ordonnée cout/(longs_n[i]**k)
    plt.plot(abscisse,ordonnee,linestyle=' ', marker='.', color=couleur) #Affichage
    plt.show()

## 1. Tri à bulle

#Exercice 1 :

#Question 1.1)

def triBul(L):
    Condition = True #Au moins une permutation est effectuée
    Cout=0
    finT=len(L) #Rang de la dernière permutation
    while Condition :
        Condition=False
        for i in range (finT-1):
            Cout+=1
            if L[i]>L[i+1]:
                L[i],L[i+1]=L[i+1],L[i]
                Condition=True
                finT=i+1 #On arrête la boucle for
    return(Cout)

#Fonctionne
Liste1=[0,5,7,8,4,6,3,9,1,2]
Liste2=[10,48,75,20,14,23,8,5,248,25,451,47,22,1,6,9,74,111]

#Question 1.2)
"""
n=len(L)
Pour une liste dans l'ordre croissant, décroissant, le nombre minimal d'itérations est n-1
pour vérifier chaque élément de 0 à len(L)-1 (le test commence sur le premier, s'arrête à l'avant dernier) Donc n-1 <= cout
Dans le cas d'une liste triée par ordre décroissant à trier dans l'ordre croissant, le nombre d'itérations sera :
Le plus grand va à la dernière position lors du premier tri
Le 2e plus grand va à l'avant dernière position lors du deuxième tri
Le rang k va à la k position lors du k tri
On a donc k² en cout pour k allant de 0 à n-1, n-1, nombre d'éléments vérifiés
Ainsi, Cout max = Somme k=0 à n-1 de k² = n(n-1)/2
n-1 <= cout <= n(n-1)/2

On majore : Cout = n(n-1)/2 -> O(n²)
"""
#Vérification par tracé

## 2. Tri par sélection

#Question 2.1)

def posG(L,m):
    max=m-1 #On prend pour valeur initiale le rang m-1, une valeur de moins dans la boucle
    for i in range (0,m-1):
        if L[i]>L[max]:
            max=i #Nouveau rang de la valeur max
    return(max)

#Question 2.2)

def bouge(L,dep,arr):
    Cout = 0
    if dep < arr :
        for i in range (arr-dep):
            L[dep+i],L[dep+i+1]=L[dep+i+1],L[dep+i]
            Cout+=1
        Cout+=1
        return(Cout)
    else :
        for i in range (dep-arr):
            L[dep-i],L[dep-i-1]=L[dep-i-1],L[dep-i]
            Cout+=1
        Cout+=1
        return(Cout)

#Question 2.3)

def triSec(L):
    Cout=0
    for Pos in range (len(L)-1):
        Cout += bouge(L,posG(L,len(L) - Pos),len(L) - 1 - Pos)
    return(Cout)

#Fonctionne
Liste1=[0,5,7,8,4,6,3,9,1,2]
Liste2=[10,48,75,20,14,23,8,5,248,25,451,47,22,1,6,9,74,111]

"""
Encadrement de son coût
Dans le cas d'une liste déjà triée, le tri va parcourir n-1 fois la liste pour trouver le
maximum, qui déjà positionné -> n'apportera de coût supplémentaire

Dans le cas opposé, le tri parcourt aussi n-1 fois la liste, en ne considérant que le coût du tri,

On a coût = n-1 = 0(n)
"""

## 3. Tri par insertion

#Exercice 3 :

#Question 3.1)

def place(L,p):
    z=L[p]
    for i in range (p):
        if L[i]>z:
            return(i)
    return(p)

#Question 3.2)

def triIns(L):
    Cout=0
    for pos in range (1,len(L)):
        Cout+=bouge(L,pos,place(L,pos))
    return(Cout)

#Question 3.3)

#Fonctionne pour les deux listes
Liste1=[0,5,7,8,4,6,3,9,1,2]
Liste2=[10,48,75,20,14,23,8,5,248,25,451,47,22,1,6,9,74,111]

#L'encadrement du coût est le même que le tri par sélection

## 4. Tri par insertion dichotomique (ou binaire)

#Exercice 4 :

#Question 4.1 :

def placeDic(L,p):
    a = 0
    b = p
    z = L[p]
    if z <= L[0]: #Si notre terme est plus petit que l'élément le plus petit (tout à gauche) -> 0 (nouvelle position)
        return(0)
    if z >= L[p-1]: #Si notre terme est plus grand que le plus grand élément (tout à droite) -> p (identique)
        return(p)
    while z<L[a] and z>L[a+1]: #Tant que z ne se retrouve pas entre deux valeurs consécutives, on poursuit
        m = (b-a)//2 #On applique la dichotomie avec la division entière pour conserver des nombres entiers
        if L[a+m] == z: #On part des extrémités, on se rapproche en cherchant pour le rang a+m
            return(i+m)
        if L[a+m] <= z: #Principe de la dichotomie
            a+= m #On ajoute la valeur à a
        else :
            b = a + m #On donne la nouvelle valeur à b
    return(a+1) #Sinon on renvoie la position

#Question 4.2

def triInsDic(L):
    Cout = 0
    for i in range(1,len(L)):
        Cout+=bouge(L,i,placeDic(L,i))
    return(Cout)

#Question 4.3)

#Fonctionne
Liste1=[0,5,7,8,4,6,3,9,1,2]
Liste2=[10,48,75,20,14,23,8,5,248,25,451,47,22,1,6,9,74,111]

## 5. Tri Rapide (récursif)

#Question 5.1

def partition(L,debut,fin):
    G = []
    D = []
    z=L[debut]
    for i in range (debut,fin): #On remarque qu'avec les inégalités on ne traite pas le cas avec L[i] = z
        if z > L[i]: #Ce cas ne nous intéresse -> on souhaite former une liste finale autour de notre valeur 'pivot'
            G.append(L[i])
        if z < L[i]:
            D.append(L[i])
    return(G,D)

#Question 5.2

def triRapid(L):
    if len(L) == 0 or len(L) == 1:
        return(L)
    z = L[0]
    G,D = partition(L,0,len(L)) #On partitionne L en deux listes avec pour pivot le 1er terme
    return(triRapid(G) + [z] + triRapid(D)) #On renvoie la liste triée à gauche + le pivot + la liste triée à droite

#On remarque que triRapid parcourt au final n -1 (pivot) fois la liste avec les récursivités

#Question 5.3

#Cela fonctionne

## 6. Tri fusion

#On prend deux compteurs : dès qu'un élément d'une des deux listes est ajouté à la liste 'Résultat',
#On incrémente le compteur en question. Si ni = len(Li), on concatène le reste des résultats de l'autre liste

#Question 6.1

def Fusion(L1,L2):
    n1 = 0
    n2 = 0
    Rep=[]
    while (True):
        if n1 == len(L1):
            return(Rep + L2[n2:])
        if n2 == len(L2):
            return(Rep + L1[n1:])
        if L1[n1]<L2[n2]:
            Rep.append(L1[n1])
            n1 += 1
        else :
            Rep.append(L2[n2])
            n2 += 1

#Pas besoin d'ajout de return, on a n1 et n2 strictement croissant, l'un des deux finira par atteindre len(Li)

#Question 6.2

def triFus(L):
    if len(L) < 2:
        return(L)
    n = len(L)
    return(Fusion(triFus(L[0 : n//2]),triFus(L[n//2 :])))

# Question 6.3

#Fonctionne

nuage(triIns,10,[10,100,500],'red',k=1) #Linéaire, la fonction nuage fonctionne








