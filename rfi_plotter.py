#!/usr/bin/env python
try:
    import matplotlib
    matplotlib.use('Agg')
    
    import numpy as np
    import matplotlib.pyplot as plt
    import argparse
    from matplotlib.gridspec import GridSpec
    
    #parser = argparse.ArgumentParser()
    #parser.add_argument('freq')
    #parser.add_argument('samp_rate')
    #parser.add_argument('nchan')
    #parser.add_argument('nbin')
    #args = parser.parse_args()
    
    def decibel(x):
        #return 10.0*np.log10(x)
        return x
    
    if __name__ == "__main__":
        #Observation parameters
        exec(args.freq)
        exec(args.samp_rate)
        exec(args.nchan)
        exec(args.nbin)
        #freq=300000000
        frequency=freq
        #samp_rate=2400000
        #nchan=1024
        #nbin=23436
        
        #Load data
        z=1000*(np.fromfile("0_0.dat", dtype="float32").reshape(-1, nchan)/nbin)
        allarrays=[]
        N=1 #amount_of_.dat_files
        for i in range(N):
            final = 1000*(np.fromfile("0_"+str(i)+".dat", dtype="float32").reshape(-1, nchan)/nbin)
            print(final.shape)
            allarrays.append(final)
        z_final = np.concatenate(allarrays,axis=1)
        #print(type(z_final))
        #print(z_final.shape)
        #z_final[z_final > 4000] = 4000
        
        #Define numpy array for Power vs Time plot
        #w = np.mean(a=z, axis=1)
        
        #Number of sub-integrations
        nsub = z_final.shape[0]
        
        #Compute average spectrum
        zmean = np.mean(z_final, axis=0)
        
        #Compute time axis
        tint = float(nbin*nchan)/samp_rate
        t = tint*np.arange(nsub)
        
        #v = np.arange(0, np.max(t)+tint, tint)
        
        #Compute frequency axis (convert to MHz)
        allfreq=[]
        for i in range(N):
            freq = np.linspace((frequency+samp_rate*i)-0.5*samp_rate, (frequency+samp_rate*i)+0.5*samp_rate, nchan, endpoint=False)*1e-6
            allfreq.append(freq)
        freq = np.concatenate(allfreq)
        print(999,freq)
        #freq = freq*i
        print(freq.shape)
        #Initialize plot
        fig = plt.figure(figsize=(100,50))
        gs = GridSpec(2,1)
        
        #Plot average spectrum
        ax1 = fig.add_subplot(gs[0,0])
        ax1.plot(freq, decibel(zmean))
        ax1.set_xlim(np.min(freq), np.max(freq)) #np.min(freq), np.max(freq)
        ax1.ticklabel_format(useOffset=False)
        ax1.set_xlabel("Frequency (MHz)")
        ax1.set_ylabel("Relative Power")
        ax1.set_title("Averaged Spectrum")
        
        #Plot dynamic spectrum
        ax2 = fig.add_subplot(gs[1,0])
        ax2.imshow(decibel(z_final), origin="lower", interpolation="None", aspect="auto",
                   extent=[np.min(freq), np.max(freq), np.min(t), np.max(t)])
        ax2.ticklabel_format(useOffset=False)
        ax2.set_xlabel("Frequency (MHz)")
        ax2.set_ylabel("Time (s)")
        ax2.set_title("Dynamic Spectrum (Waterfall)")
        
        #Plot Power vs Time
        #ax3 = fig.add_subplot(gs[1,:])
        #ax3.plot(v,w)
        #ax3.axvline(x=9180, color='blue', linestyle='--', linewidth=2)
        #ax3.axvline(x=8100, color='red', linestyle='--', linewidth=2)
        #ax3.axvline(x=7200, color='orange', linestyle='--', linewidth=2)
        #ax3.set_xlim(0,np.max(t)+tint)
        #ax3.set_xlabel("Time (s)")
        #ax3.set_ylabel("Relative Power")
        #ax3.set_title("Power vs Time")
        
        plt.tight_layout()
        plt.savefig("rfi_plot.png")
except Exception as e:
    print(e)
    pass
