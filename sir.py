import matplotlib.pyplot as plt
import pandas as pd

# Clase para el simulador
class SIR:
    def __init__(self, transmition, recovery, s, i, r, dt, start=0):
        # Tasas de transmicion y recuperacion
        self.beta = transmition
        self.gamma = recovery
        self.history = []
        
        # Valores de poblacion iniciales
        self.s =s
        self.i =i
        self.r =r
        
        # Tiemo y cambio de tiempo
        self.t = start
        self.dt = dt
        
    
    def describe(self):
        print(f"t: {self.t} \nS: {self.s} \nI: {self.i} \nR: {self.r}")
    
    # Simular siguiente
    def step(self):
        # Tasas de cambio segun las ecuaciones de Stock-Flow de SIR
        ds = - self.beta * self.s * self.i
        di = (self.beta * self.s * self.i) - (self.gamma*self.i)
        dr = self.gamma*self.i
        
        # Agregar tasa de cambio
        self.s += ds*self.dt
        self.i += di*self.dt
        self.r += dr*self.dt
        # Aumentar tiempo
        self.t+=self.dt
        self.history.append(
            {"t": self.t, "S": self.s, "I": self.i, "R": self.r}
        )
        return
    
    def next(self, steps):
        for _ in range(steps):
            self.step()
       
    def plot(self):
        # Grafica con pandas y pyplot
        df = pd.DataFrame(self.history)
        X = df.pop("t")
        plt.title(f"Simulacion SIR (β = {self.beta}, γ = {self.gamma})")
        plt.plot(X,df["S"], label="Susceptibles")
        plt.plot(X,df["I"], label="Infectados")
        plt.plot(X,df["R"], label="Recuperados")
        plt.legend()
        plt.show()