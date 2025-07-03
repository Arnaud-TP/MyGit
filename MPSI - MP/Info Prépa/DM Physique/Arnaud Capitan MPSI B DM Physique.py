#Arnaud Capitan MPSI B
#Devoir Maison - Physique informatique
#Simulations numériques
#Filtre passe-bas du premier ordre attaqué par un créneau

import cmath as cm
import math as m
import matplotlib.pyplot as plt

##Fonction onde associée, renvoie des listes

global w1
global N_points

w1=5000
N_points = 500 #Nombre de points choisis pour les graphes

"""
## Problème de cette fonction : ne prend pas en compte le changement d'échelle des temps
## Ne dispose pas non plus de suffisamment de points
def ondeassociee_v1(A, phi, f):
    listeTemps=[]
    for k in range (500):
        listeTemps.append(k*2*m.pi/500)
    listeValeurs=[]
    for k in range (500):
        listeValeurs.append(A*m.sin(phi+2*m.pi*f*listeTemps[k]))
    return(listeTemps,listeValeurs)
"""

def echelle(f): #On crée cette fonction afin de changer l'échelle de temps pour l'affichage des courbes
    n=1
    while f > n:
        n*=10
    return(f)

def ondeassociee(A, phi, f):
    listeTemps=[]
    ech=echelle(f)
    for k in range (N_points):
        listeTemps.append((k/ech)*2*m.pi/N_points)
    listeValeurs=[]
    for k in range (N_points):
        listeValeurs.append(A*m.sin(phi+2*m.pi*f*listeTemps[k]))
    return(listeTemps,listeValeurs)


#Vérification de la fonction :

X, Y=ondeassociee(1, 0, 1) #Fonction sinus de période 1s (T=1/f)
plt.plot(X, Y)
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.grid(True)
plt.title("Tracé de la fonction sinus")
plt.show() #On obtient bien la fonction sinus
plt.clf()

##Fonction complexe associée à la tension d'entrée
def complexeassociee(A, phi):
    return(A*cm.exp(phi*1j))

"""
Pour le filtre passe-bas du premier ordre
Je choisis un circuit RC série
H(jw) = 1/1 + jRCw, w1 = 1/RC = 2pi*f1 = 3000 rad/s ici
H(jw) = Us complexe / Ue complexe
-> Us complexe = Ue complexe * H(jw)
-> Amplitude Us = A*|H(jw)| = A/sqrt(1+w²/w1²)
-> Phase = phi - arctan(w/w1)
"""

##Fonction tension de sortie réelle

def TSR(A, phi, f):
    module = abs(complexeassociee(A, phi))*1/m.sqrt(1+(2*m.pi*f/3000)**2)
    phase = phi - m.atan(2*m.pi*f/3000)
    return(module, phase, f)

def TSR_passe_haut(A, phi, f):
    module = abs(complexeassociee(A, phi))*1/m.sqrt(1+1/(2*m.pi*f/3000)**2)
    phase = phi - m.atan(1/(2*m.pi*f/3000))
    return(module, phase, f)


#Vérification de la fonction :

X, Y=ondeassociee(1,0,1) #Fonction sinus de période 1s (T=1/f)
plt.plot(X, Y, color='black', label="Tension d'entrée")
A, phi, f = TSR(1,0,1)
X,Y=ondeassociee(A, phi, f)
plt.plot(X, Y, color='red', label='Tension de sortie')
#Cette fonction devrait rester inchangée car filtre passe-bas
plt.title("Filtre passe-bas basse fréquence")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.grid(True)
plt.show() #On obtient bien la même fonction sinus (superposition)
plt.clf()

X, Y=ondeassociee(1,0,477) #Fonction sinus de pulsation w = w0 environ
plt.plot(X, Y, color='black', label="Tension d'entrée")
A, phi, f=TSR(1,0,477)
X,Y=ondeassociee(A, phi, f)
plt.plot(X, Y, color ='red', label='Tension de sortie') #Cette fonction devrait être déphasée et d'amplitude plus faible
plt.title("Filtre passe-bas basse fréquence")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.grid(True)
plt.show() #On obtient un déphasage et une amplitude réduite
plt.clf()


## Fonction signal carré
#Décomposition du signal carré en série de Fourier :
#x(t) = 4/pi * somme de 0 à l'infini de sin((2k+1)2pift)/(2k+1)
#Le signal est considéré reconstitué à l'identique à partir des 50 premiers termes

def signal_carre():
    f=w1/(2*m.pi) #f = w/2pi
    ech=echelle(f)
    listeTemps=[]
    for k in range (N_points):
        listeTemps.append((k/ech)*2*m.pi/N_points)
    listeValeurs=[]
    for k in range (N_points):
        valeur = 0
        t=listeTemps[k]
        for i in range (50): #Nombre de termes de la décomposition de Fourier
            valeur+= (4/m.pi)*m.sin((2*i+1)*w1*t)/(2*i+1)
        listeValeurs.append(valeur)
    return(listeTemps,listeValeurs)


#Vérification de la fonction d'entrée carrée

X,Y=signal_carre()
plt.plot(X,Y,color='black',label="Tension d'entrée")
plt.title("Signal carrée de pulsation fondamentale w1 = 5000 rad/s")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.grid(True)
plt.show()
plt.clf()

def signal_sortie():
    f=w1/(2*m.pi) #Même échelle que le signal d'entrée
    ech=echelle(f)
    listeTemps=[]
    for k in range (N_points):
        listeTemps.append((k/ech)*2*m.pi/N_points)
    listeValeurs=[]
    for k in range (N_points):
        listeValeurs.append(0)
    for i in range (50):
        liste_provisoire=[]
        A, phi, w = TSR((4/m.pi)/(2*i+1),0,(2*i+1)*w1)
        for k in range (N_points):
            liste_provisoire.append(A*m.sin(phi+w*listeTemps[k]))
        for k in range (N_points):
            listeValeurs[k]+=liste_provisoire[k]
    return(listeTemps,listeValeurs)

X,Y=signal_carre()
plt.plot(X,Y,color='black',label="Tension d'entrée")
X,Y=signal_sortie()
plt.plot(X,Y,color='red',label="Tension de sortie")
plt.title("Signal carrée de pulsation fondamentale w1 = 5000 rad/s")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (V)")
plt.grid(True)
plt.show()
plt.clf()