import math as m

def prod(n,p):
    if p == 0:
        return(0)
    return (prod(n,p-1) + n)

def decimal (base,n):
    if len(n) == 0: #n une chaîne de caractère, type string
        return(0)
    return( int(n[-1]) + base*decimal(base, n[0:len(n)-1]))


def affichage(n):
    print(n, end=' ') # print(..., end=' ') rajoute un espace à la fin et supprime le retour à la ligne
    if n==0:
        return()
    affichage(n-1)
"""
def premier_non_rec(n): #Fonction non récursive qui renvoie une liste des entiers premiers de 2 à n
    L=[2]
    for i in range (3,n):
        L.append(i)
        for element in L[0:m.floor(m.sqrt(i))]:
            if i%element==0:
                L.pop()
                break
    return(L)

def est_premier_non_rec(p): #Fonction non récursive qui renvoie True si le nombre est premier, False sinon
    if p in premier_non_rec(p+1):
        return(True)
    return(False)
"""

def premier(n, d=2):
    if d==n :
        return(True)
    if n % d == 0:
        return(False)
    return premier(n,d+1)

#Inconvénient de faire une fonction récursive pour les nombres premiers
#Dès que le nombre premie recherché excède 3000, le nombre d'itérations maximum est dépassé
#Message d'erreur et aucun renvoie. Voir fonction au dessus pour une meilleur efficacité
#Si le nombre n'est pas premier, la fonction termine rapidement et reste efficace

def fibonacci(n):
    if (n == 0) or (n == 1):
        return(1)
    return(fibonacci(n-1)+fibonacci(n-2))

def rechercheDichotomique(element, listeTriee):
    a=0
    b= len(listeTriee)-1
    m=(a+b)//2
    while a<b:
        if listeTriee[m] == element :
            return(m)
        elif listeTriee[m] > element :
            b = m-1
        else :
            a = m+1
        m=(a+b)//2
    return(a)

def rechercheDichotomiqueRecursive(element, listeTriee, a = 0, b = -1):
    if a == b:
        return(a)
    if b == -1:
        b=len(listeTriee) - 1
    m=(a+b)//2
    if listeTriee[m] == element :
        return(m)
    elif listeTriee[m] > element :
        return(rechercheDichotomiqueRecursive(element, listeTriee, a, m-1))
    else :
        return(rechercheDichotomiqueRecursive(element, listeTriee, m+1, b))

def rechercheDichotomiqueRecursive2(element, listeTriee):
    if len(listeTriee) == 1 :
        return(0)
    m = len(listeTriee)//2
    if listeTriee[m] == element :
        return(m)
    elif listeTriee[m] > element :
        return rechercheDichotomiqueRecursive2(element, listeTriee[:m])
    else :
        return (m + rechercheDichotomiqueRecursive2(element, listeTriee[m :]))

"""
Test :
print(rechercheDichotomique(9,[3,5,6,7,9,12,34,53]))
print(rechercheDichotomiqueRecursive(9,[3,5,6,7,9,12,34,53]))
print(rechercheDichotomiqueRecursive2(9,[3,5,6,7,9,12,34,53]))
"""