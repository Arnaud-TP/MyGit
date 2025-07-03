#Arnaud CAPITAN MPSI B
#Arithmétique

## Nombres premiers

def nombres_premiers_fonction(Max):
    nombres_premiers = [2] #On initialise la liste des nombres premiers avec son premier élément
    for i in range (3,Max+1): #Pour tous les entiers allant de 3 à Max inclus
        nombres_premiers.append(i) #On l'ajoute à la liste
        for element in nombres_premiers: #Pour chaque nombre premier
            if i % element == 0 and i != element:  #Si i est divisible par l'un de ces nombres
                nombres_premiers.pop() #On l'enlève
                break #Arrêt de la boucle
    return(nombres_premiers)

## PGCD et facteurs communs

def facteurs_premiers(a): #On travaille pour a entier naturel non nul
    f_p_a = [] #Création de la liste contenant les facteurs premiers de a
    nombres_premiers=nombres_premiers_fonction(a)
    for element in nombres_premiers : #Pour chaque nombre premier
        if a == 1 : #Si a n'a pas de facteurs premiers
            exit #On sort de la boucle
        while (a % element == 0): #Tant que a est divisible par un de ces nombres premiers
            a = a // element  #On divise a par cet élément
            f_p_a.append(element) #On ajoute l'élément à la liste des facteurs premiers
    return(f_p_a)

def pgcd(a,b):
    a = abs(a) #On travaille avec des entiers naturels
    b = abs(b)
    if a == b: #Cas où a=b, on suppose a et b non tous nuls
        return(a)
    if a == 0 and b != 0:
        return(b) #PGCD(0,n) n non nul est n
    if b == 0 and a != 0:
        return(a)
    if a == 1 or b == 1: #Cas où nombre égal à 1
        return(1)
    f_p_a = facteurs_premiers(a) #Cas général
    f_p_b = facteurs_premiers(b)
    diviseurs_communs=[1] #1 est un diviseur commun de a et de b
    for element in f_p_a : #Pour chaque élément diviseur de a
        if element in f_p_b : #S'il divise b aussi
            diviseurs_communs.append(element) #On l'ajoute à la liste des diviseurs communs
            f_p_b.remove(element) #On le supprime de la liste de b pour éviter les doublons
    c=1 #Le fameux PGCD
    for element in diviseurs_communs : #Pour chaque élément de la liste des facteurs communs
        c*=element #On multiplie le PGCD par ces facteurs (la liste est non vide car contient 1)
    return(c)

"""
#Possibilité d'algorithme plus simple en utilisant PGCD(a,b) = PGCD(b,r) avec r = a - bq
def pgcd2(a,b):
    while b != 0 :
        a,b=b,a%b #La dernière étape donnera le PGCD
    return(a)
"""


## Division euclidienne (entiers naturels puis relatifs)
"""
Le théorème de la division euclidienne dit que pour tout couple d'entiers relatifs (a,b),
il existe un unique couple d'entiers (q,r) q entier relatif et r entier naturel tel que :
a = bq + r et 0 <= r < |a| (valeur absolue de a)
"""

def div_eucl_naturels(a,b): #Avec des entiers naturels exclusivement
    q=0 #Initialisation du quotient et du reste
    r=a
    while a >= b : #Tant que b est plus petit que a
        a-=b #On soustrait b à a
        q+=1 #On incrémente le quotient
        r=a #On réattribue le reste
    return(q,r)

def div_eucl(a,b): #Avec des entiers relatifs
    if b == 0:
        print("Erreur division par 0")
        return()
    if a >= 0 and b > 0: #Cas a et b positifs
        return(div_eucl_naturels(a,b))
    if a >= 0 and b < 0: #Cas a positif b négatif
        q,r=div_eucl_naturels(a,-b)
        return(-q,r)
    if a < 0 and b > 0: #Cas a négatif b positif
        q,r=div_eucl_naturels(-a,b)
        if r == 0:
            return(-q,0)
        q = q+1 #On ajoute 1 afin de satisfaire la condition 0 <= r < |a| après *(-1)
        r = r-b #On retire le b correspondant (r est alors un nombre négatif)
        return(-q,-r) #On mutliplie par -1 car a<0, on satisfait la condition 2
    q,r=div_eucl_naturels(-a,-b) #Cas a et b négatifs
    if r == 0:
        return(q,0)
    q = q+1 #Même principe
    r = -r-b
    return(q,r)

