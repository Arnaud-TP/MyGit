from matplotlib import pyplot as plt
from matplotlib import numpy as np
import cmath
import math as m
import time

##Arnaud Capitan MPSI B

##Objectif : Mandelbrot, avec une coloration en fonction de la convergence (et non la racine), zoom

#Fonction : (z²+1)(z-a) semble être une fonction satisfaisant la condition Mandelbrot (trouvée en ligne)
#Solutions : S={a, i, -i}

def f_Mandelbrot(z,a): #Itération de Newton associée
    if (3*z**2 -2*a*z+1) == 0:
        return(0)
    return(z-(z**3-a*z**2+z-a)/(3*z**2 -2*a*z+1))

def itereN_Mandelbrot(x,y,n_iter,a):
    z=complex(x,y)
    for i in range (1,n_iter+1):
        z1=f_Mandelbrot(z,a)
        if (abs(z.real-z1.real)<0.01) and (abs(z.imag - z1.imag) < 0.01):
            return(i)
        z = z1
    return(0)

def dessin_Mandelbrot(xmin,xmax,ymin,ymax,resolution,n_iter,a,valeurs_remarquables):
    valeurs_remarquables=[]
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    MAX=0
    print('Construction des valeurs. Chargement...')
    for i in range (resolution):
        if (i % m.floor(resolution/100)) == 0:
            print(i // m.floor(resolution/100),'%')
        for j in range (resolution):
            array_matrice[resolution-i-1,j]=itereN_Mandelbrot(ymin+ecart_y*j,xmin+ecart_x*i,n_iter,a)
            if array_matrice[resolution-i-1,j] > MAX :
                MAX = array_matrice[resolution-i-1,j]
                valeurs_remarquables.append(ymin+ecart_y*j)#Avant_dernier : x
                valeurs_remarquables.append(xmin+ecart_x*i)#Dernier : y
    array_matrice[0,0]=0 #On fixe la couleur noire
    end=time.time()
    print('\nDurée de calcul :', end - start)
    return(array_matrice,valeurs_remarquables)

print('Fonction étudiée : (z²+1)(z-a)')
choix=int(input("Mode 1. Zoom   Mode 2. Génération automatique"))
if choix == 1:
    a=1,7325
    nombre_iterations=50
    Resolution=500
    taille=1
    valeurs_remarquables=[]
    x1=-taille
    x2=taille
    y1=-taille
    y2=taille
    n=1
    #plt.savefig('Fractale de Newton, Mandelbrot.png', format='png', dpi=1000) #Enregistrement de l'image
    while n <= 20:
        n+=1
        A,valeurs_remarquables=dessin_Mandelbrot(x1,x2,y1,y2,Resolution,nombre_iterations,a,valeurs_remarquables)
        plt.close('all')
        plt.clf()
        plt.imshow(A, cmap='magma')
        plt.title("Fonction (z²+1)(z-a)")
        plt.colorbar()
        plt.ion()
        plt.show(block=False)
        plt.draw()
        plt.pause(0.001)
        #x=valeurs_remarquables[-2] Zoom "évolutif" dépend de la nouvelle itération
        #y=valeurs_remarquables[-1]
        #print('x=', y, 'y=', x)
        x=0.577649711
        y=0
        x1= y - taille/(n*n)
        x2= y + taille/(n*n)
        y1= x - taille/(n*n)
        y2= x + taille/(n*n)
    plt.close('all')
    plt.clf()
    plt.imshow(A, cmap='magma')
    plt.show()


if choix == 2:
    a=eval(input("Entrez la valeur de a (un réel) : ")) #Intéressant pour sqrt(3) environ égale à 1,7325
    nombre_iterations=int(input("Nombre d'itérations ? N = "))
    Resolution=int(input("Résolution ? "))
    taille=eval(input("Taille du carré de la fenêtre de calcul : "))
    valeurs_remarquables=[]
    x1=-taille
    x2=taille
    y1=-taille
    A,valeurs_remarquables=dessin_Mandelbrot(x1,x2,y1,y2,Resolution,nombre_iterations,a,valeurs_remarquables)
    plt.imshow(A, cmap='magma')
    plt.title("Fonction (z²+1)(z-a)")
    plt.colorbar()
    #plt.savefig('Fractale de Newton, Mandelbrot.png', format='png', dpi=1000) #Enregistrement de l'image
    plt.show()
    plt.close('all')
    plt.clf()

else :
    print("Erreur de données, veuillez choisir 1 ou 2.")
