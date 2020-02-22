import os
import sys
from time import sleep

#Define GRC observation parameters
bandwidth = '2400000'
channels = '1024'
t_int = '1'
duration = '10'
fmin = 1400000000
fmax = 1500000000

nbins = str(int(float(t_int) * float(bandwidth)/float(channels)))

#Delete pre-existing observation.dat file
for file_name in os.listdir('.'):
    if file_name.endswith('.dat'):
        try:
            os.remove(file_name)
        except OSError:
            pass
try:
    os.remove('rfi_plot.png')
except OSError:
    pass

print('\n\033[1;33;48m+=================================================================+')
print('\033[1;33;48m| \033[1;36;48mCygnusRFI\033[1;33;48m:\033[1;32;48m An open-source Radio Frequency Interference analyzer\033[1;33;48m |')
print('\033[1;33;48m+=================================================================+')
sleep(0.5)
print('\n\033[1;33;48m\033[4;33;48mRFI Measurement Parameters:\033[0;32;48m')
sleep(0.15)
print('\033[1;32;48mFrequency range to scan: \033[1;36;48m'+str(float(fmin)/1000000)+'-'+str(float(fmax)/1000000)+' MHz')
sleep(0.15)
print('\033[1;32;48mBandwidth per spectrum: \033[1;36;48m'+str(float(bandwidth)/1000000)+' MHz')
sleep(0.15)
print('\033[1;32;48mIntegration time per spectrum: \033[1;36;48m'+duration+' sec')
sleep(0.15)
print('\033[1;32;48mNumber of channels per spectrum (FFT Size): \033[1;36;48m'+str(float(bandwidth)/1000000)+' MHz')
sleep(0.15)
print('\033[1;32;48mIntegration time per FFT sample: \033[1;36;48m'+t_int+' sec')
sleep(0.5)
print("\n\033[1;32;48mEstimated completion time: \033[1;36;48m"+str(float(duration)*float(fmax-fmin)/float(bandwidth))+" sec")

sleep(0.5)
proceed = raw_input("\n\033[1;36;48mProceed to measurement? [Y/n]: \033[1;33;48m")

if proceed.lower() != 'n' and proceed.lower() != 'no':
    print('\n\033[1;33;48m+=================================================================+')
    print('\033[1;33;48m| [+] \033[1;32;48m Starting measurement...\033[1;33;48m                                    |')
    print('\033[1;33;48m+=================================================================+\n')
    
    q=0
    for freq in range(fmin, fmax, int(bandwidth)):
        print("\033[1;33;48m\n---------------------------------------------------------------------------\n  \033[1;33;48m[*] \033[1;32;48mCurrently monitoring f_center = "+str(0.000001*freq)+" +/- "+str(float(float(bandwidth)*0.000001)/2)+" MHz (iteration: "+str(q)+")...\n\033[1;33;48m---------------------------------------------------------------------------")
        
        #Define observation frequency
        f_center = str(freq)
        
        #Execute top_block.py with parameters
        print('\033[0m')
        sys.argv = ['top_block.py', '--c-freq='+f_center, '--samp-rate='+bandwidth, '--nchan='+channels, '--nbin='+nbins, '--obs-time='+duration]
        execfile('top_block.py')
        os.rename('observation.dat', str(q)+'.dat')
        
        q = q+1
    print('\n\033[1;33;48m+=================================================================+')
    print('\033[1;33;48m| \033[1;32;48mMeasurement finished!\033[1;33;48m |')
    print('\033[1;33;48m+=================================================================+\n')
    
    f_center = str(fmin)
    sys.argv = ['rfi_plotter.py', 'freq='+f_center, 'samp_rate='+bandwidth, 'nchan='+channels, 'nbin='+nbins, 'n='+str(q), 'dur='+duration, 'fminimum='+str(fmin), 'fmaximum='+str(fmax)]
    execfile('rfi_plotter.py')
    
    print('\033[1;32;48mYour data has been saved as \033[1;36;48mrfi_plot.png\033[1;32;48m.')
else:
    print('\n\033[1;31;48m[!] Exiting...\n')