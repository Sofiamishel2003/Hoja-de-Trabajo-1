import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


class Agent:
    def __init__(self, age, mask_compliance, vaccinated=False):
        self.age = age  # Edad
        self.mask_compliance = mask_compliance  # 0.0 (nunca usa) a 1.0 (siempre usa)
        self.vaccinated = vaccinated  # True si está vacunado
        self.state = "S"  # susceptible, infectado, recuperado
        self.time_infected = 0
        self.recovery_time = 0
    
    def interact(self, others, base_transmition, recovery, t):
        if self.state == "S":
            for other in others:
                if other.state == "I":
                    # Ajustar probabilidad según mascarilla y vacunación
                    effective_prob = base_transmition * (1 - self.mask_compliance) * (1 - other.mask_compliance)
                    if self.age > 60:
                        effective_prob *= 1.5  # Mayor riesgo por edad
                    if self.vaccinated:
                        effective_prob *= 0.1  # vacunados tienen 90% menos probabilidad
                    if random.random() < effective_prob:
                        self.state = "I"
                        self.time_infected = t
                        break
        elif self.state == "I":
            if random.random() < recovery:
                if self.time_infected>0:
                    self.recovery_time = t-self.time_infected
                self.state = "R"
            

class ABM:
    def __init__(self, population_size, transmition, recovery, initial_infected, vaccination_rate=0.0):
        self.agents = []
        self.population_size = population_size
        for _ in range(population_size):
            age = random.randint(1, 80)
            mask_compliance = random.uniform(0, 1)
            vaccinated = random.random() < vaccination_rate
            self.agents.append(Agent(age, mask_compliance, vaccinated))
        for agent in random.sample(self.agents, initial_infected):
            agent.state = "I"
        self.transmition = transmition
        self.recovery = recovery
        self.t = 0
        self.history = []  # Para guardar la historia completa
    
    def describe(self):
        counts = {"S": 0, "I": 0, "R": 0}
        for agent in self.agents:
            counts[agent.state] += 1
        print(f"t: {self.t}")
        print(f"S: {counts['S']} ({counts['S']/self.population_size:.4%})")
        print(f"I: {counts['I']} ({counts['I']/self.population_size:.4%})")
        print(f"R: {counts['R']} ({counts['R']/self.population_size:.4%})")

    def mean_recovery(self):
        times = []
        for agent in self.agents: 
            if agent.recovery_time>0:
                times.append(agent.recovery_time)
        
        return np.mean(times)

    def step(self):
        # cada agente interactúa con otros agentes
        for agent in self.agents:
            if random.random() < 0.05:  # 5% superpropagadores
                num_contacts = random.randint(50, 100)
            else:
                num_contacts = random.randint(5, 15)
            contacts = random.sample(self.agents, min(num_contacts, len(self.agents)-1))
            agent.interact(contacts, self.transmition, self.recovery, self.t)

        self.t += 1
        counts = {"S": 0, "I": 0, "R": 0}
        for agent in self.agents:
            counts[agent.state] += 1
        self.history.append({"t": self.t, "S": counts["S"], "I": counts["I"], "R": counts["R"]})
        return {"t": self.t, "S": counts["S"], "I": counts["I"], "R": counts["R"]}

    def next(self, steps):
        data = []
        for _ in range(steps):
            result = self.step()
            data.append(result)
        return pd.DataFrame(data)
        
    def plot(self):
        if not self.history:
            print("No hay datos. Ejecuta run(steps) primero.")
            return
        df = pd.DataFrame(self.history)
        plt.figure(figsize=(10,6))
        plt.title(f"Simulación ABM (Infección={self.transmition}, Recuperación={self.recovery})")
        plt.plot(df["t"], df["S"], label="Susceptibles")
        plt.plot(df["t"], df["I"], label="Infectados")
        plt.plot(df["t"], df["R"], label="Recuperados")
        plt.xlabel("Tiempo")
        plt.ylabel("Número de personas")
        plt.legend()
        plt.show()