from imutils.video import VideoStream
import imutils
import cv2
import time
import math as m
from PCA9685 import PCA9685

pwm = PCA9685(0x40, debug=False)
pwm.setPWMFreq(50)

class MotorDriver():
    def __init__(self):
        self.PWMA = 0
        self.AIN1 = 1
        self.AIN2 = 2
        self.PWMB = 5
        self.BIN1 = 3
        self.BIN2 = 4
   
    def avancer1(self, vitesse):
        pwm.setDutycycle(self.PWMA, vitesse)
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, vitesse)
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)
        
    def reculer1(self, vitesse):
        pwm.setDutycycle(self.PWMA, vitesse)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)
        pwm.setDutycycle(self.PWMB, vitesse)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)

    def stop1(self):
        pwm.setDutycycle(self.PWMA, 0)
        pwm.setDutycycle(self.PWMB, 0)
    
    def tourne_gauche1(self, vitesse):
        pwm.setDutycycle(self.PWMA, vitesse)
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        pwm.setDutycycle(self.PWMB, vitesse)
        pwm.setLevel(self.BIN1, 1)
        pwm.setLevel(self.BIN2, 0)

    def tourne_droite1(self, vitesse):
        pwm.setDutycycle(self.PWMA, vitesse)
        pwm.setLevel(self.AIN1, 1)
        pwm.setLevel(self.AIN2, 0)
        pwm.setDutycycle(self.PWMB, vitesse)
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)

def avancer(vitesse):
    Motor = MotorDriver() 
    Motor.avancer1(vitesse)

def stop():
    Motor = MotorDriver() 
    Motor.stop1()
    
