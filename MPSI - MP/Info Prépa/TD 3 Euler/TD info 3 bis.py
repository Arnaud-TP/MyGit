import math as m
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

##Constantes (à modifier pour CI directement dans le traçage des courbes)
CI = 1 #Position en 0
intervalleTemps=[0,2*m.pi] #Intervalle de définition de l'équation différentielle
h=0.001 #Ecart h

##Equation différentielle : y' = 3y + t

def PHI(u,t):
    nombre_dérivé = 3*u + t
    return(nombre_dérivé)

def f(x): #Solution théorique
    image = (1/9)*m.exp(3*x)-(x/3) - (1/9)
    return(image)

##Equation différentielle : y' = cos(t)y

def PHIc(u,t):
    nombre_dérivé = m.cos(t)*u
    return(nombre_dérivé)

def g(x): #Solution théorique
    image = m.exp(m.sin(x))
    return(image)

## Si f'(a) = b, alors f(a+h) = f(a) + hb

def pointSuivant(t,y,PHI,h):
    y_suiv = y + h*PHI(y,t)
    t_suiv = t + h
    return(t_suiv,y_suiv)

def pointSuivantCorrige(t,y,PHI,h):
    t_suiv = t + h #a+h
    y_suiv = y + h*PHI(y,t) #f(a+h)
    dy_suivant = PHI(t, y) # f'(a)
    dy_ah_suivant = PSI(t_suiv, y_suiv) # f'(a+h)
    z = (dy_ah_suivant + dy_suivant)/2 # [f'(a+h)+f'(a)]/2
    y_suiv = y + h*z #On remplace b par h
    return(t_suiv, y_suiv)

def ResolEuler(intervalleTemps,CI,PHI,pointSuivant,h): #On peut appliquer pointSuivantCorrige
    t_suiv=0
    y_suiv=CI
    Temps=[0]
    Y_images=[CI]
    while (t_suiv<=intervalleTemps[1]):
        t_suiv,y_suiv = pointSuivant(t_suiv,y_suiv,PHI,h)
        Temps.append(t_suiv)
        Y_images.append(y_suiv)
    return(Temps,Y_images)

## Tracé des courbes

Temps,Y_images = ResolEuler(intervalleTemps,0,PHI,pointSuivant,h)
plt.plot(Temps,Y_images, color='red', label="Tracé de y'=3y + t") #Tracé de y'=3y + t
Temps,Y_images = ResolEuler(intervalleTemps,1,PHIc,pointSuivant,h)
plt.plot(Temps,Y_images, color='orange', label="Tracé de y'=cos(t)y")#Tracé de y'=cos(t)y
plt.xlabel("Temps") #Légende de l'axe X
plt.ylabel("Position") #Légende de l'axe Y
plt.plot([0,2*m.pi],[0,0], color='black', label='Repère') #Axe X du repère
plt.plot([0,0],[3.5,0], color='black')#Axe Y du repère

#Tracé de la solution théorique de y'=3y + t
X=np.arange(0,2*m.pi,0.01)
Y=[0]*len(X)
for k in range (len(X)):
    Y[k]=f(X[k])
plt.plot(X,Y, color='green', label="Tracé de la solution théorique de y'=3y + t")

#Tracé de la solution théorique de y'=cos(t)*y
X=np.arange(0,2*m.pi,0.01)
Y=[0]*len(X)
for k in range (len(X)):
    Y[k]=g(X[k])
plt.plot(X,Y, color='blue', label="Tracé de la solution théorique de y'=cos(t)*y")
plt.ylim([-0.5, 5]) #On limite l'écran d'affichage

plt.legend()
plt.show()

