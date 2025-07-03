## TD 7 : Facettes et maillages
## Sujet complet
#Arnaud Capitan MPSI B

import numpy as np
import random
import math as m

## Partie 1 : Création d'un objet dans la scène

#Questions 1 2 3 Requêtes SQL //

#Q4 :

maillage_tetra =    [ [[0.,0.,0.], [0.,0.,1.], [0.,1.,0.]],
                      [[0.,0.,0.], [0.,1.,0.], [1.,0.,0.]],
                      [[0.,0.,0.], [1.,0.,0.], [0.,0.,1.]],
                      [[1.,0.,0.], [0.,1.,0.], [0.,0.,1.]], ]


def premier_sommet(maillage_tetra): #Permet de récupérer la coordonnée y du premier sommet
    return(maillage_tetra[0][0][1])

#Q5 :
"""
maillage_tetra[1] correspond à la face décrite par les coordonnées des 3 points de la deuxième liste
Les points sont [0.,0.,0.], [0.,1.,0.], [1.,0.,0.], donc maillage_tetra[1] correspond à la face S3
"""
#Q6 :

"""
from operations_vectorielles.py import pro_scalaire as ps
"""
#Q7 :

def mystere1(V):
    return(V[0]**2+V[1]**2+V[2]**2)**0.5

"""
La fonction mystere1 renvoie la norme d'un vecteur V de R3
"""

#Q8 :

def tab_to_list(A): #Convertit un tableau en liste
    Resultat=[]
    for i in range (len(A)): #Pour chaque élément du tableau (de dimension 1 lig n col)
        Resultat.append(A[i]) #Le transfert dans une liste
    return(Resultat) #Retourne la liste

def multiplie_scalaire(a,V1):
    V1=np.array(V1)
    V1=a*V1
    return(tab_to_list(V1))

#Q9 :

def barycentre(F): #G désigne le barycentre (point), F une facette [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
    G=[0,0,0]
    for i in range(3): #Pour chaque coordonnées de G
        for j in range(3): #Pour chaque sommet de la facette
            G[i]+=F[j][i]/3 #On ajoute la coordonnée moyennée
    return(G)

#Q10 :

def produit_vectoriel(V1,V2): #On suppose dimension 3
    Res=[]
    Res.append(V1[1]*V2[2]-V1[2]*V2[1]) #Déterminant sans la ligne 1
    Res.append(-(V1[0]*V2[2]-V1[2]*V2[0])) #-Déterminant sans la ligne 2
    Res.append(V1[0]*V2[1]-V1[1]*V2[0]) #Déterminant sans la ligne 3
    return(Res)

def norme_carre(V1): # ||u||² = x² + y² + z² + t² + ...
    Res=0
    for i in range (len(V1)):
        Res += V1[i]*V1[i]
    return(Res)

def norme(V1):
    return(m.sqrt(norme_carre(V1)))


def soustraction(V1,V2):
    V1=np.array(V1)
    V2=np.array(V2)
    return(tab_to_list(V1-V2))

def vecteur(A,B): #On crée un vecteur à partir des coordonnées de deux points
    Res=[]
    for i in range (len(A)):
        Res.append(B[i]-A[i])
    return(Res)

def multiplie_scalaire(a,V1):
    V1=np.array(V1)
    V1=a*V1
    return(tab_to_list(V1))

def normale(F): #F=(A,B,C), de la forme F = [ [xA,yA,zA], [xB,yB,zB], [xC,yC,zC] ]
    AB = vecteur(F[0],F[1])
    AC = vecteur(F[0],F[2])
    ABprodvectAC = produit_vectoriel(AB,AC)
    vecteur_n = multiplie_scalaire(1/norme(ABprodvectAC),ABprodvectAC)
    return(vecteur_n)

#Q 11)

def sont_proches(S1,S2,eps): #S1 une lsite contenant les coordonnées du sommet 1, eps un écart
    S1S2 = vecteur(S1,S2)
    if norme(S1S2) < eps:
        return(True)
    return(False)

def mystere2(S1,L):
    for S2 in L:
        if sont_proches(S1,S2, 1e-7):
            return(True)
    return(False)

#Q 12)

