from matplotlib import pyplot as plt
from matplotlib import numpy as np
import cmath as cm #nombres complexes
import math as m
import time #Utilisé pur mesurer les perfs

##Exemple de couleurs
def tableau(n):
    A=np.zeros((n,n)) #Tableau de 10 lignes 15 colonnes
    for k in range(n):
        A[k,k]=-k
    return(A)
A=tableau(2)

plt.imshow(A, cmap='nipy_spectral_r', interpolation='bicubic') #Couleur possible pour un polynôme à n>2 racines
plt.colorbar() #Permet de montrer l'échelle de couleur
plt.title("cmap='nipy_spectral_r'")
plt.pause(2)
plt.close()
plt.clf()

plt.imshow(A, cmap='plasma_r', interpolation='bicubic') #Couleur pour un polynôme à n>2 racines
plt.colorbar() #Permet de montrer l'échelle de couleur
plt.title("cmap='plasma_r'")
plt.pause(2)
plt.close()
plt.clf()

plt.imshow(A, cmap='Blues', interpolation='bicubic') # Couleur pour Mandelbrot's set
plt.colorbar() #Permet de montrer l'échelle de couleur
plt.title("cmap='Blues'")
plt.pause(2)
plt.close()
plt.clf()

plt.imshow(A, cmap='gist_heat_r', interpolation='bicubic') #Couleur pour Julias's set
plt.colorbar() #Permet de montrer l'échelle de couleur
plt.title("cmap='gist_heat_r'")
plt.pause(2)
plt.close()
plt.clf()

##Exercice 1 : Affichage d'une image selon son répertoire
"""
mon_image=plt.imread("H:/Classe_MPSI_B/capitana/Image.png")
plt.imshow(mon_image)
plt.pause(2) #Affiche l'image pendant 2 secondes
plt.close() #Ferme la fenêtre
plt.clf() #Clear figure, supprime la figure, l'enchaînement de ces 3 commandes permet d'automatiser l'affichage
"""

##Exercice 2 :

#1)

A=np.zeros((10,15)) #Tableau de 10 lignes 15 colonnes
for k in range(5):
    A[k,2*k+1]=1-k/5
A[0,14]=-1

"""
plt.imshow(A)
plt.colorbar() #Permet de montrer l'échelle de couleur
plt.pause(3)
plt.close()
plt.clf()
"""

#La valeur associée à chaque point dans le tableau correspond à la couleur,
#allant de -1 à 1, 1 étant une extrémité de la plage de couleur,
#et -1 l'autre extrémité (min et max)

#L'extrémité haut-droite est à -1 (violette)
#Le 0 (presque partout) est bleu cyan, et du 1 au 0, on observe un dégradé du jaune au bleu cyan
#et les points de coordonnées (k, 2k+1) (coordonnées info, lignes, colonnes)


#2a) Version 1, couleur par défaut

B=[[0,1,2],[3,4,5],[6,7,8],[9,10,11]]

"""
plt.imshow(B)
plt.colorbar()
plt.pause(2)
plt.close()
plt.clf()
"""

#2a) Version 2, couleurs données par l'énoncé
"""
plt.set_cmap('jet')
plt.imshow(B)
plt.colorbar()
plt.pause(2)
plt.close()
plt.clf()
"""

#2b)
"""
plt.imshow(B,aspect=1.5,cmap='binary',interpolation='none')
plt.pause(5)
plt.close()
plt.clf()
"""
#La commande interpolation='none' n'effectue aucune action;la remplacer par 'bicubic' par exemple
#créera un flou artificiel entre les pixels, un 'fondu' de couleurs
#La commande cmap='binary' a rendu la couleur utilisée de l'image en binary, noir et blanc
#La commande 'aspect=1.5' change la dimension des pixels, la hauteur devenant 1.5 fois plus
#grande que la longueur du pixel (initialement carré)

#2c)

"""
plt.imshow(B,aspect=0.5,interpolation='none')
plt.pause(2)
plt.close()
plt.clf()
"""

#'aspect=0.5', hauteur pixel = 0.5 * longueur pixel
#Aspect correspond à la taille, interpolation à la manière d'affichée, cmap à la palette de couleur


##Exercice 3 : Un damier

