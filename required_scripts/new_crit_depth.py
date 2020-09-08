#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 11:41:45 2019

@author: eememq
"""
import numpy as np

#function finding the depth, given the cooling rate, and checks if the 593K contour crosses this depth during core solidification
def Critical_Depth(CR, temperatures,dT_by_dt, radii, r_planet, core_size_factor,time_core_frozen, fully_frozen, dr=1000): 
    #Define two empty lists 
    t_val = [] #for the 800K temperature contour
    dt_val = [] #cooling rate contour
    for ti in range(5,temperatures.shape[1]): # changing this 5 did not work
        
        #Find the index where temperatures are 800K by finding the minimum of (a given temperature-800)
        index_where_800K_ish = np.argmin(np.absolute(temperatures[:,ti] - 800))
        if (np.absolute(temperatures[index_where_800K_ish,ti] - 800)) > 10: 
            continue
            
        #Find the index where dT_by_dt = meteorite cooling rate
        index_where_dtbydT = np.argmin(np.absolute(dT_by_dt[:,ti] + CR ))
        if (np.absolute(dT_by_dt[index_where_dtbydT,ti] + CR)) > 1E-15:
            continue
            
        t_val.append(index_where_800K_ish) # dividing both these by 2 didn't work
        dt_val.append(index_where_dtbydT) # this one too
        
    #Find the points where they cross, this will lead to a depth of formation
    assert len(t_val) == len(dt_val), "Contour length error!" # flags an errror if t_val and dt_val are not the same length 
    crosses = np.array(t_val) - np.array(dt_val) == 0 # boolean for if the indecies of the two arrays are the same 
    if not any(crosses):
        # The two lines do not cross
        x = "No cooling rate matched cooling history"
        return None, x, None, None, None
    
    # finding the depth of formation
    crossing_index2 = np.argmax(crosses) # finds the first 'maximum' which is the first TRUE, or the first crossing
    Critical_Radius = radii[dt_val[crossing_index2]] #radius where this first crossing occurs
    
    t_val2 = [] #for the 593K contour
    d_val = [] 
    for ti in range(5,temperatures.shape[1]):
        #Find the index where temperatures are 593K by finding the minimum of (a given temperature-593)
        index_where_593K_ish = np.argmin(np.absolute(temperatures[:,ti] - 593))
        if (np.absolute(temperatures[index_where_593K_ish,ti] - 593)) > 10:
            pass
        
        t_val2.append(index_where_593K_ish)
        d_val.append(((Critical_Radius)/dr - ((r_planet/dr)*core_size_factor))) #computes the depth, converts from radius to depth
        #print(d_val)
        # added int to line above to try and solve - removing this now and instead changing below line
    crossing = [np.array(t_val2) - d_val < 0.00001] #indicies where computed depth crosses temperature contour (593 K)

    crossing_index = np.argmax(crossing) # finds the first 'maximum' which is the first TRUE, or the first crossing
    Time_of_Crossing = crossing_index*(10**11) #converts to seconds
    radii_index = int(((d_val)[crossing==True]))
    
    #check to see if the depth crosses the 593K contour during solidification or before/after
    if time_core_frozen == 0:
        x= 'Core Freezes after Max Time' 
        depth = ((r_planet) - radii[int(((d_val)[crossing==True]))])/dr
        return (depth, x, time_core_frozen, Time_of_Crossing)
    else:
        if radii_index > len(radii):
            x= 'Core has finished solidifying'
            depth = 0
            return (depth, x, time_core_frozen, Time_of_Crossing)
        else:
            depth = ((r_planet) - radii[int(((d_val)[crossing==True]))])/dr
            if Time_of_Crossing == 0:
                x='hmm, see plot' #lines cross at 0 time, but doesn't tell you when it formed
                # this seems to be causing erroneous "no reuslts" when from figure a result is found...
            if Time_of_Crossing < time_core_frozen and Time_of_Crossing!=0:
                x = 'Core has not started solidifying yet'
            if time_core_frozen < Time_of_Crossing < fully_frozen:
                x= 'Core has started solidifying'
            if Time_of_Crossing > fully_frozen:
                x= 'Core has finished solidifying'
            # depth = depth of formation; x = statement on result;
            # time_core_frozen = self explanatory; Time_of_crossing = when the meteorite cools through curie T
            # Critical Radius = radius version of depth
            return (depth, x, time_core_frozen, Time_of_Crossing, Critical_Radius) 


###########################################################
# Experimental function to calculate olivine cooling rate #
###########################################################

# this function is defunct but could be fixed to produce something useful...

#funtion finding the depth, given the cooling rate, and checks if the 593K contour crosses this depth during core solidification
def Critical_Depth_ol(CR, temperatures,dT_by_dt, radii, r_planet, core_size_factor,time_core_frozen, fully_frozen): 
    #Define two empty lists 
    t_val = [] #for the 800K temperature contour
    dt_val = [] #cooling rate contour
    for ti in range(5,temperatures.shape[1]):
        
        #Find the index where temperatures are 800K by finding the minimum of (a given temperature-800)
        index_where_1100K_ish = np.argmin(np.absolute(temperatures[:,ti] - 1100))
        if (np.absolute(temperatures[index_where_1100K_ish,ti] - 1100)) > 10: 
            continue
            
        #Find the index where dT_by_dt = meteorite cooling rate
        index_where_dtbydT = np.argmin(np.absolute(dT_by_dt[:,ti] + CR ))
        if (np.absolute(dT_by_dt[index_where_dtbydT,ti] + CR)) > 1E-15:
            continue
            
        t_val.append(index_where_1100K_ish)
        dt_val.append(index_where_dtbydT)
        
    #Find the points where they cross, this will lead to a depth
    assert len(t_val) == len(dt_val), "Contour length error!" # flags an errror if t_val and dt_val are not the same length 
    crosses = np.array(t_val) - np.array(dt_val) == 0 # boolean for if the indecies of the two arrays are the same 
    if not any(crosses):
        # The two lines do not cross
        x = "No cooling rate matched cooling history"
        return None, x, None, None, None
    
    
    crossing_index2 = np.argmax(crosses) # finds the first 'maximum' which is the first TRUE, or the first crossing
    Critical_Radius = radii[dt_val[crossing_index2]] #radius where this first crossing occurs
    
    t_val2 = [] #for the 593K contour
    d_val = [] #depth 
    for ti in range(5,temperatures.shape[1]):
        #Find the index where temperatures are 593K by finding the minimum of (a given temperature-593)
        index_where_600K_ish = np.argmin(np.absolute(temperatures[:,ti] - 600))
        if (np.absolute(temperatures[index_where_600K_ish,ti] - 600)) > 10:
            pass
        
        t_val2.append(index_where_600K_ish)
        d_val.append((Critical_Radius)/1000 - ((r_planet/1000)*core_size_factor)) #computes the depth 
        
    crossing = [np.array(t_val2) - d_val == 0] #indicies where computed depth crosses temperature contour 
    crossing_index = np.argmax(crossing) # finds the first 'maximum' which is the first TRUE, or the first crossing
    Time_of_Crossing = crossing_index*(10**11) #converts to seconds
    radii_index = int(((d_val)[crossing==True]))
    
    #check to see if the depth crosses the 593K contour during solidification or before/after
    if time_core_frozen == 0:
        x= 'Core Freezes after Max Time' 
        depth = ((r_planet) - radii[int(((d_val)[crossing==True]))])/1000
        return (depth, x, time_core_frozen, Time_of_Crossing)
    else:
        if radii_index > len(radii):
            x= 'Core has finished solidifying'
            depth = 0
            return (depth, x, time_core_frozen, Time_of_Crossing)
        else:
            depth = ((r_planet) - radii[int(((d_val)[crossing==True]))])/1000
            if Time_of_Crossing == 0:
                x='hmm, see plot' #lines cross at 0 time
            if Time_of_Crossing < time_core_frozen and Time_of_Crossing!=0:
                x = 'Core has not started solidifying yet'
            if time_core_frozen < Time_of_Crossing < fully_frozen:
                x= 'Core has started solidifying'
            if Time_of_Crossing > fully_frozen:
                x= 'Core has finished solidifying'
    
            return (depth, x, time_core_frozen, Time_of_Crossing, Critical_Radius)
        

#### Function to find timing of meteorite formation
            
def Critical_Time(CR, temperatures,dT_by_dt, radii, r_planet, core_size_factor,time_core_frozen, fully_frozen,timestep): 
    #Define two empty lists 
    t_val = [] #for the 800K temperature contour
    dt_val = [] #cooling rate contour
    for ti in range(5,temperatures.shape[1]):
        
        #Find the index where temperatures are 800K by finding the minimum of (a given temperature-800)
        index_where_800K_ish = np.argmin(np.absolute(temperatures[:,ti] - 800))
        if (np.absolute(temperatures[index_where_800K_ish,ti] - 800)) > 10: 
            continue
            
        #Find the index where dT_by_dt = meteorite cooling rate
        index_where_dtbydT = np.argmin(np.absolute(dT_by_dt[:,ti] + CR ))
        if (np.absolute(dT_by_dt[index_where_dtbydT,ti] + CR)) > 1E-15:
            continue
            
        t_val.append(index_where_800K_ish)
        dt_val.append(index_where_dtbydT)
        
    #Find the points where they cross, this will lead to a depth
    assert len(t_val) == len(dt_val), "Contour length error!" # flags an errror if t_val and dt_val are not the same length 
    crosses = np.array(t_val) - np.array(dt_val) == 0 # boolean for if the indecies of the two arrays are the same 
    if not any(crosses):
        # The two lines do not cross
        x = "No cooling rate matched cooling history"
        return None, x, None, None, None
    
    
    crossing_index2 = np.argmax(crosses) # finds the first 'maximum' which is the first TRUE, or the first crossing
    Critical_Radius = radii[dt_val[crossing_index2]] #radius where this first crossing occurs
    
    t_val2 = [] #for the 593K contour
    d_val = [] #depth 
    for ti in range(5,temperatures.shape[1]):
        #Find the index where temperatures are 593K by finding the minimum of (a given temperature-593)
        index_where_593K_ish = np.argmin(np.absolute(temperatures[:,ti] - 593))
        if (np.absolute(temperatures[index_where_593K_ish,ti] - 593)) > 10:
            pass
        
        t_val2.append(index_where_593K_ish)
        d_val.append((Critical_Radius)/1000 - ((r_planet/1000)*core_size_factor)) #computes the depth 
        
    crossing = [np.array(t_val2) - d_val == 0] #indicies where computed depth crosses temperature contour 
    crossing_index = np.argmax(crossing) # finds the first 'maximum' which is the first TRUE, or the first crossing
    Time_of_Crossing = crossing_index*(timestep) #converts to seconds
    radii_index = int(((d_val)[crossing==True]))
    
    #check to see if the depth crosses the 593K contour during solidification or before/after
    if time_core_frozen == 0:
        x= 'Core Freezes after Max Time' 
        depth = ((r_planet) - radii[int(((d_val)[crossing==True]))])/1000
        return (depth, x, time_core_frozen, Time_of_Crossing)
    else:
        if radii_index > len(radii):
            x= 'Core has finished solidifying'
            depth = 0
            return (depth, x, time_core_frozen, Time_of_Crossing)
        else:
            depth = ((r_planet) - radii[int(((d_val)[crossing==True]))])/1000
            if Time_of_Crossing == 0:
                x='hmm, see plot' #lines cross at 0 time
            if Time_of_Crossing < time_core_frozen and Time_of_Crossing!=0:
                x = 'Core has not started solidifying yet'
            if time_core_frozen < Time_of_Crossing < fully_frozen:
                x= 'Core has started solidifying'
            if Time_of_Crossing > fully_frozen:
                x= 'Core has finished solidifying'
    
            return (depth, x, time_core_frozen, Time_of_Crossing, Critical_Radius)