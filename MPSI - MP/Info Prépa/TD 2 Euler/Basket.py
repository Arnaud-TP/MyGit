import math as m
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

## Quelques données à propos des dimensions au basket
#Taille d'un ballon : Diamètre entre 23.8 et 24.8 cm
#On prend pour taille de ballon un diamètre égal à 24 cm, donc de rayon 12 cm
#Masse entre 567 g et 624 g, n'influe pas

#Diamètre de l'arceau : 45 cm
#Distance entre le tireur et le bord de l'arceau (au sol) : 4.15 m
#Distance entre le tireur et le bout du panier : 4.60 m
#Hauteur de l'arceau par rapport au sol : 3.05 m
#Hauteur de tir d'un ballon : 2m20 (bras semi-tendus pour le tir)


#L'accélération g vaut 9.81 m/s²

#L'angle α de tir et la vitesse v0 de tir sont respectivement des conditions initiales
#L'une est à déterminer en fonction de l'autre

##Equation du mouvement sans frottement
"""
Système : {ballon de basket}
Référentiel terrestre supposé galiléen
On s'intéresse d'abord aux mouvements en x
On a une vitesse constante tout au long du mouvement,
qui vaut vx = v0*cos(α)     α et v0 sont respectivement des conditions initiales, l'une à déterminer, l'autre donnée
On a x = vx * t = v0*cos(α)*t

On s'intéresse ensuite aux mouvements en y
Bilan des forces qui s'exercent sur le système selon l'axe y
    Poids P= - m*g*vect(y)
    Frottements négligés
D'après la deuxième loi de Newton, Somme des forces extérieures = m*vect(a)
vect(a) = d²y/dt² vect(y), donc -m * g = m * d²y/dt²
On a donc :
- g = d²y/dt²     avec pour conditions initiales :
On a x = v0*cos(α)*t, soit x/v0*cos(α) = t avec v0*cos(α) = Cte, donc l'équation équivaut à :

- g = d²y/d(x/v0*cos(α))²   soit   - g / (v0*cos(α))² = d²y/dx²
"""

## Conditions
"""
la balle doit être en descente, donc At = 4.375 / v0*cos(α), dy/dt < 0
--> Cette condition disparaît avec l'angle minimal
la balle doit dépasser l'arceau d'au moins son rayon
-> Cette condition fixe l'angle minimal à 0.7 radian par expérimentation
la balle doit se trouver approximativement au centre de l'arceau
12 cm de rayon pour le ballon, 45 cm de diamètre pour l'arceau
-> On suppose que le panier est réussi lorsque le ballon rentre dans le panier
    pour 4.27 m < x < 4.48 m (on réduit le diamètre de l'arceau par un rayon
    de ballon ded chaque côté)
L'angle α doit être compris entre arctan(1.65/4.15) et pi/2
car tan(α) = (3.05 - 2.20)/(4.60 - 0.45) au minimum
(sinon la balle passe en dessous de l'arceau même à v0 grand)
donc 0.4 < α < 1.5 (en radian)
"""
## Méthode de vérification de la solution
"""
On crée une fonction unique vérification pour les deux, qui fait varier la solution d'une valeur faible
selon l'angle ou la vitesse, qui sera choisi initialement, d'où la nécessité de créer la fonction
au sein même de la fonction des boucles de choix
On suppose que la solution existe dans un écart max de 0.5, pour ne pas avoir une situation infinie
"""

## Partie résolution et courbes

#Déclaration des valeurs et constantes

#La pente à l'origine vaut : tan(α)
#Soit y=ax+b la tangente à l'origine, a = yB - yA / xB - xA
# a = (sin(α) + 2.20 - 2.20)/cos(α)  = sin(α)/cos(α)

intervalle=[0,4.60] #Intervalle de définition de l'équation différentielle
h=0.001 #Ecart h
α=0 #On fixe l'angle pour déclarer la variable pour les fonctions
vitesse_init = 0 # Même raison
CondInit = [2.20,m.tan(α)] #Position, pente ; les valeurs seront modifiés selon le cas
solution = 0 #Une fois la solution trouvée, on mettra solution = true

#y''= -g

def PSI(u, x, vitesse_init, α):
    acceleration = -9.81/((vitesse_init*m.cos(α))**2)
    v=[u[1],acceleration]
    return(v) #Vitesse, Accélération

def PointSui (x,u,PSI,h,vitesse_init, α):
    vit_acc = PSI(u,x, vitesse_init, α)
    vitesse_suiv = vit_acc[0] + h*vit_acc[1]
    position_suiv = u[0] + h*u[1]
    x_suivant = x+h
    u_suivant=[position_suiv, vitesse_suiv]
    return(x_suivant, u_suivant)

def ResolEul(intervalle,CondInit,PSI,PointSui,h, vitesse_init, α):
    x=intervalle[0]
    u=CondInit
    Ypos=[u[0]]
    Yvit=[u[1]]
    Xpos=[x]
    while (x <= intervalle[1]) and (u[0] > 0):  #On pose des bornes
        x, u = PointSui(x,u,PSI,h, vitesse_init, α)
        Ypos.append(u[0]) #Liste des positions verticales
        Yvit.append(u[1]) #Liste des vitesses
        Xpos.append(x) #Liste des abscisses
        if 4.15<=x<=4.60 and 3<=u[0]<=3.05 :
            u[0]=-1 #Arrêt de la boucle while, valeurs proches de la solution
    return(Xpos,Ypos,Yvit)

