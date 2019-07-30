/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication20;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 *
 * @author jtgal
 */
public class JavaApplication20 {

    /**
     * @param args the command line arguments
     */
    
    private static List<Integer> records = new ArrayList<>(); //stores all ECG data that comes in
        //in the event that we need more storage, this can be reset every 5 seconds and we can have
        //another list allocated to storing heart rate values (and that list can reset every half hour or something)
    private static List<Integer> tSamples = new ArrayList<>(); //strictly used for thresholding
    private static List<Double> updatingTValues = new ArrayList<>();
    
    private static double tHold = 0.0; //threshold value
    private static int HRPortion = 0; //which 5 second segment of data are we on
    
    public static void main(String[] args) throws IOException {
        // TODO code application logic here
        
        
        //read in an ECG file and store data in an arraylist
        try (BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\jtgal\\OneDrive\\Documents\\Pitt Summer 2019\\Senior Design\\sampleFileOutputsCSV\\a01FullOut.csv"))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                records.add(Integer.parseInt(values[1]));
                //System.out.println("Sample: " + values[0] + " ECG: " + values[1]); //printing takes a long time
                
                if (records.size() % 60000 == 0 && records.size() > 10) {
                    tSamples = new ArrayList<>();
                    getThresholdValue();
                }
                
                if (records.size() % 600 == 0 && records.size() > 10 && tHold != 0){
                    findHeartRate();
                }
            }
        }
        //60000 samples will give 10 minutes of data
        //these samples will be used to determine the threshold values to be used throughout the night
        //TODO: use a method to stall the 1st 10 minutes while calculating threshold
        //getTresholdValue();
        
        
        
        //this is going to be based on the stream of record data coming in. 
        //TODO: modify how this is called to account for data stream (once every 600 records)
        //try putting the calls inside the buffered reader, and only call when records mod size = 0 && size!=0 && tHold !=0
        //findHeartRate();
        
        
        System.out.println("");
        for (int i = 0; i < updatingTValues.size(); i++) {
            System.out.println("Threshold ecg value: " + updatingTValues.get(i));
        }
        
    }
    
    //this is to find a value less than the QRS complexes but higher than the P or T complexes
    //we will use this value to identify timestamps/sample numbers for each QRS complex
    //TODO: have this value update every 10 minutes...
    private static void getThresholdValue() {
        
        System.out.println("in getThresholdValue");
        
        //add 10 minutes of values to a list
        for (int i = records.size() - 60000; i < records.size(); i++) {
            tSamples.add(records.get(i));
        }
        System.out.println(tSamples.get(15)); //testing its stored properly
        
        int max = tSamples.get(0);
        int min = tSamples.get(0);
        int sTotal = 0;
        
        
        for (int i = 0; i < tSamples.size(); i++) {
            int curValue = tSamples.get(i);
            if (curValue > max) {
                max = curValue;
            }
            if (curValue < min) {
                min = curValue;
            }
            
            sTotal += curValue;
        }
        
        double averageECG = sTotal / tSamples.size();
        //System.out.println("Average ECG: " + averageECG);
        
        //THIS NEEDS TO BE MORE ACCURATE, IT ONLY WORKS WHEN THERE ARENT EXTREME SPIKES OR DIPS IN THE DATA
        tHold = ((max + min) / 2) + (Math.abs(max) / 5);
        
        System.out.println("   ");
        System.out.println("min " + min);
        System.out.println("max " + max);
        System.out.println("threshold " + tHold);
        System.out.println("Average ECG: " + averageECG);
        System.out.println("STotal: " + sTotal);
        
        updatingTValues.add(tHold);
        
        System.out.println("");
    }
    
    //every 6 seconds, find the average heart rate over that time
    private static void findHeartRate() {
        
        //loop through all records
        while (HRPortion < records.size() ) {
            
            List<Integer> qrsSampleNumbers = new ArrayList<>();
        
            //break into 6 second intervals
            for (int i = HRPortion; i < 600 + HRPortion && i < records.size(); i++) {
                if (records.get(i) > tHold) {
                    qrsSampleNumbers.add(i);
                    i+=4; //this ensures we dont count multiple values
                }
            }

            //heart rate stuff
            double heartRate = 0;
            double avgSeparation = 0;
            
            //this will cover the portions between new record sets when we might only have one sample point
            if (qrsSampleNumbers.size() < 2) {
                break;
            }
            
            int differences[] = new int[qrsSampleNumbers.size()-1];
            int sumNumber = 0;

            for (int i = 1; i < qrsSampleNumbers.size(); i++) {
                //System.out.println(qrsSampleNumbers.get(i));
                differences[i-1] = qrsSampleNumbers.get(i) - qrsSampleNumbers.get(i-1);
                sumNumber += differences[i-1];
            }

            avgSeparation = sumNumber / differences.length;

            heartRate = avgSeparation / 100.0 * 60.0;

            System.out.println("");
            System.out.println("Average Heart Rate: " + heartRate);
            System.out.println("TimePeriod: " + convertToTimeStamp(qrsSampleNumbers.get(0)) + " to " + convertToTimeStamp(qrsSampleNumbers.get(qrsSampleNumbers.size()-1)));
            System.out.println("Current Record Size: " + records.size());
            HRPortion += 600;
            
        }
        
    }
    
    private static String convertToTimeStamp(int sampleNumber) {
            String sampleTimeStamp = "";
            
            Date date = new Date((long)sampleNumber*10);
            sampleTimeStamp = new SimpleDateFormat("HH:mm:ss.SSS").format(date);
            
            return sampleTimeStamp;
    }

}
