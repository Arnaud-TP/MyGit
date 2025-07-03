## Autour de la dynamique gravitationnelle

import matplotlib.pyplot as plt
import math as m

## I Quelques fonctions utilitaires

#I.A.1)

assert [1, 2, 3] + [4, 5, 6] == [1, 2, 3, 4, 5, 6]

#I.A.2)

assert 2 * [1, 2, 3] == [1, 2, 3, 1, 2, 3]

#I.B.

def smul(a,L):
    Rep=[]
    for i in range (len(L)):
        Rep.append(L[i]*a)
    return(Rep)

#I.C.

#I.C.1.

def vsom(L1,L2):
    Rep=[]
    for i in range (len(L1)):
        Rep.append(L1[i]+L2[i])
    return(Rep)

#I.C.2.

def vdif(L1,L2):
    Rep=[]
    for i in range (len(L1)):
        Rep.append(L1[i]-L2[i])
    return(Rep)

## II Etude de schémas numériques

#II.B.2)

def euler(y0,z0,tm,tM,n,f): #Toutes les conditions initiales, et f la fonction
    h = (tM-tm)/(n-1) #Calcul de l'écart h
    Ly = [y0] #On initialise la liste à sa première valeur (condition initiale)
    Lz=[z0]
    for i in range (n-1):
        y_suivant = Ly[-1] + Lz[-1]*h #D'après le système S
        Lz.append(Lz[-1]+f(Ly[-1])*h)  #D'après le système S
        Ly.append(y_suivant)
    return(Ly,Lz)

def fonction_test(x,w=2*m.pi):
    return(-x*w**2)

X,Y = euler(3,0,0,3,100,fonction_test)
plt.plot(X,Y, marker='.', linewidth = 0.5, color='black', label='Euler')

def verlet(y0,z0,tm,tM,n,f):
    h = (tM-tm)/(n-1)
    Ly = [y0]
    Lz=[z0]
    for i in range (n-1):
        y_suivant = Ly[-1] + Lz[-1]*h + f(Ly[-1])*(h**2)/2 #Par définition de Verlet
        Lz.append(Lz[-1]+(f(y_suivant)+f(Ly[-1]))*h/2) #Approximation de l'intégrale par trapèze (Verlet)
        Ly.append(y_suivant)
    return(Ly,Lz)

X,Y = verlet(3,0,0,3,100,fonction_test)
plt.plot(X,Y, marker='.', linewidth = 0.5, color='red',label='Verlet')

plt.legend() #Affichage des courbes
plt.pause(3)
plt.clf()
plt.close()

global G
G = 6.67*(10**(-11))

## Problème à N corps

#III.A.2)

def norme(L):
    d=0
    for element in L:
        d += element**2
    return(m.sqrt(d))

def force2(m1,m2,p1,p2):
    distance_cube = (norme(vdif(p2,p1)))**3 #Distance r**3
    Norme_force = G*m1*m2/distance_cube #D'après la formule donnée
    return(smul(Norme_force,vdif(p2,p1))) #On multiplie ensuite le vecteur

#III.A.3)

def forceN(j,m,pos): #j est l'indice du corps, m la liste des masses de tous les corps, pos celle des positions
    Force_totale = [0,0,0]
    for i in range(len(m)):
        if i != j:
            Force_totale = vsom(Force_totale,force2(m[j],m[i],pos[j],pos[i]))
    return(Force_totale)

#III.B.1)

#position[i] renvoie la liste des coordonnées des positions de tous les astres à l'instant i
#vitsse[i] renvoie la même liste mais pour les vitesses

#III.B.2)

#D'après le schéma de Verlet : y_i+1 = y_i + h*z_i + h²/2 fi et fi = Somme des forces (forceN) / m astre (PFD)

def pos_suiv(m, pos, vit, h):
    L_pos=[]
    for i in range (len(m)):
        y_suiv = vsom(pos[i],smul(h,vit[i])) #Première partie :  y_i+1 = y_i + h*z_i
        fi = smul(1/m[i],forceN(i,m,pos))
        y_suiv = vsom(y_suiv,smul((h**2)/2,fi)) #Deuxième partie : + h²/2 fi
        L_pos.append(y_suiv)
    return(L_pos)

#III.B.3)

#D'après le schéma de Verlet : z_i+1 = z_i + (h/2)*(f_i+1)

