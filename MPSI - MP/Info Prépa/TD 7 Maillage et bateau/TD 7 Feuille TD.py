## TD 7 : Facettes et maillages
## Feuille de TD
#Arnaud Capitan MPSI B

import numpy as np
import random
import math as m

A=np.array([1,2,3])
b=[10,20,30]
B=np.array(b)
u=A+B #Addition des coordonnées du tableau
v=2.5*A #Produit par un scalaire des coordonnées du tableau
print(type(u),u,v)

## Question 5-6 : Géométrie dans R3

def tab_to_list(A): #Convertit un tableau en liste
    Resultat=[]
    for i in range (len(A)): #Pour chaque élément du tableau (de dimension 1 lig n col)
        Resultat.append(A[i]) #Le transfert dans une liste
    return(Resultat) #Retourne la liste

def addition(V1,V2):
    V1=np.array(V1) #On convertit sous forme de tableau
    V2=np.array(V2)
    return(tab_to_list(V1+V2)) #On additionne et on reconvertit sous forme de liste

def prod_scalaire(V1,V2):
    Res=[]
    for i in range(len(V1)): #on suppose len(V1) = len(V2) sinon prod scalaire impossible
        Res.append(V1[i]*V2[i])
    return(Res)

def norme_carre(V1): # ||u||² = x² + y² + z² + t² + ...
    Res=0
    for i in range (len(V1)):
        Res += V1[i]*V1[i]
    return(Res)

def soustraction(V1,V2):
    return(addition(V1,-1*V2))

def barycentre(F): #F désigne ici une famille de vecteurs dans R3
    G = [0,0,0]
    for i in range (3):
        for vecteurs in F:
            G[i]+=vecteurs[i]/len(F)
    return(G)

def produit_vectoriel(V1,V2): #On suppose dimension 3
    Res=[]
    Res.append(V1[1]*V2[2]-V1[2]*V2[1]) #Déterminant sans la ligne 1
    Res.append(-(V1[0]*V2[2]-V1[2]*V2[0])) #-Déterminant sans la ligne 2
    Res.append(V1[0]*V2[1]-V1[1]*V2[0]) #Déterminant sans la ligne 3
    return(Res)

def aire(V1,V2): #Norme du produit vectoriel
    return(abs(V1[0]*V2[1]-V1[1]*V2[0]))

def multiplie_scalaire(a,V1):
    V1=np.array(V1)
    V1=a*V1
    return(tab_to_list(V1))

# Liste aléatoire
Rand=[]
for k in range (20):
    Rand.append(random.randint(-20,20))


def fusion (L1, L2):
    M=[]
    i=0
    j=0
    while i < len(L1) and j < len(L2):
        if L1[i] < L2[j]:
            M.append(L1[i])
            i+=1
        else :
            M.append(L2[j])
            j+=1
    if i == len(L1) and j < len(L2):
        for k in range (j,len(L2)):
            M.append(L2[k])
    elif i < len(L1) and j == len(L2):
        for k in range (i,len(L1)):
            M.append(L1[k])
    return(M)

A=[1,3,5,7,9]
B=[0,2,4,6,8]

print(fusion(A,B))

"""
Question 25 :
a] Nombre de comparaisons utiles :
2 par tour pour la boucle while
1 par tour pour l'ajout d'un élément de L1 ou de L2

2 à la fin pour ajouter le reste de la liste incomplétée
=> 3L + 2 au minimum si L1 + L2 est déjà triée
=> 3*2L + 2 au maximum si les deux listes doivent être entièrement parcourues succissivement

Liste de longueur 2^k :
Meilleur des cas : 3*2^k + 2
Pire des cas : 3*2^(k+1) + 2

Pour une liste de longueur 2^n, on aura :
2^(n-1) comparaisons pour les listes de 2 éléments
puis 2^(n-2) tri fusion sur chaque paire de listes de 2 éléments, 2^(n-2)*3*2^(2+1)+2 = 3*2^(n+1) + 2
2^(n-2) comparaisons pour 4 éléments
puis 2^(n-3) tri fusion sur chaque paire de liste de 4 éléments, 2^(n-3)*3*2^(2+2)+2 = 3*2^(n+1) + 2
...
2 comparaisons pour 2^n-1 éléments, soit concaténer les deux dernières listes
Après les listes s'ajoutent
On a ainsi N comparaisons, avec N = somme k=1 à n-1 des 2^k
N = 2*((1-2^(n-1))/(1-2)) = 2^n - 2 pour les comparaisons

Entre chaque étape, on a un tri fusion effectué avec chaque liste
Coût total : Comparaisons + Tris
n-1 - 1 + 1 le nombre d'étapes de tri, coût de (3*2^(n+1) + 2)* (n-1)

Coût total :  (3*2^(n+1) + 2 )*(n-1) + 2^n - 2 de l'ordre de 2n*L

ln(L) = n(len(2)) ainsi, on a un coût en n*ln(n), le tri est efficace

"""