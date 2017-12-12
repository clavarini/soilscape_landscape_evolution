#    cliff dynamics for transport limitation

#  This code is designed to be used in conjunction with the explanatory details
#  in Willgoose (2018) "Principles of Soilscape and Landscape Evolution", Cambridge University Press
#
#    Copyright (C) 2017  Garry Willgoose, The University of Newcastle
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import numpy
import matplotlib
import matplotlib.pyplot
import copy

NUM_NODES = 100
NUM_OUTPUT = 10
PLATEAU_HEIGHT = 10
CLIFF_PROPORTION = 0.2
CLIFF_HEIGHT = PLATEAU_HEIGHT*CLIFF_PROPORTION

# the physics parameters. Note that the SIM_TIME has been determined so that the
# average elevation at the end of the simulation is 6.0. If you run with other
# values for M and N you will need to determine the appropriate value of
# SIM_TIME to get an average elevation of 6.0 at the end of the simulation.

#M = 1.0
#N = 1.0
#BETA=0.001
#SIM_TIME = 76000

#M = 2.0
#N = 2.0
#BETA=0.00025
#SIM_TIME = 28000

#M = 2.0
#N = 1.0
#BETA=0.00001
#SIM_TIME = 9600

M = 1.0
N = 2.0
BETA=0.1
SIM_TIME = 53000

DX= 10.0
OUT_TIME = int(SIM_TIME/NUM_OUTPUT)

# cambridge requirements
matplotlib.rcParams.update({'font.family': 'sans-serif'})
matplotlib.rcParams.update({'font.size': 18})
matplotlib.rcParams.update({'axes.labelsize': 'large'})
matplotlib.rcParams.update({'legend.fontsize': 'medium'})
matplotlib.rcParams.update({'legend.labelspacing': 0.2})

slope = numpy.zeros((NUM_NODES),'f')
z_change = numpy.zeros((NUM_NODES),'f')
z = numpy.zeros((NUM_NODES),'f')
qs = numpy.zeros((NUM_NODES),'f')
z_new = numpy.zeros((NUM_NODES),'f')
z_save = numpy.zeros((NUM_OUTPUT+1,NUM_NODES),'f')
save_index=1

i_half = int(NUM_NODES/2.0)
z[:i_half] = PLATEAU_HEIGHT
z[i_half] = PLATEAU_HEIGHT-CLIFF_HEIGHT
dz = z[i_half]/(NUM_NODES-i_half-1)
for i in range(i_half+1,NUM_NODES):
  z[i] = max(z[i-1]-dz,0.0)
z_new[0] = z[0]
z_save[0,:] = z
z_save[:,0] = PLATEAU_HEIGHT
print 'output 0 0 ',numpy.mean(z)

#print z
fout = open('cliff-trans.out.txt','w')
for t in range(1,SIM_TIME+1):
  output = t%OUT_TIME == 0
  for i in range(1,NUM_NODES-1):
#   upstream weighted finite difference
#    slope[i]=max((z[i-1]-z[i])/DX,0.0)

#   centrally weighted finite difference
#    slope[i]=max((z[i-1]-z[i+1])/DX,0.0)

#   downstream weighted finite difference (traditional)
    slope[i]=max((z[i]-z[i+1])/DX,0.0)
    
    qs[i] = BETA * (i*DX)**M * slope[i]**N
  for i in range(1,NUM_NODES-1):
    z_new[i] = z[i]+(qs[i-1]-qs[i])/DX
  if output:
    print 'output',t,save_index,numpy.mean(z)
    fout.write(' '+str(t)+' '+str(z_new))
    z_save[save_index]=copy.copy(z_new)
    save_index=save_index+1
  z=copy.copy(z_new)

fout.close

fig = matplotlib.pyplot.figure()

contents = fig.add_subplot(111)
for k in range(NUM_OUTPUT+1):
  if k ==0 :
    width =3
    linestyle = '-'
  else:
    width=1
    linestyle = '-'
  stuff = contents.plot(z_save[k],'k--',lw=width,linestyle=linestyle)
#contents.legend()
#contents.legend(loc='lower right')
matplotlib.pyplot.title('Transport Limitation: m='+str(M)+' , n='+str(N))
matplotlib.pyplot.xlabel('Distance')
matplotlib.pyplot.ylabel('Elevation')


matplotlib.pyplot.show()
