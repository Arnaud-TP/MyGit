#Arnaud Capitan MPSI B

## Vous pouvez exécuter directement le programme

""""""""" La commande for """""""""

## Exercice 1

#somme des n premiers entiers au carré
def somme(n):
    somme = 0
    for i in range (1,n+1): #Pour tout i allant de 1 à n inclus
        somme += i**2 # On ajoute i² à la somme
    return(somme)

n = eval(input('Calcul de la somme des n premiers entiers au carré. Entrez n :'))
print('La somme des ', n, 'premiers entiers au carré est égal à :', somme(n))

## Exercice 2

def factorielle(n):
    a=1
    if n<=0: # Si l'entier choisi est négatif, signe d'erreur
        return('Erreur')
    if (n==1 or n==0) : #Factorielle 1 ou 0 est égale à 1
        return(1)
    for i in range (1,n+1): #Pour tout i allant de 1 à n inclus, on multiplie a par i, et a vaut initialement 1.
        a*=i
    return(a)

n = eval(input('Calcul de factorielle n. Entrez n :'))
if factorielle(n) == 'Erreur':
    print("factorielle(n) n'est pas définie pour les entiers négatifs")
if factorielle(n) != 'Erreur':
    print('n factorielle est égale à :', factorielle(n))

## Exercice 3

def somme_termes(x,a,b):
    somme = 0 #On initialise la somme à 0
    ajout = 1 #On initialise le produit à 1 (soit x puissance 0)
    for k in range (1,a):
        ajout*=x #On multiplie 'ajout' par x jusqu'à la puissance a-1 de x
    if a == 0: #Le porduit étant initialisé à 1, il est nécessaire de supprimer la puissance 0
        somme+=1 #On ajoute donc manuellement x puissance 0
        a=1 #On incrémente la puissance de 1
    for i in range (a, b+1): #Pour tout i allant de a à b inclus
        ajout*=x #On ajout une puissance à x
        somme+=ajout #On additionne le nombre obtenu à somme
    return(somme)

print('Calcul de la somme des x puissance k, pour k allant de a à b inclus')
x = eval(input('Entrez x :'))
a = eval(input('Entrez a :'))
b = eval(input('Entrez b :'))
print('La somme des termes vaut :', somme_termes(x,a,b))

""""""""" La liste """""""""

#2.1)
K=[a**2 for a in range (1,16)] #Création de la liste K, liste faite de tous les éléments allant de 1 à 15 inclus mis au carré
print('La liste K est :\n', K)

#2.2)
K+=K # Doublage de la liste K
print('Liste K doublée \n', K)

#2.3)
print(K[18]) #Identification du terme à enlever
K.pop(18) #On enlève l'élément
print('Liste K (doublée) sans le 18e (17e informatiquement) élément :\n', K)

#2.4)
A=[] #Création d'une liste A vide
for i in range (0,len(K)): #Pour tout i allant de 1 au nombre de terme de la liste K
    A+=[K[len(K)-i-1]] #Les termes de K sont mis dans l'ordre contraire dans la liste A
print('La liste K inversée est :\n', A)

#2.5)
a=b=0
U=[a,b,'c',[1.5,4],'salut'] #Liste du haut de page
print(U[3][0]) #Affichage de l'élément en 1ere position de la liste située à la 4e position dans la liste U

""""""""" Chapitre Plot et Courbe """""""""

import math as m
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

#Exemple sur la fonction identité
X=np.arange(-5, 5,0.01)
Y=[0]*len(X)
for k in range(len(X)):
    Y[k]=abs((X[k])-3/2)
plt.plot(X,Y,color='cyan', label="f(x) = |x-3/2|")
#plt.show() affichage sur les deux courbes à la fin, avec un unique plt.show

def h(x):
    image = h
    image = m.sqrt(abs(x**2-3*x+2))#Fonction h
    return(image)

print("Tracé graphique de la courbe de h, sur l'intervalle [a,b], avec n points.")
a = eval(input('Entrez a :'))
b = eval(input('Entrez b :'))
n = eval(input('Entrez le nombre de points :'))

