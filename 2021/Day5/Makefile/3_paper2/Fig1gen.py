#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:19:43 2021

@author: ali
"""

import numpy as np
import matplotlib.pyplot as plt
from funcs import calcHelfrichUq
from funcs import calc_Helfrich_curve
from funcs import u_m2_calculator
from funcs import calcNelsonUl
from funcs import calc_nelson_amplitude
from funcs import calc_SoftMatter_amplitude
from funcs import get_um2
from funcs import process_ulm2




def main():

    savefig=True
    dpi = 1200
    figFormat='pdf'
    
    
    # plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams.update({'font.size': 18})
    xlabelpad  = 0
    ylabelpad  = -2
    legendfont = 18
    titlefont = 16
    linesize = 4
    linealpha=0.4
    
    fig, axes = plt.subplots(2, 1,figsize=(10,8))
    
    kbtInKJperMol = 2.494
    rInNm = 100
    
    YoungInKJperMolNm2 = 0.005*2/np.sqrt(3)*kbtInKJperMol
    kappaInKJperMol = 100*np.sqrt(3)/2*kbtInKJperMol
    
    #Nelson Model
    NelsonP = 0
    
    from matplotlib.pyplot import cm
    colors = cm.rainbow(np.linspace(0,1,5))
    alpha= 1
    for c in colors:
        c[3]=alpha
    
    
    qmax=81
    q=np.arange(qmax)
    
    beg=2
    end=qmax
    
    axi=0
    axj=0
      
    xplot, yplotHelfrich = calcHelfrichUq(qmax, rInMum = rInNm, kappaInKJperMol = kappaInKJperMol, youngInKJperMolNm2 = YoungInKJperMolNm2, kbtInKJperMol = kbtInKJperMol)
    
    yplotHelfrich=yplotHelfrich/rInNm**2
    
    ell_max=qmax
    
    
    model = 'Safran-Milner'
    u_m2 = get_um2(ell_max, rInNm, kappaInKJperMol, YoungInKJperMolNm2, kbtInKJperMol, model)
    
    
    axes[0].plot(xplot[beg:end], yplotHelfrich[beg:end] ,label= r"$\frac{\overline{\langle|U_{m}|^2\rangle}_{Helfrich}}{r^2}$" ,lw =linesize, c=colors[0])
    axes[0].plot(xplot[beg:end], u_m2[beg:end] ,label=r"$\langle|U_{m}(\frac{\pi}{2})|^2\rangle_{Safran-Milner}$" ,lw=linesize,c=colors[1])
    
    axes[0].legend(fontsize=legendfont)
    axes[0].set_title(r"$\sigma={:.4f}$".format(YoungInKJperMolNm2)
                       +",   "
                       +r"$\mathcal{{\kappa}}={:.4f}$".format(kappaInKJperMol)
                       +",   "
                       +r"$r={:.4f}$".format(rInNm)
                      , fontsize=titlefont)
    axes[0].set_ylabel('Amplitudes', labelpad=ylabelpad)
    # axes[0].set_xlabel('Mode number, $m$ ')
    axes[0].set_yscale("log")
    axes[0].set_xscale("log")   
    axes[0].grid(axis='x', which='both', color='k',alpha=0.5, linestyle=':')
    
    axes[1].plot(xplot[beg:end], yplotHelfrich[beg:end]/u_m2[beg:end] ,label= r"$\frac{\overline{\langle|U_{m}|^2\rangle}_{Helfrich}}{r^2} .\frac{1}{\langle|U_{m}(\frac{\pi}{2})|^2\rangle_{Safran-Milner}}$" , c=colors[4],lw=linesize)
    axes[1].hlines(y=1,color='k',ls=':', xmin = xplot[beg], xmax=xplot[end-1],lw=linesize)
    
    axes[1].legend(fontsize=legendfont+4, loc ='upper center')

    # axes[1].set_title("2D", fontsize=titlefont)
    axes[1].set_ylabel('Amplitude ratio', labelpad=ylabelpad+32)
    axes[1].set_xlabel('Mode number, $m$ ',labelpad=xlabelpad)
    axes[1].set_yscale("log")
    axes[1].set_xscale("log")    
    # axes[1].ticklabel_format(axis='y', style='plain')  
    
    
    axes[0].text(1.7, 0.5*10**-4, '$a)$', fontsize=15)
    axes[1].text(1.7, 3.8, '$b)$', fontsize=15)
    
    
    
    #set x ticks
    import matplotlib.transforms    
    # Create offset transform by 5 points in x direction
    dx = 5/72.; dy = 0/72. 
    offset = matplotlib.transforms.ScaledTranslation(dx, dy, fig.dpi_scale_trans)
    # apply offset transform to all x ticklabels.
    for label in axes[1].xaxis.get_majorticklabels():
        label.set_transform(label.get_transform() + offset)
    from matplotlib.ticker import StrMethodFormatter
    axes[1].xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    
    from matplotlib.ticker import FixedLocator
    axes[0].xaxis.set_minor_locator(FixedLocator([2,4,6,8,20,40,60,80]))
    axes[1].xaxis.set_minor_locator(FixedLocator([2,4,6,8,20,40,60,80]))
    axes[1].xaxis.set_minor_formatter(StrMethodFormatter('{x:.0f}'))
    
    #set y ticks
    axes[1].yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    yticks = [1,2,3,4]
    axes[1].set_yticks(yticks) 
    axes[1].set_yticklabels(yticks)
    
    
    axes[1].grid(axis='x', which='both', color='k',alpha=0.5, linestyle=':')
    fig.subplots_adjust(hspace=0.02, wspace=0.4)
    
    
    if savefig==True:
        # fig.savefig('3DAnalysisSamples_{}_transparent'.format(tempStat), dpi=800, transparent=True)
        fig.savefig('Fig1.{}'.format(figFormat), dpi=dpi, transparent=False, format=figFormat)
        
if __name__ == "__main__":
    main()











