#Arnaud Capitan MPSI B
#DM info janvier coloriage

import matplotlib.pyplot as plt
import numpy as np

"""
Taille du carré n*n
Les lignes vont de 0 à n-1 du haut vers le bas
Les colonnes vont de 0 à n-1 de gauche à droite
T[i,j] correspond à la couleur de 0 à 255

i est la ligne (ordonnée du haut vers le bas)
j la colonne (abscisse de gauche à droite)

La commande assert vérifie que la condition qui suit est vérifiée, sinon message d'erreur
"""



##Question 1 :

def listeVoisins(i,j,n):
    assert n > 0 #Condition sur n, il faut qu'il y ait au moins un pixel
    assert 0 <= j < n #Condition sur j
    assert 0 <= i < n #Condition sur n
    listeVoisins=[]
    listeVoisins.append([i,j-1]) #Voisin gauche
    if j == 0 :
        listeVoisins.pop() #Si i est en bout de tableau, on enlève le voisin (inexistant)
    listeVoisins.append([i-1,j]) #Voisin haut
    if i == 0 :
        listeVoisins.pop()
    listeVoisins.append([i,j+1]) #Voisin droite
    if j == n-1 :
        listeVoisins.pop()
    listeVoisins.append([i+1,j]) #Voisin bas
    if i == n-1 :
        listeVoisins.pop()
    return(listeVoisins)

#Exemple : Dans un carré de taille 2x2, les voisins de [1,1] sont seulement [0,1] et [1,0]
assert ((listeVoisins(1,1,2) == [[1, 0], [0, 1]]) or (listeVoisins(1,1,2) == [[0, 1], [1, 0]]))  #Selon l'ordre

##Question 2 :

#La manière dont la question est formulée laisse à penser que si la couleur c se trouve dans une autre
#zone que celle du point choisi (alors colorié), alors les deux zones seront intégralement coloriées
#On suppose alors que cette position (i,j) initiale est la seule à avoir la couleur c

#Condition du if : Si la case est dans la liste des voisins et que sa couleur n'est pas noire

"""
## Création de la fonction sans l'aide AdmetVoisinCouleur
def EtendreCouleur_moi(T,i,j,c):
    assert type(T) == np.ndarray #T est un tableau
    (colonne, ligne) = T.shape
    assert 0 <= c <= 255 #La couleur doit être entre 0 et 255
    assert colonne == ligne #On suppose colonne = ligne = n
    n = colonne
    assert n > 0 #Au moints un pixel
    T[i,j]=c #On colorie la case (i,j) avec la couleur c
    modif = 1 #Nombre de modification(s), initialisé à 1 pour entrer dans la boucle
    while modif != 0:
        modif = 0
        for i in range (n): #Ligne
            for j in range (n): #Colonne
                if (T[i,j] != 255)  and (T[i,j] != c) :
                    for [a,b] in listeVoisins(i,j,n):
                        if T[a,b] == c:
                            T[i,j] = c #On met la couleur de la case à la couleur c
                            modif=1

#Exemples et commentaires

n=100 #Création d'un tableau exemple
T=np.zeros((n,n)) #zéro == blanc
for i in range (n-1): #Ouverture en bas à droite
    T[i,i]=255 #255 == noir, ici diagonale

##Si toutes les cases sont colorées par c (une zone), alors la valeur de c deviendra la valeur minimale -> blanc

T[0,n-2]=255 #On garde un petit carré en haut à droite de valeur 0 (blanc)
T[1,n-1]=255

plt.imshow(T, cmap='binary')
plt.title("Image exemple")
plt.show()
plt.clf()
EtendreCouleur_moi(T,2,0,144)
plt.imshow(T, cmap='binary') #Ligne 2 colonne 0, donc zone du bas
plt.title("Image exemple avec coloration de zone avec ouverture")
plt.show()
plt.clf()

n=100
T=np.zeros((n,n))
for i in range (n): #Pas d'ouverture
    T[i,i]=255
T[0,n-2]=255
T[1,n-1]=255
EtendreCouleur_moi(T,2,0,144)
plt.imshow(T, cmap='binary') #Ligne 2 colonne 0, donc zone du bas
plt.title("Image exemple avec coloration de zone sans ouverture")
plt.show()
plt.clf()

"""

def AdmetVoisinCouleur(T,i,j,c):
    n=len(T)
    V=listeVoisins(i,j,n)
    for v in V :
        k,l=v[0],v[1]
        if T[k,l] == c:
            return(True)
    return(False)

#2)a]

def EtendreCouleur(T,i,j,c):
    n=len(T)
    T[i,j]=c #On colorie la case (i,j) avec la couleur c
    modif = True #Critère d'une modification, initialisée à True pour rentrer dans le boucle
    #cout=0
    while modif == True:
        modif = False
        for i in range (n): #Ligne
            for j in range (n): #Colonne
                #cout+=30
                if (T[i,j] != 255) and (AdmetVoisinCouleur(T,i,j,c) == True) and (T[i,j] != c):
                    T[i,j] = c #Si conditions, alors couleur c à la case (i,j)
                    modif=True
    #print('cout =', cout)