abscisses=[i for i in np.arange(a,b+(b-a)/n,(b-a)/n)] #Liste des abscisses
images=[h(i) for i in np.arange (a,b+(b-a)/n,(b-a)/n)] #Liste des ordonnées
plt.plot(abscisses,images, label="h(x)") #Tracé de la courbe à l'aide des abscisses, des ordonnées, et ajout d'une légende
plt.legend() #Affichage de la légende pour les courbes
plt.show() #Affichage des courbes

""""""""" Représentation de solution selon Euler """""""""

"""
Résolution de l'équation différentielle : La dérivée de f en t est PHI(f(t),t) et f(0)=ConditionInitiale
On a PHI(u,t)->3u + t donc :
"""
#1)a]
#y(a) = K*exp(3*a)-a/3 - 1/9 d'où y'(a) = 3*K*exp(3*a) - 1/3 = 3*(K*exp(3*a)- 1/9 -a/3) + a
#PHI est donc la dérivée de f en t

def PHI(f,t):
    image = 3*f(t) + t
    return(image)

#1)b]
"""
y' = 3y + t -> y = Kexp(3t)-t/3 - 1/9
y(0) = 0 -> K - 1/9 = 0 -> K = 1/9
La solution de l'équation différentielle y' = 3y + t telle que y(0) = 0 est y(t) = exp(3t)/9 *  (-t/3) -1/9
"""

def f(x):
    image = m.exp(3*x)/9 + (-x/3) -1/9 # Solution de l'équation différentielle avec pour condition initiale f(0) = 0
    return(image)

abscisses_f=[i for i in np.arange(0,1,0.001)] #Liste des abscisses des points de 0 à 1 de la solution passant par 0 en 0
images_f=[f(i) for i in np.arange (0,1,0.001)] #Liste des ordonnées des points de 0 à 1 de la solution passant par 0 en 0

#2)a]
"""D'après la formule donnée d'Euler, si f'(a) = b, alors f(a+h) = f(a) + hb (développement limité).
Les paramètres de la fonctio pointSuivant sont donc l'abscisse (t), l'ordonnée (y),
le pas (h) pour le calcul du point suivant, et la fonction PHI pour le nombre dérivé.  On obtient, d'après l'algorithme : zk le nombre dérivé en tk à l'aide de PHI et yk,
On avant tk de h, et on calcule f(tk + h) = yk + h*b
tk+1 -> tk + h   yk+1 -> yk + h*b
"""

def pointSuivant(t,y,PHI,h):
        b = PHI(f,t) #Nombre dérivé en t, la fonction qui nous intéresse étant la fonction f d'après 2)b]
        y = y + h*b #yk+1
        t = t + h #tk+1
        return(t,y)
#2)b]
def ResolEuler(intervalleTemps,CI,PHI,pointSuivant,h):
    t=CI #Condition initiale 1, t0 = 0 (début de l'intervalle)
    y=f(t) #L'autre condition initiale(f(0) = 0) est remplie par la fonction choisie calculée auparavant
    Liste_t = [] #Déclaration de la liste des abscisses
    Liste_y = [] #Déclaration de la liste des ordonnées
    while(1):
        if ((0<=t<=1) == False): #On règle ici la condition d'arrêt de la boucle
            return(Liste_t, Liste_y)
        Liste_t += [t] #Enregistrement de chaque abscisse
        Liste_y += [f(t)] #Enregistrement de chaque ordonnée
        t,y = pointSuivant(t,y,PHI,h)

#2)c]
#import numpy as np     Déjà importé précédemment
#import matplotlib.pyplot as plt    Déjà importé précédemment
X,Y=ResolEuler([0,1],0,PHI,pointSuivant,0.01)
plt.plot(X,Y,color='red', label="Solution selon la méthode d'Euler") #En rouge est affichée le tracé de la fonction selon la méthode d'Euler
X=np.arange(0,1,0.01) #Liste des abscisses de la fonction calculée comme à la 1)b]
Y=[0]*len(X)
for k in range(len(X)):
    Y[k]=f(X[k]) #Liste des ordonnées de la fonction calculée comme à la 1)b]
