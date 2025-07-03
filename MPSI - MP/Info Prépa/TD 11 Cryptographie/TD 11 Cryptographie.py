import math as m

## Exercice 1 :

# Question 1 :

def moyenne(L):
    if len(L)==0:
        print("Liste vide")
        return()
    Moy = 0
    for i in range (len(L)):
        if type(L[i]) == str :
            Moy+=eval(L[i])
        else :
            Moy+=L[i]
    Moy*=(1/len(L))
    return(Moy)

def ecart_type(L):
    Moy = moyenne(L)
    variance = 0
    for i in range (len(L)):
        if type(L[i]) == str :
            variance+=(eval(L[i]) - Moy)**2
        else :
            variance+=((L[i]) - Moy)**2
    variance*=(1/len(L)) #Cas len(L) = 0 déjà traité dans moyenne
    e_type = m.sqrt(variance)
    return(e_type)

notes2 = open("notes2.txt", "w")
notes = open("notes.txt", "r")
for ligne in notes :
    donnees = ligne.strip().split(";")
    nom = donnees[0]
    prenom = donnees[1]
    liste_notes=donnees[2:]
    moy = moyenne(liste_notes)
    e_type = ecart_type(liste_notes)
    notes2.write(nom + ";" + prenom + ";" + str(moy) + ";" + str(e_type) + "\n")
notes.close()
notes2.close()

## Exercice 2 : Le chiffre de César

#Question 2 :
global alphabet
alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
global alphabet_complet
alphabet_complet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def decale(lettre, shift, alphabet_ref): #alphabet_ref désigne l'alphabet utilisé
    if lettre in alphabet_ref : #Si la lettre est dans l'alphabet
        pos = alphabet_ref.index(lettre)
        return (alphabet_ref[(pos + shift)%len(alphabet_ref)])
    return(lettre) #Sinon return lettre

assert decale("A", 4, alphabet) == "E"
assert decale("A", -1, alphabet) == "Z"
assert decale(".", 7, alphabet) == "."

#Question 3 :

def code(texte, shift,alphabet_ref):
    texte2=""
    for i in range (len(texte)): #On suppose texte une chaîne de caractère de taille quelconque
        texte2+=(decale(texte[i],shift,alphabet_ref)) #Pas de return, la fonction est un processus
    return(texte2)

poeme_texte = open("poemes.txt", "r")
poeme_code = open("texte-code.txt", "w")
for ligne in poeme_texte :
    ligne_encode = code(ligne, 5, alphabet_complet)
    poeme_code.write(ligne_encode + "\n")
poeme_texte.close()
poeme_code.close()

## Exercice 3 : Analyse du chiffre de César

#Question 4 :

def occurences(texte,alphabet_ref):
    L=[0]*len(alphabet_ref) #Liste de 0 de la taille de l'alphabet
    for char in texte: #Pour chaque caractère du texte
        if char in alphabet_ref : #Si le caractère est dans l'alphabet
            pos = alphabet_ref.index(char)
            L[pos]+=1
    return(L)

#Question 5 :

def maximum(liste):
    max=0 #Liste de 0 initialement : si tous les caractères sont des caractères spéciaux, le maxium sera 0
    pos=-1
    for nombre in liste:
        if nombre > max:
            max = nombre
            pos=liste.index(nombre)
    return(pos)

#Question 6 :

def trouve_shift(texte,alphabet_ref):
    pos_lettre = maximum(occurences(texte,alphabet_ref)) #Position lettre + fréquente texte dans alphabet
    if alphabet_ref == alphabet :
        shift = (pos_lettre - alphabet.index("E"))%26 #On suppose la lettre E la plus fréquente de l'alphabet français
        return(shift)
    shift = (pos_lettre - alphabet_complet.index("e"))%52 #Lettre e
    return(shift)


#Question 7 :

dechiffre = open("texte_dechiffre.txt", "w")
texte_secret = open("secret.txt", "r")
shift = trouve_shift(texte_secret.read(), alphabet)
print("Le cryptage utilisé est un décalage de :", shift)
shift*=-1
texte_secret = open("secret.txt", "r")
for ligne in texte_secret :
    ligne_dechiffre = code(ligne, shift, alphabet)
    dechiffre.write(ligne_dechiffre + "\n")
texte_secret.close()
dechiffre.close()

## Corélation et détection de la langue

#Question 8 : Le fichier s'appelle texte_dechiffre

texte = open("texte_dechiffre.txt", "r")
statTexte = occurences(texte.read(),alphabet)
texte.close()

#Question 9 :

