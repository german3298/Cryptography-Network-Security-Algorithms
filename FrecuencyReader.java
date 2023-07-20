public class FrecuencyReader {
    /*
     * Frequency Reader
     * Reads the relative frecuency of every letter [a-z] from a text and stores 
     * an English letters relative frecuencies array.
     * @ author: Germán Rodríguez
     */

     private double[] frecuenciesText; //relative frecuencies of each letter in the given text [0-25] [a-z]
     private double[] frecuenciesEnglish; //english relative frecuencies of each letter [0-25] [a-z] in English language

     public double[] getTextFrecuencies () {
        return frecuenciesText;
     }

     public double[] getEnglishLettersFrecuencies () {
        return frecuenciesEnglish;
     }

     public FrecuencyReader (String text){
        frecuenciesText = new double[26];
        frecuenciesEnglish = new double[] {
            8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.996,0.153,0.772,
            4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,
            2.360,0.150,1.974,0.074
        };
        ReadFrecuencies(text);
     }

     /*
      * Reads the frecuencies from the text and 
      * creates an array with the relative frecuencies
      */
     public void ReadFrecuencies (String text) {
        int[] frecuencies = new int[26];
        text = text.toLowerCase().replaceAll("[^a-z]", "");   //Remove everything that is not a letter
        double lettersTotal = text.length();
        for (int i = 0; i < lettersTotal; i++){
            char c = text.charAt(i);
            int idx = c - 'a';
            frecuencies[idx]++;
        }
        for (int i = 0; i < frecuenciesText.length; i++)
            frecuenciesText[i] = (frecuencies[i]/lettersTotal)*100;
     }

     public void PrintFrecuencies () {
        for (int i = 0; i < frecuenciesText.length; i++)
            System.out.println("Frecuency for letter " + (char)(i+'a') + " is " + frecuenciesText[i] + "%");
     }

     public static void main (String[] args){
        FrecuencyReader FR = new FrecuencyReader(args[0]);
        FR.PrintFrecuencies();
     }
}
