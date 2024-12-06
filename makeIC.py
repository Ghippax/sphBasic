# Import core modules
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# Select file info
sphPath = "/home/ghippax/astro/sphBasic/"
sphICFolder = "IC/"

# Select sample IC to make
ic = 1

ICname = ""
if ic == 0:
    ICname = "sphere.dat"
elif ic == 1:
    ICname = "disk.dat"
else:
    ICname = "ic.dat"



### IC configuration
ic_num = 1000
ic_M = 1000
ic_m = ic_M/ic_num
ic_h = 0.1

### Input file data
x = np.zeros(0)
y = np.zeros(0)
z = np.zeros(0)
vx = np.zeros(ic_num)
vy = np.zeros(ic_num)
vz = np.zeros(ic_num)
m = np.ones(ic_num)*ic_m
h = np.ones(ic_num)*ic_h

## IC 0 - Sphere with given density profile
ic0_rad = 100
ic0_rNBins = 100

if ic == 0:
    # Radial bins
    ic0_rBins = np.linspace(0+ic0_rad/(2*ic0_rNBins),ic0_rad,ic0_rNBins)

    # Mass in each shell of the binned sphere
    def Mshell(ri,rf):
        # Volume of the shell times constant density (for any rho distribution, solve integral rho(r)*4*pi*r**2*dr between ri and rf)
        return 4/3*np.pi*(rf**3 - ri**3)*ic_M/(4/3*np.pi*ic0_rad**3)

    # Create poinst in each radial bin
    for i,r in enumerate(ic0_rBins):
        # Calculate number of points in each shell
        ic0_numShell = 0
        if i == ic0_rNBins-1:
            ic0_numShell = Mshell(ic0_rBins[i],ic0_rBins[i]+(ic0_rad - ic0_rad/(2*ic0_rNBins))/ic0_rNBins )/ic_m
        else:
            ic0_numShell = Mshell(ic0_rBins[i],ic0_rBins[i+1])/ic_m
        ic0_numShell = round(ic0_numShell)
        ic0_indices = np.arange(0, ic0_numShell, dtype=float) + 0.5

        # Equally spaced points in a sphere - https://stackoverflow.com/questions/9600801/evenly-distributing-n-points-on-a-sphere
        phi = np.arccos(1 - 2*ic0_indices/ic0_numShell)
        theta = np.pi * (1 + 5**0.5) * ic0_indices

        print(np.size(x),np.size(y),np.size(z))
        x = np.append(x,r * np.cos(theta) * np.sin(phi))
        y = np.append(y,r * np.sin(theta) * np.sin(phi))
        z = np.append(z,r * np.cos(phi))

    print(np.size(x),np.size(y),np.size(z))
    import mpl_toolkits.mplot3d
    #plt.figure().add_subplot(111, projection='3d').scatter(x, y, z);
    #plt.show()

## IC 1 - Simple disk
ic1_rad = 100
if ic == 1:
    ic1_indices = np.arange(0, ic_num, dtype=float) + 0.5

    ic1_r = np.sqrt(ic1_indices/ic_num)*ic1_rad
    ic1_theta = np.pi * (1 + 5**0.5) * ic1_indices

    x = ic1_r*np.cos(ic1_theta)
    y = ic1_r*np.sin(ic1_theta)
    z = np.zeros(ic_num)

    plt.scatter(x,y)
    plt.show()

# Load IC file
f = open(sphPath+sphICFolder+ICname, "w+")
sigDig = 10
for i in range(ic_num):
    f.write(f"{x[i]:.{sigDig}e} {y[i]:.{sigDig}e} {z[i]:.{sigDig}e} {vx[i]:.{sigDig}e} {vy[i]:.{sigDig}e} {vz[i]:.{sigDig}e} {m[i]:.{sigDig}e} {h[i]:.{sigDig}e}\n")
f.close()