##Damier
"""
n=10
A=np.zeros((n,n))
for i in range (n):
    for j in range (n):
        if (i+j)%2 == 1:
            A[i,j]=1
plt.imshow(A,cmap='binary') #Damier en noir et blanc
plt.pause(2)
plt.close()
plt.clf()
"""
##Diagonale
"""
n2=20
B=np.zeros((n2,n2)) #Couleur blanche partout
for i in range (n2):
    for j in range (n2):
        if (i == 0) or (i == (n2-1)) or (j == 0) or (j == (n2-1)): #Si i ou j = bord
            B[i,j]=0.5 #On place i ou j à la couleur grise, milieu de blanc et noir
        if (n2 - 1 - i) == j :
            B[i,j]=1 #Couleur noir pour la diagonale
plt.imshow(B,cmap='binary')
plt.pause(2)
plt.close()
plt.clf()
"""

##Exercice 4 :

"""
Itération de Newton
xn+1 = xn - f(xn)/f'(xn)
"""

#1) Méthode pour convertir un couple (x,y) de coordonnées en nombre complexe x + jy, j²=-1
"""
x=3
y=2
print(complex(x,y)) #3+2j
"""

#2)
def g_complexe(z): #Itération de Newton associée à la fonction x -> x^5 - 1
    return((4/5)*z +(1/5)*(1/z**4))

def g_couple(x,y):
    z=g_complexe(complex(x,y))
    return(z.real, z.imag)

"""
z = g_complexe(3+1j)
print(z) #(2.4005600000000005+0.79808j)
z = g_couple(3,1)
print(z) #(2.4005600000000005, 0.79808)
"""

#3)

def itereN(x,y):
    z = complex(x,y)
    for i in range (30):
        z=g_complexe(z)
    return(z)
"""
def images_random_pour_comparer_avec_racines_5e(n):
    images=[]
    entrée=[]
    for i in range(n):
        a=random.randint(-10, 10)
        b=random.randint(-10, 10)
        entrée.append(complex(a,b))
        z=itereN(a,b)
        images.append(z)
    for j in range (len(images)):
        print(images[j])
        print(entrée[j])
images_random_pour_comparer_avec_racines_5e(20)
"""

#Parmi les 20 nombres générés aléatoirement,
#seulement 2 n'ont pas convergé : (8-7j) (-2-5j), avec pour sorties (1.42-0.937j) (-1.996+0.88j)

"""
for k in range (5): #Racines 5e de l'unité
    print(itereN(np.cos(2*k*np.pi/5),np.sin(2*k*np.pi/5)))
(1+0j)
(0.30901699437494745+0.9510565162951536j)
(-0.8090169943749476+0.5877852522924731j)
(-0.8090169943749475-0.5877852522924731j)
(0.30901699437494745-0.9510565162951536j)
"""

#4)
def itereN_v2(z):
    if z == (0 + 0j):
        return(0+0j)
    for i in range (30):
        z1=g_complexe(z)
        if np.sqrt((z.real-z1.real)**2 + (z.imag - z1.imag)**2) < 0.02:
            return(z1)
        z = z1
    return(0+0j)


#5)

racine=[np.exp(k*2j*np.pi/5) for k in range (5)] #Crée les racines 5e de l'unité en une valeur

def couleur(x,y):
    zN=itereN_v2(complex(x,y))
    for k in range (5):
        if np.sqrt((zN.real-(np.exp(k*2j*np.pi/5)).real)**2 + (zN.imag-(np.exp(k*2j*np.pi/5)).imag)**2) < 0.1:
            return(k)
    return(5)

#6)

def coloration(xmin,xmax,ymin,ymax,resolution):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    for i in range (resolution):#Chaque ligne #ORDONNEE
        for j in range (resolution):#Chaque colonne #ABSCISSE
            array_matrice[i,j]=couleur(ymin+ecart_y*j,xmin+ecart_x*i)
    end=time.time()
    print('\nDurée de calcul, feuille TD :', end - start)
    return(array_matrice)

#7)
def dessin(xmin,xmax,ymin,ymax,resolution):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    for i in range (resolution):
        for j in range (resolution):#Le pixel ligne max est de la couleur de celui ligne min
            array_matrice[resolution-i-1,j]=couleur(ymin+ecart_y*j,xmin+ecart_x*i)
            #On intervertit les lignes/ordonnées (i) avec resolution-i-1
    end=time.time()
    print('\nDurée de calcul, feuille TD :', end - start)
    return(array_matrice)

