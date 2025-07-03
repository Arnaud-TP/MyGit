import numpy as np
import matplotlib.pyplot as plt

def linear_regression(t,x,u=[]): # Array of values (tk) with xk = y(tk)
    A = np.zeros((2,2))
    A[0,0] = np.sum(t*t)
    A[0,1] = np.sum(t)
    A[1,0] = A[0,1]
    A[1,1] = len(t)
    B = np.zeros((2,1))
    B[0,0] = np.sum(t*x)
    B[1,0] = np.sum(x)
    C = np.matmul(np.linalg.inv(A),B)
    if len(u) == 0:
        return(C)
    else :
        c1 = C[0,0]
        c2 = C[1,0]
        return(c1*t+c2)

t = np.array([1,2,3,4,5,6,9,10,14,14.5,14.9,16])
x = np.array([4,2,6,1,2,-3,-10,7,4,-15,4,-8])

plt.scatter(t, x, color='blue', marker='o')
plt.plot(t,linear_regression(t,x,t),color='red')
plt.show()