def mystere3(maillage):
    res = []
    for facette in maillage:
        for sommet in facette :
            if not mystere2(sommet,facette): #équivalent de if mystere2(sommet,facette) == False:
                res.append(sommet)
        return(res) #Ne renvoie le(s) sommet(s) coorespondant que de la première facette

def mystere3v2(maillage):
    res = []
    for facette in maillage:
        for sommet in facette :
            if not mystere2(sommet,facette): #équivalent de if mystere2(sommet,facette) == False:
                res.append(sommet)
    return(res) #Renvoie le(s) sommet(s) coorespondant de toutes les facettes du maillage

"""
La fonction mystere2 renvoie True si le point en paramètre est à une distance inférieure à 1e-7
d'un sommet de la facette indiquée

La fonction mystere3 renvoie la liste des sommets de la première facette  d'un maillage
qui sont à une distance à 1e-7, cela permet de savoir quels sommets font des facettes
avec des aires très petites, éventuellement pour pondérer

La fonction mystere3v2 renvoie la liste des sommets de toutes les facettes d'un maillage ...
"""

#Q 13)

"""
mystere3(maillage_tetra) renvoie une liste vide car aucun des sommets n'est proche à 1e-7 des autres
"""

#Q 14)

"""
Pour une liste L de longueur n : au pire des cas, L n'a aucun sommet proche de S1 -> return(False)
n opérations de sont_proches
Coût de sont_proches : en supposant des vecteurs de R3
Cout de vecteur : 3 opérations
Cout de sont_proches : Cout de vecteur + 1 comparaison = 4

Cout de mystere2 au pire des cas : 4n
Cout de mystere2 au meilleur des cas : 4, le premier sommet est proche de S1

Complexité de mystere3 : au meilleur des cas, mysterev2 renvoie True à chaque fois
-> Complexité de 12 (4*3 sommets)
Au pire des cas (false à chaque fois) : 12m
"""

## Partie 2 : Génération de vagues

#Q 15)
"""
h i,j codé sur 64 bits
on a 200x200 h i,j par image
On a 350 images

Total : 64*200*200*350 = 896000000 bits
1 octet = 8 bits
1 ko = 1024 octets
1 Mo = 1024 ko = 1024² octets = 1024²*8 bits

Total : 896000000/(1024²*8) = 106,81 Mo
"""

#Q 16)

#Exemple de mat_h de dimension réduite (le bateau n'est pas passé, la surface d'eau est plane):
mat_h1 =[ [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0] ]

def mat2str(mat_h): #mat_h correspond à une liste de listes sous formme d'un tableau
    chaine=""
    for lig in range(len(mat_h)):
        chaine+="|"
        for col in range (len(mat_h[0])):
            chaine+= str(mat_h[lig][col])
            chaine+=";"
        chaine+="\n"
    return(chaine)

print(mat2str(mat_h1))

#Q 17)
def ecriture(liste_vagues):
    fichier=open("fichier_vagues.txt","w")
    montext=" "
    for k in range(len(liste_vagues)):
        montext += mat2str(liste_vagues[k]) + "\n" #Doublage du retour à la ligne
    fichier.write(montext) #Ecriture de la chaîne de caractère
    fichier.close()

#Q 18) ert Q 19)

"""
Type des éléments contenus dans les listes I et J : des entiers naturels
Type des éléments contenus dans la liste N : float (valeur des éléments non nuls)

p éléments non nuls : p coordonnées de ligne colonne et valeur
on a ainsi I et J contenant p éléments (des entiers naturels de 32 bits)
on a N avec p nombres float (sur 64 bits)

ainsi, la taille pour p éléments est de 32*p + 32*p + 64*p = 128p bits
Une matrice complète classique prend  64*200*200 bits

128p>2560000 <=> p > 20000 éléments
Si plus de la moitié du tableau comprend des éléments non nuls, il est plus efficace d'utiliser une
matrice complète classique
"""

#Q 20)

def matrices_creuses(mat_h): #Création des listes I,J,N
    I=[]
    J=[]
    N=[]
    for lig in range (len(mat_h)):
        for col in range (len(mat_h[0])):
            if abs(mat_h[lig][col]) > 10**(-3):
                 I.append(lig)
                 J.append(col)
                 N.append(mat_h[lig][col])
    return(I,J,N)

