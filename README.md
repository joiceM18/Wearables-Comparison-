## Wearables-Comparison 🕧🔍🌐🕧
This is the main repository for the Wearables Comparison data analysis study. In this repository, you will find all the script that worked on during the data analysis process. We are mainly using threee devices: Empatica Embrace, the Oura ring, and Myzone heart rate monitor. 


### For Empatica Embrace, there are a few things to know:
the raw data collected from empatica device came in unix time, it came in nano second entrees so some conversoin needed to be done for better readability
there are a few files: 

1- processing_Empatica: this is the file that took the raw data from empatica and converted the unix time stamp into central time zone, with 1 minute entrees. the script takes in the entrees in nano seconds and calulates the the avergae entrees for heartbeats per minute 

-empatica_process_script: 

2- empatica_script.py: takes in the entire processed csv file script that was created anf filters the actvities that participants have done, along wwith calculating mean, max and standard deviation per activity. 

3- empatica_script.md: this is the exact same code as the .py file, just described.
### Oura Ring:
1- Oura_script.py:" includes a script that takes in the raw oura data in a csv file and filters the activity time slots, and also converts timestamps from UTC to central time, based on participant's location. we know that the timestamp in Oura was in UTC because the raw csv file entrees had 'Z' nect to the timestamp, and that is a clear indicator of the timezone. The script outputs the filtered csv file with activites, min bpm, max bpm, and stnadard deviation. 

2- oura_script.md: this is the exact same code as the .py file, just described.

### My Zone activity:
1- mz3_script.py: includes a script that imports the raw csv file for mz3 device. the raw data includes local time as there are no indicators of any unique timezone. therefore, the script ensures that local timezone is in central time, just as the participants location.

2-mz3_sript.d: this is the exact same code as the .py file, just described.

### Data Analysis:
- The file name called "data_analysis" includes a script that imports the three processed files we worked on, above^ and performs a few statistical tests and a few conclusions. the script first compares all csv files togther and withthin each activity, summary statistics are calulcate and outputted. conclusions are made by calculating ks test and p-value as well. 