plt.plot(X,Y,color='black', label="Solution théorique") #Tracé de la fonction
plt.legend()
plt.show()

"""
J'espère voir la courbe de la fonction solution en noire, et une approximation en rouge de cette même courbe (superposition partielle)
Erreur 1 : Appel de la variable y avant affectation
-> Corrigée par son ajout en CI au début de ResolEuler
Erreur 2 : PHI(u,t) erreur de type : un int et attend une fonction
-> Corrigée par le remplacement de u par solution() -> PHI(solution(),t)
Erreur 3 : solution() n'est pas un paramètre
-> Corrigée par PHI(solution,t)
Erreur 4 : Y[k]=f(X[k]), f non défini
-> Corrigée par le remplacement de solution par f dans tout le programme
Erreur 5 : La fonction tracé ne ressemble pas à exponentielle de 3x
-> Corrigée par le remplacement du * (erreur) par un + dans la fonction f
Erreur 6 ? : Pas d'affichage de la courbe rouge ? -> Superposition == précision des tracés ?
-> Suppression du tracé de la courbe noire, et apparition de la courbe rouge
"""
#3) En changeant le pas pour un pas plus petit (h = 0.00001), on observe un léger décalage (de l'ordre de 10e-4) entre les deux courbes

##

#4) On nomme g la fonction solution afin de ne pas confondre f et g
#Le nombre dérivée de f en a est donnée par l'équation différentielle : y' = cos(t)*y
#a]
def PHIc (g, t):
    image = m.cos(t)*g
    return(image)

#b] La résolution selon Euler consiste à obtenir graphiquement la solution de l'équation différentielle.
"""
On sait que la tangente vérifie : Si f'(a) = b, alors f(a+h) = f(a) + hb (+h*eps(h)), ici n'apparaît pas)
De plus, on a pour condition initiale f(0) = 1, et pour EDL1 y' = cos(t)y
y'(0) = cos(0)*y(0) = 1 (b) d'après la CI
f'(a) = cos(a)*f(a) = b
f(a+h1) = f(a) + h1*b, donc pour h1 = h (petit), on obtient f(0 + h1) = f(0) + h1*1
f(h1) = 1 + h1 On utilise cette égalité pour définir un nouveau f(a).
f'(h1) = cos(h1)*f(h1) (un nouveau b) -> f(h1 + h) = f(h1) + h*cos(h1)*f(h1)
Ainsi de suite pour définir la solution sur l'intervalle [0,2pi]
-> f(h(k)+h) = f(h(k)) + h*cos(h(k))*f(h(k))
-> h(k) + h = h(k+1)
-> f(h(k+1)+h) = f(h(k+1)) + h*cos(h(k+1))*f(h(k+1))
-> etc
"""

def ResolEuler_2(h2, pointSuivant_2,PHIc):
    t2=0 #Condition 1, 0 est le début de l'intervalle
    y2=1 #Condition 2, y(0) = 1
    Liste_t2 = []
    Liste_y2 = []
    while(1):
        if ((0<=t2<=2*m.pi) == False): #Condition d'arrêt 1, l'antécédent hors de l'intervalle défini
            return(Liste_t2, Liste_y2)
        if (y2 > 1000): # Condition 2, erreur de l'image qui diverge (utilisée pour tests)
            break
        Liste_t2 += [t2] #Enregistrement de chaque abscisse
        Liste_y2 += [y2] #Enregistrement de chaque ordonnée
        t2,y2 = pointSuivant_2(t2,y2,h2,PHIc)

# A l'aide de la formule
# -> h(k+1) = h(k) + h
# -> f(h(k+1)+h) = f(h(k+1)) + h*cos(h(k+1))*f(h(k+1))
def pointSuivant_2(t2,y2,h2, PHIc):
    t2_suivant = t2 + h2
    y2_suivant = y2 + h2*PHIc(y2, t2)
    return(t2_suivant, y2_suivant)

