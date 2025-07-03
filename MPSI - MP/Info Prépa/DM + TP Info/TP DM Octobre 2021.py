## TP DM Exercices Octobre 2021

## Exercice 1 :

def est_bissextile(a):
    return((a%400==0) or (a%4==0 and a%100 != 0))

## Exercice 2 :

def DiviseFacile(n,b):
    q=0
    while n>=b:
        n-=b
        q+=1
    return(q,n)

def DiviseTout(n,b):
    if b == 0:
        print("Erreur division par 0")
        return()
    if n >= 0 and b > 0: #Cas n et b positifs
        return(div_eucl_naturels(a,b))
    if n >= 0 and b < 0: #Cas n positif b négatif
        q,r=div_eucl_naturels(n,-b)
        return(-q,r)
    if n < 0 and b > 0: #Cas n négatif b positif
        q,r=div_eucl_naturels(-n,b)
        if r == 0:
            return(-q,0)
        q = q+1 #On ajoute 1 afin de satisfaire la condition 0 <= r < |n| après *(-1)
        r = r-b #On retire le b correspondant (r est alors un nombre négatif)
        return(-q,-r) #On mutliplie par -1 car n<0, on satisfait la condition 2
    q,r=div_eucl_naturels(-n,-b) #Cas n et b négatifs
    if r == 0:
        return(q,0)
    q = q+1 #Même principe
    r = -r-b
    return(q,r)

## Exercice 3 :

Liste_pièces=[100,50,25,10,5,1]

def monnaie(Liste_pèces,n):
    Nombre_pièces=[]
    for i in range (len(Liste_pièces)):
        n_pièces, n = DiviseFacile(n,Liste_pièces[i])
        Nombre_pièces.append(n_pièces)
    return Nombre_pièces

## Exercice 4 :

caractères = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def changebase(b,n): #N = a0 + a1*b + a2*b² + ... + an*b^n
    ListeRep=[]
    r=n
    while r>=b:
        q,r=DiviseFacile(r,b)
        ListeRep = [r] + ListeRep #On met le résultat au début
        r=q
    ListeRep = [r] + ListeRep #Pour la dernière étape
    Rep='' #On crée la chaîne de caractères associée
    for i in range(len(ListeRep)):
        rep += caractères[ListeRep[i]] #Remplace les nombres par des lettres
    return(rep)

def lecture(b,chaine):
    rep = 0
    for char in chaine :
        nombre = caractères.index(char)
        rep=rep*b + nombre #a0 + b*(a1 + b(a2 + ...)
    return(rep)

## Exercice 5 :

#Question 1 :

LignInit=[1]
listLign=[LignInit]
Ligne=[1,2,1] # k parmi 2

def ligneSuit(lignePrec):
    ligneSuivante=[1]
    for i in range(len(lignePrec)-1):
        coeff=lignePrec[i] + lignePrec[i+1] #Ajout des coefficients selon la formule du triangle de Pascal
        ligneSuivante.append(coeff)
    ligneSuivante.append(1) #Le dernier coefficient
    return(ligneSuivante)

def fabriqBinom(listLign,n): #N'est pas une fonction mais un processus : modifie la liste listLign
    der_lig = listLign[-1] #Dernière ligne ajoutée sur listLign
    for i in range(n):
        Lp = ligneSuit(der_lig) #Ligne suivante p
        listLign.append(Lp)
        der_lig = Lp #On attribue de nouveau cette dernière valeur à der_lig
        print(Lp) #Ne retourne rien

#Question 2 :

def coeff_binome(n): #Ligne n
    Rep=[1] # 0 parmi n = 1
    coeff=1 #Initialisation du coeff
    for p in range (n): # 1 <= p+1 <= n
        coeff*=(n-p)/(p+1)
        Rep.append(coeff)
    return(Rep)

def fabriqdirec(listeDir,n):
    for i in range (1,n+1): # 1 <= i <= n
        listDir.append(coeff_binome(i))

listDir=[[1]]
fabriqdirec(listDir,6)

#Question 3 :

#La première méthode est plus efficace, car une division dans la deuxième méthode oblige
#un travail avec des flottants, ce qui est plus gourmand en calcul

def factorielle(n):
    if n == 0:
        return(1)
    return(n*factorielle(n-1))

def coef_binome(n,p): #Calcul directe de p parmi n = n!/p!(n-p)!
    return(factorielle(n)//(factorielle(p)*factorielle(n-p)))
#Division entière pour avoir un entier à la place d'un float

## Exercice 6 :

#Pour tout n appartenant à N, cos((n+1)x) + cos((n-1)x) = 2cos(nx)cos(x)
# => cos((n+1)x) = 2cos(nx)cos(x) - cos((n-1)x)

def cosnx(n,U):
    if n == 0:
        return(1)
    if n == 1:
        return(U)
    cos_prec=1
    cos_actu=U
    for i in range(n-1): # 0 <= i <= n-2, suite récurrente d'ordre 2? on a le n ieme terme
        cos_suiv= 2*cos(actu)*U - cos_prec
        cos_prec = cos_actu
        cos_actu = cos_suiv
    return(cos_suiv)