stat_texte = open("stat-francais.txt", "r")
statFrancais=[]
for ligne in stat_texte :
    donnees = ligne.strip().split("\t") #Tabulation entre les stats, la tabulation s'écrit \t
    statFrancais.append(eval(donnees[1]))
stat_texte.close()

print()

#Question 10 :

def correlation(L1,L2):
    moy1 = moyenne(L1)
    moy2 = moyenne(L2)
    e_type1 = ecart_type(L1)
    e_type2 = ecart_type(L2)
    moy=0
    for i in range (len(L1)):
        moy+=((L1[i] - moy1)*(L2[i] - moy2))
    moy*=(1/(26*(e_type1*e_type2)))
    return(moy)

print("La correlation entre stat_texte et stat_francais est :", correlation(statFrancais, statTexte))

#Question 11 :

texte_secret = open("secret-europeen (copie).txt", "r")
dechiffre = open("secret_europeen (copie) dechiffre francais.txt", "w")
shift = trouve_shift(texte_secret.read(),alphabet)
print("Le cryptage utilisé est un décalage de :", shift)
shift*=-1
texte_secret = open("secret-europeen (copie).txt", "r")
for ligne in texte_secret :
    ligne_dechiffre = code(ligne, shift, alphabet)
    dechiffre.write(ligne_dechiffre + "\n")
texte_secret.close()
dechiffre.close()

"""
Il est difficile de comprendre ce qui est écrit -> On suppose ainsi l'utilisation d'une autre langue
"""

#Question 12 :

stats_langues = [statFrancais] #On récupère dans la liste les stats de l'alphabet français

stat_texte = open("stat-anglais.txt", "r")
statAnglais=[]
for ligne in stat_texte :
    donnees = ligne.strip().split("\t")
    statAnglais.append(eval(donnees[1]))
stat_texte.close()

stats_langues.append(statAnglais) #On récupère aussi dans la liste les stats de l'alphabet anglais

stat_texte = open("stat-allemand.txt", "r")
statAllemand=[]
for ligne in stat_texte :
    donnees = ligne.strip().split("\t")
    statAllemand.append(eval(donnees[1]))
stat_texte.close()

stats_langues.append(statAllemand) #Allemand

stat_texte = open("stat-espagnol.txt", "r")
statEspagnol=[]
for ligne in stat_texte :
    donnees = ligne.strip().split("\t")
    statEspagnol.append(eval(donnees[1]))
stat_texte.close()

stats_langues.append(statEspagnol) #Et espagnol


def trouve_shift_mieux(texte): #Uniquement en majuscule
    shift_utilise=0
    maximum=0
    langue=["Français","Anglais","Allemand","Espagnol"]
    for shift in range (26):
        for stats in stats_langues: #stats_langues contient l'alphabet Fr, An, Al, Esp dans cet ordre
            texte2 = code(texte,shift,alphabet)
            statTexte = occurences(texte2,alphabet) #Stats du texte à la position shift
            corr=correlation(stats,statTexte)
            if maximum < corr :
                maximum=corr
                Langue=langue[stats_langues.index(stats)]
                shift_utilise=shift
    print("La langue utilisée est :", Langue)
    print("Le shift de déchiffrement est :", shift_utilise)
    print("La corrélation est de :", maximum)
    return(shift_utilise)

def fichier_to_texte(fichier): #Permet de convertir un fichier en une longue chaîne de caractères
    texte = ""
    for ligne in fichier:
        ligne_collee=ligne.strip().split(",") #Suppression des virgules
        for i in range (len(ligne_collee)):
            texte+=ligne_collee[i]
    texte2 = ""
    for ligne in texte:
        ligne_collee=ligne.strip().split(".") #Suppression des points
        for i in range (len(ligne_collee)):
            texte2+=ligne_collee[i]
    return(texte2)

texte_secret = open("secret-europeen (copie).txt", "r")
dechiffre = open("secret_europeen (copie) dechiffre.txt", "w")
shift = trouve_shift_mieux(fichier_to_texte(texte_secret))
texte_secret = open("secret-europeen (copie).txt", "r")
for ligne in texte_secret :
    ligne_dechiffre = code(ligne, shift, alphabet)
    dechiffre.write(ligne_dechiffre + "\n")
texte_secret.close()
dechiffre.close()

## Exercice 5 : Le chiffre de Vigenère

#Question 13 :

def vigenere(texte,clef,alphabet_ref): #On suppose que le texte est une longue chaîne de caractère / clef est en chiffre
    texte_code=""
    for i in range (len(texte)):
        if texte[i] in alphabet_ref: #Si c'est une lettre de l'alphabet, on la décale selon le shift correspondant
            texte_code+=decale(texte[i],clef[i%len(clef)],alphabet_ref)
        else :
            texte_code+=texte[i] #Si c'est un caractère spécial, on ne change rien
    return(texte_code)

