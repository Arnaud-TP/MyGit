#tD 22 oct Arnaud Capitan MPSI B
import math as m
import random as rd

## Fonction création de système aléatoire de taille n (nombre inconnus = nombre équations)

def creA(n,a,b): # creation de liste de n lignes de n+1 termes entier entre a et b
    A=[]
    for i in range (n):
        lignei=[]
        for k in range(n+1):
            lignei.append(rd.randint(a,b))
        A.append(lignei)
    return A
S=creA(6,-2,12)
Smemo=[S[k].copy() for k in range (len(S))] # copie ligne par ligne la liste S



# exemple [[5, 0, 7, 5], [4, 8, -1, 8], [10, 6, 11, 1]]

## Fonction affichage

def affichage(S):
    for ligne in range(len(S)):
        print(S[ligne]) #l'arrondi a déjà été fait dans échelonnage

print('\nAffichage de la matrice S\n')
affichage(S)


#Question 1 Veuillez définir une fonction echange de paramètres S, n1,n2 qui effectue l'echange des lignes n1 et n2 de S.

## Fonction échange
def echange(S,n1,n2):
    #on suppose n1 et n2 inférieurs à len(S)
    m=len(S[0]) # le nombre des termes de la ligne 0 de S
    for col in range(m):
        S[n1][col],S[n2][col]=S[n2][col],S[n1][col]
    # pas de return la liste de listes subit "in place" les opérations

""" Exemple
echange(S,1,2)
affichage(S)
#[[5, 0, 7, 5], [10, 6, 11, 1], [4, 8, -1, 8]]
affichage(Smemo)   # on vérifie que la liste Smemo est bien conservée.
#[[5, 0, 7, 5], [4, 8, -1, 8], [10, 6, 11, 1]]
"""

#Question 2  # définir une fonction Combine de paramètres S,n1, alpha1, piv) qui effectue Ligne_n1=Lignen1+alpha1.Ligne piv
#Attention comme dans le modèle vous effectuerez un exemple et afficherez votre résultat.

S=[Smemo[k].copy() for k in range (len(S))] #On récupère la liste Smemo initiale

## Fonction combine

def combine(S,n1,alpha,piv):
    m=len(S[0])
    for col in range(m):
        S[n1][col] += alpha*piv[col]

""" Exemple
combine (S,1,4,S[2])
affichage(S)
# [[1, 12, 10, 6], [18, 40, 14, 30], [2, 7, 2, 6]]
affichage(Smemo)
#[[1, 12, 10, 6], [10, 12, 6, 6], [2, 7, 2, 6]]
#On a bien une combinaison de la ligne 2 et de 4 fois la ligne 3
"""

#Question 3 Définir cherchposMax qui cherche et trouve la psition du plus grand coefficient en VALEUR ABSOLUE placé entre la ligne k et la dernière ligne et placé dansla colonne k .
#On testera son code sur une matrice d'exemple en utilisant creA (première cellule) pour n valant au moins 6.

S=[Smemo[k].copy() for k in range (len(S))]

## Fonction cherchposMax

def cherchposMax(S,k):
    ligne=k
    record=abs(S[k][k]) # initialisation au point S_k,k de la ligne et la colonne k (en diagonale)
    for pos in range(k,len(S)):
        if abs(S[pos][k]) > abs(record) :
            record = S[pos][k]
            ligne = pos
    return ligne

#[[6, 3, 3, -2, 1, 6, 3], [8, 5, -2, 0, 5, 4, -2], [10, -1, 11, 2, -1, 7, 10], [-1, 10, 4, 9, 2, 9, 11], [5, 5, 8, 9, -2, 7, 2], [-2, 6, 1, 10, 10, 2, 12]]
#Pour la première colonne, la fonction nous renvoie 2, soit la troisième ligne



#Question 4 Définir une fonction fois qui multiplie une ligne n1 par un nombre alpha
S=[Smemo[k].copy() for k in range (len(S))]

## Fonction fois

def fois(S,n1,alpha):
    m=len(S[n1])
    for col in range(m):
        S[n1][col] *= alpha

""" Exemple
affichage(S)
#[[2, 6, -2, 5, -2, 6, 5], [10, 9, -2, 10, -2, 12, 7], [1, -2, 2, 5, 8, 1, -1], [5, 6, 10, 2, 8, 8, -1], [-1, -1, 0, 8, 1, -1, 9], [9, 4, 1, 1, 5, 4, 1]]
fois(S,1,8)
affichage(S)
#[[2, 6, -2, 5, -2, 6, 5], [80, 72, -16, 80, -16, 96, 56], [1, -2, 2, 5, 8, 1, -1], [5, 6, 10, 2, 8, 8, -1], [-1, -1, 0, 8, 1, -1, 9], [9, 4, 1, 1, 5, 4, 1]]
"""

