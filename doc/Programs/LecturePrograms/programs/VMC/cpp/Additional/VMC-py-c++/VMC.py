#Variational Monte Carlo program for the Helium atom which utilizes the code in MC.cpp
#Written by Magnar K. Bugge

from math import sqrt
from numpy import linspace
import MC

MCcycles = 100000000 #Number of MC cycles
MCcycles2 = 10000 #Number of MC cycles for determination of optimal delta
delta_min = .01 #Minimum length of Metropolis step
delta_max = 2.0 #Maximum length of Metropolis step
tolerance = .01
idum = MC.seed() #Seed for random number generator

#Function which should be close to zero for optimal delta
def difference(delta):
    x = MC.runMC(MCcycles2,delta,idum,alpha)
    return x.accepted*1.0/MCcycles2 - .5 #We want 50% accepted moves

#Array of alpha values
values = linspace(1.4,2.5,23) #(alpha values)

outfile = open('data','w')

#Loop over alpha values
for alpha in values:

    #Determination of optimal delta value (for each alpha), i.e.
    #finding the zero-point of the difference function by the bisection method
    minimum = delta_min
    maximum = delta_max
    while maximum - minimum > tolerance:
        if difference(minimum)*difference((minimum+maximum)/2) < 0:
            maximum = (minimum + maximum) / 2
        else:
            minimum = (minimum + maximum) / 2
    delta = (minimum + maximum) / 2
    
    #Run MC calculation (store results in x)
    x = MC.runMC(MCcycles,delta,idum,alpha)
    idum = x.idum

    #Calculate statistics
    E = x.sum / x.N
    E2 = x.squaresum / x.N
    sigma = sqrt(E2 - E**2)
    acceptance = x.accepted*1.0/MCcycles
    error = sigma / sqrt(x.N)

    #Print results to screen
    #print 'alpha = %f, <E> = %f, sigma = %f, error = %f, acceptance = %f' %(alpha,E,sigma,error,acceptance)

    #Print results to file
    outfile.write('%f %f %f %f %f\n' %(alpha,E,sigma,error,acceptance))

outfile.close()
