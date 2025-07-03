# Arnaud Capitan MPSI B
# DM 3 Physique : Force Centrales

import matplotlib.pyplot as plt

## Sujet : Simulation numérique : mouvement dans un champ de forces centrales

"""
On se propose de résoudre numériquement l’équation différentielle du mouvement
d’un point matériel sous l’action d’une force F=-k/r²

On montre que la trajectoire est plane.
 * Pour -k > 0, la force est répulsive et on doit obtenir une trajectoire correspondant à
une branche répulsive d’hyperbole.
 * Pour -k = 0, il n’y pas de force et la trajectoire est une droite.
 * Pour -k < 0, la force est attractive et on s’attend à avoir une ellipse, une parabole ou
une branche attractive d’hyperbole selon la valeur de k

On se placera en coordonnées cartésiennes.
Par projection du principe fondamental de la dynamique, montrer que le système
d’équations différentielles à résoudre est alors :
m d²x/dt² = -k*x/((x²+y²)**(3/2))
m d²y/dt² = -k*y/((x²+y²)**(3/2))

On va travailler en coordonnées adimensionnées, donc on prendra m = 1.
Le centre de force est placé à l’origine du repère en (0 ;0).
"""

## Partie 1 : Mise en équation

"""
Système { Point matériel de masse m }
Etude dans un référentiel supposé galiléen
Bilan des forces :   ->           ->
    | Force centrale F  = -k/r² . er
                                                                 ->                        ->   ->     ->
r désignant la distance du point matériel au centre de force, et er le vecteur unitaire de er = OM / ||OM||
On nomme O le centre de force de la force centrale en F=-k/r² (qui sera aussi notre origine O(0;0) )
M est le point repérant la position du point matériel de masse m               ->       ->       ->
M de coordonnées M(x;y) (mouvement plan dans le cas d'une force centrale) d'où OM = x . ex + y . ey
(ex et ey sont les vecteurs unitaires de la base cartésienne)

D'après le principe fondamental de la dynamique,
    ->               ->     ->            ->
m d²OM/dt² = -k/r² * OM / ||OM||    Or, ||OM|| = r = (x² + y²)**(1/2)
       ->     ->                   ->     ->
m d²(x.ex + y.ey)/dt² = -k/r² * (x.ex + y.ey) / r

                         ->    ->
On projette sur les axes ex et ey :
    | m d²x/dt² = -k/r**3 * x
    | m d²y/dt² = -k/r**3 * y
Ce qui nous donne enfin, sachant r = (x² + y²)**(1/2) :
    | m d²x/dt² = -k*x / ((x²+y²)**(3/2))
    | m d²y/dt² = -k*y / ((x²+y²)**(3/2))

En travaillant en coordonnées adimensionnées, m = 1 kg, d'où le système d'équation :
    | d²x/dt² = -k*x / ((x²+y²)**(3/2))
    | d²y/dt² = -k*y / ((x²+y²)**(3/2))
"""

## Partie 2 : Simulation

"""
On testera plusieurs forces, par k = -1 ; k=0 ; k = 0.3 ; k =0.5 ; k =1 et k =2.
k=-1 doit conduire à une hyperbole répulsive.
k=0 doit conduire à une droite.
k= 0.3 doit conduire à une hyperbole attractive.
k=0.5 doit conduire à une parabole.
k= 1 doit conduire à un cercle.
k=2 doit conduire à une ellipse.

On choisira comme conditions initiales sur la position ( x 0 =1 ; y 0 =0) et sur la vitesse
(v x0 =0 ; v y0 =1)
"""

#Système d'équation couplé pour m = 1 kg

def equa_diff(x,y,k): #Arguments : k et les coordonnées x et y à un instant t
    d2x = -k*x/((x**2+y**2)**(3/2))
    d2y = -k*y/((x**2+y**2)**(3/2))
    return (d2x,d2y)

#Approximation d'Euler de la trajectoire, x(t+h) = x(t) + h*x'(t) + h²/2 * x''(t) pour la position
# x'(t+h) = x'(t) + h*x''(t) pour la vitesse    x_th désigne la coordonnées x au temps t+h
# h désigne l'écart de temps entre chaque point successif

def approx_euler(h,x,y,dx,dy,k): #Arguments : k, h, les coordonnées x, y, dx/dt et dy/dt à un instant t
    d2x,d2y = equa_diff(x,y,k)
    x_th = x + h*dx + ((h**2)/2) * d2x
    y_th = y + h*dy + ((h**2)/2) * d2y
    dx_th = dx + h*d2x
    dy_th = dy + h*d2y
    return(x_th,y_th,dx_th,dy_th)

def Euler(N,T,x0,y0,vx0,vy0,k): #N points, durée T de la simulation
    X=[x0]
    Y=[y0]
    VX=[vx0]
    VY=[vy0]
    Temps = [0]
    h = T/N
    for i in range (1,N): #Le temps t=0 correspond aux conditions initiales, on commence directement à t=h
        Temps.append(h*i) #Inutile
        x_th,y_th,dx_th,dy_th = approx_euler(h,X[-1],Y[-1],VX[-1],VY[-1],k) #On prend les dernières valeurs
        X.append(x_th)
        Y.append(y_th)
        VX.append(dx_th)
        VY.append(dy_th)
    return(X,Y)

#500 points, 10 secondes, x0=1 ; y0=0 ; vx0=0 ; vy0=1
"""
k=-1 doit conduire à une hyperbole répulsive.
k=0 doit conduire à une droite.
k= 0.3 doit conduire à une hyperbole attractive.
k=0.5 doit conduire à une parabole.
k= 1 doit conduire à un cercle.
k=2 doit conduire à une ellipse.
"""
Liste_k = [-1,0,0.3,0.5,1,2]
Nom = ["k = -1, hyperbole répulsive", "k = 0, droite", "k = 0.3, hyperbole attractive",
       "k = 0.5, parabole", "k = 1, cercle", "k = 2, ellipse"]
Couleur = ['red','blue','orange','green','black','pink']
for k in Liste_k:
    X,Y = Euler(500,5,1,0,0,1,k)
    plt.plot(X,Y,color=Couleur[Liste_k.index(k)],label=Nom[Liste_k.index(k)])
plt.title("Trajectoires y=f(x) pour une force centrale F=-k/r² selon la valeur de k")
plt.legend()
plt.axis('equal')
plt.show()




