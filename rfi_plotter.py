#!/usr/bin/env python
try:
    import matplotlib
    matplotlib.use('Agg')
    
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 32})
    import argparse
    from matplotlib.gridspec import GridSpec
    
    parser = argparse.ArgumentParser()
    parser.add_argument('freq')
    parser.add_argument('samp_rate')
    parser.add_argument('nchan')
    parser.add_argument('nbin')
    parser.add_argument('n')
    parser.add_argument('dur')
    parser.add_argument('fminimum')
    parser.add_argument('fmaximum')
    args = parser.parse_args()
    
    def decibel(x):
        return 10.0*np.log10(x)
        #return x
    
    if __name__ == "__main__":
        #Observation parameters
        exec(args.freq)
        exec(args.samp_rate)
        exec(args.nchan)
        exec(args.nbin)
        exec(args.n)
        exec(args.dur)
        exec(args.fminimum)
        exec(args.fmaximum)
        
        frequency=freq
        
        #Load data
        z=1000*(np.fromfile("0.dat", dtype="float32").reshape(-1, nchan)/nbin)
        allarrays=[]
        
        #N = amount of .dat files
        for i in range(int(n)):
            final = 1000*(np.fromfile(str(i)+".dat", dtype="float32").reshape(-1, nchan)/nbin)
            allarrays.append(final)
        z_final = np.concatenate(allarrays,axis=1)
        
        #Define numpy array for Power vs Time plot
        
        #Number of sub-integrations
        nsub = z_final.shape[0]
        
        #Compute average spectrum
        zmean = np.mean(z_final, axis=0)
        
        #Compute time axis
        tint = float(nbin*nchan)/samp_rate
        t = tint*np.arange(nsub)
        
        #Compute frequency axis (convert to MHz)
        allfreq=[]
        for i in range(int(n)):
            freq = np.linspace((frequency+samp_rate*i)-0.5*samp_rate, (frequency+samp_rate*i)+0.5*samp_rate, nchan, endpoint=False)*1e-6
            allfreq.append(freq)
        freq = np.concatenate(allfreq)
        
        #Initialize plot
        fig = plt.figure(figsize=(5*n,20.25))
        gs = GridSpec(1,1)
                
        #Plot average spectrum
        ax1 = fig.add_subplot(gs[0,0])
        ax1.plot(freq, decibel(zmean), '#3182bd')
        ax1.fill_between(freq, decibel(zmean), color='#deebf7')
        ax1.set_xlim(np.min(freq), np.max(freq)) #np.min(freq), np.max(freq)
        ax1.set_ylim(np.amin(decibel(zmean))-0.5, np.amin(decibel(zmean))+15)
        ax1.ticklabel_format(useOffset=False)
        ax1.set_xlabel("Frequency (MHz)", labelpad=25)
        ax1.set_ylabel("Relative Power (dB)", labelpad=25)
        ax1.set_title("\nAveraged RFI Spectrum", pad=25)
        ax1.annotate('Frequency range scanned: '+str(float(fminimum)/1000000)+'-'+str(float(fmaximum)/1000000)+' MHz ($\\Delta\\nu$ = '+str(float((fmaximum)-float(fminimum))/1000000)+' MHz)\nBandwidth per spectrum: '+str(float(samp_rate)/1000000)+' MHz\nIntegration time per spectrum: '+str(dur)+" sec\nNumber of channels per spectrum (FFT size): "+str(nchan), xy=(17, 1179), xycoords='axes points', size=32, ha='left', va='top', color='brown')
        ax1.grid()
        
        plt.tight_layout()
        plt.savefig("rfi_plot.png")
except Exception as e:
    print(e)
    pass
