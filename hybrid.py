from abm import ABM
from sir import SIR
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Hybrid:
    def __init__(self, population_size, transmition, recovery, initial_infected, vaccination_rate):
        self.population_size = population_size
        self.transmition = transmition
        self.recovery = recovery
        self.initial_infected = initial_infected
        self.vaccination_rate = vaccination_rate
        
        self.swap = 0
        self.history = []
        # Init ABM
        self.abm = None
        self.sir = None
        self.t = 0
    
    def abm_start(self, swap, end):
        
        # Iniciar ABM
        self.abm = ABM(
            self.population_size,
            self.transmition,
            self.recovery,
            self.initial_infected,
            self.vaccination_rate
        )
        
        # Simular ABM hasta el punto de cambio
        self.abm.next(swap)
        self.swap = swap
        
        # Se calcula poblacion
        i_end = 0
        s = 0
        r = 0
        for i in self.abm.agents:
            if i.state == "I":
                i_end+=1
            elif i.state == "R":
                r+=1
            else:
                s+=1

        # Calcular constantes para SIR
        r0 = (self.initial_infected-i_end)/self.initial_infected
        gamma = 1/self.abm.mean_recovery()
        beta = r0*gamma
        
        # Evaluar SIR hasta punto final
        self.sir = SIR(
            beta,
            gamma,
            s/self.population_size,
            i_end/self.population_size,
            r/self.population_size,
            1,
            start=swap
        )
        self.sir.next(end-swap)
        
        # Conctenar Historiales y escalar
        abm_history = pd.DataFrame(self.abm.history)
        abm_history["S"] = abm_history["S"]/self.population_size
        abm_history["I"] = abm_history["I"]/self.population_size
        abm_history["R"] = abm_history["R"]/self.population_size
        sir_history = pd.DataFrame(self.sir.history)
        self.history = pd.concat([abm_history, sir_history], ignore_index=True)
    
    def plot(self):
        plt.figure(figsize=(10,6))
        plt.title(f"Simulación Modelo Hibrido")
        plt.plot(self.history["t"], self.history["S"], label="Susceptibles")
        plt.plot(self.history["t"], self.history["I"], label="Infectados")
        plt.plot(self.history["t"], self.history["R"], label="Recuperados")
        plt.plot([self.swap,self.swap],[0,1],linestyle=":", label="Cambio")
        plt.xlabel("Tiempo")
        plt.ylabel("Número de personas")
        plt.legend()
        plt.show()