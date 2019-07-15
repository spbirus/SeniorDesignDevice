/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package combinecsvfiles;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 *
 * @author jtgal
 */
public class CombineCSVFiles {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        // TODO code application logic here
        
        //get info from sample csv file
        List<String> sampleRecords = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\jtgal\\OneDrive\\Documents\\Pitt Summer 2019\\Senior Design\\sampleFileOutputsCSV\\samples\\c10FullOut.csv"))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                sampleRecords.add(values[1]);
            }
        }
        
        //get info from annotation csv file
        //broken into two columns, sample# (multiple of 6000), and apnea label
        List<String> annotationRecords = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader("C:\\Users\\jtgal\\OneDrive\\Documents\\Pitt Summer 2019\\Senior Design\\sampleFileOutputsCSV\\Annotations\\c10Annotations.csv"))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                annotationRecords.add(values[2]);
            }
        }
        
        int annotationIndex = 0;
        int y = (annotationRecords.size() - 1 ) * 6000;
        System.out.println("SampleSize: " + sampleRecords.size());
        

        System.out.println("Annotations Size: " + annotationRecords.size());
        System.out.println("Last annotation at sample # " + (y-6000));
        
        List<List<String>> combinedRecords = new ArrayList<>();
        for (int i = 0; i < y ; i++) {
            if (i % 6000 == 0 && annotationIndex < annotationRecords.size()) {
                combinedRecords.add(Arrays.asList(sampleRecords.get(i), annotationRecords.get(annotationIndex)));
                annotationIndex++;
            } else {
                combinedRecords.add(Arrays.asList(sampleRecords.get(i), ""));
            }

        }
        
        FileWriter csvWriter = new FileWriter("C:\\Users\\jtgal\\OneDrive\\Documents\\Pitt Summer 2019\\Senior Design\\sampleFileOutputsCSV\\Combined\\c10.csv"); 
        
        for (List<String> rowData : combinedRecords) {  
            csvWriter.append(String.join(",", rowData));
            csvWriter.append("\n");
        }

        csvWriter.flush();  
        csvWriter.close(); 
        
    }
    
}
