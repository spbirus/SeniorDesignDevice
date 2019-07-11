import os, csv
import numpy as np
import time #unnecessary, but good for curiosity

start_time = time.time()

path = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/Combined'

#X = np.array()
#y = np.array()

# ecgSample = []
# ecgAnnotation = []

ecgSample = np.array([[]])
ecgAnnotation = np.array([[]])

for filename in os.listdir(path):

    X = np.empty((0,6000), dtype=int)
    y = np.empty((0,1), dtype=str)
    # X = np.array([[]], dtype=int)
    # y = np.array([[]], dtype=str)

    i = 0
    j = 0
    fullFN = path + '/' + filename
    # reader = csv.reader(open(fullFN, "rb"), delimiter=',')
    # for row in reader:
    #     print(row)
    with open(fullFN , newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            #ecgSample.append(int(row[0]))
            ecgSample = np.append(ecgSample, int(row[0]))
            if i == 0:
                #ecgAnnotation.append(row[1])
                ecgAnnotation = np.append(ecgAnnotation, row[1])
            if i == 5999:
                i = 0

                #add Samples and annotation to their npArrays,
                #then clear the temp arrays
                X = np.vstack((X, ecgSample))
                y = np.vstack((y, ecgAnnotation))
                #break
                j+=1
                
                # ecgSample.clear()
                # ecgAnnotation.clear()

                ecgSample = np.array([[]])
                ecgAnnotation = np.array([[]])

                continue
            i += 1
            # if j == 10:
            #     break
        #break #(use this break if using just a single file)

print("DONE")
end_time = time.time()
time_spent = end_time - start_time
print("RUNTIME: " + str(time_spent) + " seconds")