#Quelques exemples :

assert div_eucl(192,23) == (8,8)
assert div_eucl(192,-23) == (-8,8)
assert div_eucl(-192,23) == (-9,15)
assert div_eucl(-192,-23) == (9,15)

## Algo euclide étendu (nous sert uniquement pour la solution particulière de Bézout)
"""
Exemple de l'algo d'Euclide simple :

24 = 5*4 + 4    -> 4 = 1*24 + (-4)*5
5 = 4*1 + 1     -> 1 = 1*5 + (-1)*4     -> 1 = 1*5 + (-1)*(1*24 + (-4)*5) -> 1 = (-1)*24 + 5*5

Même exemple avec l'algo d'Euclide étendu :

Première étape :
PGCD(24,5) = 1
24 => (1,0)
5 => (0,1)
4 = 1*24 + (-4)*5   4 => (1,0) + (-4)*(0,1), 4 => (1,-4)
4 =/= PGCD on recommence

Deuxième étape :
PGCD(5,4) = 1
5 => (0,1)
4 => (1,-4)
5 = 4*1 + 1 <=> 1 = 5 + (-1)*4, 1 => (0,1) + (-1)*(1,-4), 1 => (-1,5)
1=PGCD, on renvoie (-1,5)
"""

def combin(listeA,listeB,coeff): #Combinaisons des nombres d'une liste A + q*B
    if len(listeA) != len(listeB):
        print("Erreur données ! Combinaison impossible.")
        return()
    N = len(listeA)
    Liste_résultat=[0]*N
    for i in range (N):
        Liste_résultat[i] = listeA[i] + coeff*listeB[i]
    return(Liste_résultat)

def euclide_etendu(a,b,liste=[[1,0],[0,1]]): #Liste initialisée à (1,0) pour a et (0,1) pour b
    q,r=div_eucl(a,b) #Quotient et reste de la division euclidienne
    PGCD = pgcd(a,b) #PGCD(a,b) égal à PGCD(b,r1) égal à PGCD(r1,r2) etc...
    if r == PGCD: #Si le reste est égal au PGCD, l'algo termine
        return(combin(liste[0],liste[1],-q)) #On renvoie le couple correspondant
    return(euclide_etendu(b,r,[liste[1],combin(liste[0],liste[1],-q)])) #Sinon on recommence l'algorithme

#Exemples
assert euclide_etendu(24,5) == [-1,5]
assert euclide_etendu(-218,-947) == [-404,93]


## Algo équation diophantienne
"""
Théorie :
au + bv = c
Si PGCD(a,b) ne divise pas c, alors il n'y a aucune solution entière
Si PGCD(a,b) divise c :
Cas 1 : PGCD(a,b) = 1, on cherche une solution particulière aU+bV=1, puis on multiplie U et V par c
Cas 2 : PGCD(a,b) > 1, on divise a, b et c par ce PGCD, et on répète le cas 1
Dans les deux cas, on peut écrire A=a//PGCD, B=b//PGCD, C=c//PGCD
-> On a PGCD(A,B) = 1, on passe au cas 1 puis on mulitplie par C pour obtenir une solution particulière

Une fois la solution particulière trouvée :

a*u0 + b*v0 = a*u + b*v avec (u0,v0) la solution particulière
On remarque alors qu'il est possible de diviser de part et d'autre de l'équation par le PGCD
A*u0 + B*v0 = A*u + B*v avec PGCD(A,B) = 1 (pour le lemme de Gauss)
A(u0 - u) = B(v - v0)
A divise B(v - v0) et A ne divise pas B ==> A divise v - v0
Il existe k entier relatif tel que v - v0 = k*A  ==> v = v0 + k*A
A(u0 - u) = B(v - v0) et v - v0 = k*A  ==> u0 - u = k*B
v = v0 + k*A
u = u0 - k*B
On exploite ce dernier résultat dans notre algorithme
"""




