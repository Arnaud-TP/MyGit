import math

def f(x): #f(x) pour les 3 fonctions : dichotomie, interpolation, méthode de Newton
    return(math.cos(x) - 1/2) #Fonction dont on veut trouver la racine par une valeur approchée
A=0 #Intervalle dans lequel se trouve la racine souhaitée
B=3
EPS=0.001 #Epsilon, erreurMax, précision. Ces 3 variables déclarées seront constantes et sont appelées dans toutes les fonctions pour éviter de changer partout dans le cas de l'étude comparative

## Exercice 1 : Dichotomie

a=A #Réinitialisation des variables
b=B
erreurMax = EPS
print("L'intervalle contenant la/les racines est [", A, ';', B,"] et l'ecart epsilon est :", EPS)

def dichotomie(a,b,f,erreurMax):
    n=0
    while(abs(b-a)>erreurMax): #Dichotomie
        m=(a+b)/2
        if(f(m)*f(a)<0):
            b=m
        else:
            a=m
        n=n+1
    return(m, n)

print("Une racine de cette fonction et le nombre d'itérations de la dichotomie sont respectivement :", dichotomie(a, b, f, erreurMax))

## Exercice 2 : Interpolation

#Le test |bn - an|>eps n'est pas pertinent ici car l'une des bornes risque d'être fixe pendant que l'autre borne se déplacera pour aller se placer proche de la racine de la fonction
#Un test utilisant f(xI - eps)*f(xI + eps) peut déterminer si xI est suffisament proche de la solution f(x) = 0 car les écarts autour de la valeur xI
#(c'est-à-dire xI + ou - eps, pour epsilon petit) pour xI proche de b tq f(b) = 0, auront des images de signes contraires.

a=A #Réinitialisation des variables
b=B
eps = EPS

#L'opération d'interpolation consiste à résoudre : 0 = ((f(b) - f(a))/(b-a))*(x-a) + f(a) pour x
# x = a - f(a)*(b-a)/((f(b) - f(a))
def interpolation(a,b,f,eps):
    x=a-(f(a)*(b-a))/(f(b) - f(a)) #Détermination du premier point xI
    if f(x)*f(a) > 0 : #Détermination du point fixe lors de l'interpolation
        print("Le point fixe de l'interpolation est le point a") #D'après le calcul conditionnel de l'interpolation, f(x)*f(a)<0 le point b est déplacé à xI, et inversement
    else :
        print("Le point fixe de l'interpolation est le point b")
        n=1
        while((f(x-eps)*f(x+eps)>0)and(n<50)): #Condition de l'interpolation + Compte tour
            x = a - f(a)*(b-a)/(f(b) - f(a))
            if(f(x)*f(a)<0):
                b=x
            else:
                a=x
            n=n+1
        return(x,n)

print("Une racine de cette fonction et le nombre d'itérations de l'interpolation sont respectivement :", interpolation(a, b, f, eps))

## Exercice 3 : Newton

##Question 1 :
#lim eps -> 0 (f(x+eps) - f(x))/ eps = f'(x)
#Donc pour eps proche de 0, cette formule est une approximation de f'(x)

# Question : Montrer que xI = x - f(x)/f'(x) avec x appartenant à {a;b}, avec I(xI;0) le point d'inteserction de
# l'une des tangentes en a ou b avec l'axe des absicces, xI appartenant à ]a;b[

# L'équation des tangentes en a et b sont respectivement : yA = f'(a)(x-a) + f(a) et yB = f'(b)(x-b) + f(b)
# Après résolution de yA = 0 et yB = 0, on obtient xI = -f(a)/f'(a) + a (de même pour b), d'où le résultat.
# Pour la condition xI appartenant à ]a;b[ Démonstration en cours ?

##Question 2 :

a=A #Réinitialisation des variables
b=B
eps = EPS
def df(x): #Utilisation de la formule d'une meilleur approximation de la dérivée de f en x
    NombreDérivé = (f(x+eps*0.25)-f(x-eps*0.25))/(0.5*eps)
    return(NombreDérivé)

def ChoixSelonPente(a,b): #Pour simplifier la fonction, j'introduis celle-ci qui effectue le calcul de la valeur absolue de la pente pour ne pas le mettre dans la fonction principale
    if (abs(df(a)) - abs(df(b)) > 0): #Choix du point a ou du point b selon la valeur de la pente. Ici, la plus grande pente est celle au point a
        xI = a-f(a)/df(a)
    else :
        xI = b-f(b)/df(b)
    return(xI)

def RacineApprocheeNewton(a,b,f,eps):
    xI = ChoixSelonPente(a,b) #Première itération
    n=1
    while ((f(xI-eps)*f(xI+eps)>0)and(n<50)): #Utilisation de la condition de l'interpolation + Compte tour
        if(f(xI)*f(a)<0):
            b=xI
        else:
            a=xI
        n=n+1
        xI = ChoixSelonPente(a,b)
    return(xI, n)

print("Une racine de cette fonction et le nombre d'iterations selon la methode de Newton sont respectivement :", RacineApprocheeNewton(a,b,f,eps))