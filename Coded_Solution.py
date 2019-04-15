#!/usr/bin/env python
# coding: utf-8

# # IMPORTANT
# Please read the word document, attached with this notebook before reviewing this. 
# Also please keep every sample code snippet in mind when reading this code.
# The code looks different due to different modalities used but the purpose or result is 
# very similar to that of the same code snippets.
# This notebook assumes you have knowledge about what each piece is doing by following the snippets and description.
# 
# #### The code is written in general to be applied to bigger data set then the one provided. The same code could be used if there were hundreds of locations and hence the solution method was also choosen by keeping this in mind.

# # Extracting Data
# 
# 

# # All libraries used 



#ALL IMPORTS, SOME OF THESE REQUIRE PRIOR DOWNLOADING
import pandas as pd
import googlemaps
from census import Census
from us import states
import numpy as np
import re


# # Entering data



#Creating a dataframe with all information provided in the problem
# Id - Ids of facilities
# Zip - Zipcode of Facilities
# Count - Staff Count
df = pd.DataFrame(columns={'Id','Zip','Count'})
df['Id'] = pd.Series(['A','B','C','D',"E"])
df['Zip'] = pd.Series([98007,98290,98065,98801,98104])
df['Count']=pd.Series([21,52,43,9,64])
display(df)


# # Miscellaneous Data 




api='AIzaSyBwg2yzaFtklLTSrGk-0wTLme_2UO8tyD8'
google = googlemaps.Client(key=api)
List =[["NON",0,0]]
#FINDS NAME, LATITUDE AND LONGITUDE USING GOOGLE MAPS API

for Zip in df['Zip']:
    js = google.geocode(Zip)
    name = js[0]['formatted_address'].split(',')[0]
    lat = js[0]["geometry"]["location"]["lat"]
    long = js[0]["geometry"]["location"]["lng"]
    List.append([name,lat,long])

#ADDS THE NAME LATITUDE AND LONGITUDE INTO THE DATAFRAME
df['Name']= [w[0] for w in List[1:]]
# df['lat']= [w[1] for w in List[1:]]
# df['long']= [w[2] for w in List[1:]]

#df['Name'] = str(df['Name']).split(',')[0]





display(df)


# # Estimating Average Time Section

# # DO NOT RUN BELOW CODE REPEATEDLY!!
# This code is just for illustration purposed on how I got my Data using Google Maps API. Since
# Google Maps is not free beyond a certain limit. Running this piece of code repeatedly may cause 
# going beyond the limit and hence charging my CREDIT CARD!
# 
# This is commented out by default while testing please uncomment.
# Please uncomment below code
# 




# #Function calculates Distances in meters and 
# # Transportation time in seconds using three modes of transport Driving & Transit via bus
# def DistCal(df,index):
#     currentName = df['Name'][index]
#     thedf = pd.DataFrame()
#     listOfDist =[]
#     listOfDurD =[]
#     listOfDurT =[]
#     listOfDurW =[]
#     for name in df['Name']:
#  #This part finds estimated time taken to travel via driving
#         matrix =  google.distance_matrix(currentName,name,mode='driving')
#         currentDist = matrix["rows"][0]["elements"][0]["distance"]["value"]
#         currentDur =float(matrix['rows'][0]['elements'][0]['duration']['value'])
#         listOfDist.append(currentDist)
#         listOfDurD.append(currentDur)
#     #print(listOfDurD)
# #This part finds estimated time taken to travel via bus
#     for name in df['Name']:
#         matrix =  google.distance_matrix(currentName,name,mode='transit',transit_mode ='bus')
#         #currentDist = matrix["rows"][0]["elements"][0]["distance"]["value"]
#         currentDur =float(matrix['rows'][0]['elements'][0]['duration']['value'])
#         #listOfDist.append(currentDist)
#         listOfDurT.append(currentDur)
##  This finds estimated time taken to travel via bus
#     for name in df['Name']:
#         matrix =  google.distance_matrix(currentName,name,mode='walking')
#         #currentDist = matrix["rows"][0]["elements"][0]["distance"]["value"]
#         currentDur =float(matrix['rows'][0]['elements'][0]['duration']['value'])
#         #listOfDist.append(currentDist)
#         listOfDurW.append(currentDur)
#     thedf['Dist'] = listOfDist
#     thedf['AvgTravelTimeD']= listOfDurD
#     thedf['AvgTravelTimeT']=listOfDurT
#     thedf['AvgTravelTimeW']=listOfDurW
    
