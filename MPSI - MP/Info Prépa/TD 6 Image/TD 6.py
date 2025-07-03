## TD 6 Manipulation d'image
#Arnaud Capitan MPSI B

from matplotlib import pyplot as plt
import numpy as np

plt.close()
original=plt.imread("C:/Users/Arnaud/Desktop/Info/TD 6 Image/lady.png") #A la maison
plt.imshow(original)
plt.title("Image lady.png")
plt.show()
plt.clf()


#Question 1 :

for i in range (472):
    for j in range (720):
        if ((i - 218)**2 + (j - 330)**2) < 36: #Equation de cercle
            original[j,i]=(0.267, 0.176, 0.0667, 1) #Couleur d'un pixel marron

plt.imshow(original)
plt.title("Image lady.png avec tâche sur la joue")
plt.show()
plt.clf()

#Question 2 :

original=plt.imread("C:/Users/Arnaud/Desktop/Info/TD 6 Image/lady.png") #A la maison

print("Lignes, colonnes, profondeur :")
print(np.shape(original)) #Lignes, colonnes, hauteur
lignes, colonnes, hauteur = np.shape(original)
while (lignes % 4) != 0:
    lignes += -1
while (colonnes % 4) != 0:
    colonnes += -1
original2=original[0:lignes,0:colonnes]
print("Lignes, colonnes :")
print(lignes, colonnes)
plt.imshow(original2)
plt.title("Image redimensionnée")
plt.show()
plt.clf()

#Question 3 :

#a]

tableauB=np.zeros((lignes//2,colonnes//2,hauteur))
for i in range (lignes):
    for j in range (colonnes):
        if ((j%2) == 0) and ((i%2) == 0):
            tableauB[i//2,j//2]=original2[i,j]
plt.imshow(tableauB)
plt.title("Image réduite")
plt.show()

#Notre oeil ne fait pas vraiment la différence, en y faisant attention on le remarque mais
#cela ne change que peu l'aspect de l'image à l'oeil nu

#b] c] d] e]

def redim(image): #Redimensionne l'image pour que les col/lignes soient multiples de 4
    lignes, colonnes, hauteur = np.shape(image)
    while (lignes % 4) != 0:
        lignes += -1
    while (colonnes % 4) != 0:
        colonnes += -1
    image2=image[0:lignes,0:colonnes]
    return(image2)

def dedouble(image,redim_fonction):
    image=redim_fonction(image)
    lignes, colonnes, hauteur = np.shape(image)
    tableau=np.zeros((lignes,colonnes,hauteur))
    for i in range(lignes):
        for j in range (colonnes):
            if (i%2 == 0) and (j%2 == 0):
                tableau[i//2,j//2]=image[i,j]
            if (i%2 != 0) and (j%2 == 0):
                tableau[lignes//2 + i//2,j//2]=image[i,j]
            if (i%2 == 0) and (j%2 != 0):
                tableau[i//2,colonnes//2 + j//2]=image[i,j]
            if (i%2 != 0) and (j%2 != 0):
                tableau[lignes//2 + i//2,colonnes//2 + j//2]=image[i,j]
    return(tableau)

#f]
def redim_puissance_de_2(image): #Redimensionne l'image pour que les col/lignes soient multiples de 4
    lignes, colonnes, hauteur = np.shape(image)
    if lignes < colonnes :
        dimension = lignes
    else :
        dimension=colonnes
    n=1 #Compteur
    condition = True
    while(condition==True):
        if dimension - 2**n < 0:
            condition=False
            dimension = 2**(n-1)
        n+=1
    image2=image[lignes//2 - dimension//2:lignes//2 + dimension//2,colonnes//2 - dimension//2:colonnes//2 + dimension//2]
    return(image2)

tableauA=dedouble(original,redim)
plt.imshow(tableauA)
plt.title("lady.png dédoublée")
plt.pause(1)
plt.clf()
for i in range (6):
    plt.clf()
    plt.title("lady.png")
    tableauA=dedouble(tableauA,redim)
    plt.imshow(tableauA)
    plt.pause(1)

plt.clf()
tableauA=dedouble(original,redim_puissance_de_2)
print("Lignes, colonnes, profondeur :")
print(np.shape(tableauA)) #Lignes, colonnes, hauteur
plt.imshow(tableauA)
plt.pause(1)
plt.clf()
for i in range (16):
    plt.clf()
    tableauA=dedouble(tableauA,redim_puissance_de_2)
    plt.imshow(tableauA)
    plt.title("lady.png, cyclique")
    plt.pause(1)
plt.close()
plt.clf()

#Pour une dimension de 2**8, on retrouve l'image initiale après 8 itérations
#En effet les permutations sont 'cycliques'
#Il existe k entier naturel non nul tel que s°s°s°...°s = Id


##Exercice 3

k=5
A=np.arange(0,2**k,1)

def echange(A,prem,deuz):
    A[prem],A[deuz] = A[deuz],A[prem]

def puissance_2(N):
    k=0
    while (N!=1):
        N=N//2
        k+=1
    return(k)


def dedoubleInplace(A): #Fonction uniquement pour A unidimensionnel
    n=puissance_2(len(A))
    for i in range(n-1):
        for ligneI in range (2**i,len(A),2**(i+2)):
            for j in range (2**i):
                echange(A,ligneI+j,ligneI + 2**i + j)

def redimension(n):
    a=1
    b=0
    while (True):
        if not (a<=n):
            return(2**(b-1))
        a*=2
        b+=1

def recoupe(image): #Redimensionne l'image pour que les col/lignes soient 2^k
    lignes, colonnes, hauteur = np.shape(image)
    if redimension(lignes) > redimension(colonnes) :
        image=image[0:redimension(colonnes),0:redimension(colonnes)]
    else :
        image=image[0:redimension(lignes),0:redimension(lignes)]
    return(image)

"""
Rappel :
B1 = image[2] place en B1 la ligne 2 de l'image (3e ligne)
B2 = image[ :,1] place en B2 la colonne 1 de l'image (2e colonne)
"""

##Problème de fonction : devrait fonctionner en théorie

def echange_image(image,orig,dest): #image désigne un tableau
    Ligne_1=image[orig].copy()
    image[orig]=image[dest]
    image[dest]=Ligne_1
    for i in range(len(image)):
        sauv = image[i,orig]
        image[i,orig] = image[i,dest]
        image[i,dest] = sauv

def dedoubleInplace_image(image):
    image=recoupe(image)
    N=puissance_2(len(image))
    print(np.shape(image))
    print(image[0,1])
    for i in range(N-1):
        for ligneI in range (2**i,len(A),2**(i+2)):
            for j in range (2**i):
                echange_image(A,ligneI+j,ligneI + 2**i + j)

original=plt.imread("C:/Users/Arnaud/Desktop/Info/TD 6 Image/lady.png") #A la maison
#Cout en 0(n*ln(n)) par parcours successif des entiers 0 <= i <= n de l'image de taille n*n