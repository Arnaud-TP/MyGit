from matplotlib import pyplot as plt
from matplotlib import numpy as np
import cmath
import math as m
import time

##Arnaud Capitan MPSI B

#8 1) et 2), d'autres fonctions et coloration

#Fonction 1 : Degré 10, f_1(z) = z**10 -1   Solutions : S = {racines 10e de l'unité}

def f_1(z): #Itération de Newton associée
    return(z-(z**10-1)/(10*z**9))

def itereN_1(z,n_iter):
    if z == (0 + 0j):
        return(0+0j)
    for i in range (1,n_iter+1):
        z1=f_1(z)
        if (abs(z.real-z1.real)<0.01) and (abs(z.imag - z1.imag) < 0.01):
            return(z1)
        z = z1
    return(0+0j)

def couleur_1(x,y,n_iter):
    zN=itereN_1(complex(x,y),n_iter)
    for k in range (10):
        if (abs(zN.real-(np.exp(k*2j*np.pi/10)).real)<0.1) and (abs(zN.imag-(np.exp(k*2j*np.pi/10)).imag)<0.1):
            return(k)
    return(10)

def dessin_1(xmin,xmax,ymin,ymax,resolution,n_iter):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    print('Construction des valeurs. Chargement...')
    for i in range (resolution):
        if (i % m.floor(resolution/100)) == 0:
            print(i // m.floor(resolution/100),'%')
        for j in range (resolution):
            array_matrice[resolution-i-1,j]=couleur_1(ymin+ecart_y*j,xmin+ecart_x*i,n_iter)
    end=time.time()
    print('\nDurée de calcul :', end - start)
    return(array_matrice)


A=dessin_1(-2,2,-2,2,1000,30)
plt.imshow(A, cmap='nipy_spectral_r')
plt.title("Fonction 1")
plt.colorbar()
#plt.savefig('Fractale de Newton, degré 10.png', format='png', dpi=1000) #Enregistrement de l'image
plt.show()
plt.clf()

#Fonction 2 : Degré 8, f_2(z) = z**8 + z**4 - 2*z**2 + 1
solution=[]#Déterminer par Wolframalpha
solution.append(np.sqrt((1/2)*(-1j-np.sqrt(-1+4j))))
solution.append(-np.sqrt((1/2)*(-1j-np.sqrt(-1+4j))))
solution.append(np.sqrt((1/2)*(1j-np.sqrt(-1+4j))))
solution.append(-np.sqrt((1/2)*(1j-np.sqrt(-1+4j))))
solution.append(np.sqrt((1/2)*(1j+np.sqrt(-1+4j))))
solution.append(-np.sqrt((1/2)*(1j+np.sqrt(-1+4j))))
solution.append(np.sqrt((1/2)*(-1j+np.sqrt(-1+4j))))
solution.append(-np.sqrt((1/2)*(-1j+np.sqrt(-1+4j))))

def f_2(z): #Itération de Newton associée
    return(z-(z**8 + z**4 -2*z**2 + 1)/(8*z**7 + 4*z**3 -4*z))

#On ne supprime pas les valeurs interdites ; étant irrationnelles, on suppose que Python ne tombera
#jamais exactement dessus par le calcul approché (n'étant pas des racines du polynome)

def itereN_2(z,n_iter):
    if z == (0 + 0j):
        return(0+0j)
    for i in range (1,n_iter+1):
        z1=f_2(z)
        if (abs(z.real-z1.real)<0.01) and (abs(z.imag - z1.imag) < 0.01):
            return(z1)
        z = z1
    return(0+0j)

def couleur_2(x,y,n_iter):
    zN=itereN_2(complex(x,y),n_iter)
    for k in range (8):
        if (abs(zN.real-(solution[k]).real)<0.1) and (abs(zN.imag-(solution[k]).imag)<0.1):
            return(k)
    return(8)

def dessin_2(xmin,xmax,ymin,ymax,resolution,n_iter):
    array_matrice=np.zeros((resolution,resolution))
    ecart_x=(xmax-xmin)/resolution
    ecart_y=(ymax-ymin)/resolution
    start=time.time()
    print('Construction des valeurs. Chargement...')
    for i in range (resolution):
        if (i % m.floor(resolution/100)) == 0:
            print(i // m.floor(resolution/100),'%')
        for j in range (resolution):
            array_matrice[resolution-i-1,j]=couleur_2(ymin+ecart_y*j,xmin+ecart_x*i,n_iter)
    end=time.time()
    print('\nDurée de calcul :', end - start)
    return(array_matrice)


B=dessin_2(-0.5,0.5,-0.5,0.5,1000,50)
plt.imshow(B, cmap='jet')
plt.title("Fonction 2")
#plt.savefig('Fractale de Newton, degré 8.png', format='png', dpi=1000) #Enregistrement de l'image
plt.show()
plt.clf()





#Pour le dégradé de couleur, il faudrait créer un cmap avec des alternances couleurs / bandes noires
#Les cmap ne disposent pas de ce genre de dégradé / le créer est trop complexe, de même que pour le zoom