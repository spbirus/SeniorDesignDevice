# Imports
import numpy as np
import os, csv
import time #unnecessary, but good for tracking and debugging

start_time = time.time()
      
# Each row is a training example, each column is a feature  [X1, X2, X3]
# X=np.array(([0,0,1],[0,1,1],[1,0,1],[1,1,1]), dtype=float)
# y=np.array(([0],[1],[1],[0]), dtype=float)


#generate X and y numpy arrays

path = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/Combined'

ecgSample = np.array([[]])
ecgAnnotation = np.array([[]])

X = np.empty((0,6000), dtype=int)
y = np.empty((0,1), dtype=int)

for filename in os.listdir(path):

    if filename == 'a05.csv':
        continue

    if filename == 'a02.csv' or filename == 'a04.csv' or filename == 'a06.csv' \
        or filename == 'a08.csv' or filename == 'a10.csv' or filename == 'a12.csv' \
        or filename == 'a14.csv' or filename == 'a16.csv' or filename == 'a18.csv' \
        or filename == 'a20.csv':
        continue
    if filename == 'b01.csv':
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
        #break #(use this break if using just a single file)

#end array generation

# Define useful functions    

# Activation function
def sigmoid(t):
    return 1/(1+np.exp(-t))

# Derivative of sigmoid
def sigmoid_derivative(p):
    return p * (1 - p)

# Class definition
class NeuralNetwork:
    def __init__(self, x,y):
        self.input = x
        self.weights1= np.random.rand(self.input.shape[1],1000) # considering we have 4 nodes in the hidden layer
        self.weights2 = np.random.rand(1000,1)
        self.y = y
        self.output = np. zeros(y.shape)
        
    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.layer2 = sigmoid(np.dot(self.layer1, self.weights2))
        return self.layer2
        
    def backprop(self):
        d_weights2 = np.dot(self.layer1.T, 2*(self.y -self.output)*sigmoid_derivative(self.output))
        d_weights1 = np.dot(self.input.T, np.dot(2*(self.y -self.output)*sigmoid_derivative(self.output), self.weights2.T)*sigmoid_derivative(self.layer1))
    
        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def train(self, X, y):
        self.output = self.feedforward()
        self.backprop()
        

NN = NeuralNetwork(X,y)
for i in range(2): # trains the NN 1,500 times
    if i % 1 ==0: 
        print ("for iteration # " + str(i) + "\n")
        print ("Input : \n" + str(X))
        print ("Actual Output: \n" + str(y))
        print ("Predicted Output: \n" + str(NN.feedforward()))
        print ("Loss: \n" + str(np.mean(np.square(y - NN.feedforward())))) # mean sum squared loss
        # print ("Weights1 ", NN.weights1)        
        # print ("Weights2 ", NN.weights2)
        print ("\n")
  
    NN.train(X, y)

print("DONE")
end_time = time.time()
time_spent = end_time - start_time
print("RUNTIME: " + str(time_spent) + " seconds")
print("If you're reading this, awesome")

print ("Weights1 ", NN.weights1)        
print ("Weights2 ", NN.weights2)

print("DONTONIA")



############################################################

ecgSample = np.array([[]])
ecgAnnotation = np.array([[]])

A = np.empty((0,6000), dtype=int)
B = np.empty((0,1), dtype=int)

for filename in os.listdir(path):

    if filename != 'a05.csv':
        continue

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
                A = np.vstack((A, ecgSample))
                B = np.vstack((B, ecgAnnotation))

                j+=1

                #reset sample and annotation temp arrays
                ecgSample = np.array([[]])
                ecgAnnotation = np.array([[]])

                continue
            i += 1
            # if j == 10: #for debugging
            #     break
        break #**use this break if using just a single file**

NN.input = A
NN.y = B
wumbo2 = NN.feedforward()

outFN = 'C:/Users/jtgal/OneDrive/Documents/Pitt Summer 2019/Senior Design/sampleFileOutputsCSV/testing/a05FinalTestingECG.csv'

with open(outFN, 'w') as csvFile:
    for value in wumbo2:
        if value > 0.5: #write A
            value_str = str(value)
            csvFile.write(value_str + ',A\n')
        else: #write N
            value_str = str(value)
            csvFile.write(value_str + ',N\n')
csvFile.close()

# for valueThing in wumbo2:
#     if valueThing[0] > 0.01:
#         print(valueThing[0])
    

print("DONTONIA")
