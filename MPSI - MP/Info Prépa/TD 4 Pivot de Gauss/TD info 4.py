import math as m
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

##
#
# Représentation de solution selon Euler
#
##

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

Temps,Y_images = ResolEuler(intervalleTemps,0,PHI,pointSuivant,h) #Condition initiale : y(0)=0
plt.plot(Temps,Y_images, color='red', label="Tracé de y'=3y + t") #Tracé de y'=3y + t
Temps,Y_images = ResolEuler(intervalleTemps,1,PHIc,pointSuivant,h) #Condition initiale : y(0)=1
plt.plot(Temps,Y_images, color='orange', label="Tracé de y'=cos(t)y")#Tracé de y'=cos(t)y
plt.xlabel("Temps") #Légende de l'axe X
plt.ylabel("Position") #Légende de l'axe Y
plt.plot([-0.5,2*m.pi],[0,0], color='black', label='Repère') #Axe X du repère
plt.plot([0,0],[3.5,-0.2], color='black')#Axe Y du repère

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

##
#
# L'équation du second ordre
#
##

##Constantes
CondInit = [1,0] #Position, vitesse  Conditions initiales
intervalle=[0,3*m.pi] #Intervalle de définition de l'équation différentielle
h=0.001 #Ecart h

## y''= -y'/5 -4y + sin(t)

def PSI(u, t): #Calcul de la vitesse et de l'accélération à partir de l'équation différentielle
    acceleration = -(u[1])/5 -4*(u[0]) + m.sin(t)
    v=[u[1],acceleration]
    return(v) #Vitesse, Accélération


## y''= -4y

def PSI(u, t): #Calcul de la vitesse et de l'accélération à partir de l'équation différentielle
    acceleration = -4*u[0]
    v=[u[1],acceleration]
    return(v) #Vitesse, Accélération


##
#
# D'après la formule d'Euler, si f'(a) = b, f(a+h) = f(a) + hb
# Donc :   Si f''(a) = b, f'(a+h) = f'(a) + hb
##



def PointSui (t,u,PSI,h): #Calcul de la position et de la vitesse à partir de la méthode d'Euler
    vit_acc = PSI(u,t) #On appelle les valeurs f'(a) et f''(a)
    vitesse_suiv = vit_acc[0] + h*vit_acc[1] # Calcul de f'(a+h)
    position_suiv = u[0] + h*u[1] #Calcul de f(a+h)
    t_suivant = t+h #t suivant, incrémentation de h
    u_suivant=[position_suiv, vitesse_suiv]
    return(t_suivant, u_suivant)

def ResolEul(intervalle,CondInit,PSI,PointSui,h):
    t=intervalle[0]
    u=CondInit
    Xpos=[u[0]]
    Yvit=[u[1]]
    Ttemps=[t]
    while (t <= intervalle[1]):
        t, u = PointSui(t,u,PSI,h)
        Xpos.append(u[0]) #Liste des positions
        Yvit.append(u[1]) #Liste des vitesses
        Ttemps.append(t) #Liste des abscisses (instants)
    return(Ttemps,Xpos,Yvit)

T,X,Y = ResolEul(intervalle,CondInit,PSI,PointSui,h)
plt.plot(T,X, color='green', label='Tracé de la position')
plt.plot(T,Y, color='red', label='Tracé de la vitesse')
plt.plot(X,Y, color='blue', label='Portrait de phase')
plt.title("Représentation graphique des courbes")
plt.xlabel("Temps") #Légende de l'axe X
plt.ylabel("Position") #Légende de l'axe Y
plt.plot([-1.5,3*m.pi+0.5],[0,0], color='black', label='Repère') #Axe X du repère
plt.plot([0,0],[3,-3], color='black')#Axe Y du repère
plt.axis('equal') #Repère orthonormé
plt.legend()
plt.show()