## III. a) Estimation de la poussée d'Archimède

#Q 21)

#Condition du if
#Si la coordonnée z du barycentre est inférieure à la hauteur de l'eau aux coordonnées (x,y)

def lister_FI(maillage,hauteur): #La fonction hauteur est supposée connue
    facettes_immergées=[]
    for facette in maillage:
        G=barycentre(facette) #G contient les coordonnées x,y,z du barycentre de la facette
        if G[2] < hauteur(G[0],G[1]):
            facettes_immergées.append(facette)
    return(facettes_immergées)

#Q 22)

def p(G,hauteur): #Pression hydrostatique au barycentre G = [xG,yG,zG]
    return (9.81*1000*(hauteur(G[0],G[1]) - G[2]))

def aire(V1,V2): #Norme du produit vectoriel (R2)
    return(abs(V1[0]*V2[1]-V1[1]*V2[0]))

def aire_facette(F): #Norme du produit vectoriel (R3)
    AB = vecteur(F[0],F[1])
    AC = vecteur(F[0],F[2])
    return(norme(produit_vectoriel(AB,AC)))


def force_facette(F,hauteur):
    vecteur_normal = normale(F)
    S=aire_facette(F)
    return(multiplie_scalaire(-S*p(barycentre(F),hauteur),vecteur_normal))

#Q 23)
#Résultante des forces = somme des vecteurs force F

def resultante(L,hauteur): #Les facettes de la liste L sont supposées immergées, hauteur supposée connue
    res=[0,0,0]
    for facette in L:
        res = addition(res,force_facette(facette,hauteur))
    return(res[2]) #Coordonnées z de la résultante des forces

##III. b) Tri des facettes

#Q 24)

def fusion(L1,L2): #L1 et L2 supposées triées par aire décroissante
    res=[]
    i=0
    j=0
    while i < len(L1) and j < len(L2):
        if aire_facette(L1[i]) > aire_facette(L2[j]):
            res.append(L1[i])
            i+=1
        else :
            res.append(L2[j])
            j+=1
    if i == len(L1) and j < len(L2):
        for k in range (j,len(L2)):
            res.append(L2[k])
    elif i < len(L1) and j == len(L2):
        for k in range (i,len(L1)):
            res.append(L1[k])
    return(res)

#Q 25) a] Récursivité

def trier_facettes(L):
    if len(L) == 1:
        return(L)
    if len(L) == 2:
        if aire_facette(L[0]) < aire_facette(L[1]): #Si la liste est dans l'ordre croissant de surface
            return[L[1],L[0]] #On renvoie la liste triée par ordre décroissant de surface
        return(L) #Sinon on renvoie la liste (déjà triée par ordre décroissant)
    return(fusion(trier_facettes(L[:len(L)//2]),trier_facettes(L[len(L)//2 + 1:])))

#Q 25) b] Question TD


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

#Q 26)

maillageG=[[[1,0,0],[1,1,0],[0,0,0]],[[1,1,0],[1,1,1],[0,0,0]],[[1,0,0],[0,1,0],[0,0,0]],[[0,0,0],[0.1,0,0],[0,0,0.1]]]
facettes_triées = trier_facettes(maillageG)
grandesFacettes = facettes_triées[:((len(facettes_triées) + 1)//2)] #On inclut la valeur médiane

#Q 27)

"""
Conditions initiales : z0 = 0, v0 = 0
PFD selon l'axe ez :
dv/dt= 1/m * F(eau -> gondole) - g
dzG/dt = v

F(eau -> gondole) correspond à la fonction resultante
"""
#Méthode d'Euler : f(a+h) = f(a) + h*f'(a) (+h²/2 * f''(a), terme non pris en compte)

m = 100 #Exemple de masse de la gondole
g=9.81

def nouvelle_hauteur(posG, vitG, mailG,hauteur): #Fonction hauteur supposée connue
    dt = 1.0/25.0
    facettes_immergees = listerFI(mailG)
    posG = posG + dt*vitG #Méthode d'Euler
    vitG = vitG + dt*((1/m)*resultante(facettes_immergees,hauteur) - g) #Accélération donnée par PFD
    return(posG, vitG)








