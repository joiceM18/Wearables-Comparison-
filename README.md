# Wearables-Comparison-
This is the main repository for the wearbale comparison data analysis study. In this repository, you will find all the script that worked on during the data analysis process. We are mainly using threee devices: Empatica Embrace, the Oura ring, and Myzone heart rate monitor. 


## For Empatica Embrace:
# A few things to know ->the raw data collected from empatica device came in unix time, it came in nano second entrees so some conversoin needed to be done for better readability
there are a few files: 
1- processing_Empatica: this is the file that took the raw data from empatica and converted the unix time stamp into central time zone, with 1 minute entrees. the script takes in the entrees in nano seconds and calulates the the avergae entrees for heartbeats per minute 

2-processed empatica: takes in the entire processed csv file script that was created anf filters the actvities that participants have done, along wwith calculating mean, max and standard deviation per activity. 

## 2

# 1

text
