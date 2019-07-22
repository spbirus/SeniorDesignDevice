import os, csv
import numpy as np
import time #unnecessary, but good for curiosity

start_time = time.time()

path = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/HeartRates'
pathAnnotation = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/Annotations'

X = np.empty((0,10), dtype=float)
y = np.empty((0,1), dtype=int)

ecgHR = np.array([[]])
ecgAnnotation = np.array([[]])

for filename in os.listdir(path):

    print(filename)

    heartRateFN = path + '/' + filename

    partialAnnotationFN = filename.replace('.csv', 'Annotations.csv')
    annotationFN = pathAnnotation + '/' + partialAnnotationFN

    i = 0
    with open(heartRateFN , newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            ecgHR = np.append(ecgHR, float(row[0]))
            if i == 9: #new annotation (10 heart rate values per annotation)
                i = 0

                #add Samples and annotation to their npArrays,
                X = np.vstack((X, ecgHR))
                
                #reset sample and annotation temp arrays
                ecgHR = np.array([[]])
                
                continue
            i += 1
    #clear after done with file
    ecgHR = np.array([[]])   

    with open(annotationFN , newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if row[2] == 'A': #annotation is an A
                ecgAnnotation = np.append(ecgAnnotation, 1)
            else: # annotation is an N
                ecgAnnotation = np.append(ecgAnnotation, 0)

            #add annotation to numpy array
            y = np.vstack((y, ecgAnnotation))

            #clear annotation temp array
            ecgAnnotation = np.array([[]])

            if y.shape[0] == X.shape[0]:
                break
    #clear after done with file
    ecgAnnotation = np.array([[]])

    #break #**use this break if testing just a single file**

print("DONE")
end_time = time.time()
time_spent = end_time - start_time
print("RUNTIME: " + str(time_spent) + " seconds")