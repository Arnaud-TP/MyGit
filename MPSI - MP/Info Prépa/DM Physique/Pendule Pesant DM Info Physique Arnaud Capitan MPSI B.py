#Arnaud Capitan MPSI B

##### Simulation numérique : pendule pesant #####

#Equation différentielle à résoudre : d²x/dt² + 4*sin(x)=0
#On prend pour conditions initiales v0 = 0 rad/s, x0 = 0.4 radian

#Pour la fonction sinus, il est nécessaire d'importer le module math de Python
#Pour tracer les courbes, il est nécessaire d'avoir le module matplotlib.Pytplot

import math as m
import matplotlib.pyplot as plt
import time #Pour tracer les graphes successivement avec la commande time.sleep(temps)

## Question 1 :
"""
Montrer analytiquement que dans le cas des angles faibles, la période T de ce pendule
est indépendante de l'angle initial. Calculer la valeur de T exprimée en secondes.
On dit qu'il y a isochronisme des oscillations.
"""

"""
Réponse :

Dans le cas des angles faibles, sin(x) ~ x
Ainsi l'équation différentielle à résoudre devient d²x/dt² + 4x=0
On obtient une EDL du 2nd ordre à coefficients constants.
Equation caractéristique : r² + 4 = 0
delta = -16 < 0
r1 = 2i, r2 = -2i => w = 2

=> x(t) = A*cos(wt) + B*sin(wt) avec w = 2 et A,B des constantes d'intégration réelles
dx/dt= -A*w*sin(wt) + B*w*cos(wt)
On détermine les constantes d'intégration à partir des conditions initiales
A t = 0:
dx/dt = 0 => B = 0 => x(t) = A*cos(wt)
x = 0.4  => A = x0 = 0.4

x(t) = x0*cos(wt) = 0.4*cos(2t)

Période : T = 2*pi/w = 2*pi/2 = pi  Résultat indépendant de x0
          T = 3.14 s
"""

## Question 2 :
"""
Résoudre l'équation différentielle non linéarisée, à l'aide d'un script Python, par la méthode d'Euler.
On choisira une durée maximum de 40 secondes, un nombre de points de 600.
On construira 3 listes de même taille : une liste des dates t, une liste des
positions angulaires x et une liste des vitesses angulaires dx/dt.
"""

"""
Réponse :

J'utilise la notation d²x/dt²|x0, dx/dt|x0 et x|x0 pour décrire l'accélération, la vitesse
et l'angle en x0

D'après la formule d'Euler,
Si f'(a) = b, f(a+h) = f(a) + hb
Si f''(a) = b, f'(a+h) = f'(a) + hb

On commence par déterminer x|x0 + h = x0 + h * dx/dt|x0 par la formule d'Euler

On connaît le x suivant

En tout point, on a d²x/dt² l'accélération donnée par l'équation différentielle :
d²x/dt² = -4*sin(x) => Si on connaît x, on connaît d²x/dt²
=> Par condition initiale, on connaît x0 donc d²x/dt²|x0
=> En connaissant x suivant, on connaît d²x/dt² suivant

D'après la formule d'Euler, si on connaît d²x/dt²|x0 et dx/dt|x0 (conditions initiales),
dx/dt|(x0+h) = dx/dt|x0 + h*d²x/dt²|x0

On connaît le dx/dt suivant

Ainsi, par la méthode d'Euler et à partir de l'équation différentielle,
Si on connaît les conditions initiales (dx/dt|x0 et x|x0), on peut déterminer l'allure
complète de la courbe solution de l'équation différentielle.

On procède en trois temps :
Une première fonction accélération avec l'équation différentielle, pour déterminer l'accélération
Une deuxième fonction point_suivant qui renvoie la vitesse et la position en a+h
avec pour paramètres l'accélération, la vitesse et la position en a
Une troisième fonction qui calcule les temps, les positions et les vitesses dans des listes

On a une durée d'acquisition de 40 secondes max, avec 600 points
h = 40/600 = 1/15 (en commençant à t=0, on s'arrête à t = 40 - 1/15 pour conserver les 600 points)
intervalle_temps = [0,40], on fera une boucle tant que t < tf
"""

def acceleration(x):
    return(-4*m.sin(x))

def point_suivant(pos_a,vit_a,acc_a,h): #Paramètres : Position, vitesse et accélération en a
    pos_ah = pos_a + h*vit_a #Formule d'Euler, pos_ah désigne la position en a+h
    vit_ah = vit_a + h*acc_a #Formule d'Euler appliquée sur la vitesse
    return(pos_ah,vit_ah)

"""
On peut définir une fonction point_suivant plus précise en modifiant l'approximation d'Euler
on rajoute le terme d'accélération en h²/2
On a f(a+h) = f(a) + h*f'(a) + h²/2 * f''(a) d'après la formule de Taylor
"""

def point_suivant2(pos_a,vit_a,acc_a,h):
    pos_ah = pos_a + h*vit_a + (h*h/2)*acc_a #L'approximation d'Euler néglige les autres termes
    vit_ah = vit_a + h*acc_a
    return(pos_ah,vit_ah)


