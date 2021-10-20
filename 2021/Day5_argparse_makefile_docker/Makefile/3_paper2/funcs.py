#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:19:43 2021

@author: ali
"""

import numpy as np
import matplotlib.pyplot as plt

def calcHelfrichUq (qmax, rInMum, kappaInKJperMol, youngInKJperMolNm2, kbtInKJperMol):
    x = np.arange(qmax)
    y = np.ones(x.shape)
    for q in x:
        if q==0 or q==1:
            y[q]=0.
        else:
            y[q] = calc_Helfrich_curve(q,rInMum, kappaInKJperMol, youngInKJperMolNm2, kbtInKJperMol)
    return x, y

def calc_Helfrich_curve(q,r,kappa, y, kbt):

    qq=q/r
    multiplyer = (kbt)/(2*y)
    multiplyer *= 1/(2*np.pi*r)
    
    U2  = 1/qq
    U2 -= 1/np.sqrt( qq*qq+y/kappa )
    U2 *= multiplyer
    
    
    return U2

def u_m2_calculator(ulms, mUpperLimit=None):
    ulms = np.asarray(ulms)
    ell_max = ulms.shape[0]
    if mUpperLimit == None:
        mMax = ell_max
    else:
        mMax = mUpperLimit
        


    from scipy.special import lpmn
    from scipy.special import factorial
    lpmns, lpmn_derivatives = lpmn(ell_max-1,ell_max-1,0)

    lpmns=np.transpose(lpmns)
    Legendre_lm=np.zeros_like(ulms)
    Legendre_lm[:,ell_max:-1]=lpmns
    negativelpmns = np.copy(lpmns)
    for l in range(negativelpmns.shape[0]):
        for m in range(negativelpmns.shape[0]):
            negativelpmns[l][m]*=(-1)**m
            negativelpmns[l][m]*=factorial(l-m)/factorial(l+m)
    negativelpmns = np.flip(negativelpmns, axis=1)
    Legendre_lm[:,1:ell_max]=negativelpmns[:,:-1]
    Legendre_lm = np.square(Legendre_lm)

    multiplier= np.zeros_like(ulms)
    for ell in range(ell_max):
        for m in range(-ell,ell+1):
            multiplier[ell][ell_max+m]=(2*ell+1)/(4*np.pi)
            multiplier[ell][ell_max+m]*=factorial(ell-np.abs(m))/factorial(ell+np.abs(m))

    multiplier*=Legendre_lm
    multiplier*=ulms
    u_m=np.sum(multiplier[:mMax,:], axis=0)
    u_m.shape
    u_m_positive= u_m[ell_max:]
    
    u_msum = (u_m_positive+np.flip(u_m[:ell_max+1]) )
    return u_msum[:mMax]
    # return 2*u_msum

def calcNelsonUl (qmax, rInMum, kappaInKJperMol, youngInKJperMolNm2, kbtInKJperMol, p):
    x = np.arange(qmax)
    y = np.ones(x.shape)
    for q in x:
        if q==0 or q==1:
            y[q]=0.
        else:
            y[q] = calc_nelson_amplitude(q,rInMum, kappaInKJperMol, youngInKJperMolNm2, kbtInKJperMol,p)
    return x, y

def calc_nelson_amplitude(ell,r,kappa, y, kbt, P):
    pc=4*np.sqrt(kappa*y)/(r**2)
    gamma = r*r*y/kappa
    
    kr = kappa# * (1 + ( (61*kbt*np.sqrt(gamma))/(4096*kappa) )*(1- 1568*P/(915*np.pi*pc) ) )
    pr = P# + ( (kbt*pc*np.sqrt(gamma))/(24*np.pi*kappa) )*( 1+ (63*np.pi*P)/(128*pc)  )
    yr = y#*( 1 - ( (3*kbt*np.sqrt(gamma))/(256*kappa) )*( 1+ (4*P)/(np.pi*pc)   )    )
    
    A = kr*(ell+2)*(ell+2)*(ell-1)*(ell-1)
    B = pr*r*r*r*( 1 + ell*(ell+1)/2 )
    C = yr*r*r*( 3*(ell*ell + ell - 2)/( 3*(ell*ell + ell) -2 )   )
    
    return kbt/(A - B + C)


def calc_SoftMatter_amplitude(q,r,kappa, y, kbt):

    U2 = kbt/( (q+2)*(q-1) )
    U2 *= 1/( q*(q+1)*kappa +y*r*r )
    return U2

def get_um2(ell_max, rInMum, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model, p=0):
    ulms2=np.zeros((ell_max,2*(ell_max)+1))
    for i in range(ell_max):
        if i == 0 or i== 1:
                amplitude = 0
        else:
            if model=='Nelson':
                amplitude = calc_nelson_amplitude(ell=i, r=rInMum, kappa=kappaInKJperMol, y=YoungInKJperMolNm2, kbt=kbtInKJperMol, P=p)
            elif model=='Safran-Milner':
                amplitude = calc_SoftMatter_amplitude(q=i, r=rInMum, kappa=kappaInKJperMol, y=YoungInKJperMolNm2, kbt=kbtInKJperMol)
            elif model=='NelsonAH':
                amplitude = calc_nelson_amplitude(ell=i, r=rInMum, kappa=kappaInKJperMol, y=YoungInKJperMolNm2, kbt=kbtInKJperMol, P=p)
        
        for j in range(-i,i+1):
            ulms2[i][ell_max+j] = amplitude
    return u_m2_calculator(ulms2)

import sys
Resultspath = '/Users/ali/Documents/Dr Ejtehadi/Programming/Latest Tiam/Ali/Membrae/DerivedData/Membrae/Build/Products/Debug/Results/'
if Resultspath not in sys.path:
    sys.path.append(Resultspath)
from Python_functions.cpp.load_ulm_cpp import load_ulm_cpp
def process_ulm2(ProjectName, filenames, extension):
    """
    filename:  list of file(filepath)
    frames:    Manually input the frames.
    extension: The extension of the file
    rotatoins: The number of random rotations for the angular averaging. 1 for no averaging.
    """
    
    ulm2matrixs = []
    ulms2 = []
    u_m2=[]
    for filename in filenames:
        try:
            ulm_name = Resultspath + ProjectName + '/'+ filename + '/'+ filename + extension
            ulm2, std, ell_max = load_ulm_cpp(ulm_name)
            #VCM already squares the data
            u_m2.append(u_m2_calculator(ulm2))
            
            ulm2matrixs.append(np.copy(ulm2))
            
            ulm2 = np.sum(ulm2, axis=1)
            for i in range(ell_max):
#                 ulm2[i] = 4*np.pi*ulm2[i]/(2*i+1)
                ulm2[i] = ulm2[i]/(2*i+1)
            
            ulms2.append(ulm2)
        except:
            pass
    
    ulm2matrixAVG = np.mean(ulm2matrixs,axis=0)
    
    ulms2 = np.asarray(ulms2)
    avg = np.mean(ulms2,axis=0)
    if ulms2.shape[0]!=1:
        std = np.std( ulms2,axis=0)/np.sqrt(ulms2.shape[0]-1)
        ulm2matrixSTD = np.std(ulm2matrixs,axis=0)/np.sqrt(ulms2.shape[0]-1)
    else:
        std = np.zeros_like(avg)
        ulm2matrixSTD = np.zeros_like(ulm2matrixs)
    u_m_avg = np.mean(u_m2,axis=0)
    if ulms2.shape[0]!=1:
        u_m_std = np.std( u_m2,axis=0)/np.sqrt(ulms2.shape[0]-1)
    else:
        u_m_std = np.zeros_like(u_m_avg)
    
    return avg, std, ell_max, u_m_avg, u_m_std, ulm2matrixAVG, ulm2matrixSTD












def main():



    plt.rcParams.update({'font.size': 12})
    xlabelpad  = 0
    ylabelpad  = -2
    legendfont = 10
    titlefont = 12
    
    linealpha=0.4
    
    fig, axes = plt.subplots(1, 1,figsize=(15,8))
    
    kbtInKJperMol = 2.494
    rInMum = 11.0186
    rInMum = 11
    #Test
    # rInMum = 2.5
    
    YoungInKJperMolMum2 = 192.864*kbtInKJperMol
    YoungInKJperMolMum2 = 170.*kbtInKJperMol
    #Test
    # YoungInKJperMolNm2 =0.069
    
    kappaInKJperMol = 1.86565*kbtInKJperMol
    kappaInKJperMol = 15*kbtInKJperMol
    #Test
    # kappaInKJperMol = 86.6
    
    #Nelson Model
    NelsonP = 0
    
    
    qmax=71
    q=np.arange(qmax)
    
    beg=2
    end=qmax
    
    axi=0
    axj=0
    AlexandraQ   = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 30, 40, 50, 60, 70
                    ]
    AlexandraUq2 = [0.00021, 0.00015, 0.0001, 0.000078, 0.000063, 0.000052, 0.000043, 0.000043, 0.0000335, 0.0000285, 0.000027, 0.000025, 0.000019, 0.000018, 
                    0.000018, 0.0000168, 0.0000155, 0.00001195, 0.0000136, 0.0000058, 0.0000031, 0.0000017, 0.000001, 0.00000044
                    ] 
    
    AlexandraUq2 = np.asarray(AlexandraUq2)
    
    xplot, yplot = calcHelfrichUq(qmax, rInMum = rInMum, kappaInKJperMol = kappaInKJperMol, youngInKJperMolNm2 = YoungInKJperMolMum2, kbtInKJperMol = kbtInKJperMol)
    
    yplot=yplot/rInMum**2
    axes.plot(xplot[beg:end], yplot[beg:end], label="Helfrich" , c = 'orange')
    
    AlexandraUq2=AlexandraUq2/rInMum**2
    # axes.plot(AlexandraQ, AlexandraUq2 , label="Alexandra's data", c= 'g')
    
    ell_max=qmax
    
    
    model = 'Safran-Milner'
    u_m2 = get_um2(ell_max, rInMum, kappaInKJperMol, YoungInKJperMolMum2, kbtInKJperMol, model)
    #SoftMatter Model
    axes.plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{Safran-Milner}|^2\rangle$" , c='r')
    
    
    
    model = 'Nelson'
    u_m2 = get_um2(ell_max, rInMum, kappaInKJperMol, YoungInKJperMolMum2, kbtInKJperMol, model, 0)
    axes.plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{Nelson}|^2\rangle$ $P=0$", c ='b' )
    
    
    NelsonP = -60
    u_m2 = get_um2(ell_max, rInMum, kappaInKJperMol, YoungInKJperMolMum2, kbtInKJperMol, model, NelsonP)
    # axes.plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{{Nelson}}|^2\rangle$ $P={:.1e}kPa$".format(NelsonP*10**4/6.022), c ='skyblue' )
    
    
    axes.legend(fontsize=legendfont)
    axes.set_title("2D", fontsize=titlefont)
    axes.set_ylabel(r'$\langle|u_{m}|^2\rangle$', labelpad=ylabelpad)
    axes.set_xlabel('Mode number, $m$ ',labelpad=xlabelpad)
    axes.set_yscale("log")
    axes.set_xscale("log")    
    
    plotstat=False
    if plotstat==True:
        fig, axes = plt.subplots(2, 2,figsize=(15,8))
        
        ProjectName = "MemTest/step20/friction0_1/300k"
        
        # filename= ["2021_06_24_time_13_22_000","2021_06_24_time_13_22_001","2021_06_24_time_13_22_002","2021_06_24_time_13_22_003","2021_06_24_time_13_23_000"]
        filename= ["2021_07_12_time_18_42_000", "2021_07_12_time_18_42_001",]
        
        avg, std, ell_max, um2, um2_error = process_ulm2(ProjectName, filenames=filename, extension='_mem0_Dulmts.txt')
        
        
        kbtInKJperMol = 2.494
        rInNm = 10_800
        rInNm = 2_500
        YoungInKJperMolNm2 = 0.0577#*10**6
        YoungInKJperMolNm2 = 0.0693#*10**6
        kappaInKJperMol = 4.330
        kappaInKJperMol = 85.7
        
        #Nelson Model
        NelsonP = 0
        axj=0
        axes[axi][axj].plot(xplot[beg:end], um2[beg:end], '.', label=r"$U_m^2$")
        
        
        xplot, yplot = calcHelfrichUq(qmax, rInMum = rInNm, kappaInKJperMol = kappaInKJperMol, youngInKJperMolNm2 = YoungInKJperMolNm2, kbtInKJperMol = kbtInKJperMol)
        
        yplot=yplot/rInNm**2
        axes[axi][axj].plot(xplot[beg:end], yplot[beg:end], label="Helfriche" , c = 'orange')
        
        model = 'Safran-Milner'
        u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model)
        #SoftMatter Model
        axes[axi][axj].plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{Safran-Milner}|^2\rangle$" , c='r')
        
        
        model = 'Nelson'
        u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model, 0)
        axes[axi][axj].plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{Nelson}|^2\rangle$ $P=0$", c ='b' )
        
        # rInNm = 250
        # u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model, 0)
        # axes[axi][axj].plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{{Nelson}}|^2\rangle$ $P=0$ $R_{{{}}}$".format(rInNm), c ='b' )
        
        # rInNm = 25000
        # u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model, 0)
        # axes[axi][axj].plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{{Nelson}}|^2\rangle$ $P=0$ $R_{{{}}}$".format(rInNm), c ='b' )
        
        
        axes[axi][axj].legend(fontsize=legendfont)
        axes[axi][axj].set_title("2D R=2500", fontsize=titlefont)
        axes[axi][axj].set_ylabel(r'$\langle|u_{m}|^2\rangle$', labelpad=ylabelpad)
        axes[axi][axj].set_xlabel('Mode number, $m$ ',labelpad=xlabelpad)
        axes[axi][axj].set_yscale("log")
        axes[axi][axj].set_xscale("log")
        
        axi=0
        axj=1
        rInNm = 2_500
        xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        axes[axi][axj].plot(xplot[beg:end], yplot[beg:end] , label="Nelson3D")
        Teff=kbtInKJperMol*np.sqrt(YoungInKJperMolNm2*rInNm**2/kappaInKJperMol)/kappaInKJperMol
        axes[axi][axj].errorbar(xplot[beg:end], avg[beg:end], yerr = std[beg:end], fmt='.', label=r"$U_{{\ell,m}}^2$, $T_{{eff}}={:.4}$".format(Teff))
        
        # rInNm = 250
        # xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        # axes[axi][axj].plot(xplot[beg:end], yplot[beg:end] , label="Nelson3D $R_{{{}}}$".format(rInNm))
        
        # rInNm = 25000
        # xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        # axes[axi][axj].plot(xplot[beg:end], yplot[beg:end] , label="Nelson3D $R_{{{}}}$".format(rInNm))
        
        
        
        xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        
        print(avg[beg:end]/yplot[beg:end])
        
        axes[axi][axj].legend(fontsize=legendfont)
        axes[axi][axj].set_title("3D R=2500", fontsize=titlefont)
        axes[axi][axj].set_ylabel(r'$\langle|u_{\ell,m}|^2\rangle$', labelpad=ylabelpad)
        axes[axi][axj].set_xlabel('Mode number, $\ell$ ',labelpad=xlabelpad)
        axes[axi][axj].set_yscale("log")
        axes[axi][axj].set_xscale("log")
        
        filename= ["2021_06_24_time_13_22_000","2021_06_24_time_13_22_001","2021_06_24_time_13_22_002","2021_06_24_time_13_22_003","2021_06_24_time_13_23_000"]
        # filename= ["2021_07_12_time_18_42_000", "2021_07_12_time_18_42_001",]
        
        avg, std, ell_max, um2, um2_error = process_ulm2(ProjectName, filenames=filename, extension='_mem0_Dulmts.txt')
        
        
        kbtInKJperMol = 2.494
        rInNm = 10_800
        # rInNm = 2_500
        YoungInKJperMolNm2 = 0.0577#*10**6
        # YoungInKJperMolNm2 = 0.0693#*10**6
        kappaInKJperMol = 4.330
        # kappaInKJperMol = 85.7
        
        #Nelson Model
        NelsonP = 0
        axi=1
        axj=0
        axes[axi][axj].plot(xplot[beg:end], um2[beg:end], '.', label=r"$U_m^2$")
        
        
        xplot, yplot = calcHelfrichUq(qmax, rInMum = rInNm, kappaInKJperMol = kappaInKJperMol, youngInKJperMolNm2 = YoungInKJperMolNm2, kbtInKJperMol = kbtInKJperMol)
        
        yplot=yplot/rInNm**2
        axes[axi][axj].plot(xplot[beg:end], yplot[beg:end], label="Helfriche" , c = 'orange')
        
        model = 'Safran-Milner'
        u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model)
        #SoftMatter Model
        axes[axi][axj].plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{Safran-Milner}|^2\rangle$" , c='r')
        
        
        model = 'Nelson'
        u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model, 0)
        axes[axi][axj].plot(xplot[beg:end], u_m2[beg:end] ,label= r"$\sum \langle|U_{Nelson}|^2\rangle$ $P=0$", c ='b' )
        
        axes[axi][axj].legend(fontsize=legendfont)
        axes[axi][axj].set_title("2D R=10'800", fontsize=titlefont)
        axes[axi][axj].set_ylabel(r'$\langle|u_{m}|^2\rangle$', labelpad=ylabelpad)
        axes[axi][axj].set_xlabel('Mode number, $m$ ',labelpad=xlabelpad)
        axes[axi][axj].set_yscale("log")
        axes[axi][axj].set_xscale("log")
        
        axi=1
        axj=1
        
        xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        axes[axi][axj].plot(xplot[beg:end], yplot[beg:end] , label="Nelson3D")
        Teff=kbtInKJperMol*np.sqrt(YoungInKJperMolNm2*rInNm**2/kappaInKJperMol)/kappaInKJperMol
        axes[axi][axj].errorbar(xplot[beg:end], avg[beg:end], fmt='.', yerr = std[beg:end], label=r"$U_{{\ell,m}}^2$, $T_{{eff}}={:.4}$".format(Teff))
        
        # kappaInKJperMol = 40
        # xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        # axes[axi][axj].plot(xplot[beg:end], yplot[beg:end] , label="Nelson3D $\kappa_{{{}}}$".format(kappaInKJperMol))
        
        # kappaInKJperMol = 400
        # xplot, yplot = calcNelsonUl(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, 0)
        # axes[axi][axj].plot(xplot[beg:end], yplot[beg:end] , label="Nelson3D $\kappa_{{{}}}$".format(kappaInKJperMol))
        
        
        
        axes[axi][axj].legend(fontsize=legendfont)
        axes[axi][axj].set_title("3D R=10'800", fontsize=titlefont)
        axes[axi][axj].set_ylabel(r'$\langle|u_{\ell,m}|^2\rangle$', labelpad=ylabelpad)
        axes[axi][axj].set_xlabel('Mode number, $\ell$ ',labelpad=xlabelpad)
        axes[axi][axj].set_yscale("log")
        axes[axi][axj].set_xscale("log")
        
        fig.subplots_adjust(hspace=0.3, wspace=0.3)

if __name__ == "__main__":
    main()











