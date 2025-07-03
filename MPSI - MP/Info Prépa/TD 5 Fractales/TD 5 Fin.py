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

def dessin_Mandelbrot(xmin,xmax,ymin,ymax,resolution,n_iter,a):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    print('Construction des valeurs. Chargement...')
    for i in range (resolution):
        for j in range (resolution):
            array_matrice[resolution-i-1,j]=itereN_Mandelbrot(ymin+ecart_y*j,xmin+ecart_x*i,n_iter,a)
    array_matrice[0,0]=0 #On fixe la couleur noire
    end=time.time()
    print('\nDurée de calcul :', end - start)
    return(array_matrice)

print('Fonction étudiée : (z²+1)(z-a)')
choix=int(input("Mode 1. Zoom   Mode 2. Génération automatique\n\n"))

if choix == 1:
    print("\n\nPour arrêter le programme à tout moment, fermer le Shell.")
    print("L'affichage se sert d'un bug de plt.pause\n\n")
    a=1.7325
    nombre_iterations=100
    Resolution=500
    taille=1
    x1=-taille
    x2=taille
    y1=0.5656-taille
    y2=0.5656+taille
    n=1
    #plt.savefig('Fractale de Newton, Mandelbrot.png', format='png', dpi=1000) #Enregistrement de l'image
    while n <= 15:
        print('Itération', n)
        n+=1
        A=dessin_Mandelbrot(x1,x2,y1,y2,Resolution,nombre_iterations,a)
        plt.close('all')
        plt.clf()
        plt.imshow(A, cmap='magma')
        plt.title("Fonction (z²+1)(z-a)")
        plt.colorbar()
        plt.ion()
        plt.show(block=False)
        plt.draw()
        plt.pause(0.001)
        x=0.5656 #Point remarquable
        y=0
        x1= y - taille/(n**3)
        x2= y + taille/(n**3)
        y1= x - taille/(n**3)
        y2= x + taille/(n**3)
    plt.close('all')
    plt.clf()
    A=dessin_Mandelbrot(x1,x2,y1,y2,1000,150,a)
    plt.imshow(A, cmap='magma')
    plt.title("Fonction (z²+1)(z-a)")
    plt.colorbar()
    plt.ion()
    plt.show(block=False)
    plt.draw()
    plt.pause(0.001)
    time.sleep(30)

if choix == 2:
    print('\n\nRappel : Fonction étudiée : (z²+1)(z-a)\n')
    a=eval(input("Entrez la valeur de a (un réel) : ")) #Intéressant pour sqrt(3) environ égale à 1,7325
    nombre_iterations=int(input("Nombre d'itérations ? N = "))
    Resolution=int(input("Résolution ? "))
    x=eval(input("Taille du carré de la fenêtre de calcul : "))
    A=dessin_Mandelbrot(-x,x,-x,x,Resolution,nombre_iterations,a)
    plt.imshow(A, cmap='Blues_r')
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.title("Fonction (z²+1)(z-a)")
    plt.colorbar()
    #plt.savefig('Fractale de Newton, Mandelbrot.png', format='png', dpi=1000) #Enregistrement de l'image
    plt.pause(8)
    plt.close('all')
    plt.clf()

else :
    print("Erreur de données, veuillez choisir 1 ou 2.")
