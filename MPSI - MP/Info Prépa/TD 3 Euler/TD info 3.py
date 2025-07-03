import math as m
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt


"""
CondInit=[]
CondInit.append(eval(input("Entrez la position initiale (à l'instant 0) :")))
CondInit.append(eval(input("Entrez la vitesse initiale (à l'instant 0) :")))
h = eval(input('Ecart :'))
intervalle=[]
intervalle.append(eval(input("Borne inférieure de l'intervalle :")))
intervalle.append(eval(input("Borne supérieure de l'intervalle :")))
"""

##Constantes
CondInit = [1,0] #Position, vitesse  Conditions initiales
intervalle=[0,3*m.pi] #Intervalle de définition de l'équation différentielle
h=0.01 #Ecart h

## y''= -y'/5 -4y + sin(t)
def PSI(u, t): #Calcul de la vitesse et de l'accélération à partir de l'équation différentielle
    acceleration = -(u[1])/5 -4*(u[0]) + m.sin(t)
    v=[u[1],acceleration]
    return(v) #Vitesse, Accélération


## y''= -4y
"""
def PSI(u, t): #Calcul de la vitesse et de l'accélération à partir de l'équation différentielle
    acceleration = -4*u[0]
    v=[u[1],acceleration]
    return(v) #Vitesse, Accélération
"""

"""
D'après la formule d'Euler, si f'(a) = b, f(a+h) = f(a) + hb
Donc :   Si f''(a) = b, f'(a+h) = f'(a) + hb
"""

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
#plt.title("...")
#plt.plot(liste1,liste2, color='...', label='...', style = '...', lw = '...')
plt.xlabel("Temps") #Légende de l'axe X
plt.ylabel("Position") #Légende de l'axe Y
plt.plot([-1.5,3*m.pi+0.5],[0,0], color='black', label='Repère') #Axe X du repère
plt.plot([0,0],[3.5,-3.5], color='black')#Axe Y du repère
plt.axis('equal') #Repère orthonormé
plt.legend()
plt.show()




