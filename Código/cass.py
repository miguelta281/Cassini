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
        