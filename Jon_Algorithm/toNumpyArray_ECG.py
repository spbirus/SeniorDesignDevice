import os, csv
import numpy as np
import time #unnecessary, but good for curiosity

start_time = time.time()

path = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/Combined'

ecgSample = np.array([[]])
ecgAnnotation = np.array([[]])

X = np.empty((0,6000), dtype=int)
y = np.empty((0,1), dtype=int)

for filename in os.listdir(path):

    if filename == 'a10.csv':
        break

    print(filename)

    #0 is for no apnea, 1 is for apnea

    i = 0
    j = 0 #debugging variable
    fullFN = path + '/' + filename

    with open(fullFN , newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[0] == 'hart':
                continue
            ecgSample = np.append(ecgSample, int(row[0]))
            if i == 0:
                if row[1] == 'A':
                    ecgAnnotation = np.append(ecgAnnotation, 1)
                else: # annotation is an N
                    ecgAnnotation = np.append(ecgAnnotation, 0)
            if i == 5999: #new annotation
                i = 0

                #add Samples and annotation to their npArrays,
                X = np.vstack((X, ecgSample))
                y = np.vstack((y, ecgAnnotation))

                j+=1

                #reset sample and annotation temp arrays
                ecgSample = np.array([[]])
                ecgAnnotation = np.array([[]])

                continue
            i += 1
            # if j == 10: #for debugging
            #     break
        break #**use this break if using just a single file**

print("DONE")
end_time = time.time()
time_spent = end_time - start_time
print("RUNTIME: " + str(time_spent) + " seconds")