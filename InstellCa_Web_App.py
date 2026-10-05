import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(
    page_title=" 🌑 InstellCa Web",
    page_icon="",
    layout="wide"
)
st.title("🌑 InstellCa : Exoplanet Instellation Calculator")
st.markdown("""
InstellCa represents a digital twin of climate states on a rocky exoplanet. 
Specifically, it provides latitudinal irradiance and thermal profiles due to radiative heat transport from the host star. 
This is based on a generalised model for irradiance that holds even for extremely close-in planets where standard models and approximations fail (Sadh and Gavassino (ApJ, 2026), Sadh (2026),  arXiv:2608.09241).  
""")

# Main code

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 19:00:38 2020

Updated on Sun Oct  4 08:41:15 2026

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
import sqlite3
import pyvo
import pandas as pd

fig=plt.figure(figsize=(9,6),constrained_layout=False)

service = pyvo.dal.TAPService(
    "http://voparis-tap-planeto.obspm.fr/tap"
)
query = """
SELECT star_radius, radius, star_teff, semi_major_axis, target_name, eccentricity
FROM exoplanet.epn_core
"""
results = service.search(query)
df = results.to_table().to_pandas()
starrad=df["star_radius"]
planrad=df["radius"]
temp=df["star_teff"]
semiax=df["semi_major_axis"]
name=df["target_name"]
eccentricity=df["eccentricity"]  
st.sidebar.header("Model Settings")
df["target_name"] = df["target_name"].astype(str).str.strip()
planet_names = sorted(df["target_name"].dropna().unique())
exoplanet = st.sidebar.selectbox("Select Target Exoplanet:", planet_names)
bond_albedo = st.sidebar.slider(
    "Bond Albedo (A):",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.01,
    help="Planetary bolometric reflection coefficient"
)
rotation_option = st.sidebar.radio(
    "Rotation Options:",
    ["Tidal Locking", "Asynchronous Rotation"],
    index=1
)
parameter = 0 if "Tidal" in rotation_option else 1
run_button = st.sidebar.button("Run InstellCa Model", type="primary")
for i in range(len(starrad)):
    if name[i]==exoplanet:
        rp1=planrad[i]
        rs1=starrad[i]
        fa1=temp[i]
        al1=semiax[i]
        ecc=eccentricity[i]
if np.isnan(rp1)==True:
    st.warning("Radius of planet is missing. :")
    user_val = st.text_input("Please enter value in Jupiter radii units :")
    if not user_val:
        st.warning("Please enter a value above to continue.")
        st.stop()
    rp1=float(user_val)
if np.isnan(rs1)==True:
    st.warning("Radius of the star is missing. :")
    user_val = st.text_input("Please enter value in solar units :")
    if not user_val:
        st.warning("Please enter a value above to continue.")
        st.stop()
    rs1=float(user_val)
if np.isnan(al1)==True:
    st.warning("Semi-major axis is missing. :")
    user_val = st.text_input("Please enter value in AU :")
    if not user_val:
        st.warning("Please enter a value above to continue.")
        st.stop()
    al1=float(user_val)
if np.isnan(fa1)==True:
    st.warning("Stellar Effective temperature is missing :")
    user_val = st.text_input("Please enter value (K):")
    if not user_val:
        st.warning("Please enter a value above to continue.")
        st.stop()
    fa1=float(user_val)
if not run_button:
    st.info(" Please select an exoplanet from the sidebar menu and click **Run InstellCa Model** to generate the thermal profile.")
elif exoplanet == "-- Select an Exoplanet --":
    st.warning("⚠️ Please choose a valid target exoplanet from the sidebar dropdown before running the model.")    