# x0 et vit_x0 correspondent aux conditions initiales, et fonction correspond à point_suivant 1 et 2
#Vous pourrez mettre point_suivant2 en paramètres pour avoir une meilleure approximation
def Resolution_Euler(x0, vit_x0, intervalle_temps, N_points, fonction):
    t = intervalle_temps[0] #Borne de temps inférieure, on commence à t0
    tf = intervalle_temps[1] #Borne de temps supérieure
    h = (intervalle_temps[1] - intervalle_temps[0])/N_points
    pos = x0
    vit = vit_x0
    acc = acceleration(x0)
    Liste_temps=[]
    Liste_pos=[]
    Liste_vit=[]
    while(t < tf): #Condition de fin
        Liste_temps.append(t)
        Liste_pos.append(pos)
        Liste_vit.append(vit)
        pos,vit = fonction(pos,vit,acc,h) #On calcule la position et la vitesse suivante
        acc = acceleration(pos) #On calcule l'accélération suivante, en on recommence
        t += h
    return(Liste_temps,Liste_pos,Liste_vit)

## Question 3 :
"""
Tracer la courbe donnant l'angle x en fonction du temps t
"""

"""
On remarque qu'avec 600 points, la position diverge vers +infini, et avec 400 points vers -infini.
Toutefois, en augmentant le nombre de points (N=6000 par exemple) on observe toujours
cette légère divergence, causée par l'approximation d'Euler.
En traçant le portrait de phase (voir ci-dessous), on remarque la différence entre 600 points
et 6000 points : la vitesse diverge plus rapidement pour un nombre faible de points

En traçant l'accélération en fonction du temps et en superposant cette courbe avec celle de
la position, on remarque que lorsque la position atteint un point critique (elle diverge lentement
à cause de l'approximation d'Euler) qui est x > pi/2 ou x < -pi/2, l'accélération donnée
par l'équation différentielle d²x/dt² = -4*sin(x) change de variation, modifiant
ainsi la vitesse et donc la position, d'où le résultat.

En augmentant le nombre de points, on réduit l'écart h donc l'erreur de l'approximation
de Gauss, ce qui limite la divergence de la position observée pour 600 points
"""


def affiche_courbes(fonction):
    Temps,Pos,Vit=Resolution_Euler(0.4, 0, [0,40], 600, fonction) #Courbe de x(t) pour 600 points
    plt.plot(Temps,Pos, color='red', label='Trace de la courbe x(t) avec 600 points')
    Temps,Pos,Vit=Resolution_Euler(0.4, 0, [0,40], 6000, fonction) #Courbe de x(t) pour 6000 points
    plt.plot(Temps,Pos, color='blue', label='Trace de la courbe x(t) avec 6000 points')
    Temps,Pos,Vit=Resolution_Euler(0.4, 0, [0,40], 600, fonction) #Portrait de phase pour 600 points
    plt.plot(Pos,Vit, color='red',marker=',', lw=0.5, label='Trace du portrait de phase pour 600 points')
    Temps,Pos,Vit=Resolution_Euler(0.4, 0, [0,40], 6000, fonction) #Portrait de phase pour 6000 points
    plt.plot(Pos,Vit, color='blue', marker=',', lw=0.5, label='Trace du portrait de phase pour 6000 points')
    plt.axis()
    plt.xlabel("Temps")
    plt.ylabel("Position angulaire")
    plt.legend()
    plt.show()

## Affichage des courbes solutions de l'équation du pendule pesant (supprimer l'un des #)
#affiche_courbes(point_suivant)
#affiche_courbes(point_suivant2) #Meilleure approximation avec la formule de Taylorpour compléter Euler

## Question 4 :
"""
Définir une fonction Euler(x0) qui renvoie la valeur de la période T du pendule en
fonction de l'angle initial x0, toujours dans le cas d'une vitesse initiale nulle.
On définira une liste d'une dizaine d'angles x0 allant de 0 à pi/2 et on
construira la liste des périodes T associées à chacun des angles initiaux.
"""

"""
Première condition : On a un extremum de position
Deuxième condition : Cet extremum est un maximum
On a ainsi les temps de deux maximum successifs, leur différence sera la période recherchée.

On prend 6000 points pourune meilleur précision
"""
#6000 points pour plus de précision
#Il est possible de modifier le nombre de points et la fonction utilisée point_suivant 1 ou 2
def Euler(x0):
    Temps,Pos,Vit=Resolution_Euler(x0, 0, [0,40], 6000, point_suivant)
    Mesure_1=False #La première mesure n'a pas été effectuée
    for i in range(len(Temps)-1):
        if Vit[i]*Vit[i+1]<0 and Vit[i]>0:
            if Mesure_1 == True: #Si la mesure 1 a déjà été effectuée
                return(Temps[i]-t1) #On renvoie la différence de temps
            t1 = Temps[i] #Sinon on mesure le premier temps
            Mesure_1 = True #On change la valeur de Mesure_1 à True : la mesure est faite

Liste_angles=[]
Liste_périodes=[]
for i in range (1,11): #1 <= i <= 10, x0=0 ne représente pas le mouvement
    Liste_angles.append(i*(m.pi/2)/10)
for i in range (10):
    Liste_périodes.append(Euler(Liste_angles[i]))




## Question 5 :
"""
Enfin, on tracera la courbe T(x0), qui donne la période en fonction de l'angle initial.
"""

def courbe_periode():
    plt.plot(Liste_angles, Liste_périodes)
    plt.plot([0,0],[0,0]) #Pour avoir l'origine
    plt.title("Période en fonction de l'angle initial")
    plt.axis()
    plt.xlabel("Angle initial (rad)")
    plt.ylabel("Période des oscillations")
    plt.show()

##Affichage de la courbe représentant la période en fonction de l'angle x0 (supprimer le #)
#courbe_periode() #Pour l'affichage de la courbe représentant la période en fonction de l'angle x0

