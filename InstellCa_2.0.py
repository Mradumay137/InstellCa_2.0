#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:00:38 2020

@author: Mradumay
"""
import math
import matplotlib.pyplot as plt
from scipy.integrate import quad
import numpy as np
import pandas as pd
from colorama import Fore, Style
import os
import glob
import sys
from scipy import integrate

num=int(input("Enter number of planets to be plotted:"))
num1=round(math.sqrt(num))
parameter=int(input("Enter 0 for tidal locking and 1 for diurnal rotation:"))
col=num1
row=math.ceil(num/num1)
cwd=os.getcwd()
extension = 'csv'
cwd1=cwd+"/Exoplanet_Catalogues"
cwd2=cwd+"/Limb_darkening_data"
os.chdir(cwd1)
files = glob.glob('*.{}'.format(extension))
l=len(files)
namef="exoplanet.eu_catalog_new.csv"
exo=[]
if num<2:
    fig=plt.figure(figsize=(row**2/2+row+8, col**2+2*col+4),constrained_layout=False)
if num>2:
    fig=plt.figure(figsize=(col**2+2*col+11,row**2/2+row+11), constrained_layout=False)
for te in range(1,num+1):
    itr=0
    for entry in files:
        if entry==namef and l==1:
            catalog=0
            print(Fore.WHITE +"Exoplanet.eu catalog found")
            print(Style.RESET_ALL)
            break
        else:
            catalog=float(input("Enter 0 for Exoplanet.eu, 1 for NASA arxiv, and 2 for entering manually:"))
            break
    if l==0:
        print(Fore.RED +"No catalog found. Enter parameters manually")
        print(Style.RESET_ALL)
        catalog=2
    while catalog!=0 and catalog!=1 and catalog!=2:
            catalog=float(input(Fore.RED +"Wrong option entered. Please re-enter:"))
            print(Style.RESET_ALL)
    if catalog==0:
        for entry in files:
            itr=itr+1
            if entry==namef:
                break
            if entry!=namef and itr==l: 
                sys.exit(Fore.RED +"Exoplanet.eu catalog not found")
                print(Style.RESET_ALL)
        data=pd.read_csv(os.path.join(cwd1,"exoplanet.eu_catalog_new.csv"))
        df=pd.DataFrame(data)
        starrad=df["star_radius"]
        planrad=df["radius"]
        temp=df["star_teff"]
        semiax=df["semi_major_axis"]
        name=data["name"]
        eccentricity=data["eccentricity"]  
        Mass=data["star_mass"] 
        metallicity=data["star_metallicity"]
        exoplanet=input("Enter the name of exoplanet:")
        exo.append(exoplanet)
        opt=float(input("Enter 1 if you wish to change st_rad,2 for pl_rad, 3 for Teff, 4 for sm_axis else enter any #: "))
        g=1
        while g!=0:
            for i in range(len(starrad)):
                if name[i]==exoplanet:
                    g=0
                    break
                elif name[i]!=exoplanet and i==len(starrad)-1:
                    exoplanet=input(Fore.RED +"Exoplanet not found. Please check the name and type again:")
                    print(Style.RESET_ALL)
        for i in range(len(starrad)):
            if name[i]==exoplanet:
                rp1=planrad[i]
                rs1=starrad[i]
                fa1=temp[i]
                al1=semiax[i]
                ecc=eccentricity[i]
                M1=Mass[i]
                met=metallicity[i]
        if opt==1 or opt==12 or opt==13 or opt==14:
            rs1=float(input("Enter stellar radius:"))
        if opt==2 or opt==12 or opt==23 or opt==24:
            rp1=float(input("Enter planet radius:"))
        if opt==3 or opt==13 or opt==23 or opt==34:
            fa1=float(input("Enter effective temperature:"))
        if opt==4 or opt==14 or opt==24 or opt==34:
            al1=float(input("Enter semi-major axis:"))
    if catalog==1:
        filename=input("Enter name of NASA arxiv csv file:")
        it=0
        for entry in files:
            it=it+1
            if entry==filename:
                g1=0
                break
        if it==len(files):
            sys.exit(Fore.RED +"File name incorrect or file missing. Please check file or re-type")
            print(Style.RESET_ALL)
        data=pd.read_csv(os.path.join(cwd1,filename),error_bad_lines=False,skiprows=361,low_memory=False)
        df=pd.DataFrame(data)
        planrad=df["pl_radj"]
        starrad=df["st_rad"]
        temp=df["st_teff"]
        semiax=df["pl_orbsmax"]
        name=data["pl_name"]   
        eccentricity=data["pl_orbeccen"] 
        Mass=data["st_mass"]
        metallicity=data["st_metfe"]
        exoplanet=input("Enter the name of exoplanet:")
        exo.append(exoplanet)
        opt=float(input("Enter 1 if you wish to change st_rad,2 for pl_rad, 3 for Teff, 4 for sm_axis else enter any #: "))
        g2=1
        while g2!=0:
            for i in range(len(starrad)):
                if name[i]==exoplanet:
                    g2=0
                    break
                elif name[i]!=exoplanet and i==len(starrad)-1:
                    exoplanet=input(Fore.RED +"Exoplanet not found. Please check the name and type again:")
                    print(Style.RESET_ALL)
        for i in range(len(starrad)):
            if name[i]==exoplanet:
                    rp1=planrad[i]
                    rs1=starrad[i]
                    fa1=temp[i]
                    al1=semiax[i]
                    ecc=eccentricity[i]
                    M1=Mass[i]
                    met=metallicity[i]
        if opt==1 or opt==12 or opt==13 or opt==14:
            rs1=float(input("Enter stellar radius:"))
        if opt==2 or opt==12 or opt==23 or opt==24:
            rp1=float(input("Enter planet radius:"))
        if opt==3 or opt==13 or opt==23 or opt==34:
            fa1=float(input("Enter effective temperature:"))
        if opt==4 or opt==14 or opt==24 or opt==34:
            al1=float(input("Enter semi-major axis:"))
    para=1    
    while para!=4 and para!=1 and para!=2:
            para=float(input(Fore.RED +'Wrong option entered. Please re-enter:'))
            print(Style.RESET_ALL)
    if catalog==2:
        print(Style.RESET_ALL)
        rp1=float(input("Enter radius of planet in Jupiter radii:"))
        rs1=float(input("Enter radius of the host star in units of solar radius:"))
        fa1=float(input("Enter effective Temperature of host star in K:"))
        al1=float(input("Enter semi-major axis of the planet from the star in AU:"))
        ecc=float(input("Enter eccentricity:"))        
        exoplanet=input("Enter name:")
        if para==4:
            M1=float(input("Enter stellar mass(solar units):"))
            met=float(input("Enter metallicity[Fe/H]:"))
    if para==1:
        u=0.6
        met=0
        M1=1
    if para==2:
        u1=float(input("Enter bolometric quadratic coefficient(u1):"))
        u2=float(input("Enter bolometric quadratic coefficient(u2):"))   
        met=0
        M1=1        
    if np.isnan(rs1)==True or np.isnan(fa1)==True or np.isnan(al1)==True:
        continue
        print(Fore.RED +"Crucial parameter missing")
        print(Style.RESET_ALL)
    else:    
        if np.isnan(rp1)==True:
            rp1=input(Fore.RED +"Radius of planet is missing. Please enter value in Rj units:")
            print(Style.RESET_ALL)
            rp1=float(rp1)
        if np.isnan(met)==True:
            met=float(input(Fore.RED +"Metallicity[Fe/H] missing in dataset. Enter manually:"))
            print(Style.RESET_ALL)
        if np.isnan(M1)==True:
            M1=float(input(Fore.RED +"Stellar mass missing in dataset. Enter manually:"))
            print(Style.RESET_ALL)
        number=1
        obli=0
        if np.isnan(ecc)==True:
            ecc=0
        elif ecc!=0 and ecc<0.3:
            print(Fore.WHITE +"Eccentric orbit detected, calculating values at periastron \033[1;30;47m")
            print(Style.RESET_ALL)
        elif ecc>0.3:
            number=4
            print(Fore.WHITE +"Highly eccentric orbit(e>0.3). Calculating annual mean \033[1;30;47m")
            print(Style.RESET_ALL)
        true1=np.linspace(0,270,number)
        if te==num:
            print(Fore.WHITE +'Generating Plot, Please wait ~1 minute.. \033[1;30;47m')
        print(Style.RESET_ALL)
        average=[]
        inverse=[]        
        for j in range(0,number):
            # Orbital and physical parameters
            true=true1[j]*np.pi/180 
            ob1=float(obli)
            ob=ob1*np.pi/180
            rp1=float(rp1)
            rs1=float(rs1)
            al1=float(al1)
            fa1=float(fa1)
            ecc=float(ecc)
            M=M1*2*10**(30)
            rs=rs1*6.955*10**8
            rp=rp1*6.4*10**6*11.21
            al2=al1*1.496*10**11
            al=al2*(1-ecc**2)/(1+ecc*math.cos(true))
            d=al-rs-rp
            ch=math.acos(rp/(d+rp))
            s3=(math.asin(abs(rs-rp)/al))       
            s1=(np.pi/2+s3)
            s1=math.floor(s1*180/np.pi)
            s1=s1*np.pi/180
            term=(math.asin(abs(rs-rp)/al))             
            s=np.pi/2
            symp=math.acos((rs+rp)/al)
            la1=np.linspace(-s,s,300)
            la2=np.linspace(-s*57.3,s*57.3,300)
            if parameter==0:
                la1=np.linspace(-s1,s1,300)
                la2=np.linspace(-s1*57.3,s1*57.3,300)
            lon1=np.linspace(-np.pi,np.pi,300)
            if parameter==0:
                lon1=np.linspace(0,0,300)
            surfgrav=100*6.67*10**(-11)*M/rs**(2)
            logg=math.log10(surfgrav)
            oldfor=[]
            final=[]
            denom=[]
            numer=[]
            approx=[]            
            #Limb Darkening
            if para==1 and u==0.6: 
                fa=fa1*(1.0573) #Milne-Eddington
            if para==1 and u==0:
                fa=fa1
            P=5.67*10**(-8)*fa**(4)*4*np.pi*rs**2
            zalist=[]
            areaval=[]
            areaneg=[]
            inla=[]
            integrated=[]
            integrated_comp=[]
            for new in range(len(la1)):
                la=la1[new]
                final=[]
                oldfor=[]  
                symmetry=np.pi/2+(math.asin(abs(rs-rp*math.cos(la))/al))
                for k in range(len(lon1)):
                    lon=lon1[k]                     
                    beta=al+rp*math.cos(np.pi-la)
                    y1=math.acos((rs**2-rp**2*(math.sin(la))**2)/(beta*rs - rp*math.sin(la)*(math.sqrt(rp**2*(math.sin(la))**2-rs**2+beta**2))))*180/np.pi
                    y4=math.acos((rs**2-rp**2*(math.sin(la))**2)/(beta*rs + rp*math.sin(la)*(math.sqrt(rp**2*(math.sin(la))**2-rs**2+beta**2))))*180/np.pi
                    y5=math.acos(rs/math.sqrt(al**2+rp**2-2*al*rp*math.cos(la)))*180/np.pi
                    y6=math.acos((rs+rp*abs(math.sin(la)))/al)
                    y=(y1)*np.pi/180
                    y2=(y4)*np.pi/180
                    y3=(y5)*np.pi/180
                    y7=math.acos(rs/al)
                    y=y7
                    ad1=180*math.atan(rs*math.sin(y)/(d+rs-(rs*math.cos(y))))/np.pi
                    ad=math.floor(ad1)*np.pi/180
                    vis=math.acos(rs/(math.sqrt(al**2+rp**2-2*al*rp*math.cos(la))))
                    P1=5.67*10**(-8)*fa1**(4)*4*np.pi*(rs)**2                
                    y2=y6
                    #Geometric Limits                    
                    if la>0 and abs(la)<symp and abs(lon)<symp: 
                        ll=-math.acos((rs*(al-rp*math.cos(la))+rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))
                        ul=math.acos((rs*(al-rp*math.cos(la))-rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))                        
                    if la<0 and abs(la)<symp and abs(lon)<symp:
                        ll=-math.acos((rs*(al-rp*math.cos(la))+rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))
                        ul=math.acos((rs*(al-rp*math.cos(la))-rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))     
                    if abs(la)>=symp and la>0 and abs(lon)>=symp:
                        ll=-la+math.acos((al*math.cos(la)-rp)/rs)
                        ul=math.acos((rs*(al-rp*math.cos(la))-rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))                        
                    if abs(la)>=symp and la<0 and abs(lon)>=symp:                        
                        ul=-la-math.acos((al*math.cos(la)-rp)/rs)
                        ll=-math.acos((rs*(al-rp*math.cos(la))+rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))                    
                    if parameter==0:
                        if abs(la)>=symp and la>0:
                            ll=-la+math.acos((al*math.cos(la)-rp)/rs)
                            ul=math.acos((rs*(al-rp*math.cos(la))-rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))                            
                        if abs(la)>=symp and la<0:
                            ul=-la-math.acos((al*math.cos(la)-rp)/rs)
                            ll=-math.acos((rs*(al-rp*math.cos(la))+rp*math.sin(la)*np.sqrt(al**2+rp**2-rs**2-2*al*rp*math.cos(la)))/(al**2+rp**2-2*al*rp*math.cos(la)))                 
                    if la==0:
                        ll=math.acos(rs/(al-rp))
                        ul=math.acos(rs/(al-rp))                   
                    #General integral function
                    def function(x,th,la): 
                        rho=al+rp*math.cos(la)*math.cos(lon)
                        a=(-rs*math.cos(th)*math.cos(x)+rho)*math.cos(la)*math.cos(lon)+(-rs*math.cos(th)*math.sin(x)-rp*math.cos(la)*math.sin(lon))*math.cos(la)*math.sin(lon) 
                        b=rs*math.sin(th)*math.sin(la)-rp*math.sin(la)**2
                        c=(rs*math.cos(th)*math.cos(x)-rho)**2+(rs*math.cos(th)*math.sin(x)+rp*math.cos(la)*math.sin(lon))**2+(rs*math.sin(th)-rp*math.sin(la))**2
                        ast=(rs*math.cos(th)*math.cos(x)-rho)*math.cos(th)*math.cos(x)+(rs*math.cos(th)*math.sin(x)-rp*math.cos(la)*math.sin(lon))*math.cos(th)*math.sin(x) 
                        bst=rs*math.sin(th)**2-rp*math.sin(la)*math.sin(th)
                        mu=abs(ast+bst)/math.sqrt(c)                     
                        if para==1:
                            lf=1-u*(1-mu)
                        if para==2:
                            lf=1-u1*(1-mu)-u2*(1-mu)**2
                        return abs(a+b)*lf*mu*math.cos(th)/(c**1.5)
                    def integration(th,la): #First integral
                        return quad(function,-y3,y3,args=(th,la))[0] #A bit simplistic approximation for rotation but works well        
                    #Second integral                    
                    value=quad(lambda th: integration(th,la),ll, ul)[0]
                    la5=math.atan(al*math.tan(la)*math.cos(la)/(al*math.cos(la)-rp))
                    lon5=math.atan(al*math.tan(lon)*math.cos(lon))/(al*math.cos(lon)-rp)                    
                    tange=math.acos(rp/(al))        
                    value2=value*P/(4*np.pi*np.pi)
                    if lon>symmetry or lon<-symmetry: # Penumbra always illuminated but not the fully-illuminated zone that experiences a diurnal cycle.
                       value2=0
                    final.append(value2)                    
                    old=P1*(al*math.cos(la)*math.cos(lon)-rp)/(4*np.pi*(al**2+rp**2-2*al*rp*math.cos(la)*math.cos(lon))**1.5)
                    if lon>tange or la>tange:
                        old=0
                    if lon<-tange or la<-tange:
                        old=0    
                    oldfor.append(old)        
                newval=np.mean(final)
                integrated.append(newval)
                integrated_comp.append(np.mean(oldfor)) 
            inverse.append(integrated_comp)
            average.append(integrated)
            aver=np.asarray(average)
            inve=np.asarray(inverse)           
            P_lat_orbit_avg = np.mean(aver, axis=0)  
            inve1=np.mean(inve,axis=0)
            err=P_lat_orbit_avg[150]-inve1[150]
            A = 0.2
            aver1 = ((P_lat_orbit_avg * 10**8 * (1 - A)) / 5.67) ** 0.25         
        P_global_avg = np.sum(P_lat_orbit_avg * np.cos(la1)) / np.sum(np.cos(la1))         
        T_b = ((P_global_avg * 10**8 * (1 - A)) / 5.67) ** 0.25
        print(T_b)
        maxlatitude=symp*57.3
        plt.subplot(row,col,te)
        if parameter==0:
            plt.plot(la2,P_lat_orbit_avg,'b-',label="Geometric Model")
            plt.plot(la2,inve1,'r--', label="Inverse-square law")
        if parameter==1:    
            plt.plot(la2,aver1,'b-',label="Geometric Model")
            #plt.plot(la2,P_lat_orbit_avg,'b-',label="Geometric Model")
            #plt.plot(la2,inve1,'r--', label="Inverse-square law")
        plt.axvline(x=maxlatitude,color='gray',linestyle='--',label='Critical point of symmetry')
        plt.axvline(x=-maxlatitude,color='gray',linestyle='--')
        plt.title("{0}".format(exoplanet),fontsize=16)
        plt.xlabel("Latitude ",fontsize=16)
        if parameter==0:
            plt.ylabel("Irradiance ($W/m^2$)",fontsize=16)
        if parameter==1:
            #plt.ylabel("Diurnal Instellation ($W/m^2$)",fontsize=16)
            plt.ylabel("Effective Temperature (K)",fontsize=16)
        
        plt.legend(fontsize=16)
imagename=exoplanet+".jpg"
if num>1:
    imagename=input("Saving image..Enter image name and format:")
plt.savefig(imagename,dpi=300)
plt.show()  
print("The Terminator extends to ",round((np.pi/2+term)*57.3,3), "degrees from the equator")
