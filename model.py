import math
import random
import matplotlib.pyplot as plt
import numpy as np

class SIR:

    def __init__(self, population, recoveryPeriodInDays, avgNumOfContactsPerPerson, 
                 transmissionRate):
        self.population = population
        self.infected = 10  
        self.recovered = 0
        self.susceptible = 10000
        self.recoveryRate = 0.036
        self.effectiveContactRate = avgNumOfContactsPerPerson * transmissionRate
        self.infectedNums = []
        self.recoveredNums = []
        self.susceptibleNums = []
        
    def updatePopulation(self):
        for i in range(1,201):
            self.infectedPerDay = (
                self.effectiveContactRate * self.susceptible * self.infected / self.population)
            self.recoveredPerDay = (self.recoveryRate * self.infected)
            self.susceptible += -(self.infectedPerDay)
            self.infected += self.infectedPerDay - self.recoveredPerDay
            self.recovered += self.recoveredPerDay
            self.recoveredNums.append(self.recovered)
            self.infectedNums.append(self.infected)
            self.susceptibleNums.append(self.susceptible)
        
if __name__ == "__main__":
    ins = input('Enter a number of contacts per day for a population (must be 13 or under) ')
    socialDistancing = input('Are you social Distancing? [Yes or No] ')
    
    population = 10010
    initInfected = 100
    initRecovered = 0
    initSusceptible = population - initInfected - initRecovered
    avgNumOfContactsPerPerson = int(ins)
    if socialDistancing.lower() == 'no':
        transmissionRate = 0.128
    elif socialDistancing.lower() == 'yes':
        transmissionRate = 0.026

    #find beta aka our transmission rate
    
    #find gamma aka our transition rate to infectous to recovered
    recoveryPeriodInDays = 14
    sir = SIR(population,recoveryPeriodInDays,avgNumOfContactsPerPerson,
              transmissionRate)

    sir.updatePopulation()
    days = [i for i in range(1,201)]
    plt.plot(days, sir.infectedNums,label = 'infected')
    plt.plot(days,sir.recoveredNums,label = 'recovered')
    plt.plot(days, sir.susceptibleNums,label = 'susceptible')
    plt.xlabel('Days')
    plt.ylabel('Number')
    plt.legend()
    plt.show()
    