Ecart = eval(input("Entrez l'écart h pour la résolution d'Euler, y' = cos(t)y :"))
X,Y=ResolEuler_2(Ecart,pointSuivant_2, PHIc)
plt.plot(X,Y,color='red', label="Solution selon la méthode d'Euler")
#plt.legend()
#plt.show() On affiche les deux courbes sur un même graphe

#c]
"""
L'équation différentielle y' = cos(t)y admet pour solutions y(t) = K*exp(sin(t)), K un réel
a = 1 et b = -cos(t) sont continues sur [O,2pi] -> Application du théorème des EDL du premier ordre.
Ainsi, pour y(0) = 1, on obtient : y(0) = K*exp(sin(0)) et sin(0) = 0
-> y(0) = K et y(0) = 1 d'après la condition initiale -> K = 1
y(t) = exp(sin(t))
"""
def g(x):
    image = m.exp(m.sin(x))
    return(image)

X=np.arange(0,2*m.pi,0.01) #Liste des abscisses de la fonction calculée comme à la 1)b]
Y=[0]*len(X)
for k in range(len(X)):
    Y[k]=g(X[k]) #Liste des ordonnées de la fonction calculée comme à la 1)b]
plt.plot(X,Y,color='black', label="Solution théorique") #Tracé de la fonction
plt.legend()
plt.show()

#d] Pour h = 0.0001, on observe un écart très faible entre les deux courbes,
#la méthode d'Euler fonctionne pour approximer les solutions d'équations différentielles

## EULER_CORRIGE

#5)a]
"""
z =[ f'(a+h) + f'(a) ] / 2      Nouvelle évaluation, accompagne celle d'Euler :
Si f'(a) = b, alors f(a+h) = f(a) + hb
-> On a toutefois besoin de l'évaluation d'Euler pour calculer f(a+h), et en déduire f'(a+h)
"""

def pointSuivantCorrige(x3,y3,h3,PSI):
    x_suiv = x3 + h3 #Calcul de a+h
    y_suiv = y3 + h3*m.cos(y3)*y3 #Calcul de f(a+h)
    dy_suivant = PSI(x3, y3) # f'(a)   y' = cos(t).y d'après léquation différentielle
    dy_ah_suivant = PSI(x_suiv, y_suiv) # f'(a+h)
    z = (dy_ah_suivant + dy_suivant)/2 # A l'aide de cette nouvelle dérivée, on déduit f(a+h) = f(a) + hb
    y_suiv = y3 + h3*z #Calcul de la nouvelle approximation
    return(x_suiv, y_suiv)

def PSI(t, y):
    dy = m.cos(t)*y
    return(dy)

def ResolEuler_3(h3,pointSuivantCorrige,PSI):
    t3=0
    y3=1
    Liste_t3 = []
    Liste_y3 = []
    while(1):
        if ((0<=t3<=2*m.pi) == False):
            return(Liste_t3, Liste_y3)
        if (y3 > 1000):
            break
        Liste_t3 += [t3]
        Liste_y3 += [y3]
        t3,y3 = pointSuivantCorrige(t3,y3,h3,PSI)

X,Y=ResolEuler_3(Ecart,pointSuivantCorrige, PSI)
plt.plot(X,Y,color='red', label="Solution selon la méthode d'Euler corrigée")
X=np.arange(0,2*m.pi,0.01)
Y=[0]*len(X)
for k in range(len(X)):
    Y[k]=g(X[k])
plt.plot(X,Y,color='black', label="Solution théorique")
plt.legend()
plt.show()

"""
On observe qu'avec le même écart h, la courbe est environ au même écart de l'approximation
(en un point, 0.0005 pour la méthode sans corrigé, 0.0008 pour le corrigé), mais cette fois-ci
la courbe approximée est du coté gauche de la courbe tracée (après le premier maximum atteint).
On en déduit que les deux approximations sont précises (dans la mesure d'un tracé graphique donnant une très bonne
approximation de la solution), mais la correction de la méthode d'Euler n'apporte pas de précision supplémentaire
(d'après l'analyse du graphe).
"""