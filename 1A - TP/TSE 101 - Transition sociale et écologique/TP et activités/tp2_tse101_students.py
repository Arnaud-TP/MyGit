import numpy as np
import matplotlib.pyplot as plt


filename ='data_tp2.csv'

temperature = []
solar= []
magnet= []

A=np.loadtxt(filename)
A=A.transpose()

temperature=A[0]
solar=A[1]
magnet=A[2]

index_t=np.arange(1900,2001)

plt.plot(index_t,temperature,'r-+', label="Température")
plt.plot(index_t,solar,'k', label="Activité solaire")
plt.plot(index_t,magnet,'k--',  label="Activité magnétique")
plt.title('Quelques paramètres au cours du temps')
plt.xlabel('Année')
plt.ylabel('Valeurs normalisées')
plt.legend(loc="upper left")
plt.grid()
plt.show()
    
    
def correlation(x,y):
    xb=np.mean(x)
    yb=np.mean(y)    
    aux1 = 0
    aux2 = 0
    aux3 = 0
    for i in range (len(x)):
        aux1 += (x[i]-xb)*(y[i]-yb)
        aux2 += (x[i]-xb)**2
        aux3 += (y[i]-yb)**2    
    c= aux1/np.sqrt(aux2*aux3)
    return c

print("Corrélation (Sn,Bn) :", correlation(solar,magnet))

# Corrélation de 0.93, on en déduit que les diagrammes sont corrélés, Bn semble bien représenter l'activité solaire, au vue de la corrélation

print("Corrélation (Sn,Tn) de 1900 à 2000 :", correlation(solar,temperature))

# Le coefficient de corrélation élevé semble montrer que la température et l'activité solaire sont corrélés

print("Corrélation (Sn,Tn) de 1900 à 1950 :", correlation(solar[:50],temperature[:50]))

# Cela semblait en effet être le cas de 1900 à 1950

print("Corrélation (Sn,Tn) de 1950 à 2000 :", correlation(solar[50:],temperature[50:]))

# Mais de 1950 à 2000, on observe une décorrélation des données, elles évoluent dans des sens opposés

def r_square(y,y_hat):
    yb=np.mean(y)
    aux1=0
    aux2=0
    for i in range (len(y)):
        aux1 += (y[i]-y_hat[i])**2
        aux2 += (y[i]-yb)**2  
    rs=1-aux1/aux2
    return rs


def regression(x,y):
    N=len(x)
   
    aux1=np.sum(x)
    aux2=np.sum(y)
    aux3=np.sum(y*x)
    aux4=np.sum(x*x)
    
    a = (N*aux3 - aux1*aux2)/(N*aux4 - aux1**2)
    b = (aux2 - a*aux2)/N 
    return a,b

def prediction(x,a,b):
    y = a*x + b
    return y


a,b=regression(magnet,solar)
print(f"Terme de la regression (Bn,Sn) a = {round(a,2)} b = {round(b,2)}")
R2 = r_square(solar,prediction(solar,a,b))
print(f"Validation du critère R2 en prédiant Sn à partir de Bn, R2 = {round(R2,3)}")

# D'abord entre S et B, on obtient pour critère R2 = 0.999, les prédictions sont bonnes

a,b=regression(solar,temperature)
print(f"Terme de la regression (Bn,Sn) a = {round(a,2)} b = {round(b,2)}")
R2 = r_square(solar,prediction(solar,a,b))
print(f"Validation du critère R2 en prédiant Tn à partir de Sn, R2 = {round(R2,3)}")

a,b=regression(solar[50:],temperature[50:])
print(f"Terme de la regression (Bn,Sn) sur la période 1950-2000 a = {round(a,2)} b = {round(b,2)}")
R2 = r_square(solar[50:],prediction(solar[50:],a,b))
print(f"Validation du critère R2 en prédiant Tn à partir de Sn sur la période 1950 - 2000, R2 = {round(R2,3)}")

# Puis entre T et S, on obtient pour critère R2 = 0.905