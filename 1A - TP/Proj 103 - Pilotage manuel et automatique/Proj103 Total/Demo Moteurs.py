#!/usr/bin/python

from PCA9685 import PCA9685
import time

Dir = [
    'forward',
    'backward',
]
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

    def MotorRun(self, motor, index, speed):
        if speed > 100:
            return
        if(motor == 0):
            pwm.setDutycycle(self.PWMA, speed)     #Par défaut la vitesse des moteurs est à 0
            if(index == Dir[0]): #Moteur 1, vers l'avant
                print ("1")
                pwm.setLevel(self.AIN1, 0)
                pwm.setLevel(self.AIN2, 1)
            else:
                print ("2")     #Moteur 1, vers l'arriere
                pwm.setLevel(self.AIN1, 1)
                pwm.setLevel(self.AIN2, 0)
        else:
            pwm.setDutycycle(self.PWMB, speed)
            if(index == Dir[0]):
                print ("3") #Moteur 2, vers l'avant
                pwm.setLevel(self.BIN1, 0)
                pwm.setLevel(self.BIN2, 1)
            else:
                print ("4") #Moteur 2, vers l'arrier
                pwm.setLevel(self.BIN1, 1)
                pwm.setLevel(self.BIN2, 0)

    def MotorStop(self, motor):
        if (motor == 0):
            pwm.setDutycycle(self.PWMA, 0)
        else:
            pwm.setDutycycle(self.PWMB, 0)

    def avancer(self):
        pwm.setDutycycle(self.PWMA, 50)
        pwm.setLevel(self.AIN1, 0)
        pwm.setLevel(self.AIN2, 1)
        print("1 , 3")
        pwm.setDutycycle(self.PWMB, 50)
        pwm.setLevel(self.BIN1, 0)
        pwm.setLevel(self.BIN2, 1)

    def stop(self):
        pwm.setDutycycle(self.PWMA, 0)
        pwm.setDutycycle(self.PWMB, 0)
    
    def tourne_gauche(self):
        pwm.setDutycycle(self.PWMA, 25)
        pwm.setLevel(self.AIN1, 0)
        pwm.setDutycycle(self.PWMB, 25)
        pwm.setLevel(self.BIN2, 1)

    def tourne_droite(self):
        pwm.setDutycycle(self.PWMB, 50)
        pwm.setLevel(self.AIN1, 0)


#Moteur 1 = moteur de gauche
Motor = MotorDriver()