"""
A=coloration(-2,2,-2,2,1000)
plt.imshow(A, cmap='nipy_spectral_r')
plt.title("Fractales de Newton")
plt.show()
plt.clf()

A=dessin(-2,2,-2,2,1000)
plt.imshow(A, cmap='nipy_spectral_r')
plt.title("Fractales de Newton")
plt.show()
plt.clf()
"""
#-> ~33 secondes
#On souhaite améliorer ce temps

##Tentatives pour améliorer les performances du programme

##4) bis

#Le test de distance avec la racine est lourd pour les grandes itérations
#Je privilégie un test simpliste mais plus efficace
#Proche en partie im, proche en partie reel

def mon_itereN_1(z,n_iter): #On compare partie réelle et imaginaire séparément
    if z == (0 + 0j):
        return(0+0j)
    for i in range (1,n_iter+1):
        z1=g_complexe(z)
        if (abs(z.real-z1.real)<0.01) and (abs(z.imag - z1.imag) < 0.01):
            return(z1)
        z = z1
    return(0+0j)

def mon_itereN_2(z,n_iter): #On compare le carré du module, sqrt étant une opération 'longue'
    if z == (0 + 0j):
        return(0+0j)
    for i in range (1,n_iter+1):
        z1=g_complexe(z)
        if ((z1.real-z.real)**2 + (z1.imag-z.imag)**2) < 0.0001:
            return(z1)
        z = z1
    return(0+0j)

##5) bis

#Même problème avec l'opération racine

def mon_couleur_1(x,y,n_iter):
    zN=mon_itereN_1(complex(x,y),n_iter)
    for k in range (5):
        if (abs(zN.real-(np.exp(k*2j*np.pi/5)).real)<0.1) and (abs(zN.imag-(np.exp(k*2j*np.pi/5)).imag)<0.1):
            return(k)
    return(5)

def mon_couleur_2(x,y,n_iter):
    zN=mon_itereN_2(complex(x,y),n_iter)
    for k in range (5):
        if ((zN.real-(np.exp(k*2j*np.pi/5)).real)**2 + (zN.imag-(np.exp(k*2j*np.pi/5)).imag)**2) < 0.01:
            return(k)
    return(5)
##6) bis

def mon_dessin_1(xmin,xmax,ymin,ymax,resolution,n_iter):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    print('Construction des valeurs. Chargement...')# Rajoute une "barre" de chargement
    for i in range (resolution):
        if (i % m.floor(resolution/100)) == 0:#
            print(i // m.floor(resolution/100),'%')#
        for j in range (resolution):
            array_matrice[resolution-i-1,j]=mon_couleur_1(ymin+ecart_y*j,xmin+ecart_x*i,n_iter)
    end=time.time()
    print('\nDurée de calcul, v1 :', end - start)
    return(array_matrice)


A=mon_dessin_1(-2,2,-2,2,1000,30)
plt.imshow(A, cmap='nipy_spectral_r')
plt.title("Fractales de Newton, degré 5")
#plt.savefig('Fractales de Newton, degré 5.png', format='png', dpi=1000) #Enregistrement de l'image
plt.show()
plt.clf()

#-> ~14 secondes pour 1000, 346 secondes pour 5000 (image en PJ)
"""
def mon_dessin_2(xmin,xmax,ymin,ymax,resolution,n_iter):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    #print('Construction des valeurs. Chargement...')# Rajoute une "barre" de chargement
    for i in range (resolution):
        #if (i % m.floor(resolution/100)) == 0:#
        #    print(i // m.floor(resolution/100),'%')#
        for j in range (resolution):
            array_matrice[resolution-i-1,j]=mon_couleur_2(ymin+ecart_y*j,xmin+ecart_x*i,n_iter)
    end=time.time()
    print('\nDurée de calcul, v2 :', end - start)
    return(array_matrice)


A=mon_dessin_2(-2,2,-2,2,1000,30)
plt.imshow(A, cmap='nipy_spectral_r')
plt.title("Fractales de Newton")
plt.show()
plt.clf()

#-> ~21 secondes
"""

#Donc la boucle de comparaison des valeurs réelles/imaginaires séparément est plus rapide
#On se place à une définition de 5000, en bicubic, pour obtenir l'image en pièce-jointe

