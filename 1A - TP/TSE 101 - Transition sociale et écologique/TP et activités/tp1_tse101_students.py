import numpy as np
import matplotlib.pyplot as plt


a= 1.5 #Alpha
b= 0.05 #Beta
c= 0.5 #Gamma
d= 0.05 #Delta

#a=taux de reproduction des proies (constant, indépendant du nombre de prédateurs)
#b=taux de mortalité des proies face aux prédateurs rencontrés
#c=taux de mortalité des prédateurs (constant, indépendant du nombre de proies)
#d=taux de reproduction des prédateurs en fonction des proies rencontrées et mangées

def proie(x,y): #Renvoie la variation du nombre de proies
    e = x*(a-b*y)
    return e
 
def proie_generalise(x,y):
    ap=a/2
    g = x*(a-b*y-ap*x)
    return g

def predateur(x,y):
    f= -y*(c-d*x)
    return f

def Lotka_Volterra(x_0,y_0,uc,vc,tmin,tmax,h):
    liste_t=[tmin]
    liste_x=[x_0]
    liste_y=[y_0]
    t=tmin
    x=x_0
    y=y_0
    aux_x=0
    aux_y=0
    while t<=tmax:
        t+=h
        liste_t.append(t)
        aux_x=x+h*(proie(x,y)+uc)
        aux_y=y+h*(predateur(x,y)+vc)
        x=max(0,aux_x)
        y=max(0,aux_y)
        liste_x.append(x)
        liste_y.append(y)
    return liste_t,liste_x,liste_y

def Lotka_Volterra_commande(x_0,y_0,tmin,tmax,h):
    liste_t=[tmin]
    liste_x=[x_0]
    liste_y=[y_0]
    liste_u=[0]
    t=tmin
    x=x_0
    y=y_0
    aux_x=0
    aux_y=0
    while t<=tmax:
        t+=h
        liste_t.append(t)
        uc=-proie(x,y)
        aux_x=x+(proie(x,y)+uc)*h
        aux_y=y+(predateur(x,y))*h
        x=max(0,aux_x)
        y=max(0,aux_y)
        liste_x.append(x)
        liste_y.append(y)
        liste_u.append(uc)
    return liste_t,liste_x,liste_y,liste_u

def Lotka_Volterra_generalise(x_0,y_0,tmin,tmax,h):
    liste_t=[tmin]
    liste_x=[x_0]
    liste_y=[y_0]
    t=tmin
    x=x_0
    y=y_0
    aux_x=0
    aux_y=0
    while t<=tmax:
        t+=h
        liste_t.append(t)
        aux_x=x+h*proie_generalise(x,y)
        aux_y=y+h*predateur(x,y)
        x=max(0,aux_x)
        y=max(0,aux_y)
        liste_x.append(x)
        liste_y.append(y)
    return liste_t,liste_x,liste_y

def affichage_Lotka_Volterra_temps(x_0,y_0,uc,vc,tmin,tmax,h):
    T,X,Y=Lotka_Volterra(x_0,y_0,uc,vc,tmin,tmax,h)
    plt.plot(T,X, label="Proie")
    plt.plot(T,Y, label="Prédateur")
    plt.title('Populations au cours du temps')
    plt.xlabel("Temps d'étude (en année)")
    plt.ylabel('X = Population de proies et Y=population de prédateur')
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

def affichage_Lotka_Volterra_diag(x_0,y_0,uc,vc,tmin,tmax,h):
    T,X,Y=Lotka_Volterra(x_0-2,y_0-2,uc,vc,tmin,tmax,h)
    plt.plot(X,Y, label="X0=2 et Y0=8")
    T,X,Y=Lotka_Volterra(x_0,y_0,uc,vc,tmin,tmax,h)
    plt.plot(X,Y, label="X0=4 et Y0=10")
    T,X,Y=Lotka_Volterra(x_0+2,y_0+2,uc,vc,tmin,tmax,h)
    plt.plot(X,Y, label="X0=6 et Y0=12")
    plt.title('Population de prédateur en fonction de la population de proie')
    plt.xlabel('X = Population de proies')
    plt.ylabel('Y = Population de prédateurs')
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

def affichage_Lotka_Volterra_commande_temps(x_0,y_0,tmin,tmax,h):
    T,X,Y,U=Lotka_Volterra_commande(x_0,y_0,tmin,tmax,h)
    plt.plot(T,X, label="Proie")
    plt.plot(T,Y, label="Prédateur")
    plt.plot(T,U, label="Repeuplement/prélèvement")
    plt.title('Populations au cours du temps avec prélèvement')
    plt.xlabel("Temps d'étude (en année)")
    plt.ylabel('X = Population de proies et Y=population de prédateur')
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

def affichage_Lotka_Volterra_generalise_temps(x_0,y_0,tmin,tmax,h):
    T,X,Y=Lotka_Volterra_generalise(x_0,y_0,tmin,tmax,h)
    plt.plot(T,X, label="Proie")
    plt.plot(T,Y, label="Prédateur")
    plt.title('Populations au cours du temps (modèle généralisé)')
    plt.xlabel("Temps d'étude (en année)")
    plt.ylabel('X = Population de proies et Y=population de prédateur')
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

def affichage_Lotka_Volterra_generalise_diag(x_0,y_0,tmin,tmax,h):
    T,X,Y=Lotka_Volterra_generalise(x_0-2,y_0-2,tmin,tmax,h)
    plt.plot(X,Y, label="X0=2 et Y0=8")
    T,X,Y=Lotka_Volterra_generalise(x_0,y_0,tmin,tmax,h)
    plt.plot(X,Y, label="X0=4 et Y0=10")
    T,X,Y=Lotka_Volterra_generalise(x_0+2,y_0+2,tmin,tmax,h)
    plt.plot(X,Y, label="X0=6 et Y0=12")
    plt.title('Population de prédateur en fonction de la population de proie (modèle généralisé)')
    plt.xlabel('X = Population de proies')
    plt.ylabel('Y = Population de prédateurs')
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()

tmax = 50
h = 0.005
affichage_Lotka_Volterra_temps(4,10,0,0,0,tmax = tmax,h=h)
affichage_Lotka_Volterra_diag(4,10,0,0,0,tmax = tmax,h=h)

affichage_Lotka_Volterra_temps(4,2,0,0,0,tmax = tmax,h=h)
affichage_Lotka_Volterra_diag(4,2,0,0,0,tmax = tmax,h=h)

affichage_Lotka_Volterra_commande_temps(4,10,0,tmax = tmax,h=h)

affichage_Lotka_Volterra_generalise_temps(4,10,0,tmax = tmax,h=h)
affichage_Lotka_Volterra_generalise_diag(4,10,0,tmax = tmax,h=h)
