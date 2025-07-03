"""
Le but de ce programme est de résoudre n'importe quel système LINEAIRE de taille donnée (nombre d'inconnus, nombre d'équations),
ou de dire si ce système est impossible / admet une infinité de solutions, et déterminer lesquelles
"""

import math as m
import random as rd
import time

## Fonction création de système selon l'utilisateur

def crea_util(nmb_inc,nmb_equa):
    A=[]
    for i in range (nmb_equa):
        lignei=[]
        for k in range (nmb_inc):
            print('Coefficient de x', k+1, 'de la', i+1, 'e équation :')
            a=eval(input(''))
            lignei.append(a)
        print('Dernier coefficient de la', i+1, 'e équation :')
        a=eval(input(''))
        lignei.append(a)
        A.append(lignei)
    return A

## Fonction création de système aléatoire
def creA(n,a,b): # creation de liste de n lignes de n+1 termes entier entre a et b
    A=[]
    for i in range (n):
        lignei=[]
        for k in range(n+1):
            lignei.append(rd.randint(a,b))
        A.append(lignei)
    return A

## Fonction affichage

def affichage(S):
    for ligne in range(len(S)):
        print(S[ligne])

## Fonction échange

def echange(S,n1,n2):
    #on suppose n1 et n2 inférieurs à len(S)
    m=len(S[0]) # le nombre des termes de la ligne 0 de S
    for col in range(m):
        S[n1][col],S[n2][col]=S[n2][col],S[n1][col]

## Fonction combine

def combine(S,n1,alpha,piv):
    m=len(S[0])
    for col in range(m):
        S[n1][col] += alpha*piv[col]

## Fonction cherchposMax

def cherchposMax(S,k):
    ligne=k
    record=abs(S[k][k]) # initialisation au point S_k,k de la ligne et la colonne k (en diagonale)
    for pos in range(k,len(S)):
        if abs(S[pos][k]) > abs(record) :
            record = S[pos][k]
            ligne = pos
    return ligne

## Fonction fois

def fois(S,n1,alpha):
    m=len(S[n1])
    for col in range(m):
        S[n1][col] *= alpha

## Fonction échelonnage

def echelonnage(S):
    for m in range(len(S)):
        echange(S,m,cherchposMax(S,m))
        if abs(S[m][m]) < 0.001 :
            print('\nPivot nul à la position :', m)
            S[m][m]=0
            return(1)
        fois(S,m,1/S[m][m]) #On a placé le premier pivot à 1
        for i in range (m+1,len(S)):
            combine(S,i,-S[i][m],S[m])
    for ligne in range(len(S)):
        for col in range(len(S[0])):
            if col<ligne:
                S[ligne][col]=0
            else :
                S[ligne][col]=round(S[ligne][col],4)
    return(0)

## Fonction résolution

def resolution(S):
    echelonnage(S)
    for m in range (1,len(S)):
        ligne_piv = S[-m] #La ligne pivot est la dernière ligne avant celle souhaitée, donc S[-m]
        colonne_modif = len(S) - m
        for ligne in range (len(S)-m):
            coefficient = S[ligne][colonne_modif] #On suppose que le système est de Cramer
            combine(S,ligne,-coefficient,ligne_piv)
    for ligne in range(len(S)):
        for col in range(len(S[0])):
            if S[ligne][col] == int(S[ligne][col]):
                S[ligne][col]=int(S[ligne][col])
            else :
                S[ligne][col]=round(S[ligne][col],3)

## Fonction affichage de la solution

def aff_sol(S):
    print('\nLe système à résoudre est :\n')
    affichage(S)
    resolution(S)
    print('\nAffichage de la solution de S :\n')
    for k in range (len(S)):
        print('x', k+1,'=',S[k][-1]) # S[k][-1] dernier coefficient (donc solution) de la ligne k

## Programme

print('Bienvenue dans le programme de résolution de système.')
while (1): #Boucle en cas d'échec de données
    print('\nVous souhaitez...')
    print('\n1. Résoudre un système donné \n2. Résoudre un système aléatoire \n3. Quittez\n')
    choix = eval(input())

    if choix == 3 :
        print('Fin du programme.')
        time.sleep(3)
        exit()

    if (choix != 1 ) and (choix != 2):
        print('\nErreur de données ! Il faut choisir 1, 2 ou 3\n')

    if choix == 1:
        n_inc = int(eval(input("\nNombre d'inconnues ?\n")))
        n_eq = int(eval(input("\nNombre d'équations ?\n")))
        S=crea_util(n_inc,n_eq)

        if n_inc > n_eq :
            yo=1


        if n_inc < n_eq : #Plus d'équations que d'inconnues ; on trouve l'unique solution et on vérifie le sys
            Smemo=[S[k].copy() for k in range (len(S))] #On copie la matrice S
            for m in range (n_inc): #On échelonne à partir des plus grand coefficients la matrice
                echange(Smemo,m,cherchposMax(Smemo,m))
                if abs(Smemo[m][m]) < 0.001 :
                    print('\nPivot nul à la position : ', m)
                    print("Supprimez l'inconnue en question.") #Un pivot nul sera ici considéré
                    print('\nFin du programme.')               #comme une erreur de l'utilisateur
                    time.sleep(6)
                    exit()
            print("\nOn détermine la solution unique du système\n")
            Scopy=[Smemo[k].copy() for k in range (n_inc)]
            aff_sol(Scopy)
            Résultat=[]
            for x in range (len(Scopy)): #On copie les résultats dans une liste
                Résultat.append(Scopy[x][-1])
            print('\nVérification des équations à partir de la solution.')
            for i in range (n_eq):
                verif=0
                for j in range (n_inc):
                    verif+=Résultat[j]*S[i][j]
                if abs(verif - S[i][-1])>0.01:
                    print('\nSystème impossible !')
                    print("L'équation de la ligne", i+1," n'est pas satisfaite !")
                    print('\n\nFin du programme.')
                    time.sleep(30)
                    exit()
            print('Toutes les équations ont été vérifiées.')
            print('Le système admet donc pour unique solution :')
            for k in range (len(Scopy)):
                print('x', k+1,'=',Scopy[k][-1])

        if n_inc == n_eq :
            aff_sol(S)

        print('\n\nFin du programme.')
        time.sleep(90)
        exit()

    if choix == 2:
        taille = int(eval(input("\nTaille du système ?\n")))
        if (taille<2):
            print('\nLa taille doit être supérieure ou égale à 2 pour avoir un système !')
            print('\nFin du programme.')
            time.sleep(3)
            exit()
        print('\nLes coefficients sont générés aléatoirement entre a et b entiers.\n')
        a=int(eval(input('Entrez a :')))
        b=int(eval(input('Entrez b :')))
        if (a>=b):
            print('\na doit être un entier inférieur strictement à b !')
            print('Fin du programme.')
            time.sleep(3)
            exit()
        S=creA(taille,a,b)
        aff_sol(S)
        time.sleep(90)
        exit()