def dessin(ResolEul,intervalle,CondInit,PSI,PointSui,h, vitesse_init, α, solution, verification):
    Xpos,Ypos,Yvit = ResolEul(intervalle,CondInit,PSI,PointSui,h, vitesse_init, α)
    variation_donnee, solution = verification(Xpos,Ypos, solution)
    if solution == 1:
        plt.clf()
    plt.plot(Xpos,Ypos, color='orange', linewidth=3)
    plt.xlabel("Position horizontale") #Légende de l'axe X
    plt.ylabel("Position verticale") #Légende de l'axe Y
    plt.plot([-0.5,5],[-0.01,-0.01], color='green', linewidth=3) #Axe X du repère
    plt.plot([0,4.60],[0,0], color='red')#Ligne de tir de lancer franc
    plt.plot([4.60,4.60],[0,3.95], color='blue', linewidth=3)#Panier de basket
    plt.plot([4.15,4.60],[3.05,3.05], color='red', linewidth=2)#Arceau
    plt.plot([4.15,4.25,4.50,4.60],[3.05,2.75,2.75,3.05], color='grey')#Filet
    plt.plot([0,0],[0.1,-0.1], color='black')#Axe Y du repère
    plt.axis('equal') #Repère orthonormé
    plt.xlim([-0.5, 5]) #On borne la fenêtre de dessin
    plt.ylim([-0.5, 5])
    if solution == 1:
        print("L'angle initial et la vitesse initiale doivent être ", α, 'radians et ', vitesse_init, 'm/s')
        plt.title("Tracé de la courbe d'un tir idéal")
        return(variation_donnee, solution)
    if (abs(variation_donnee) == 0.05) or (abs(variation_donnee) == 0.005): #Affichage de la courbe uniquement lorsque la solution est proche
        plt.title('Approximation de la solution : tracé des courbes')
        plt.pause(1.5) #Affichage pour un court instant de la courbe
        plt.close() #Fermeture automatique du dessin
        plt.clf()   #Clear figure, efface le dessin
    return(variation_donnee, solution)


def solveur(ResolEul,intervalle,CondInit,PSI,PointSui,h, vitesse_init, α, dessin):
    print('Quelle valeur initiale souhaitez-vous choisir ?')
    choix = eval(input('1. Vitesse Initiale   2. Angle\n'))
    solution = False
    n=0
    if (choix != 1) and (choix != 2):
        print('Erreur de valeur !')
        return(-1)

    if choix == 1: # CAS 1 : la vitesse v0 est donnée
        vitesse_initiale=eval(input("Vitesse initiale (m/s):"))
        α= m.pi/3 #Angle raisonnable de tir
        CondInit = [2.20,m.tan(α)] #Nécessaire pour l'approximation

        if (vitesse_initiale < 5) or (vitesse_initiale > 20): #Vitesse trop faible, trop élevée
            print('Vitesse trop faible !')
            return(-1)

        def verification1(Xpos,Ypos, solution):
            if 4.15<=Xpos[-1]<=4.60 and 3<=Ypos[-1]<=3.05 : #Proche de la solution, arrêt du tracé
                if 4.27 <= Xpos[-1] <= 4.48 : #Condition de tir réussi
                    solution=1
                    return(0, solution)
                if 4.15 <= Xpos[-1] < 4.27 : #Condition de tir un peu court
                    return(-0.005, solution)
                if 4.48 < Xpos[-1] <= 4.60 : #Condition de tir un peu long
                    return(0.005, solution)
            if Ypos[-1]>3.05 : #Tir trop haut
                return(0.01, solution)
            return(-0.01, solution)#Tir ni trop haut, ni proche de la solution, donc trop bas

        while solution != 1 and n < 100 :
            n+=1 #Nombre d'itérations
            correction, solution = dessin(ResolEul,intervalle,CondInit,PSI,PointSui,h, vitesse_initiale, α, solution,verification1)
            α+=correction
            CondInit = [2.20,m.tan(α)]
        print("Le nombre d'itérations est n =", n)
        if n == 100 :
            print('Pas de solution pour cette valeur donnée.')
        plt.show()

    if choix == 2: # CAS 2 : l'angle α est donné
        α= eval(input('Angle initial (radian):'))
        CondInit = [2.20,m.tan(α)]
        vitesse_initiale = 6 #Vitesse raisonnable pour un tir au basket, première itération

        if (α < 0.7) or (α >= 1.5): #Voir condition
            print('Valeur incorrecte !')
            return(-1)

        def verification2(Xpos,Ypos, solution):
            if 4.15<=Xpos[-1]<=4.60 and 3.04<=Ypos[-1]<=3.05 : #Proche de la solution, arrêt du tracé
                if 4.27 <= Xpos[-1] <= 4.48 : #Condition de tir réussi
                    solution=1
                    plt.clf()
                    return(0, solution)
                if 4.15 <= Xpos[-1] < 4.27 : #Condition de tir un peu court
                    return(0.05, solution)
                if 4.48 < Xpos[-1] <= 4.60 : #Condition de tir un peu long
                    return(-0.05, solution)
            if Ypos[-1]>3.05 : #Tir trop haut
                return(-0.20, solution)
            return(0.20, solution)#Tir ni trop haut, ni proche de la solution, donc trop bas

        while solution != 1 and n < 100 :
            n+=1 #Nombre d'itérations
            correction, solution = dessin(ResolEul,intervalle,CondInit,PSI,PointSui,h, vitesse_initiale, α, solution,verification2)
            vitesse_initiale+=correction
        print("Le nombre d'itérations est n =", n)
        if n == 100 :
            print('Pas de solution pour cette valeur donnée.')
        plt.show()



solveur(ResolEul,intervalle,CondInit,PSI,PointSui, h, vitesse_init, α, dessin)
