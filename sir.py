import matplotlib.pyplot as plt
import pandas as pd

# Clase para el simulador
class SIR:
    def __init__(self, transmition, recovery, s, i, r, dt):
        # Tasas de transmicion y recuperacion
        self.beta = transmition
        self.gamma = recovery
        
        # Valores de poblacion iniciales
        self.s =s
        self.i =i
        self.r =r
        
        # Tiemo y cambio de tiempo
        self.t = 0
        self.dt = dt
    
    # Simular siguiente
    def next(self):
        # Tasas de cambio segun las ecuaciones de Stock-Flow de SIR
        ds = - self.beta * self.s * self.i
        di = (self.beta * self.s * self.i) - (self.gamma*self.i)
        dr = self.gamma*self.i
        
        # Agregar tasa de cambio
        self.s += ds*self.dt
        self.i += di*self.dt
        self.r += dr*self.dt
        # Aumentar tiempo
        self.t+=0.01
        return (self.t, self.s, self.i, self.r)
        
    def plot(self, n):
        # Ciclo de simulacion
        entries = []
        for i in range(n):
            t,s,i,r = self.next()
            entries.append({"t": t, "S": s, "I": i, "R": r})
            
        # Grafica con pandas y pyplot
        df = pd.DataFrame(entries)
        X = df.pop("t")
        plt.title(f"Simulacion SIR (β = {self.beta}, γ = {self.gamma})")
        plt.plot(X,df["S"], label="Susceptibles")
        plt.plot(X,df["I"], label="Infectados")
        plt.plot(X,df["R"], label="Recuperados")
        plt.legend()
        plt.show()