#     return thedf
## Calculating the distance and average time in between.
# thedfA = DistCal(df,0)   
# thedfB = DistCal(df,1)
# thedfC = DistCal(df,2)
# thedfD = DistCal(df,3)
# thedfE = DistCal(df,4)
# display(thedfA)
# display(thedfB)
# display(thedfC)
# display(thedfD)
# display(thedfE)
# SAVED ALL DATA INTO CSV SINCE WOULD NOT NEED TO RUN THIS OVER AND OVER AGAIN!!!
# thedfA.to_csv('thedfA.csv')
# thedfB.to_csv('thedfB.csv')
# thedfC.to_csv('thedfC.csv')
# thedfD.to_csv('thedfD.csv')
# thedfE.to_csv('thedfE.csv')


# # Description:
# According to bureau of transportation statistics 82.8% people washington used cars, while public transport 
# was used by 6.3% and 3.5% people walked to work. So after normalizing 89.42% used cars, 6.8% used public transport
# and only 3.78% walked.
# link to resource: https://www.bts.gov/content/commuting-work
# 
# Assumption: That since people use cars mostly to commute to work they will use cars for going to a health facility



#Loading the csv's into a dataframe 
dfA = pd.read_csv('thedfA.csv')
dfB = pd.read_csv('thedfB.csv')
dfC = pd.read_csv('thedfC.csv')
dfD = pd.read_csv('thedfD.csv')
dfE = pd.read_csv('thedfE.csv')
#Multiplying by the weights of each mode of transportation and also dividing by 3600 to convert seconds to hours
df['AvgTimeFromA']=(0.8942*dfA['AvgTravelTimeD']+0.068*dfA['AvgTravelTimeT']+0.0378*dfA['AvgTravelTimeW'])/3600
df['AvgTimeFromB']=(0.8942*dfB['AvgTravelTimeD']+0.068*dfB['AvgTravelTimeT']+0.0378*dfB['AvgTravelTimeW'])/3600
df['AvgTimeFromC']=(0.8942*dfC['AvgTravelTimeD']+0.068*dfC['AvgTravelTimeT']+0.0378*dfC['AvgTravelTimeW'])/3600
df['AvgTimeFromD']=(0.8942*dfD['AvgTravelTimeD']+0.068*dfD['AvgTravelTimeT']+0.0378*dfD['AvgTravelTimeW'])/3600
df['AvgTimeFromE']=(0.8942*dfE['AvgTravelTimeD']+0.068*dfE['AvgTravelTimeT']+0.0378*dfE['AvgTravelTimeW'])/3600

display(df)
# Reading Matrix of Average Time the first value in AvgTimeFromA is the time in hours taken to go from A to A
# the second value is the time taken to go from A to B and so on
# The reason that time going from A to B is not neccessarily same as From going to B to A, is that traffic might be different
# on BtoA from AtoB and the terrain will be different. It takes less time going from a hill downwards then to go upwards


# ## Searching US census 
# First we need to get all nearest zipcodes to an area
# I used this website to get data all zipcodes :https://simplemaps.com/data/us-zips
# In order to get population data we need access the US census Api 
# the easiest way to achieve this is to install the library specifically made to use this api
# called census. It is free and easy to use documentation for the library is here:
# https://github.com/datamade/census
# 
# Using 2016 data since that was the latest available
# 



def Findzips(name,row):
    return bool(re.search(name,row))
c = Census("239253498b57f1aa989a21fc35572830fc4c63ae",year=2016)
#IN order to get total population in a  city we need all zipcodes nearest to the place
thezip = pd.read_csv('ZipCodes.csv')
thezip = thezip[thezip['state_id'].apply(Findzips,args=('WA',))]
#display(thezip)
poplist =[]
#THIS GETS POPULATION ESITIMATES FOR ALL REGIONS IN AMERICAN COMMUNITY SURVEY

for names in df['Name']:
    emptylist=[]
    #Finds zipcodes nearest to the area but restricts it to 6 atmost
    CurrentZip = thezip[thezip['city'].apply(Findzips,args=(names,))][:6]
    #display(CurrentZip)
    for zipcodes in CurrentZip['zip']:
        #this returns the total population estimate for every zipcode for 2016
        #B01003_001E is the variable name for total population
        
        d = c.acs5.zipcode('B01003_001E',zipcodes)
        if(len(d)!=0):
            d=d[0]['B01003_001E']
            d=d
            emptylist.append(d)
    poplist.append(sum(emptylist))
        
#display(poplist)


# In[6]:


df['Population'] = poplist
df['RatioMin'] = df['Count']/(0.5*df['Population'])
df['RatioMax'] = df['Count']/(df['Population'])
#df =df.drop(columns=['Population'])
display(df)


# # Optimization
# The problem of this nature can be modelled as a knap-sack problem. The best method to 
# find a 'reasonable' solution is to use the greedy approach. It might not give the globally
# optimal solution but usually is a very good approximator for the globally optimal solution
# For more information on the greedy approach goto: https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-0002-introduction-to-computational-thinking-and-data-science-fall-2016/lecture-videos/lecture-1-introduction-and-optimization-problems/
# 
# 
# Or 
# 
# https://en.wikipedia.org/wiki/Greedy_algorithm 