def etat_suiv(m, pos, vit, h):
    position_suiv = pos_suiv(m, pos, vit, h)
    L_vit=[]
    for i in range (len(m)):
        fi_suiv = smul(1/m[i],forceN(i,m,position_suiv))
        fi = smul(1/m[i],forceN(i,m,pos))
        vit_suiv = vsom(vit[i],smul(h/2,vsom(fi,fi_suiv)))
        L_vit.append(vit_suiv)
    return(position_suiv,L_vit)

#III.B.4)

"""
a] Relation graphique :     1 ln(N) <-> 2 ln(tau)

b] On peut émettre l'hypothèse que la complexité est en N², le carré du temps étant proportionnel à N
"""

#III.B.5)

"""
a] On estime pour etat_suiv la complexité :
pos_suiv a une complexité en :
    N fois une boucle contenant :
        vsom de listes de 3 éléments ( O(1) )
        smul d'un scalaire et de forceN
            forceN d'une complexité en O(N)

pos_suiv d'une complexité en O(N²)

etat_suiv est d'une complexité de l'ordre de
    O(N²) pour pos_suiv
    N fois une boucle contenant :
        forceN 2 fois, avec v_som et smul sur des listes de taille N ( O(N), complexité maximale de la boucle)

-> Donc etat_suiv est de complexité en O(N²)

b] Cohérent avec le résultat
"""


##IV.C) Simulation

"""
"1" "soleil" "2.0e+30"
"2" "terre" "5.9742e+24"
"3" "mercure" "3.3022e+23" Masses en kg

"astre" "date_m" x      y       z       vx      vy      vz
1       1       0.0     0.0     0.0     0.0     0.0     0.0
2       1       1.0167  0.0     0.0     0.0     29.79   0.0
3       1       0.4667  0.0     0.0     0.0     47.89   0.0

1 u.a = 1,5 * 10^11 m
Distances en u.a, vitesses en km/s
On convertit les distances en m/s et les vitesses en m/s
"""

##Variables et constantes

def conversion(a,L): #Pour convertir des listes de positions / vitesses
    L_rep = []
    for i in range (len(L)):
        L_rep.append(smul(a, L[i]))
    return(L_rep)

#Ordres des astres : Soleil, Terre, Mercure,

global ua
ua = 1.5e+11
global masse
masse = [2.0e+30, 5.9742e+24, 3.3022e+23]
global p0
p0 = [[0.0, 0.0, 0.0], [1.0167,0.0,0.0], [0.4667, 0.0, 0.0]]
p0 = conversion(ua, p0) #On convertit les grandeurs en unité du système international
global v0
v0 = [[0.0, 0.0, 0.0], [0.0,29.79,0.0], [0.0, 47.89, 0.0]]
v0 = conversion(1000, v0)
global t0
t0 = 0 #Ici ne sert pas, on ne fait pas de requête SQL -> On prend pour date t0 = 0

"""
Note :

La fonction ci-dessous calcule la liste de toutes les positions de tous les astres à partir des conditions
initiales indiquées ci-dessus, mais pour la simulation en représentation 2D (pas de changement de coordonnées
selon l'axe z) on indique des nouvelles variables / listes nommées x_pos et y_pos
"""

def simulation_verlet(deltat,n): #Incrément de temps en seconde deltat, nombre d'itérations n
    L_pos = [conversion(1/ua,p0)]
    pos = p0
    vit = v0
    for i in range (n):
        pos, vit = etat_suiv(masse, pos, vit, deltat)
        L_pos.append(conversion(1/ua,pos))
    return(L_pos)

L = simulation_verlet(10000,10000)
x1,y1 = [],[] #Soleil, on peut mettre ses cooordonnées à [0,0] -> Poids grand devant les autres
x2,y2 = [],[] #Terre
x3,y3 = [],[] #Mercure
for i in range (len(L)):
    x1.append(L[i][0][0])
    y1.append(L[i][0][1])
    x2.append(L[i][1][0])
    y2.append(L[i][1][1])
    x3.append(L[i][2][0])
    y3.append(L[i][2][1])

plt.plot(x1,y1, color='red', label='Soleil', marker='.', linewidth = 0.1)
plt.plot(x2,y2,color='blue',label='Terre', marker=',', linewidth = 0.1)
plt.plot(x3,y3, color='black', label='Mercure', marker=',', linewidth = 0.1)
plt.title("Simulation Verlet du Système Solaire (Soleil Mercure Terre)")
plt.legend()
plt.show()









