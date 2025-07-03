## Exercice 4 : DM du DS d'info
#Arnaud Capitan MPSI B

## a]

"""
Si la liste donne a comme élu, alors a est présent dans plus de N//2 votes
Donc il existe n entier naturel n>N//2 tel que n est le nombre de votes reçu par a
Au sens large, on prend cet entier n strictement supérieur à N//2
De plus, tous les autres entiers b distincts de a (les autres candidats)
apparaissent nécessairement au plus N - n < N//2 fois

Par définition, on a donc a candidat
a élu => a candidat


On peut aussi voir la définition autrement :
Si b représente tous les autres candidats, il suffit d'avoir n(a) > n(b) pour que a soit un postulant.
En effet, on a alors n le nombre de voix du candidat 'a'
n <= N, les autres candidats ont alors k < n,
k < n <= N On prend
Cas 1 : p l'écart entre n et N, k + p < N donc k + p <= N
Cas 2 : q l'écart entre k et n, k + q = n <= N
k + p (ou q) <= N nous donne  k <= N - p (ou q), le candidat apparaît bien N-p (ou N-q) fois dans la liste
"""

## b]

"""
Si a est un postulant de L, alors il existe n>N//2 tel que voix(a) <= n et voix(b) <= N - n (autres candidats)
Par définition, si a est postulant de L, alors tous les autres candidats ont au plus N - n < N//2 voix
Or, il faut avoir un nombre de voix strictement supérieur à la moitié soit :    voix > N//2
Donc a postulant => autres candidats b non élu
"""

## c]

"""
La liste [i1,i2,i3,i4,i5,i6,i6,i6] donne un postulant i6 pour n € {5;6;7}
i6 n'apparaît que 3 fois dans une liste de 8 candidats, on a ainsi i6 postulant mais pas élu
"""

## d]
# i]


"""
Ent [ n ] désigne la partie entière de n

La liste LD ne donne pas d'élu, donc :   max_voix_candidt_possible_LD <= Ent[ (N+1)/4 ]
a un postulant pour la valeur l de LG ===> Tous les autres candidats ont au plus Ent[ (N+1)/2 ] - l voix

Donc un autre candidat, dans le meilleur cas, aura  Ent [ (N+1)/4 ] + Ent [ (N+1)/2 ] - l
On a l > Ent [ (N+1)/4 ] par définition de a postulant de rang l ===> Nombre_voix_max_autres_candidats < Ent [ (N+1)/2 ]

Les autres candidats ne peuvent être élus et peuvent avoir pour nombre de voix maximum n < Ent [ (N+1)/2 ]

On a 'a' un postulant pour la valeur l de LG donc :

'a' a plus de voix que tous les autres candidats de LG. Toutefois, rien ne garantit d'avoir suffisamment de voix
dans le liste LD

Exemple 'a' postulant dans LG et postulant dans L
[a,a,a,i1,i1,i2,i3,i4] [i1,i1,i4,i5,i6,i7]
On a aucun élu dans la liste LD, 'a' postulant pour l = 5 dans LG, mais a n'est pas postulant de L
Même si 'a' est élu dans LG, rien ne garantit que 'a' est un postulant

Exemple : [a,a,a,a,a,i1,i1,i1] [i1,i1,i1,i1,i2,i2,i2,i2]
'a' élu à gauche, donc 'a' postulant d'après 1] dans LG (ici pour l=5)
pas d'élu dans LD, pourtant i1 postulant pour n = 11, mais pas 'a'

Il est possible d'avoir 'a' postulant dans L pour 'a' postulant dans LG

"""

#ii]
#A]

"""
On a un candidat C qui est postulant pour les valeurs l et m respectivement dans les listes LG et LD
Ainsi, on a tous les autres candidats de
 * la liste gauche qui ont au plus Ent[(N+1)/2] - l voix, l > Ent [N+1 /4], soit nG < Ent[N+1 /4]
 * la liste droite qui ont au plus Ent[(N+1)/2] - m voix, m > Ent[N+1 /4], soit nD < Ent[N+1 /4]
 Nombre max de voix possible au total : nTOT < N+1 - (l + m) pas d'autres candidats élus possibles
 (car l et m > Ent[N+1 /2])

Pour le candidat C :
 * la liste gauche nG > Ent[(N+1)/2] - l (plus de voix que les autres candidats de LG)
 * la liste droite nD > Ent[(N+1)/2] - m (que LD)

 Nombre de voix total : n(C) > N+1 - (l+m) donc n(C) > nTOT, le candidat C a plus de voix que tous les autres,
 il est un postulant pour n = l+m de L
 """

#B]
"""
[a,a,c,d,e] [a,a,b,b,b] a postulant pour l = 2 de LG, b postulant pour m = 3 de LD
Pourtant, même avec a =/= b et l<m, a est un postulant de L pour n = 7 (et non b)

Je ne suis pas sûr d'avoir bien compris le concept de postulant.
"""