#Question 5 Définr le programme de mise en forme échelonnée si possible sans problème

## Fonction échelonnage

def echelonnage(S):
    for m in range(len(S)):
        echange(S,m,cherchposMax(S,m))
        if abs(S[m][m]) < 0.001 :
            print('\nPivot nul à la position :\n', m)
            return()
        fois(S,m,1/S[m][m]) #On a placé le premier pivot à 1
        for i in range (m+1,len(S)):
            combine(S,i,-S[i][m],S[m])
    for ligne in range(len(S)):
        for col in range(len(S[0])):
            if col<ligne:
                S[ligne][col]=0
            else :
                S[ligne][col]=round(S[ligne][col],4)

echelonnage(S)
print('\nEchelonnage de S\n')
affichage(S)

""" Exemple
affichage(S)

[8, 4, 1, 1, 11, 2, 9]
[-1, 12, 7, 1, 12, 5, 9]
[7, 11, 2, -2, 1, 8, 11]
[0, 11, 6, 4, 7, -2, 10]
[12, 8, 10, 6, 12, 4, 8]
[2, 6, -1, -1, 5, 10, 9]

echelonnage(S)
affichage(S)

[1.0, 0.667, 0.833, 0.5, 1.0, 0.333, 0.667]
[0, 1.0, 0.618, 0.118, 1.026, 0.421, 0.763]
[0, 0, 1.0, 0.806, 1.613, -0.387, -0.194]
[0, 0, 0, 1.0, -0.895, -2.076, 0.434]
[0, 0, 0, 0, 1.0, 0.017, 0.25]
[0, 0, 0, 0, 0, 1.0, -0.003]

"""
    # selon l'algo pour la diagonale de 0 à n
                  #chercher sous la diagonale la position du max
                  # echanger les deux lignes : on nomme piv cette diagonale
                  # pour toutes les lignes sous piv,
                        #si S[piv][piv]!=0
                              #calculer alpha et combiner pour creer des 0
                        # sinon stopper le processus par  return


S=[Smemo[k].copy() for k in range (len(S))]


## Fonction résolution

def resolution(S):
    echelonnage(S)
    for m in range (1,len(S)):
        ligne_piv = S[-m] #La ligne pivot est la dernière ligne avant celle souhaitée, donc S[-m]
        colonne_modif = len(S) - m
        for ligne in range (len(S)-m):
            coefficient = S[ligne][colonne_modif] #On suppose que le système est de Cramer
            combine(S,ligne,-coefficient,ligne_piv)
    for ligne in range(len(S)): #Présentation des résultats
        for col in range(len(S[0])):
            if S[ligne][col] == int(S[ligne][col]):
                S[ligne][col]=int(S[ligne][col]) #On arrondi à l'entier pour supprimer les décimales
            else :
                S[ligne][col]=round(S[ligne][col],3)

print('\nRésolution de S\n')
resolution(S)
affichage(S)

""" Exemple
affichage(S)

[8, 4, 1, 1, 11, 2, 9]
[-1, 12, 7, 1, 12, 5, 9]
[7, 11, 2, -2, 1, 8, 11]
[0, 11, 6, 4, 7, -2, 10]
[12, 8, 10, 6, 12, 4, 8]
[2, 6, -1, -1, 5, 10, 9]

résolution(S)
affichage(S)

[1, 0, 0, 0, 0, 0, 0.278]
[0, 1, 0, 0, 0, 0, 1.125]
[0, 0, 1, 0, 0, 0, -1.124]
[0, 0, 0, 1, 0, 0, 0.652]
[0, 0, 0, 0, 1, 0, 0.25]
[0, 0, 0, 0, 0, 1, -0.003]

"""

## Fonction affichage de la solution

S=[Smemo[k].copy() for k in range (len(S))]

def aff_sol(S):
    print('\nLe système à résoudre est :\n')
    affichage(S)
    resolution(S)
    print('\nAffichage de la solution de S :\n')
    for k in range (len(S)):
        print('x', k+1,'=',S[k][-1]) # S[k][-1] dernier coefficient (donc solution) de la ligne k

aff_sol(S)

""" Exemple
affichage(S)

[8, 4, 1, 1, 11, 2, 9]
[-1, 12, 7, 1, 12, 5, 9]
[7, 11, 2, -2, 1, 8, 11]
[0, 11, 6, 4, 7, -2, 10]
[12, 8, 10, 6, 12, 4, 8]
[2, 6, -1, -1, 5, 10, 9]

aff_sol(S)
affichage(S)


Affichage de la solution de S :

x 1 = 0.278
x 2 = 1.125
x 3 = -1.124
x 4 = 0.652
x 5 = 0.25
x 6 = -0.003
"""