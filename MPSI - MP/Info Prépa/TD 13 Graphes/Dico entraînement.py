### I Exercice 1 - Questions indépendantes

import math as m
import matplotlib.pyplot as plt

## Q1

def suite(a,n):#u0, rang n
    u = a
    assert n >= 0
    for i in range (n):
        u = 2*u + 3 #un=1=2*un + 3
    return u

assert suite(2,2)== 17 #u0 = 2, u1 = 7, u2 = 17
assert suite(30,0)==30 #u0 = 30 renvoie u0

print(suite(3,5)) #pour u0 = 3, u5=189

## Q2

def occurrences(t):
    n = len(t) #Longueur de t
    d = dict() #Création d'un dictionnaire
    for i in range(n):
        if t[i] not in d.keys(): #Si t[i] ne fait pas partie du dictionnaire
            d[t[i]] = 1 #On le crée (attribution de la valeur 1)
        else:
            d[t[i]] += 1 #On lui ajoute 1
    return d

assert occurrences(['c','b','a','a','b','a','b']) == {'c':1, 'a': 3, 'b': 3}



def plus_frequent(t):
    n = len(t)
    assert n > 0 #longueur de la liste supérieur strictement à 0 (sinon pas de liste)
    for i in range (n):
        assert type(t[i]) == str #Les informations contenues dans la liste sont des caractères
    d = occurrences(t) #On récupère les occurences
    max=d[t[0]]
    position = 0
    for i in range (n):
        if max < d[t[i]]: #Si le max est dépassé
            max = d[t[i]]
            position=i #On récupère sa position
    return t[position]#On renvoie le caractère à la position


assert plus_frequent(['a','b','a','b','c','c','c','a','a']) == 'a'

assert plus_frequent(['a','a','b','a','b','a']) == 'a'


##Q3

def inverse(d):
    d_inverse = { d[cle ] : cle for cle in d }
    return d_inverse

assert inverse({'a': 3, 'b': 3}) == {3: 'a', 3: 'b'}


### II Exercice 2

## Q4

def distance(P1 :tuple, P2 :tuple)->float:
    return m.sqrt((P1[0]-P2[0])**2+(P1[1]-P2[1])**2) #racine de la somme des carrés

assert distance((0,0),(3,4)) == 5
assert distance((0,1),(0,3)) == 2

## Q5

t1 = [(0,0),(3,4),(3,5),(7,6)]

'''print(len(t1))
print(t1[1][0])
print(distance (t1[1] ,t1[2]))
Soit:
len(t1) renvoie le nombre d'éléments de t1. On a 4 tuples donc len(t1) = 4
t1[1][0] renvoie le 0ième élément du tuple de position 1 dans t1.
distance(t1[1],t1[2]) renvoie la distance entre les points désignés par le tuple de position 1 et de position 2'''

p = [(1,1),(1,2),(1,4),(8,7),(0,1)]

assert len(p)==5
assert p[3][1] == 7
assert distance(p[0],p[1])==1



## Q6

def max_abscisses(t):
    n=len(t)
    assert n > 0 #Vérification de la longueur de la liste
    max = t[0][0] #Le premier est le max
    for i in range(n):
        if t[i][0] > max: #On compare avec les autres
            max = t[i][0] #Si plus grand trouvé on le remplace
    return max

assert max_abscisses([(7,1),(15,4),(9,5),(4,6)]) == 15


## Q7

def distance_totale(t):
    n = len(t)
    assert n > 0
    distance_totale = 0 #Pour chaque élément on rajoute à la distance la distance entre le point i et i+1
    for i in range(len(t)-1): #On s'arrête à len(t) - 1, le point en len(t) sera pris par i+1
        distance_totale = distance_totale + distance(t[i],t[i+1])
    return distance_totale

assert distance_totale([(0,0),(3,4),(4,4),(4,5)]) == 7


## Q8

def liste_abscisses(t):
    n = len(t)
    assert n > 0
    liste_abscisses = []
    for i in range(n): #Pour tous les éléments de la liste
        liste_abscisses.append(t[i][0]) #On rajoute chaque abscisse à la liste, qu'on appelle par t[i][0]
    return liste_abscisses

assert liste_abscisses([(8,0),(5,4),(2,5),(1,3)]) == [8, 5, 2, 1]

def liste_ordonnees(t):
    n = len(t)
    assert n > 0
    liste_ordonnees = []
    for i in range(n):
        liste_ordonnees.append(t[i][1])#On rajoute chaque ordonnée à la liste, qu'on appelle par t[i][0]
    return liste_ordonnees

assert liste_ordonnees([(8,0),(5,4),(2,5),(1,3)]) == [0, 4, 5, 3]


##Q9

def affiche(t):
    lx = liste_abscisses(t) #On récupère la liste des abscisses
    ly = liste_ordonnees(t) #Ordonnées
    plt.figure()
    plt.title("Tracé de t")
    plt.plot(lx,ly, color='red')
    plt.grid()
    plt.show()

affiche([(8,0),(5,4),(2,5),(1,3)])