##ii) C]
'''
a =/= b et m = l

Tous les autres candidats ont dans la liste de gauche moins de N+1/4 voix (stricte), de même pour la liste droite
Tous les autres candidats ont au total moins de N+1/2 voix strictement, pas d'élu pour les autres candidats

Pour le candidat a, il aura au maximum m voix, et de même pour b, avec respectivement Ent[N+1 /2] - m voix dans l'autre liste

Donc le candidat a aura au total au maximum m + Ent[N+1 / 2] - m (large) ce qui correspond à la moitié
=> Nombre de votes insuffisant pour être élu
De même pour b par raisonnement similaire
=> Pas d'élu
'''

## 5] Pour faire cette question, on admet les résultats des questions précédentes malgré les contre-exemples

def nbreA(a,sond):
    n=0
    for candidat in sond :
        if candidat == a:
            n+=1
    return(n)

def miG(sond):
    return (sond[0:len(sond)//2])

def miD(sond):
    return (sond[len(sond)//2:])



#On a 'a' postulant pour n(a) > n(b), avec b tous les autres candidats
def postulant(sond): #len(sond) = N
    max_n = 0 #Nombres de voix du postulant
    Postulant = 0 #Postulant
    max = 0 #Nombres de voix max du deuxième plus grand (pour déterminer le 'rang' du postulant)
    candidat_deja_croise = []
    for candidat in sond :
        if candidat not in candidat_deja_croise :
            candidat_deja_croise.append(candidat)
            p=nbreA(candidat,sond)
            if p > max :
                if p > max_n:
                    max = max_n
                    max_n = p
                    Postulant = candidat
                else :
                    max = p
    if max_n > len(sond) // 2:
        return(Postulant,len(sond) - max)
    return(-1,0)
##Cout de cette fonction 0(n²)

#Exemple 1:

assert postulant([1,2,3,4,5,5,5,5,6,6]) == (-1,0) #Pas assez de voix pour 5 le postulant

assert postulant([1,2,3,4,4,4,4]) == (4,6) #4 postulant pour l = 6 (4 élu)


#Sachant que l'on va s'intéresser surtout à la méthode diviser pour régner, on crée une nouvelle fonction

def postulant_v2(sond): #Soit 3 soit 2, coût égal à 8 pour les comparaisons, donc O(1)
    N = len(sond)
    if N == 3:
        if sond[0] == sond[1] == sond[2]:
            return(sond[0],3,N)
        if sond[0] == sond[1] or sond[1] == sond[2]:
            return(sond[1],2,N)
        if sond[0] == 2:
            return(sond[0],2,N)
        else:
            return(-1,0,N)
    if sond[1] == sond[0]:
        return(sond[0],2,N)
    return(-1,0,N)


""" Informations à notre disposition :

a =/= b et m=l pas d'élu    Cas 1
a =/= b et m > l => renvoie (b, N/2 + m - l) Cas 2
a = b, renvoie (a, m + l) Cas 3


Cas 4
Question d] i) Admettons que la proposition soit toujours vraie (malgré le contre-exemple)
-> On aurait n = N - l, n > N/2 (on aurait Ent[(N+1)/4] < l < N/2, d'où N - l > N/2
"""

def elu4(sond):
    if len(sond) <= 3:
        return(postulant_v2(sond))
    (a,b,L1) = elu4(miG(sond))
    (c,d,L2) = elu4(miD(sond))
    if a == -1 and c == -1:
        return(-1,0,L1+L2) #Pas d'élu dans les deux listes -> Pas d'élu
    if a == -1: #On a éliminé la possibilité de c=-1, donc on a un postulant c
        return(c,L1+L2-d,L1+L2) #Cas 4
    if c == -1:
        return(a,L1+L2-b,L1+L2) #Cas 4
    if a == c:
        return(a, b + d,L1+L2) #Cas 3
    if b == d:
        return(-1,0,L1+L2) #Cas 1
    if d > b:
        return(c,L2 + d - b, L1 + L2) #Cas 2
    return(a,L1 + b - d, L1+L2) #Cas 2

#Pour une liste de taille n, on aura n division avec un coût de 0(1) -> Coût linéaire

assert elu4([12,12,88,45,12,45,12,12,88,45,12,88,12,45,12,88,12,56,12,12,12,12,88,12]) == (12, 17, 24)
"""
24 taille totale de la liste, '12' le postulant de n=17 (n=17 convient, on a 14 fois le candidat '12'
pour seulement 5 fois le candidats '8', n=17 convient
"""

#Je prends la liste contre-exemple a=1,i1=2,i2=3 elu4([a,a,a,a,a,i1,i1,i1,i1,i1,i1,i1,i2,i2,i2,i2]) -> (1,10,16)
#Pourtant ce n'est pas a mais i1 le postulant de la liste
#Ce problème fait qu'il faudrait soit corriger l'erreur (pourquoi cet exemple n'est pas valable)
# On pourrait aussi ajouter une vérification avec nombreA qui nous renverrai (-1,0) pour la liste si
#il n'y a pas confirmation que le postulant est un élu dans la liste (auquel cas -> (-1,0)






