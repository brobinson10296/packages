import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#NBNADS needs to be equal to number of bands used with xtraxt_bands tool

def bands_function(bands_input_file=None,OUTCAR=None,NBANDS=None,shift_to=None,CB1=1000,scale_x=None,soc=False):
    if NBANDS==None:
        with open(OUTCAR) as f:
            NBANDS=[int(line.split()[-1]) for line in f if 'NBANDS' in line][0]
    bands = np.loadtxt(bands_input_file)
    bands = np.reshape(bands,(NBANDS,int(len(bands)/NBANDS),2))
    #set soc factor
    if soc==True:
        soc_factor=2
    else:
        soc_factor=1
    #scales x axis to match other data
    if scale_x!=None:
        max_x=max(bands[0][-1])
        scale=scale_x/max_x
        bands[:,:,0]*=scale
    #sets VBM to 0
    VBM_to_0 = max(bands[soc_factor*(CB1-1)-1][:,1])
    bands[:,:,1]-=VBM_to_0
    #non-shifted Eg
    VBM=max(bands[soc_factor*(CB1-1)-1][:,1])
    CBM=min(bands[soc_factor*(CB1-1)][:,1])
    Eg_no_shift=CBM-VBM
    #apply rigid scissor shift to conduction bands
    if shift_to != None:
        CBM=min(bands[soc_factor*(CB1-1)][:,1])
        shift=shift_to-CBM
        for count,n in enumerate(bands,1):
            if count>soc_factor*(CB1-1):
                n[:,1]+=shift
    #finds VBM and CBM to get band gap
    VBM=max(bands[soc_factor*(CB1-1)-1][:,1])
    CBM=min(bands[soc_factor*(CB1-1)][:,1])
    Eg=CBM-VBM
    return bands,Eg,Eg_no_shift