def tourne_droite(vitesse):    
    Motor = MotorDriver()
    Motor.tourne_droite1(vitesse//2)
    
def tourne_gauche(vitesse):
    Motor = MotorDriver()
    Motor.tourne_gauche1(vitesse//2)
    
def reculer(vitesse):
    Motor = MotorDriver() 
    Motor.reculer1(vitesse)

def distance(topLeft, topRight, bottomLeft, bottomRight): #Fonction distance avec racine carrée
	L = [((topLeft[0]-topRight[0])**2 + (topLeft[1]-topRight[1])**2),((topLeft[0]-bottomLeft[0])**2 + (topLeft[1]-bottomLeft[1])**2),((topRight[0]-bottomRight[0])**2 + (topRight[1]-bottomRight[1])**2), ((bottomLeft[0]-bottomRight[0])**2 + (bottomLeft[1]-bottomRight[1])**2)]
	L1 = [max(L)]
	L.remove(L1[0])
	L1.append(max(L)) # Récupération des deux arêtes les plus grandes
	L = (m.sqrt(L1[0])+m.sqrt(L1[1]))/2 # Moyenne des deux plus grandes arêtes détectées
	return(9813/L - 11.5) # Facteur correctif de distance + retrait de la distance de la caméra à l'avant du véhicule

def angle(topLeft, topRight, bottomLeft, bottomRight):
    L = [m.sqrt((topLeft[0]-topRight[0])**2 + (topLeft[1]-topRight[1])**2),m.sqrt((bottomLeft[0]-bottomRight[0])**2 + (bottomLeft[1]-bottomRight[1])**2)]
    L_horizontal = (L[0]+L[1])/2
    L = [m.sqrt((topLeft[0]-bottomLeft[0])**2 + (topLeft[1]-bottomLeft[1])**2),m.sqrt((topRight[0]-bottomRight[0])**2 + (topRight[1]-bottomRight[1])**2)]
    L_vertical = (L[0]+L[1])/2
    if L[0] > L[1] :
        orientation = 1 #Marqueur tourné vers la droite par rapport à la caméra
    else :
        orientation = -1 #Marqueur tourné vers la droite par rapport à la caméra
    if (L_horizontal**2 >= L_vertical**2) or (1 - (L_horizontal/L_vertical)**2 < 0.1):
        return("|theta| < 10°")
    else :
        theta = 2*orientation*(180/m.pi)*m.asin(1 - L_horizontal/L_vertical)
        return(str(theta))

def test_recadre(cX):
    if abs(cX-500) <= 50:
        return(True)

def recadre(cX,L):
    facteur = 1
    if L < 50:
        facteur = 1/2
    if not test_recadre(cX):
        if 530 < cX <= 600:
            print("Tourne à droite de 2°")
            Motor = MotorDriver()
            Motor.tourne_droite1(20)
            time.sleep(facteur*0.04) #calibré pour tourner un peu
            Motor.stop1() 
            time.sleep(0.25)
        elif 600 < cX:
            print("Tourne à droite de 5°")
            Motor = MotorDriver()
            Motor.tourne_droite1(25)
            time.sleep(facteur*0.05) #calibré pour tourner un peu
            Motor.stop1() 
            time.sleep(0.25)
        elif 400 <= cX < 470 :
            print("Tourne à gauche de 2°")
            Motor = MotorDriver()
            Motor.tourne_gauche1(20)
            time.sleep(facteur*0.04) #calibré pour tourner un peu
            Motor.stop1() 
            time.sleep(0.25)
        elif cX < 400 :
            print("Tourne à gauche de 5°")
            Motor = MotorDriver()
            Motor.tourne_gauche1(25)
            time.sleep(facteur*0.05) #calibré pour tourner un peu
            Motor.stop1() 
            time.sleep(0.25)

def draw(frame, topLeft, topRight, bottomLeft, bottomRight, markerID):
    cv2.line(frame, topLeft, topRight, (0, 255, 0), 2) # draw the bounding box of the ArUCo detection
    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
    cX = int((topLeft[0] + bottomRight[0]) / 2.0) # compute and draw the center (x, y)-coordinates of the ArUco marker
    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
    cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
    dist = distance(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de la distance entre le véhicule
    cv2.putText(frame, str(dist),
        (topRight[0], topRight[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2)
    theta = angle(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de l'angle
    cv2.putText(frame, theta,
        (bottomRight[0], bottomRight[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2)
    cv2.putText(frame, str(markerID), # draw the ArUco marker ID on the frame
        (topLeft[0], topLeft[1] - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 255, 0), 2)
    
def debut():
    print("depart")
    Motor = MotorDriver() 
    Motor.avancer1(50)
    time.sleep(2.15) #temps d'attente à calibrer pour parcourir 80 cm
    Motor.stop1()
   
    
def demi_tour():
    print("demi tour")
    Motor = MotorDriver()
    Motor.tourne_droite1(25)
    time.sleep(1.5) #à calibrer pour tourner à 180°
    Motor.stop1()
    Motor = MotorDriver() 
    Motor.avancer1(50)
    time.sleep(3.5) #se rapproche de la balise
    Motor.stop1()
    








arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
arucoParams = cv2.aruco.DetectorParameters_create()
vs = VideoStream(src=0).start() # Début du flux vidéo

def conduite_auto_droite():
    debut()
    compteur = 0
    detect = False #Déclaration des variables
    etape = 0 #Détection de marqueur
    marqueur_sel = 1 #Premier marqueur sélectionné : marqueur impair
    cX_mem = 0 #Valeur de cX que l'on garde en mémoire
    L_mem = 0 #Va leur de L que l'on garde en mémoire
    while(True): #Boucle sur les captures de la vidéo
        frame = vs.read()
        frame = imutils.resize(frame, width=1000) # Redimensionnement de la capture
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams) # Detection des marqueurs aruco
        if len(corners) == 0 and not detect:
            print("Recherche marqueur_sel...")
            Motor = MotorDriver()
            Motor.tourne_droite1(25)
            time.sleep(0.03) #calibré pour tourner un peu
            Motor.stop1()
            time.sleep(0.3)
        
        if len(corners) > 0: # Si au moins un marqueur est détecté
            ids = ids.flatten() # Etalement des IDs détectés
            D = dict()  #Détection des différents marqueurs, et association de leur id et distance dans un dictionnaire dans le cas où l'on en détecte plusieurs
            for (markerCorner, markerID) in zip(corners, ids): # Affichage des marqueurs ArUCo détectés
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners # Extraction des coins du marqueur (qui sont toujours dans l'ordre Haut-Gauche, HD, BD, BG)
                topRight = (int(topRight[0]), int(topRight[1])) # Conversion en int des valeurs
                bottomRight = (int(bottomRight[0]), int(bottomRight[1])) 
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                #draw(frame, topLeft, topRight, bottomLeft, bottomRight, markerID)
                
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                dist = distance(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de la distance entre le véhicule
                theta = angle(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de l'angle
                D[dist]=[markerID,cX]
                
            L = D.keys() #Récupération de toutes les distances des marqueurs détectés
            L = min(L) #Récupération du minimum de ces distances
            ID = D[L][0] #Récupération de l'ID du marqueur correspondant détecté
            cX = D[L][1]
            if ID % 2 == marqueur_sel: #Le marqueur le plus proche est le bon marqueur
                print(" ! Detection marqueur_sel ! ")
                compteur = 0
                detect = True
                L_mem = L
                cX_mem = cX
        if len(corners) > 0 and not detect: # Marqueur faux
            print("Recherche marqueur_sel...")
            Motor = MotorDriver()
            Motor.tourne_droite1(25)
            time.sleep(0.03) #calibré pour tourner un peu
            Motor.stop1()
            time.sleep(0.3)
            
        if len(corners) == 0 and detect :
            compteur += 1
            if compteur == 5 :
                detect = False
                print("Perte du marqueur_sel. Reprise de la recherche...")
                compteur = 0
        if detect :
            if L_mem < 20 : #Condition d'arrêt
                if etape == 0:
                    demi_tour()
                if etape == 1:
                    print("FIN")
                etape +=1
                marqueur_sel = 1 - marqueur_sel
                detect = False
            elif test_recadre(cX_mem):
                Motor = MotorDriver() 
                Motor.avancer1(50)
                time.sleep(0.20) #temps d'attente à calibrer pour parcourir 10 cm
                Motor.stop1()
                time.sleep(0.30)
            else :
                recadre(cX_mem,L_mem)
        if etape == 2: #Fin
            break
    cv2.destroyAllWindows()
    vs.stop()
    
def conduite_auto_gauche():
    debut()
    compteur = 0
    detect = False #Déclaration des variables
    etape = 0 #Détection de marqueur
    marqueur_sel = 1 #Premier marqueur sélectionné : marqueur impair
    cX_mem = 0 #Valeur de cX que l'on garde en mémoire
    L_mem = 0 #Valeur de L que l'on garde en mémoire
    while(True): #Boucle sur les captures de la vidéo
        frame = vs.read()
        frame = imutils.resize(frame, width=1000) # Redimensionnement de la capture
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams) # Detection des marqueurs aruco
        if len(corners) == 0 and not detect:
            print("Recherche marqueur_sel...")
            Motor = MotorDriver()
            Motor.tourne_gauche1(25)
            time.sleep(0.05) #calibré pour tourner un peu
            Motor.stop1()
            time.sleep(0.3)
        
        if len(corners) > 0: # Si au moins un marqueur est détecté
            ids = ids.flatten() # Etalement des IDs détectés
            D = dict()  #Détection des différents marqueurs, et association de leur id et distance dans un dictionnaire dans le cas où l'on en détecte plusieurs
            for (markerCorner, markerID) in zip(corners, ids): # Affichage des marqueurs ArUCo détectés
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners # Extraction des coins du marqueur (qui sont toujours dans l'ordre Haut-Gauche, HD, BD, BG)
                topRight = (int(topRight[0]), int(topRight[1])) # Conversion en int des valeurs
                bottomRight = (int(bottomRight[0]), int(bottomRight[1])) 
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                #draw(frame, topLeft, topRight, bottomLeft, bottomRight, markerID)
                
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                dist = distance(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de la distance entre le véhicule
                theta = angle(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de l'angle
                D[dist]=[markerID,cX]
                
            L = D.keys() #Récupération de toutes les distances des marqueurs détectés
            L = min(L) #Récupération du minimum de ces distances
            ID = D[L][0] #Récupération de l'ID du marqueur correspondant détecté
            cX = D[L][1]
            if ID % 2 == marqueur_sel: #Le marqueur le plus proche est le bon marqueur
                print(" ! Detection marqueur_sel ! ")
                compteur = 0
                detect = True
                L_mem = L
                cX_mem = cX
        if len(corners) > 0 and not detect: # Marqueur faux
            print("Recherche marqueur_sel...")
            Motor = MotorDriver()
            Motor.tourne_gauche1(25)
            time.sleep(0.05) #calibré pour tourner un peu
            Motor.stop1()
            time.sleep(0.3)
            
        if len(corners) == 0 and detect :
            compteur += 1
            if compteur == 5 :
                detect = False
                print("Perte du marqueur_sel. Reprise de la recherche...")
                compteur = 0
        if detect :
            if L_mem < 20 : #Condition d'arrêt
                if etape == 0:
                    demi_tour()
                if etape == 1:
                    print("FIN")
                etape +=1
                marqueur_sel = 1 - marqueur_sel
                detect = False
            elif test_recadre(cX_mem):
                Motor = MotorDriver() 
                Motor.avancer1(50)
                time.sleep(0.20) #temps d'attente à calibrer pour parcourir 10 cm
                Motor.stop1()
                time.sleep(0.30)
            else :
                recadre(cX_mem,L_mem)
        if etape == 2: #Fin
            break
    cv2.destroyAllWindows()
    vs.stop()