if exoplanet != "-- Select an Exoplanet --" and run_button:    
    if parameter==1:
        st.write(f"### Calculating thermal profile over one diurnal rotation for **{exoplanet}**. The simulation may take up to 2 minutes to complete...")
    if parameter==0:
        st.write(f"### Calculating irradiance profile for **{exoplanet}**. The simulation may take up to 2 minutes to complete...")
    number = 1    
    itr=0           
    para=1
    u=0.6
    number=1
    obli=0
    g=1
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
    print(Fore.WHITE +'Generating Plot, Please wait ~30 seconds.. \033[1;30;47m')
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
        la1=np.linspace(-s,s,100)
        la2=np.linspace(-s*57.3,s*57.3,100)
        if parameter==0:
            la1=np.linspace(-s1,s1,150)
            la2=np.linspace(-s1*57.3,s1*57.3,150)
        lon1=np.linspace(-np.pi,np.pi,180)
        if parameter==0:
            lon1=np.linspace(0,0,180)
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
                    rho=al-rp*math.cos(la)*math.cos(lon)
                    if abs(la)>np.pi/2:
                        rho=al+rp*math.cos(la)*math.cos(lon)
                    a=(-rs*math.cos(th)*math.cos(x)+rho)*math.cos(la)*math.cos(lon)+(-rs*math.cos(th)*math.sin(x)-rp*math.cos(la)*math.sin(lon))*math.cos(la)*math.sin(lon) 
                    b=rs*math.sin(th)*math.sin(la)-rp*math.sin(la)**2
                    c=(rs*math.cos(th)*math.cos(x)-rho)**2+(rs*math.cos(th)*math.sin(x)+rp*math.cos(la)*math.sin(lon))**2+(rs*math.sin(th)-rp*math.sin(la))**2
                    ast=(rs*math.cos(th)*math.cos(x)-rho)*math.cos(th)*math.cos(x)+(rs*math.cos(th)*math.sin(x)-rp*math.cos(la)*math.sin(lon))*math.cos(th)*math.sin(x) 
                    bst=rs*math.sin(th)**2-rp*math.sin(la)*math.sin(th)
                    mu=abs(ast+bst)/math.sqrt(c)
                    if para==1:
                        lf=1-u*(1-mu)                    
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
        A = bond_albedo
        aver1 = ((P_lat_orbit_avg * 10**8 * (1 - A)) / 5.67) ** 0.25 
        inve_prof = ((inve1 * 10**8 * (1 - A)) / 5.67) ** 0.25
        offset=abs(np.max(aver1)-np.max(inve_prof))
    P_global_avg = np.sum(P_lat_orbit_avg * np.cos(la1)) / np.sum(np.cos(la1))         
    T_b = ((P_global_avg * 10**8 * (1 - A)) / 5.67) ** 0.25
    st.write(f'The dayside-average effective temperature is {T_b:.2f} K')
    if parameter==1:
        st.write(f'The thermal baseline offset is {offset:.1f} K')
    maxlatitude=symp*57.3
    if parameter==0:
        st.write("The Terminator extends to ",round((np.pi/2+term)*57.3,3), "degrees from the equator")
    plt.subplot(1,1,1)
    if parameter==0:
        plt.plot(la2,P_lat_orbit_avg,'b-',label="Geometric Model")
        plt.plot(la2,inve1,'r--', label="Inverse-square law")
    if parameter==1:    
        plt.plot(la2,aver1,'b-',label="3D geometric profile")
        plt.plot(la2,inve_prof,'r--', label="2D point-source profile")
    plt.axvline(x=maxlatitude,color='gray',linestyle='--',label='Critical point of symmetry')
    plt.axvline(x=-maxlatitude,color='gray',linestyle='--')
    plt.title("{0}".format(exoplanet),fontsize=16)
    plt.xlabel("Sub-stellar angle",fontsize=16)
    if parameter==0:
        plt.ylabel("Irradiance ($W/m^2$)",fontsize=16)
    if parameter==1:
        #plt.ylabel("Diurnal Instellation ($W/m^2$)",fontsize=16)
        plt.ylabel("Effective Temperature (K)",fontsize=16)       
    plt.legend(fontsize=16)
    st.pyplot(fig)
    
    
