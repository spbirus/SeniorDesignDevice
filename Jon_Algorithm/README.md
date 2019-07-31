# Jon's Primary Algorithm
Heart rate extraction algorithm and neural network training/testing algorithms

## The final prototype
getHRvalues.py runs though some files I have saved locally to extract peaks from the ECG samples.
It then filters for relevant peaks, and then will use those peaks and their timestamps to give
a heart rate value every 6 seconds (600 samples)

both of the toNumpyArray files were testing to extract all of our data, and the code within these file are used in the trainNN scripts

the trainNN files were where the neural network was trained and tested. we trained on 12 datasets, and tested on a 13th
by changing the input array for the feedforward function
