import numpy as np
import math as m
import matplotlib.pyplot as plt
from time import sleep

imp0=377.0  # Free space impedance

size=1800  # Domain size
#Dielectric distribution
epsilon = 1
eps= np.ones(size)
eps[:] = epsilon

# setting  ABC constants _AFTER_ epsilon (we need speed of ligth in media)
# Taflove, eq. 6.35
c = 1/np.sqrt(epsilon)
a = (c-1)/(c+1)
b = 2/(c + 1)
# Left boundary
wl_nm1,wl_n,wl_np1 = 0,0,0 # Field at x=0 at time steps n-1, n, n+1
wlp1_nm1,wlp1_n,wlp1_np1 = 0,0,0 # Field at x=1 at time steps n-1, n, n+1
# Right boundary
wr_nm1,wr_n,wr_np1 = 0,0,0 # Field at x=size at time steps n-1, n, n+1
wrm1_nm1,wrm1_n,wrm1_np1 = 0,0,0 # Field at x=size-1 at time steps n-1, n, n+1

#Source 
source_width = 30.0*np.sqrt(epsilon)
#source_width = size*np.sqrt(epsilon)
delay = 10*source_width
source_x = int(1.0*size/2.0)  #Source position
def source(current_time, delay, source_width):
    return m.exp(-(current_time-delay)**2/(2.0 * source_width**2))


#Model
total_steps = int((size+delay)*np.sqrt(epsilon))  # Time stepping
frame_interval = int(total_steps/30.0)
all_steps = np.linspace(0, size-1, size)


#Inital field E_z and H_y is equal to zero
ez = np.zeros(size)
hy = np.zeros(size)
x = np.arange(0,size-1,1)
#print(x)
for time in range(total_steps):
    ######################
    #Magnetic field
    ######################
    hy[-1] = hy[-2]
    hy[x] = hy[x] + (ez[x+1] - ez[x])/imp0
    ######################
    #Electric field
    ######################
    ez[0] = ez[1]
    ez[x+1] = ez[x+1] + (hy[x+1]-hy[x])*imp0/eps[x+1]
    ez[source_x] += source(time, delay, source_width)
    ######################
    # Output
    ######################
    if time % frame_interval == 0:
        plt.clf()
        plt.title("Ez after t=%i"%time)
        plt.plot(all_steps, ez, all_steps, hy*imp0)
        plt.savefig("step1-at-time-%i.png"%time,pad_inches=0.02, bbox_inches='tight')
        plt.draw()
        #    plt.show()
        plt.clf()
        plt.close()