# # Finding Nearest Facility with adequate staff
# For every facility it is important to find the nearest facility that is available in an area excluding the areas own facility e.g and also taking into account if the facility has above or below the required minimum resources.
# 
# Required ratio =1/2808 =0.0003561
# According to the assumptions made about the patients arriving for a checkup Facility A,D have lower then required 
# Ratio when the whole population comes and only A is deficent when bare minimum of population comes for a checkup



#Function finds similarity in two lists
#Using this to construct a priority queue that will create a ordered list of facilities closest to a place based on 
# average time taken to reach there
def findClosest(list1,list2):
    listOfSim =[]
    for indexs in list1:
        for i in list2:
            if(i==indexs):
                
                listOfSim.append(i)
    return listOfSim
listOfClosest =[]   
#display(df)
required =0.0003561
Bin =[]
i=0
#Finds those places with adequate resources.
for ratio in df['RatioMax']:
    if(ratio>=required):
        Bin.append(i)
    
    i+=1

for ids in df['Id']:
    name = 'AvgTimeFrom'+ids
    #Sorts df values based on lowest average time taken.
    Templist =np.argsort(-df[name].values, axis=0)
    
    
    #display(Templist)
    OrderList=[]
    #this finds a ordered list of facilities based on time taken to reach there
    # Example if E is the closest surplus facility to A then it will be first in the list
    for ids in findClosest(np.fliplr([Templist[:-1]])[0],Bin):
        OrderList.append(df['Id'][ids])
    listOfClosest.append(OrderList)
#display(listOfClosest)
# for thing in listOfClosest:
#     print(thing)
#Stores list in dataframe
df['Closest']=listOfClosest    

display(df)


# # Amount of Surplus or Deficit

# Now we will find how much each facility lacks or has in surplus



required =0.0003561
#Calculates the required staff neccessary to achieve ratio
def CalculateK(pop):
    k = np.ceil(pop*required)
    return k
df['Surplus/Deficit'] = [CalculateK(w) for w in df['Population']]
#Subtracts actual from required to get surplus/deficit
df['Surplus/Deficit'] = df['Count'] - df['Surplus/Deficit']
display(df)


# # Using greedy approach
# We will optimize by first targeting the facility with most deficit. We will eliminate it's deficit by giving all of the surplus from the nearest surplus facility. This reduces average time taken because it uses the nearest facilities resources first.
# ### Note: When re running this part please rerun Amount of Surplus or Deficit first, since it resets deficit/surplus column

# In[9]:


#finding facility with most dire need of resources because the code will be easily abstractable for a larger dataset.
def MostInNeed(df):
    return df['Surplus/Deficit'].idxmin()
#creates an array of instructions for the solution. In a standard format
def Instruction(Giver, Taker, Amount):
    if(Amount==0):
        return '*'
    else:
        return 'Give '+str(Amount)+' From '+str(Giver) +' to '+Taker
def GiveAway(df):
    #List to contain instructions
    listOfInstr = []
    #index of most in need i.e with highest deficit
    index = MostInNeed(df)
    for ids in df['Closest'][index]:
        #print(ids)
        #Current Id of closest facility with surplus
        indexE = df.index[df['Id'] == ids][0]
        #If 
        if(np.abs(df['Surplus/Deficit'][indexE])>=np.abs(df['Surplus/Deficit'][index])):
            deficit =df['Surplus/Deficit'][index]
            df['Surplus/Deficit'][indexE]+=deficit
            df['Surplus/Deficit'][index]=0

            listOfInstr.append(Instruction(df['Id'][indexE],df['Id'][index],np.abs(deficit)))
        else:
            #print('IM HERE')
            surplus= df['Surplus/Deficit'][indexE]
            df['Surplus/Deficit'][indexE]=0
            df['Surplus/Deficit'][index]+=surplus
            listOfInstr.append(Instruction(df['Id'][indexE],df['Id'][index],surplus))
    #display(listOfInstr)
        
    return listOfInstr
#List to contain all instructions on how to reallocate resources.
listOfAllInstr =[]
#Does the giveaway function for the amount facilities with Ratio less the required
for i in range(df[df['RatioMax']<required]['RatioMax'].count()):
    listOfAllInstr.append(GiveAway(df))


# # OUTPUT / RESULT OF TECHNIQUE:



#Prints all instructions generated.
for i in listOfAllInstr:
    for j in i:
        #print(j)
        if(j!='*'):
            print(j)
            
# output tells how much from each facility needs to be reallocated.       







