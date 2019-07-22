import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math, os, csv
from statistics import mean

import time #unnecessary, but good for curiosity

start_time = time.time()

pathExample = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/a123456.csv'


measures = {}

def get_data(filename):
    dataset = pd.read_csv(filename)
    return dataset

def rolmean(dataset, hrw, fs):
    mov_avg = dataset['hart'].rolling(int(hrw*fs)).mean()
    avg_hr = (np.mean(dataset.hart))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    mov_avg = [x*1.2 for x in mov_avg]
    dataset['hart_rollingmean'] = mov_avg

def detect_peaks(dataset):
    window = []
    peaklist = []
    listpos = 0
    for datapoint in dataset.hart:
        rollingmean = dataset.hart_rollingmean[listpos]
        if (datapoint < rollingmean) and (len(window) < 1):
            listpos += 1
        elif (datapoint > rollingmean):
            window.append(datapoint)
            listpos += 1
        else:
            if len(window) != 0:
                maximum = max(window)
                beatposition = listpos - len(window) + (window.index(max(window)))
                peaklist.append(beatposition)
                window = []
            listpos += 1
    measures['peaklist'] = peaklist
    measures['ybeat'] = [dataset.hart[x] for x in peaklist]

    #get an average value for ybeat, then clear all lower
    #then also remove the associated peaklist values
    thold = Average(measures['ybeat'])
    print("Average of peaks, which is our thold: ", round(thold,2))
    print("We threshold because we also store peaks from S and T complexes")
    print("We don't want those values when finding heart rate")
    detect_actual_peaks(thold)
    print("DONE DELETING OTHER PEAKS")

def Average(lst): 
    return mean(lst) 

#clears out low peaks that arent qrs peaks
def detect_actual_peaks(thold):
    for value in measures['ybeat']:
        if value < thold:
            index = measures['ybeat'].index(value)
            del measures['ybeat'][index]
            del measures['peaklist'][index]
    
    #ensure duplicates are cleared
    if min(measures['ybeat']) < thold:
        detect_actual_peaks(thold)

#NOT USED
def calc_RR(dataset, fs):
    RR_list = []
    peaklist = measures['peaklist']
    cnt = 0
    while (cnt < (len(peaklist)-1)):
        RR_interval = (peaklist[cnt+1] - peaklist[cnt])
        ms_dist = ((RR_interval / fs) * 1000.0)
        RR_list.append(ms_dist)
        cnt += 1
    measures['RR_list'] = RR_list

def calc_bpm():
    #RR_list = measures['RR_list']
    #measures['bpm'] = 60000 / np.mean(RR_list)
    create_bpm_list()

#create a list of bpm every 6 seconds (10 per minute)
    #10 samples per annotation
def create_bpm_list():
    timingIndex = 1
    tempPeaklist = []
    for value in measures['peaklist']:
        tempPeaklist.append(value)
        if value > 600*timingIndex:
            #differenceList = [tempPeaklist[i+1]-tempPeaklist[i] for i in range(len(tempPeaklist)-1)]
            max = tempPeaklist[len(tempPeaklist)-1]
            min = tempPeaklist[0]
            interval = (max - min) / 100.0
            bpmVal = (len(tempPeaklist)-1) * 60.0 / interval

            #bpm_list.append(Average(differenceList)*60/100)
            bpm_list.append(bpmVal)
            tempPeaklist.clear
            timingIndex += 1
    print("average bpm: " , round(Average(bpm_list),2))
    print("done creating bpm list")

#NOT NEEDED (if using, also use calc_RR)
def plotter(dataset, title):
    peaklist = measures['peaklist']
    ybeat = measures['ybeat']
    plt.title(title)
    plt.plot(dataset.hart, alpha=0.5, color='blue', label="raw signal")
    plt.plot(dataset.hart_rollingmean, color ='green', label="moving average")
    plt.scatter(peaklist, ybeat, color='red', label="average: %.1f BPM" %measures['bpm'])
    plt.legend(loc=4, framealpha=0.6)
    plt.show()

def process(dataset, hrw, fs): #Remember; hrw was the one-sided window size (we used 0.75) and fs was the sample rate (file is recorded at 100Hz)
    rolmean(dataset, hrw, fs)
    detect_peaks(dataset)
    #calc_RR(dataset, fs)
    calc_bpm()
    #plotter(dataset, "My Heartbeat Plot")


#**********
#Main program

#p = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/CombinedNotDone'
p = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/Combined'
p2 = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/NewHeartRates'

for filename in os.listdir(p):
    #reset bpm_list for each file, since we write to our own bpm outfile
    bpm_list = []


    print(filename)
    fullFN = p + '/' + filename
    outFN = p2 + '/' + filename

    dataset = get_data(fullFN)
    process(dataset, 0.75, 100)

    #write bpms to output file
    with open(outFN, 'w') as csvFile:
        bpm_list_string = []
        for bpm in bpm_list:
            bpm_str = str(bpm)
            csvFile.write(bpm_str + '\n')
    csvFile.close()

    #We have imported our Python module as an object called 'hb'
    #This object contains the dictionary 'measures' with all values in it
    #Now we can also retrieve the BPM value (and later other values) like this:
    #bpm = measures['bpm']
    #To view all objects in the dictionary, use "keys()" like so:
    #print (measures.keys())





end_time = time.time()
time_spent = end_time - start_time
print("RUNTIME: " + str(time_spent) + " seconds")
print("DONE")