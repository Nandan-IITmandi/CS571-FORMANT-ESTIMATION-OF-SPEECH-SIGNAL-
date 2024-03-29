

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 11:16:47 2021

@author: teche
"""

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
import librosa
import scipy
from scipy.signal import find_peaks
# Reading the audio file 
speech,fs=sf.read("should.wav")
print('sampling rate', fs) #sampling rate of the audio file 
ln = len(speech)
n=np.linspace(0,ln-1,ln)

#Plot of the speech signal in time domain 
plt.figure(1)
plt.plot(n,speech)
plt.legend(['plot of sample'])
plt.xlabel('sample')
plt.ylabel('amplitude')
plt.grid()

# Hamming window and DFT transformation of speech signal 
def enframe(x, winsize, hoplength, fs, wintype):
    hpln = int(fs*hoplength*0.001)
    winsz =int(fs*winsize*0.001)
    temp=winsz -(len(x)%hpln)
    z =np.pad(x,(0,temp),'constant')
    if wintype == 'hamm':
        win =np.hamming(winsz)
    elif wintype=='rect':
        win=np.ones(winsz)
    frame =[]
    l =len(x)
    for i in range(0,l,hpln):
        a=z[i:i+winsz]*win
        frame.append(a)
    return(frame)

frames = enframe(speech, 30 ,15 ,fs, 'hamm')  #calling the frame function 
# n = np.arange( fs*(winsize - hoplength) )  
F=[]
X=[]
f=fs/1000

#DFT Spectrum of single  frame
for i in  frames:
    b=np.log10(np.abs(np.fft.fft(i)))
    n1=np.linspace(0,len(b)-1, len(b))
    b=b[0:len(b)//2]
    freq=n1*(f/len(n1))
    freq=freq[0:len(freq)//2]
    X.append(b)
    F.append(freq)
def autocorr(x):
    result=np.correlate(x,x, mode='full')
    return result[int(result.size/2):]
    
  
#Applying LPC Analysis
s=0
xs=frames[0]
a=librosa.lpc(xs,30)
im=np.ones(300)
w,h=scipy.signal.freqz([1],a, 150)
plt.figure(2)
plt.subplot(2,1,1)
plt.plot(F[s],X[s])
plt.xlabel('sample of frames')
plt.ylabel('Frequency')
plt.title('Hamming window DFT spectrum')
z=np.log10(np.abs(h))
plt.subplot(2,1,2)
plt.plot(F[s],z)
plt.xlabel('sample of frames')
plt.ylabel('frequency')
plt.title('LPC output of DFT spectrum')

#Formant frequency detection 
y=X[0]
x1=F[0]
plt.figure(3)
peaks2, sr=find_peaks(y,prominence=1)
plt.plot(x1,y)
x2=x1[peaks2]
print("Formant frequencies are " ,x2)
plt.plot(x2,y[peaks2],"g")
plt.title('Formant frequency Detection')

    