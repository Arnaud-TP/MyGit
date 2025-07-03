from imutils.video import VideoStream
import imutils
import cv2
import numpy as np
import math as m
import time

ret = 1.699023774489603
camera_matrix = np.array([[1.96680637e+03, 0, 5.95726306e+02], [0, 1.95980851e+03, 4.82540730e+02], [0, 0, 1]], dtype=np.float32)
distortion_coeffs = np.array([-1.16039043e-01,3.67278308e+00,-1.59178789e-03,2.04738310e-02,-2.65135029e+01], dtype = np.float32)
marker_size = 0.05
marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
							[marker_size / 2, marker_size / 2, 0],
							[marker_size / 2, -marker_size / 2, 0],
							[-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)


def distance(corners): #Fonction distance avec racine carrée
	(topLeft, topRight, bottomRight, bottomLeft) = corners # extract the marker corners (which are always returned in top-left, top-right, bottom-right, and bottom-left order)
	topRight = (int(topRight[0]), int(topRight[1])) # Convert the values to int
	bottomRight = (int(bottomRight[0]), int(bottomRight[1])) 
	bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	topLeft = (int(topLeft[0]), int(topLeft[1]))
	L = [((topLeft[0]-topRight[0])**2 + (topLeft[1]-topRight[1])**2),((topLeft[0]-bottomLeft[0])**2 + (topLeft[1]-bottomLeft[1])**2),((topRight[0]-bottomRight[0])**2 + (topRight[1]-bottomRight[1])**2), ((bottomLeft[0]-bottomRight[0])**2 + (bottomLeft[1]-bottomRight[1])**2)]
	L1 = [max(L)]
	L.remove(L1[0])
	L1.append(max(L)) # Récupération des deux arêtes les plus grandes
	L = (m.sqrt(L1[0])+m.sqrt(L1[1]))/2 # Moyenne des deux plus grandes arêtes détectées
	return(9813/L - 11.5) # Facteur correctif de distance + retrait de la distance de la caméra à l'avant du véhicule

def recadre(cX):
	(topLeft, topRight, bottomRight, bottomLeft) = corners # extract the marker corners (which are always returned in top-left, top-right, bottom-right, and bottom-left order)
	topRight = (int(topRight[0]), int(topRight[1])) # Convert the values to int
	bottomRight = (int(bottomRight[0]), int(bottomRight[1])) 
	bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
	topLeft = (int(topLeft[0]), int(topLeft[1]))
	cX = int((topLeft[0] + bottomLeft[0] + topRight[0] + bottomRight[0]) / 4.0) 
	if abs(cX-500) <= 50:
		return(True)
	elif 550 < cX <= 600:
		print("Tourne à droite de 2°")
		return(False)
	elif 600 < cX:
		print("Tourne à droite de 5°")
		return(False)
	elif 400 <= cX < 450 :
		print("Tourne à gauche de 2°")
		return(False)
	elif cX < 400 :
		print("Tourne à gauche de 5°")
		return(False)

def draw(frame, corners, markerID, dist, theta):
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
	dist = "{:.2f}".format(dist)
	cv2.putText(frame, "Dist : " + str(dist),
		(topRight[0], topRight[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 255, 0), 2)
	cv2.putText(frame, "TopLeft ID : " + str(markerID), # draw the ArUco marker ID on the frame
		(topLeft[0], topLeft[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 255, 0), 2)
	theta = "{:.2f}".format(theta)# Fonction d'affichage de l'angle
	cv2.putText(frame, "Theta : " + str(theta),
		(bottomRight[0], bottomRight[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 255, 0), 2) 

def rotate(M):
	return np.array([[M[1,0],M[1,1]],[M[2,0],M[2,1]],[M[3,0],M[3,1]],[M[0,0],M[0,1]]])
   
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_1000)
arucoParams = cv2.aruco.DetectorParameters()

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()
while(True):
	frame = vs.read()
	frame = imutils.resize(frame, width=1000) # Grab the frame from the threaded video stream and resize it to have a maximum width of 1000 pixels
	frame = cv2.undistort(frame, camera_matrix, distortion_coeffs)
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams) # Detect ArUco markers in the input frame		
	if len(corners) > 0: # Verify *at least* one ArUco marker was detected
		detect = True
		ids = ids.flatten() # Flatten the ArUco IDs list
		for (markerCorner, markerID) in zip(corners, ids): # Affichage des marqueurs ArUCo détectés
			corners = markerCorner.reshape((4, 2))
			if len(corners) >= 4:
				_, rvec, tvec = cv2.solvePnP(marker_points, rotate(corners), camera_matrix, distortion_coeffs, False, cv2.SOLVEPNP_IPPE_SQUARE)
				rotation_matrix, _ = cv2.Rodrigues(rvec)
				rotation_angles_rad = np.arccos((np.trace(rotation_matrix)-1)/2.0)
				rotation_angles_deg = np.degrees(rotation_angles_rad)
				rotation_direction = np.sign(rotation_matrix[2, 1] - rotation_matrix[1, 2])
				rotation_angles_deg = (2*(rotation_angles_deg - 180))* rotation_direction
				dist = distance(corners)
				draw(frame, corners, markerID, dist, rotation_angles_deg)
			a = recadre(corners)
	cv2.imshow("Frame", frame) # Affichage de la fenêtre de sortie (flux vidéo + affichage des marqueurs détectés)
	key = cv2.waitKey(1) & 0xFF #Récupération de la touche pressée sur le clavier (255 par défaut)
	if key == ord("q"): # Touche 'q' pour quitter et terminer le programme
		break 
cv2.destroyAllWindows()
vs.stop()


