## DM Tour de Hanoï
#Arnaud Capitan MPSI B

import numpy as np
import matplotlib.pyplot as plt

"""
Résolution de la Tour de Hanoï dans des cas simples (fait au brouillon)
Déplacement de la tour de A à B
Avec 1 anneau :

On le deplace de A à B : fin

Avec 2 anneaux :

On déplace 1 de A à C
2 de A à B
1 de C à B

Avec 3 anneaux :

1 de A à B
2 de A à C
1 de B à C
3 de A à B
1 de C à A
2 de C à B
1 de A à B

Avec 4 anneaux :

1 de A à C
2 de A à B
1 de C à B
3 de A à C
1 de B à A
2 de B à C
1 de A à C -> Colonne de 3 formée en C
4 de A à B
1 de C à B
2 de C à A
1 de B à A
3 de C à B
1 de A à C
2 de A à B
1 de C à B

On remarque plusieurs éléments :
Un mouvement sur deux est celui de l'anneau 1
L'anneau 1 tourne toujours dans le même sens (se deplace de gauche à droite ou de droite à gauche)
Le sens est déterminée dès le premier mouvement selon le nombre d'anneaux (pair ou impair)
Il semble que le mouvement d'un anneau autre que le 1 soit contraint :
    -> Il n'y a qu'une position possible pour l'anneau autre que le 1 pour le déplacement
    -> Faciliter d'une fonction déplace_autre qui bouge un anneau autre que la 1
    -> Fonction déplace_1 qui ne déplace que l'anneau 1 selon le sens

Par cet algorithme, peu importe la taille de la première colonne, elle finit par se déplacer.
Seul le choix de la colonne B ou C pour le premier déplacement de l'anneau 1 donnera
son emplacement de destination.
"""

def initialise_tour(n): #Permet de créer une tour de Hanoï de taille n en première position
    A = []
    B=[]
    C=[]
    for i in range(n):
        A.append(n-i)
    if n%2 == 0:
        return([A,B,C],-1) #Sens de droite à gauche A->C->B->A
    return([A,B,C],1) #Sens de gauche à droite A->B->C->A

def deplace_1(L,sens):
    position=0 #Liste[position] contient le premier anneau
    if 1 in L[1]:
        position=1
    if 1 in L[2]:
        position=2
    L[position].pop()
    L[(position+sens)%3].append(1)
    return((position+sens)%3)

def deplace_autre(L,k): #Le nombre k indique la position du 1 après son déplacement
    if len(L[(k+2)%3])==0: #Si cette liste est vide
        anneau=L[(k+1)%3].pop() #On extrait l'anneau à deplacer de la dernière liste
        L[(k+2)%3].append(anneau) #On l'ajoute
    elif len(L[(k+1)%3])==0: #De même
        anneau=L[(k+2)%3].pop()
        L[(k+1)%3].append(anneau)
    elif L[(k+1)%3][-1] > L[(k+2)%3][-1]: #Si les listes sont non vides, on peut faire le teste
        anneau=L[(k+2)%3].pop()
        L[(k+1)%3].append(anneau)
    else :
        anneau=L[(k+1)%3].pop()
        L[(k+2)%3].append(anneau)

## Fonction récursive solution :

def algo_solution_rec(L,n,sens):
    pos=deplace_1(L,sens) #L'algo ne peut terminer qu'après déplacement de l'anneau 1
    if len(L[1]) == n: #Si tous les anneaux se trouvent dans la colonne B
        return() #On ne fait rien, la boucle termine
    deplace_autre(L,pos)
    return(algo_solution_rec(L,n,sens))

## Fonction solution par boucle while :

def algo_solution(L,n,sens):
    while(True): #L'algo finit, la boucle est infinie
        pos=deplace_1(L,sens)
        if len(L[1]) == n:
            return()
        deplace_autre(L,pos)

def Hanoi(n,fonction):
    L,sens=initialise_tour(n)
    print(L)
    fonction(L,n,sens)
    print(L)

"""
Hanoi(10,algo_solution_rec) #A partir de 11 le maximum de récursivité est dépassé
Hanoi(20,algo_solution) #Fonctionne pour tout entier naturel non nul à partir d'un certain temps
"""
## Gloutton

