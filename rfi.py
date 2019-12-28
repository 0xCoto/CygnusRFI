import os
import sys
import datetime
from time import sleep

#Define GRC observation parameters
bandwidth = '2400000'
channels = '512'
nbins = '5000' #t_int = 1.06666667 sec
duration = '10'
fmin = 380000000
fmax = 460000000

number_of_days_to_run = 1

print("\n------------------------------\nBeginning RFI measurement...\n------------------------------\n")

#1 spectra/~7 hours (7 = round(24/3.52))
for k in range(1): #amount_of_sweeps = int(round(3.52*number_of_days_to_run))
    print("[!] Sweep number = "+str(k+1)+"\n")
    q=0
    for freq in range(fmin, fmax, int(bandwidth)):
        print("\n-------\n[*] Currently monitoring f_center = "+str(0.000001*freq)+" +/- "+str(float(float(bandwidth)*0.000001)/2)+" MHz (q="+str(q)+")...\n------\n")
        
        #Define observation frequency
        f_center = str(freq)
        
        #Delete pre-existing observation.dat file
        #Note current datetime
        #currentDT = datetime.datetime.now()
        #obsDT = currentDT.strftime("%d_%H_%M")
        
        #Execute top_block.py with parameters
        sys.argv = ['top_block.py', '--c-freq='+f_center, '--samp-rate='+bandwidth, '--nchan='+channels, '--nbin='+nbins, '--obs-time='+duration]
        execfile('top_block.py')
        os.rename('observation.dat', str(k)+"_"+str(q)+'.dat')
        
        #Execute plotter
        sys.argv = ['rfi_plot.py', 'freq='+f_center, 'samp_rate='+bandwidth, 'nchan='+channels, 'nbin='+nbins]
        execfile('rfi_plotter.py')
        #os.rename('rfi_plot.png', obsDT+'.png')
        q = q+1
    print("\n\n[+] Sweep complete! Moving on to next sweep...\n")