def texte_to_clef(txt): #Permet de fabriquer la liste clef avec les nombres à partir d'une chaîne de caractères
    clef=[]
    for i in range (len(txt)):
        clef.append(alphabet_complet.index(txt[i]))
    return(clef)

Txt_org="LE FUTUR DE LA CRYPTOGRAPHIE EST LA PHYSIQUE QUANTIQUE."
Txt_code=vigenere(Txt_org,texte_to_clef("FUTUR"),alphabet)
print(Txt_code)


#Question 14 :

"""
Sur des longs textes, en connaissant la taille de la clef, il est possible d'appliquer le principe
de trouve_shift (en supposant que la langue est française) sur toutes les n*k-lettre avec
k entier relatif et n la longueur de la clef.
Avec un grand échantillon de ces lettres, en comparant les occurences (soit avec l'alphabet français pour la lettre E / ou tous
les alphabets) il est possible de déterminer le mot clef.

L'avantage de ce système de chiffrement est qu'un message-clef de la longueur du message à encoder est incassable :
Une autre clef pourrait fournir un message clair cohérent en étant pourtant très différent du message initial.
Le chiffre de Beales utilisait par exemple la déclaration dindépendance des Etats-Unis
(source : L'Histoire des Codes Secrets, la partie arithmétique était mon 2e sujet du Grand Oral)
"""

def decrypte(texte,longueur,alphabet_ref): #alphabet  -> majuscules ou alphabet_complet -> maj et min
    echantillons_texte=[""]*longueur #On découpe le texte en longueur_clef parties
    for i in range (len(texte)): #Pour chaque caractère du texte
        if texte[i] in alphabet_ref: #S'il est dans l'alphabet
            echantillons_texte[i%longueur]+=texte[i] #On l'ajoute à la liste correspondante
    Mot_Clef=""
    Clef=[]
    for i in range (longueur):
        shift=trouve_shift(echantillons_texte[i],alphabet_ref) #On cherche le shift de chaque échantillon
        Mot_Clef+=alphabet_ref[shift] #On ajoute au mot_clef sa lettre correspondante
        shift*=-1
        Clef.append(shift) #On ajoute directement l'opposé du shift pour le déchiffrement
    print("Le mot-clef est :", Mot_Clef)
    texte_clair=""
    for i in range (len(texte)):
        if texte[i] in alphabet_ref:
            texte_clair+=decale(texte[i],Clef[i%longueur],alphabet_ref) #Si le caractère est dans l'alphabet
        else:
            texte_clair+=texte[i] #Sinon rajoute le caractère spécial
    return(texte_clair)

Txt_long_code="ahW lRX tbSUA YSFgJg, Jb PTbvNNgANSh YF BNNZtR Rm QO PQSn, Wt JgB UcAfNPtR R'NUdtVVime Zm UfqaHWxR Rm YfwhaS_fMWng (ma gCcUcANSh dZS YF tNSUCR SAg TzNSçiVXS) Xiz YcCgJg YJg a*Y-YJhBeJ iiJQ X SvgNSz WStNYWn Jh a Zi QcvTZSCe Rm QO PQSn. oDRH Ca UzNSR éHViaYWtYTb QJ kRX tRYhzRX, RS kbRdieFbB QSA TQkhWSvPJg (Xcqg ODRH t'FZxUFPmg TzNSçiVX xbZf YF tRYhzR s / cC YcCf Zmf OtcMOjRYg) NZ RXh cTgAVGZm IS QéhmeRWvRW tR awg QtRK. y'ODNShiTJ lR Qm XmAgèam IS PMWnSWSuRSh RXh dZ'Ca amfXOoR-QtRK lR Zi QcvTZSCe RC RSAfFUm à maHclRW mfY qaHOAfFPtR : HSS NZhzR QtRK xbZfzNNh STizaNf hS uRXgiTJ kYFWz HcpéWSvg Sv éhiaY xbZfBNSh gWèA IWnSéfmaY lh amfXOoR WvVYWiY. TR QpVKTzR Rm gSiYJg hYWtVXOqg die SFRRdtR Zi IékYFfigNcv I'qaIéxRSRiaHS QJg rYOBf-IvVX (fTizPJ : q'PVXhwVWS QJg pTRmf GmPWSBf, tN dieYWm FfqgMaégNeCR éBNNh ZTb 2J AhOSB Ii tWOvQ CzNQ)"

#Le texte a été chiffré par la fonction vigenere avec un mot clef de taille 4

# La taille du mot-clef est 4, et l'alphabet de référence est alphabet_complet
#La fonction decrypte fonctionne
