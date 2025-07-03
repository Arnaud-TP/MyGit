import bookmaker1, bookmaker2
import auxiliary_functions

sites = {
		#"Bookmaker1": bookmaker1,
		#"Bookmaker2": bookmaker2,
		}

all_competitions = ['LDC','ligue-europa-conf','ligue-europa','copa-america','euro','qualif-euro','coupe-de-france','ligue1','ligue2','laliga','laliga2','coupe-d-allemagne','bundesliga','bundesliga2','fa-cup','premier-league','premier-league2','coupe-d-italie','serie-a','serie-b','primeira-liga','segunda-liga']

competition_names = {
    'LDC':"Ligue des Champions",
	'ligue-europa-conf':"Ligue Europa Conference",
	'ligue-europa':"Ligue Europa",
 	'copa-america':"Copa America",
	'euro': "Euro",
	'qualif-euro': "Qualifications Euro",
	'coupe-de-france': "Coupe de France",
	'ligue1':"Ligue 1",
	'ligue2':"Ligue 2",
	'laliga':"La Liga",
	'laliga2': "La Liga 2",
	'coupe-d-allemagne':"Coupe d'Allemagne",
	'bundesliga':"Bundesliga",
	'bundesliga2':"Bundesliga 2",
	'fa-cup': "FA Cup",
	'premier-league': "Premier League",
	'premier-league2': "Championship",
	'coupe-d-italie':"Coupe d'Italie",
	'serie-a':"Série A",
	'serie-b':"Série B",
	'primeira-liga': "Primeira Liga",
	'segunda-liga':"Segunda Liga"
}

def arbitrage(L, freebet_bookmakers = []): #Liste de la forme L = [("Winamax",[2.8,2.8,2.5]),("FDJ",[2.9,2.6,2.6])]
	lst_bms = []
	lst_val = []
	lst_bms_freebet = []
	lst_val_freebet = []
	for i in range(3):
		max_bm = "None"
		max_bm_freebet = "None"
		max_val = 1.000000000001
		max_val_freebet = 1.000000000001
		for bms_odds in L:
			if freebet_bookmakers == []:
				try :
					if max_val_freebet < bms_odds[1][i]:
						if max_val < bms_odds[1][i]:
							max_val_freebet = max_val
							max_bm_freebet = max_bm
							max_val = bms_odds[1][i]
							max_bm = bms_odds[0]
						else : 
							max_val_freebet = bms_odds[1][i]
							max_bm_freebet = bms_odds[0]
				except :
					pass
			else :
				try:
					if max_val < bms_odds[1][i]:
						max_val = bms_odds[1][i]
						max_bm = bms_odds[0]
					if max_val_freebet < bms_odds[1][i] and (bms_odds[0] in freebet_bookmakers):
						max_val_freebet = bms_odds[1][i]
						max_bm_freebet = bms_odds[0]
				except:
					pass
		lst_bms.append(max_bm)
		lst_val.append(max_val)
		lst_bms_freebet.append(max_bm_freebet)
		lst_val_freebet.append(max_val_freebet)
	if freebet_bookmakers != []:
		if len(lst_val_freebet) == 3:
			i = lst_val_freebet.index(min(lst_val_freebet))
			lst_val_freebet[i] = lst_val[i]
			lst_bms_freebet[i] = lst_bms[i]
	return (lst_bms, lst_val, aux.taux(lst_val), lst_bms_freebet, lst_val_freebet, aux.taux(lst_val_freebet)) #On renvoie la liste des bookmakers, les côtes, et les indicateurs

def run_arbitrage(competitions = all_competitions, bookmakers = sites.keys(), freebet_bookmakers = [], affichage = True):
	if not affichage:
		dico_final = {}
	assert all(bms in sites.keys() for bms in bookmakers)
	assert all(bms in sites.keys() for bms in freebet_bookmakers)
	for competition in competitions:
		flag_affichage = True
		Dico_global_parties = {} #Dictionnaire qui contient toutes les parties d'une même compétition pour chacun des sites
		for site in sites.keys():
			Dico_global_parties[site] = sites[site].get_games(competition)
		games = aux.find_games(Dico_global_parties)
		if affichage:
			L = []
			for game in games.keys():
				t1,t2 = game
				sites_odds = games[game]
				bmsa, cotea, (ta,Ga), bmsb, coteb, (tb,Gb) = arbitrage(sites_odds, freebet_bookmakers)
				cotea2 = cotea.copy()
				cotea2.sort()
				L.append([ta,(t1,t2,bmsa,cotea,(ta,Ga),bmsb,coteb,(tb,Gb))])
			L.sort(key=lambda x: x[0])
			if L != []:
				for i in range(len(L)):
					(t1,t2,bmsa,cotea,(ta,Ga),bmsb,coteb,(tb,Gb)) = L[i][1]
					if flag_affichage == True :
						print("\n------------------------------------------------------------")
						print("\tCompetition :", competition)
						print("------------------------------------------------------------")
						flag_affichage = False
					print("\n\t\tMatch : ",t1," - ",t2)
					if bmsb[1] == "None":
						print("\t", bmsa,cotea,"Taux :",ta,"Gain :",Ga) # (t,G) Taux de conversion freebet et gain pour 100€ joué
					else:
						print("\t", bmsa,cotea,"Taux :",ta,"Gain :",Ga,"\t\t", bmsb,coteb,"Taux :",tb,"Gain :",Gb)
		else :
			for game in games.keys():
				dico_final[game]=(arbitrage(games[game])[:3],competition_names[competition])
	if not affichage:
		return(dico_final)
	return()

if __name__ == '__main__':
	run_arbitrage(affichage = True)