def equation_diophantienne(a,b,c): #Résolution de au + bv = c pour (u,v) entiers relatifs
    PGCD = pgcd(a,b)
    if c % PGCD != 0:
        print("\nPas de solutions, PGCD(",a,",",b,") ne divise pas",c)
        return()
    UV=euclide_etendu(a//PGCD,b//PGCD) #Solution de a'U + b'V = 1, avec a' = a//PGCD, etc pour b' et c'
    Solution_particulière=combin([0,0],UV,c//PGCD) #Solution de a'U + b'V = c'
    print("\nUne solution particulière de ",a,"u +",b,"v =",c," est le couple U,V =",Solution_particulière)
    U=Solution_particulière[0]
    V=Solution_particulière[1]
    print("Les solutions de l'équation diophantienne : ",a,"u +",b,"v =", c,"sont u =",U,"- k*(",b//PGCD,") et v =",V,"+ k*(",a//PGCD,") pour k entier relatif.")

## Programme principal

print("Bienvenue dans le programme arithmétique.")
print("\nVous souhaitez :")
print("1. Calculer un PGCD")
print("2. Avoir une decomposition en facteurs premier d'un nombre")
print("3. Resoudre une equation diophantienne au + bv = c")
print("4. Avoir la liste des nombres premiers jusqu'a n")
print("Autre. Fin du programme\n\n")
choix = eval(input(""))
if choix == 1:
    print("\n\nBienvenue dans le programme de calcul PGCD(a,b)\n")
    a=int(input("Entrez le nombre a : "))
    b=int(input("Entrez le nombre b : "))
    print("Le PGCD de",a,"et de",b,"est : ", pgcd(a,b))
    print("\n\nFin du programme. Appuyez sur entrée pour terminer.")
    Fin=input()
if choix == 2:
    print("\n\nBienvenue dans le programme de décomposition en facteurs premiers\n")
    a=int(input("Entrez le nombre n (positif): "))
    if a < 1:
        print("Erreur de saisi ! n > 1 requis.")
        print("\n\nFin du programme. Appuyez sur entrée pour terminer.")
        Fin=input()
    else :
        print("La décomposition de",a,"est ",facteurs_premiers(a))
        print("\n\nFin du programme. Appuyez sur entrée pour terminer.")
        Fin=input()
if choix == 3:
    print("\n\nBienvenue dans le programme solveur d'equation diophantienne") #Pas de caractère à accent pour l'invite de commande
    print("Equation de la forme au + bv = c, pour u et v entiers relatifs a determiner")
    a=eval(input("Entrez le nombre a : "))
    b=eval(input("Entrez le nombre b : "))
    c=eval(input("Entrez le nombre c : "))
    if a == 0 or b == 0 or c == 0 :
        print("a,b et c doivent être non nuls !")
        print("\n\nFin du programme. Appuyez sur entree pour terminer.")
        Fin=input()
    else :
        equation_diophantienne(a,b,c)
        print("\n\nFin du programme. Appuyez sur entree pour terminer.")
        Fin=input()
if choix == 4:
    n=int(input("\n\nVous souhaitez calculer les nombres premiers jusqu'a n = "))
    if n < 2:
        print("\nn doit être au minimum égal à 2 !")
        print("\nFin du programme. Appuyez sur entrée pour terminer")
        Fin=input()
    else :
        print("Voici la liste des nombres premiers allant jusqu'a ", n)
        print(nombres_premiers_fonction(n))
        print("\n\nFin du programme. Appuyez sur entree pour terminer.")
        Fin=input()