def DiviseFacile(a,b): #Division euclidienne entière de a par b
    q=0
    while a>=b:
        a-=b
        q+=1
    return(a,q) #a correspond au reste, q au quotient

def RenduMonnaieGlouton(s,Sn):
    N=len(Sn)
    Rep=[0]*N
    for i in range (N):
        s,n=DiviseFacile(s,Sn[N-1-i])
        Rep[N-1-i] = n
    if s != 0 :
        print("Reste de monnaie :", s)
    return(Rep)

assert RenduMonnaieGlouton(573,[1,2,5,10,25,50,100]) == [1,1,0,2,0,1,5] #Monnaie canonique
assert RenduMonnaieGlouton(99,[1,10,100]) == [9,9,0] #Cas du Birr Ethiopien, une monnaie non canonique

"""
On souhaite montrer la terminaison de l'algorithme.
Pour tout entier naturel strictement positif s (une somme d'argent):
Si s est supérieure à Sn[N], on récupère le reste de la division euclidienne de s par Sn[n]
-> Le quotient égal au nombre de pièces est ajouté à la liste Rep
-> Le reste, une fois inférieure strictement à Sn[N], passe au même test mais avec Sn[N-1]
...
-> Une fois que le reste arrive à Sn[0], celui doit être obligatoirement égal à 1
    -> Sinon toute somme d'argent impaire ne fonctionnerait pas
En faisant la division euclidienne de s par Sn[0] = 1, on récupère obligatoirement un reste nul (Fin)
et le nombre de pièces correspondant. Si 1 n'est pas présent, la boucle termine quand même et
affiche la monnaie restante.

Ainsi, tout au long de l'algorithme, sachant que l'on ne conserve pas la valeur de s le long
de l'exécution de l'algo, on a l'égalité suivante :
Pour tout i entier 0 <= i <= N-1, avec len(Sn) = N :
Somme d'argent initiale = s + Rep[i]*Sn[i], avec s strictement décroissante tout au long de l'algo
A la fin, si Sn[0] = 1 on a forcément un reste nul, sinon affichage de la somme d'argent restante
"""

def RenduMonnaieGloutonRecursive(s,Sn,Rep=[],i=0):
    if i == len(Sn):
        Rep2=[]
        for j in range (len(Rep)):
            Rep2.append(Rep.pop()) #Principe des piles pour inverser Rep
        return(Rep2)
    s,n=DiviseFacile(s,Sn[len(Sn)-i-1])
    Rep.append(n)
    return(RenduMonnaieGloutonRecursive(s,Sn,Rep,i+1))

assert RenduMonnaieGloutonRecursive(573,[1,2,5,10,25,50,100]) == [1,1,0,2,0,1,5]
assert RenduMonnaieGloutonRecursive(99,[1,10,100]) == [9,9,0]

## Convolution

#Le noyau est nécessairement de dimension impaire pour pouvoir l'appliquer
# (2k+1)//2 -> k

def debutFin(noyau,image): #On a besoin de la dimension du noyau et de l'image, on suppose le noyau carré
    n=len(noyau)//2
    lig,col,h=np.shape(image)
    return([n,n],[lig-n-1,col-n-1])