#Explication de la condition du if
"""
T[i,j] != 255
la case n'est pas noire, on cherche à colorer
les zones délimitées par les cases noires

AdmetVoisinCouleur(T,i,j,c) == True
La case admet une case voisine de la couleur de c

T[i,j] != c Si la case est déjà grise, on ne rentre pas dans
la boucle, on ne s'intéresse qu'aux cases blanches
-> Cette dernière condition est notre condition d'arrêt :
si toutes les cases pouvant être colorées ont été colorées, alors la boucle s'arrête
"""

#Exemple

n=10
T=np.zeros((n,n))
for i in range (n): #Pas d'ouverture
    T[i,i]=255
T[0,n-2]=255
T[1,n-1]=255
plt.imshow(T, cmap='binary')
plt.title("Image exemple")
plt.show()
plt.clf()
EtendreCouleur(T,2,0,144)
plt.imshow(T, cmap='binary') #Ligne 2 colonne 0, donc zone du bas
plt.title("Image exemple avec coloration de zone sans ouverture")
plt.show()
plt.clf()#La fonction fonctionne


#2)b]
import math as m

#Dans le pire des cas, on a l'image suivante
n=32
T=np.zeros((n,n))
for i in range (n):
    if (i % 2) == 0:
        if (i//2) % 2 == 0:
            for j in range (n-1):
                T[i,j]=255
        if (i//2) % 2 == 1:
            for j in range (1,n):
                T[i,j]=255
T[n-1,n-2]=255
T[n-2,n-1]=255
T[n-1,n-1]=0 #Création d'une case blanche pour conserver la couleur, voir ci-dessous
plt.imshow(T, cmap='binary')
plt.title("Image exemple")
plt.show()
plt.clf()
EtendreCouleur(T,0,n-1,144)
##IMPORTANT :
#Si on ne met pas de case blanche (ici en bas à droite) dans le cas d'une zone unique,
#la valeur c de la couleur grise
#qui se trouve alors partout est maintenant la valeur minimale -> correspond alors à la couleur blanche
#Si on travaille en RGB on perd ce problème mais on augmente en complexité en jouant sur le rouge vert et bleu
plt.imshow(T, cmap='binary')
plt.title("Image exemple avec coloration de zone sans ouverture")
plt.show()
plt.clf()

"""
Estimation du coût:
n désigne la dimension du tableau
Nombre de tours de la boucle while:
au maximum, (n+1)/2 en nombre de lignes parcourues totalement, multiplié par n pour chaque case de ces lignes
On ajoute n/2 pour les cases de 'transition' entre chaque ligne totalement parcourue
(n+1)n/2 + n/2 = (n+2)n/2 itérations de la boucle while
n*n dans le cas de l'appel de chaque ligne chaque colonne
Coût majoré à 30 environ pour la condition -> N'augmente pas l'ordre de n
On néglige les attributions de valeur de le coût
On a donc un ordre du coût de O(n4)
Exemple avec n = 100 : Nombre d'opérations obtenues, environ cout = 743100000 (voir fonction)
100^4 = 10^8, cout/10^8 environ égal à 7, estimation correcte
"""

# d = 4

## Question 3:

def EtendreCouleur2(T,i,j,c):
    Voisins=[[i,j]]
    n=len(T)
    while len(Voisins) != 0 :
        L=Voisins.pop()
        T[L[0],L[1]]=c
        for [a,b] in listeVoisins(L[0],L[1],n):
            if (T[a,b] != c and T[a,b] != 255):
                Voisins.append([a,b])

#Vérification
n=32
T=np.zeros((n,n))
for i in range (n):
    if (i % 2) == 0:
        if (i//2) % 2 == 0:
            for j in range (n-1):
                T[i,j]=255
        if (i//2) % 2 == 1:
            for j in range (1,n):
                T[i,j]=255
T[n-1,n-2]=255
T[n-2,n-1]=255
T[n-1,n-1]=0
plt.imshow(T, cmap='binary')
plt.title("Vérification de la fonction 2")
plt.show()
plt.clf()
EtendreCouleur2(T,0,n-1,144)
plt.imshow(T, cmap='binary')
plt.title("Vérification de la fonction 2")
plt.show() #La fonction fonctionne
plt.clf()

## Question 4 :
#Le temps de calcul est raisonnablement, mais voici ce que l'on observe :
#On a la courbe du cout de la première fonction cout/n**4 qui est stable à environ 8 pour n qui augmente
#On a les courbes du cout de la deuxième fonction cout/n**4 et cout/n**3 qui tendent vers 0
#On a la courbe du cout de la deuxième fonction cout/n**2 qui est stable à environ 40 pour n qui augmente
"""
def EtendreCouleur2_avec_cout(T,i,j,c):
    cout2=0
    Voisins=[[i,j]]
    cout2+=1 #Attribution
    while len(Voisins) != 0 :
        cout2+=1 #Test du while
        L=Voisins.pop()
        cout2+=1 #Opération pop
        T[L[0],L[1]]=c
        cout2+=3 #Lecture de L deux fois, attribution
        for [a,b] in listeVoisins(L[0],L[1],n):
            cout2+=3 #Lecture des 3 paramètres de listeVoisins
            cout2+=14 #Coût de listeVoisins en négligeant les assert (supprimables)
            cout2+=1 #Attribution
            cout2+= 4 #Lecture et comparaison de valeurs
            if (T[a,b] != c and T[a,b] != 255):
                Voisins.append([a,b])
                cout2+=1 #.append
    return(cout2)

def EtendreCouleur_avec_cout(T,i,j,c):
    cout=0
    n=len(T)
    cout+=1#Attribution
    T[i,j]=c
    cout+=1#Attribution
    modif = True
    cout+=1#Attribution
    while modif == True:
        cout+=1#Comparison
        modif = False
        cout+=1#Attribution
        for i in range (n):
            for j in range (n):
                cout+=27 #Cout de AdmetVoisinCouleur
                cout+=3 #Comparaisons
                if (T[i,j] != 255) and (AdmetVoisinCouleur(T,i,j,c) == True) and (T[i,j] != c):
                    T[i,j] = c #Si conditions, alors couleur c à la case (i,j)
                    modif=True
                    cout+=2 #Attributions
    return(cout)

def creer_tableau():
    T=np.zeros((n,n)) #On recreer le tableau modifié
    for i in range (n):
        if (i % 2) == 0:
            if (i//2) % 2 == 0:
                for j in range (n-1):
                    T[i,j]=255
            if (i//2) % 2 == 1:
                    for j in range (1,n):
                        T[i,j]=255
    return(T)

X=[]
Y1=[]
Y2=[]
Y3=[]
Y4=[]
for i in range (1,20):
    n=5*i
    X.append(n)
    T=creer_tableau()
    Y1.append(EtendreCouleur_avec_cout(T,0,n-1,146)/n**4)
    T=creer_tableau()
    Y2.append(EtendreCouleur2_avec_cout(T,0,n-1,130)/n**4)
    T=creer_tableau()
    Y3.append(EtendreCouleur2_avec_cout(T,0,n-1,130)/n**3)
    T=creer_tableau()
    Y4.append(EtendreCouleur2_avec_cout(T,0,n-1,130)/n**2)

plt.plot(X,Y1, label='cout/n**4 de EtendreCouleur', color='red')
plt.plot(X,Y2, label='cout/n**4 de EtendreCouleur2', color='green')
plt.plot(X,Y3, label='cout/n**3 de EtendreCouleur2', color='blue')
plt.plot(X,Y4, label='cout/n**2 de EtendreCouleur2', color='pink')
plt.grid()
plt.legend()
plt.title('Courbe des couts')
plt.show()
"""

## Bonus : sapin

T=np.zeros((30,30))
for j in range (30): #Herbe
    T[26, j]=255
for i in range (5): #Soleil
    T[i,21]=255
T[5,22]=255
T[6,23]=255
T[7,24]=255
for j in range (25,30):
    T[8,j]=255
for i in range (22,26):#Tronc du sapin
    T[i,8]=255
    T[i,14]=255
for j in range (8,15):
    T[22,j]=255
for j in range (4,19):#Sapin
    T[22,j]=255
for j in range (6,17):
    T[18,j]=255
for j in range (8,15):
    T[14,j]=255
T[21,5]=255
T[20,6]=255
T[19,7]=255
T[21,17]=255
T[20,16]=255
T[19,15]=255

T[17,7]=255
T[16,8]=255
T[15,9]=255
T[17,15]=255
T[16,14]=255
T[15,13]=255

T[13,9]=255
T[12,10]=255
T[11,11]=255
T[13,13]=255
T[12,12]=255
T[11,11]=255

plt.imshow(T, cmap='binary')#Avant coloriage
plt.title("Sapin en cours de création")
plt.show()
plt.clf()

EtendreCouleur2(T,29,0,110)#Herbe

EtendreCouleur2(T,21,6,140)#Sapin
EtendreCouleur2(T,17,8,140)
EtendreCouleur2(T,13,10,140)

EtendreCouleur2(T,0,0,180)#Ciel

EtendreCouleur2(T,0,29,80)#Soleil

EtendreCouleur2(T,23,10,10)#Tronc

T[0,29]=0 #Pour conserver l'échelle de couleur
plt.imshow(T, cmap='nipy_spectral_r')#Après coloriage
plt.title("Meilleurs voeux et bonne santé.")
plt.show()
plt.clf()
