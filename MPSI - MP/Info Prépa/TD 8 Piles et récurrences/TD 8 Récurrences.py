#Arnaud Capitan MPSI B
# Récurrences

import matplotlib.pyplot as plt #Courbe du coût dernier exercice
import math as m
## Exercice 1

def recopierPile(p):
    if len(p) == 0:
        return([])
    q = []
    rep=[]
    for i in range (len(p)):
        element=p.pop()
        q.append(element)
    for i in range (len(q)):
        element=q.pop()
        p.append(element)
        rep.append(element)
    return(rep)

assert recopierPile([1,2,3,4,5]) == [1,2,3,4,5]

## Exercice 2

def controlPar(expr):
    pil=[]
    ouvre=['(','{','[']
    ferme=[')','}',']']
    for elemt in expr :
        if elemt in ouvre :
            i = ouvre.index(elemt)
            pil.append(ferme[i])
        if elemt in ferme :
            if len(pil) == 0: #Si la pile est vide :
                print("Trop de caractères de fermetures !")
                return(-1)
            if elemt == pil[-1] : #Si le caractère a son correspondant
                pil.pop()
            else : #S'il ne l'a pas
                print("Caractère pas fermé !")
                return(-1) #Erreur
    print("Bravo ! Tout est bon.")
    return(0) # Tout va bien

exprA='print([5]+[6])'
exprB='print([{A}+{B])'
exprC='print([{A}+{B}]))'

assert controlPar(exprA) == 0 # Bravo ! Tout est bon.
assert controlPar(exprB) == -1 # Caractère pas fermé !
assert controlPar(exprC) == -1 # Trop de caractères de fermetures !

## Exemple 2.1 :

def suiteU(n,U0):
    if n == 0:
        return(U0)
    return 2*suiteU(n-1,U0) + 1

for k in range(3):
    print(suiteU(k,1))

#Que fait cette fonciton ?
#Réponse : suiteU est une suite définie par récurrence un+1 = 2un + 1, avec U0 un paramètre
#Ici on calcule et on affiche les 3 premiers termes, 1, 3 et 7

## Exercice 3 :

def suite_u(n):
    if n == 0: # u0 = 1
        return(1)
    if n == 1: # u1 = 2
        return(2)
    return(2*suite_u(n-1) - 3*suite_u(n-2))

assert suite_u(5) == -10

## Exercice 4 :

def factorielle(n):
    if n == 0 : # 0! = 1
        return(1)
    return(n*factorielle(n-1))

assert factorielle(5) == 120

## Exercice 5 :

#Quel est le calcul fait par la fonction suivante :

def Sn(a,b):
    if a>b:
        return(0)
    return(Sn(a,b-1)+b)

# Réponse : Cette fonction calcule la somme des nombres allant de a à b inclus (b>a) sinon renvoie 0

## Exercice 6 :

def doublerec(n,U0,U1,a,b):
    if n == 0:
        return(U0)
    if n == 1:
        return(U1)
    return(a*doublerec(n-1,U0,U1,a,b) + b*doublerec(n-2,U0,U1,a,b))

#Question 1 :

#u(n+2) = u(n+1) + u(n), u0 = 1, u1 = 1
assert doublerec(0,1,1,1,1) == 1
assert doublerec(1,1,1,1,1) == 1
assert doublerec(2,1,1,1,1) == 2
assert doublerec(3,1,1,1,1) == 3
assert doublerec(4,1,1,1,1) == 5

#Question 2 :
"""
Nombre d'opérations : C(n) = C(n-1) + C(n-2) + 3 et C(1) = C(n) = 0
Suite constante respectant l'équation :  x = x + x + 3 => x = - 3

C(n) + 3 = C(n-1) + 3 + C(n-2) + 3      On pose D(n) = C(n) + 3
D(n) = D(n-1) + D(n-2) <=> D(n) - D(n-1) - D(n-2) = 0
Equation caractéristique : Delta = 5 > 0
q1 = (1 + sqrt(5)) / 2      q2 = (1 - sqrt(5)) / 2
C(n) = D(n) - 3 = A*q1**n + B*q2**n - 3

C(n) = 0 ne fait pas de sens, le coût du n ième terme est non nul car renvoie aun-1 + bun-2
Je suppose une erreur et prend C(1) = 0, car renvoie directement le terme U0 comme pour C(1)

Pour C(0) = 0
==> A + B = 3

Pour C(1) = 0
==> A(1+sqrt(5)) + B(1-sqrt(5)) = 6
==> (A+B) + (A-B)*sqrt(5) = 6
==> A-B = 3*sqrt(5)/5
==> A = 3*sqrt(5)/5 + B

==> 3*sqrt(5)/5 + B + B = 3 ==> B = (3/2)(1-sqrt(5)/5)
==> A = 3 - B ==> A = 3 - (3/2)(1-sqrt(5)/5) ==> A = 3((1/2) + sqrt(5)/10)


Ordre de grandeur : C(n) =  A*q1**n + B*q2**n - 3
q2 = (1 - sqrt(5)) / 2      2 < sqrt(5) < 3 => -2 < 1 - sqrt(5) < -1 => -1 < q2 < -1/2 < 0
-1 < q2 < 0 => B*q2^n terme négligeable pour n grand

O(C(n)) = (1+sqrt(5))/2)^n

Fonction itérative par somme des C(n) : C(n) par double récurrence ?
"""

def C(n):
    if n == 1 or n == 0:
        return(0)
    return(C(n-1) + C(n-2) + 3)