## Je mets on programme comme ceci car même avec la correction je n'arrive pas à afficher une image simplement flouttée
"""
def convolution1(image,kern,i,j):
    somme=0
    dim_kern = len(kern)
    dim_kern_sur_2 = dim_kern//2
    for lig in range(dim_kern):
        for col in range (dim_kern):
            somme += image[i-dim_kern_sur_2+lig,j-dim_kern_sur_2+col]*kern[lig,col]
    return(somme)

def convolution_couleur(image,kern,i,j):
    somRGB=image[i,j].copy()
    dim_kern = len(kern)
    dim_kern_sur_2 = dim_kern//2
    for couleur in range (3): #Les 3 couleurs du RGB
        somme=0.01 #Pour contraste, on prend un nombre non nul
        for lig in range(dim_kern):
            for col in range (dim_kern):
                somme += image[i-dim_kern_sur_2+lig,j-dim_kern_sur_2+col][couleur]*kern[lig,col]
        somRGB[couleur]=somme
    return(somRGB)


def moyenne(ker):
    dim = len(ker)
    moy=0
    for lig in range (dim):
        for col in range (dim):
            moy+=abs(ker[lig,col])
    return(moy)

def convolutionT(A,ker):
    dim1,dim2 = debutFin(ker,A)
    lig = dim2[0]-dim1[0]
    col = dim2[1]-dim1[1]
    Array=A.copy() #On a un tableau de même dimension
    #Array=Array*moyenne(ker)
    for i in range (lig):
        print(((100*i/lig)//1),"% Chargement de la convolution...")
        for j in range (col):
            Array[i,j]=convolution_couleur(A,ker,dim1[0]+i,dim1[1]+j)
    return((Array//1))#/moyenne(ker))//1)

Image=plt.imread("C:/Users/Arnaud/Desktop/Info/DM + TP Info/Image_convolution.jpg")

plt.imshow(Image)
plt.title("Image étudiée")
plt.pause(3)
plt.close()
plt.clf()

# Premier Kernel -> Moyenne

Ker=np.ones((3,3))
image2=convolutionT(Image,Ker)
plt.imshow(image2)
plt.title("Kernel : Moyenne")
plt.show()
plt.pause(3)
plt.close()
plt.clf()


# Deuxième Kernel -> Variation

Ker=np.array([[0.,1.,0.],[1.,-4.,1.],[0.,1.,0.]])
image3=convolutionT(Image,Ker)
plt.imshow(image3)
plt.title("Kernel : Variation")
plt.show()
plt.pause(3)
plt.close()
plt.clf()

# Troisième Kernel -> Contraste

Ker=np.array([[0.,0.,0.,0.,0.],[0.,0.,-1.,0.,0.],[0.,-1.,-5.,-1.,0.],[0.,0.,-1.,0.,0.],[0.,0.,0.,0.,0.]])
image4=convolutionT(Image,Ker)
plt.imshow(image4)
plt.title("Kernel : Contraste")
plt.show()
plt.pause(3)
plt.close()
plt.clf()

# Quatrième Kernel -> Renforce Bord

Ker=np.array([[0.,0.,0.],[-1.,1.,0.],[0.,0.,0.]])
image5=convolutionT(Image,Ker)
plt.imshow(image5)
plt.title("Kernel : Renforce Bord")
plt.show()
plt.pause(3)
plt.close()
plt.clf()
"""
##
"""
Pour la dérivée partielle, le kernel renforce bord en place la variation (pour h=1)
f(x+1,y) - f(x,y) -> Le kernel de renforce bord se place ici en (x+1,y) (pour son centre)
Son orientation est sur la même ligne de la gauche vers la droite

Pour la dérivée seconde :
On a f(x+2h) - 2f(x) + f(x-2h) / 4h²    Pour h = 1, on obtient le kernel suivant
np.array([[0,0,0,0,0],[0,0,0,0,0],[1/4,0,-2/4,0,1/4],[0,0,0,0,0],[0,0,0,0,0]])
Kernel centré en x, de dimension carrée 5x5
"""

def conv_col_cor(A,kern,i,j):
    SomRGB=A[i,j].copy()
    centreK=np.shape(kern)[0]//2
    r=np.shape(kern)
    ligne=i-centreK
    colonne=j-centreK
    for couleur in range(3):
        som=0.05
        for lig in range(r[0]):
            for col in range(r[1]):
                som+=A[lig+ligne,col+colonne][couleur]*kern[lig,col]
        SomRGB[couleur]=som
    return(SomRGB)

def conv_corr(A,kern):
    Conv=A.copy()
    xy0,xy1=debutFin(kern,A)
    for i in range (xy0[0],xy1[0]+1):
        for j in range (xy0[1],xy1[1]+1):
            Conv[i,j]=conv_col_cor(A,kern,i,j)
    return(Conv)
k=np.ones((3,3))

Image=plt.imread("C:/Users/Arnaud/Desktop/Info/DM + TP Info/Image_convolution.jpg")
voir=conv_corr(Image,k)
plt.imshow(voir)
plt.show()
#Même image que pour mes fonctions, pourtant difficile de reconnaître l'image initiale
