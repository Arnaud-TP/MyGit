from imutils.video import VideoStream
import imutils
import cv2
import time
import math as m
from PCA9685 import PCA9685
import time

#initialisation moteurs
Dir = ['forward','backward',]
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

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

def distance(topLeft, topRight, bottomLeft, bottomRight): #Fonction qui permet de gérer la distance v1 du robot par rapport au marqueur
    L = [abs(topLeft[0]-topRight[0]),abs(topLeft[1]-bottomLeft[1]),abs(bottomLeft[0]-bottomRight[0]),abs(topRight[1]-bottomRight[1])]
    L1 = [max(L)]
    L.remove(L1[0])
    L1.append(max(L)) # Récupération des deux arêtes les plus grandes
    L = (L1[0]+L1[1])/2 # Moyenne des deux plus grandes arêtes détectées
    return(9813/L - 11.5) # Facteur correctif de distance + retrait de la distance de la caméra à l'avant du véhicule

def distance2(topLeft, topRight, bottomLeft, bottomRight): #Fonction distance avec racine carrée
	L = [((topLeft[0]-topRight[0])**2 + (topLeft[1]-topRight[1])**2),((topLeft[0]-bottomLeft[0])**2 + (topLeft[1]-bottomLeft[1])**2),((topRight[0]-bottomRight[0])**2 + (topRight[1]-bottomRight[1])**2), ((bottomLeft[0]-bottomRight[0])**2 + (bottomLeft[1]-bottomRight[1])**2)]
	L1 = [max(L)]
	L.remove(L1[0])
	L1.append(max(L)) # Récupération des deux arêtes les plus grandes
	L = (m.sqrt(L1[0])+m.sqrt(L1[1]))/2 # Moyenne des deux plus grandes arêtes détectées
	return(9813/L - 11.5) # Facteur correctif de distance + retrait de la distance de la caméra à l'avant du véhicule

def recadre(cX, cY):
	if abs(cX-500) <= 40 :
		return True #si le marqueur est centré on renvoie qu'il est bien centré
	
	elif cX > 500 : #le marqueur est trop à droite
		print("tourne de 5° vers la droite") #on corrige un poco (on réitèrera cette étape autant de fois que necessaire)
		return False #on va tester à la prochaine itération
	
	elif cX < 500 : #le marqueur est trop à gauche
		print("tourne de 5° vers la gauche") #on corrige
		return False

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
arucoParams = cv2.aruco.DetectorParameters()

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()

# loop over the frames from the video stream
def conduite_auto_droite():
    while(True):
        frame = vs.read()
        frame = imutils.resize(frame, width=1000) # Grab the frame from the threaded video stream and resize it to have a maximum width of 1000 pixels
        (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams) # Detect ArUco markers in the input frame		
        if len(corners) > 0: # Verify *at least* one ArUco marker was detected
            ids = ids.flatten() # Flatten the ArUco IDs list
            D = dict()  #Détection des différents marqueurs, et association de leur id et distance
            for (markerCorner, markerID) in zip(corners, ids): # Affichage des marqueurs ArUCo détectés
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners # extract the marker corners (which are always returned in top-left, top-right, bottom-right, and bottom-left order)
                topRight = (int(topRight[0]), int(topRight[1])) # Convert the values to int
                bottomRight = (int(bottomRight[0]), int(bottomRight[1])) 
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                cv2.line(frame, topLeft, topRight, (0, 255, 0), 2) # draw the bounding box of the ArUCo detection
                cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
                
                cX = int((topLeft[0] + bottomRight[0]) / 2.0) # compute and draw the center (x, y)-coordinates of the ArUco marker
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
                
                dist = distance2(topLeft,topRight,bottomLeft,bottomRight) # Fonction d'affichage de la distance entre le véhicule
                cv2.putText(frame, str(dist),
					(topRight[0], topRight[1] - 15),
					cv2.FONT_HERSHEY_SIMPLEX,
					0.5, (0, 255, 0), 2)
                D[dist]=markerID
                
                cv2.putText(frame, str(markerID), # draw the ArUco marker ID on the frame
					(topLeft[0], topLeft[1] - 15),
					cv2.FONT_HERSHEY_SIMPLEX,
					0.5, (0, 255, 0), 2)
            
            L = D.keys() #Récupération de toutes les distances des marqueurs détectés
            L = min(L) #Récupération du minimum de ces distances
            ID = D[L] #Récupération de l'ID du marqueur correspondant détecté
            etape = 1
            #1ere étape : avancer jusqu'au centre de l'arène
            if etape == 1 :
                  Motor = MotorDriver() 
                  Motor.avancer1(50)
                  timesleep(2) #temps d'attente à calibrer pour parcourir 80 cm
                  Motor.stop1()
                  etape += 1
                
            #2e étape : tourner du bon coté (selon l'ordre donné initialement)
            if etape == 2 :
                  Motor = MotorDriver()
                  Motor.tourne_droite1(25)
                  time.sleep(0.825) #à calibrer pour tourner à 90°
                  Motor.stop1()
                  if recadre(cX,cY):
                        etape += 1
                    
            #3e étape : avancer jusqu'à 20cm de la balise
            if etape == 3:
                  Motor = MotorDriver() 
                  Motor.avancer1(50)
                  time.sleep(0.25) #temps d'attente à calibrer pour parcourir 10 cm
                  Motor.stop1()
                  if L <= 20 :
                        etape += 1

            #4e étape : demi-tour
            if etape == 4:
                  Motor = MotorDriver()
                  Motor.tourne_droite1(25)
                  time.sleep(0.825) #à calibrer pour tourner à 180°
                  Motor.stop1()
                  if recadre(cX,cY):
                        etape += 1

            #5e étape : avancer jusqu'à 20cm de la balise
            if etape == 5:
                  Motor = MotorDriver() 
                  Motor.avancer1(50)
                  time.sleep(0.25) #temps d'attente à calibrer pour parcourir 10 cm
                  Motor.stop1()
                  if L <= 20:
                        etape += 1
            
            #6e étape : sortie du mode auto
            if etape == 6:
                  break
    

        cv2.imshow("Frame", frame) # Affichage de la fenêtre de sortie (flux vidéo + affichage des marqueurs détectés)
        key = cv2.waitKey(1) & 0xFF #Récupération de la touche pressée sur le clavier (255 par défaut)
        #if key != 255 : #Affichage de la touche pressée si ce n'est pas la touche par défaut
		#	print(key)
        if key == ord("q"): # Touche 'q' pour quitter et terminer le programme
            break 
    cv2.destroyAllWindows()
    vs.stop()

conduite_auto()
