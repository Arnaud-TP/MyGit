def taux(L1): #Cette fonction renvoie le gain / perte pour 100€ joué, ainsi que le taux de conversion freebet du match
	L = L1.copy()
	L.sort()
	a = L[0]
	b = L[1]
	c = L[2]
	G = 100/(1/a + 1/b + 1/c) - 100
	t = max((a-1)*(b-1)*(c-1)/(a*(b+c-2)),(c-1)*(1-1/a-1/b))
	return(round(t,3),round(G,2))

def find_games(D): #Dictionnaire de la forme D['Winamax'] = [{'team1': 'AVS Futebol SAD', 'team2': 'Maritimo', 'odds': [2.09, 2.98, 2.8]}]
	L = {}
	for site in D.keys():
		for elem in D[site]:
			if ((elem['team1'],elem['team2']) not in L.keys()) :
				if ((elem['team2'],elem['team1']) not in L.keys()):
					L[(elem['team1'],elem['team2'])] = [(site,elem['odds'])]
				else :
					L[(elem['team2'],elem['team1'])].append((site,elem['odds'].reverse()))
			else :
				L[(elem['team1'],elem['team2'])].append((site,elem['odds']))
	return(L) #Dictionnaire de la forme : L[('Nice','Lille')] = [(site1,[1odd1,1odd2,1odd3]),(site2,[2odd1,2odd2,2odd3])]