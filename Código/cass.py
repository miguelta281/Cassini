#!/usr/bin/env python
# coding: utf-8

# In[1]:
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from scipy.io import wavfile
import pandas as pd
import matplotlib.gridspec as gridspec


def spectrograma2D (canal, fs, norm =0,dim = "2D",cmapp = "hot" ,a = 10, b =8): 
    """
    canal: Vector con las frecuencias
    fs: frecuencia de muestreo
    norm: vector normalizado
    dim: Verla en 2D o 3D
    cmapp: escala de color de la figura
    a,b: Tamaño de la figura
    """
    
    Sxx, f, t, im= plt.specgram(canal,Fs=fs, cmap = cmapp)
    Sxx_n = (Sxx / np.max(Sxx)) 
    
    if norm == 0:
        if dim == "2D":
            plt.figure(figsize=(a,b))
            plt.pcolormesh(t, f, Sxx, cmap= cmapp)
            plt.ylabel('Frecuencia [Hz]', fontsize = 16)
            plt.xlabel('Tiempo [s]', fontsize = 16)
            plt.colorbar()    
            plt.show()
            
        elif dim == "3D":        
            fig = plt.figure(figsize=(a,b))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(t[None,:], f[:,None], Sxx, cmap= cmapp)
            ax.set_xlabel('Tiempo [s] ')
            ax.set_ylabel('Frecuencia [Hz]')
            ax.set_zlabel('Potencia')
            plt.show()
    
    elif norm == 1:
        if dim == "2D":          
            plt.figure(figsize=(a,b))
            plt.pcolormesh(t, f, Sxx_n, cmap= cmapp)
            plt.ylabel('Frecuencia [Hz]', fontsize = 16)
            plt.xlabel('Tiempo [s]', fontsize = 16)
            plt.colorbar()    
            plt.show()
            
        elif dim == "3D":         
            fig = plt.figure(figsize=(a,b))
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(t[None,:], f[:,None], Sxx_n, cmap= cmapp)
            ax.set_xlabel('Tiempo [s] ')
            ax.set_ylabel('Frecuencia [Hz]')
            ax.set_zlabel('Potencia')
            plt.show()
    
    return (t,f,Sxx)

def spectrogramaLog(canal, fs, norm =0,dim = "2D",cmapp = "hot" ,a = 10, b =8):

    Sxx, f, t, im= plt.specgram(canal,Fs=fs, cmap = cmapp)
    Sxx_l = 10*np.log10(Sxx)
    
    plt.figure(figsize=(a,b))
    plt.pcolormesh(t, f, Sxx_l, cmap= cmapp)
    plt.ylabel('Frecuencia [Hz]', fontsize = 16)
    plt.xlabel('Tiempo [s]', fontsize = 16)
    plt.colorbar()    
    plt.show()
    
    return (t,f,Sxx)

def spectrogramaScal(canal, fs, norm =0,dim = "2D",cmapp = "hot" ,a = 10, b =8):
    
    plt.plot(range(0, 10))

    scale_factor = 0.2

    xmin, xmax = plt.xlim()

    Sxx, f, t, im= plt.specgram(canal,Fs=fs, cmap = cmapp)
    Sxx_n = (Sxx / np.max(Sxx)) 
    
    plt.figure(figsize=(a,b))
    plt.pcolormesh(t, f, Sxx, cmap= cmapp)
    plt.ylabel('Frecuencia [Hz]', fontsize = 16)
    plt.xlabel('Tiempo [s]', fontsize = 16)
    plt.xlim(xmin * scale_factor, xmax * scale_factor)
    plt.colorbar()    
    plt.show()
    
    return (t,f,Sxx)

def matr (f,t,Sxx):
    a1 = []
    for i in range(len((f))):
        b1 = []
        for j in range(len(t)):
            b1.append(Sxx[i][j])
        a1.append(np.array(b1))
    a2 = pd.DataFrame(a1)
    a2.index = f
    return a2

def huella (f,t,Sxx,name,potencia):
    data = matr(f,t,Sxx)
    data.index = f
    
    l = []
    b = []
    h = []
    for i in range(0,data.shape[1]):
        #print(i)
        s = []
        jaja  =data.index
        for j in range(len(data.iloc[:,0])):
            k = jaja[j]
            if (data.iloc[:,i][k] > potencia):
                s.append(j)
        l.append(s)
    for i in range(len(l)):
        c = []
        for j in range(len(l[i])):
            #print(l[i][j])
            c.append(f[l[i][j]])
        b.append(c)
        
    for i in range(len(b)):
        for j in range(len(b[i])):
            h.append(b[i][j])
    
    h.sort()
    
    plt.figure(figsize=(6,6))
    plt.plot(h,'*', label = name)
    plt.ylabel('Frecuencia [Hz]', fontsize = 16)
    plt.legend()
    plt.show()
    
    return h,data

def huella_p (f,t,Sxx,name,dis_val):
    
    huellaa = []
    huellaa, data = huella(f,t,Sxx,name,dis_val)
    
    pp = np.zeros((int(np.max(huellaa)+10), len(huellaa)))
    p = []
    for i in range(len(huellaa)):
        jiji = data.index
        indice = int(np.where(data.index == huellaa[i])[0])
        pp[int(jiji[indice])] = np.max(data.iloc[indice])
        p.append(np.max(data.iloc[indice]))

    
    hhh = np.array(huellaa)
    ppp = np.array(p)
    
    plt.figure(figsize=(16,8))
    plt.subplots_adjust(hspace=0.5)   
        
    plt.subplot(121)
    fff = np.linspace(0,len(pp),len(pp))
    ttt = np.linspace(0,len(pp[0]),len(pp[0]))
    plt.pcolormesh(ttt, fff, pp, cmap= "hot")
    plt.ylim(int(np.min(huellaa)-10),int(np.max(huellaa)+10))
    #plt.ylim(4000,5000)
    plt.ylabel('Frecuencia [Hz]', fontsize = 16)
    plt.colorbar()
    
    plt.subplot(122)
    plt.stem(hhh, ppp)
    plt.ylabel('Potencia', fontsize = 16)
    plt.xlabel('Frecuencia [Hz]', fontsize = 16)
    
     
    plt.show()
    
  
             
    return hhh, ppp 