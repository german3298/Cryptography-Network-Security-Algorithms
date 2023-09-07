public class FrecuencyReader {
    /*
     * Frequency Reader
     * Reads the relative frecuency of every letter [a-z] from a text and stores 
     * an English letters relative frecuencies array.
     * @ author: Germán Rodríguez
     */

     private double[] frecuenciesEnglish; //english relative frecuencies of each letter [0-25] [a-z] in English language

     public double[] getEnglishLettersFrecuencies() {
        return frecuenciesEnglish;
     }

     public FrecuencyReader (){
        frecuenciesEnglish = new double[] {
         0.081670,0.014920,0.027820,0.042530,0.127020,0.022280,0.020150,
         0.060940,0.069960,0.001530,0.007720,0.040250,0.024060,0.067490,
         0.075070,0.019290,0.000950,0.059870,0.063270,0.090560,0.027580,
         0.009780,0.023600,0.001500,0.019740,0.000740
        };
     }

     /*
      * Reads the frecuencies from the text and 
      * creates an array with the relative frecuencies
      */
     public double[] readFrecuencies (String text) {
        int[] frecuencies = new int[26];
        double[] frecuenciesText = new double[26];
        text = text.toLowerCase().replaceAll("[^a-z]", "");   //Remove everything that is not a letter
        double lettersTotal = text.length();
        for (int i = 0; i < lettersTotal; i++){
            char c = text.charAt(i);
            int idx = c - 'a';
            frecuencies[idx]++;
        }
        for (int i = 0; i < frecuenciesText.length; i++)
            frecuenciesText[i] = (frecuencies[i]/lettersTotal);
         return frecuenciesText;
     }

     public void printFrecuencies (double[] frecuenciesText) {
        for (int i = 0; i < frecuenciesText.length; i++)
            System.out.println("Frecuency for letter " + (char)(i+'a') + " is " + frecuenciesText[i] + "%");
     }

      /*
       * Counts the number of ocurrences of the 
       * given trigram at the given text
       */
      public int countTrigram(String text,String trigram){
         text = text.toLowerCase().replaceAll("[^a-z]", "");
         int times = 0;
         String textTrigram = "";
         for (int i = 0; i < (text.length()-2);i++) {
             char first = text.charAt(i);
             char second = text.charAt(i+1);
             char thirst = text.charAt(i+2);
             textTrigram = "" + first + second + thirst;
             if (textTrigram.equals(trigram)) times++;
         }
         return times;
      }

     public static void main (String[] args){
        FrecuencyReader FR = new FrecuencyReader();
        double[] frecuencies = FR.readFrecuencies(args[0]);
        FR.printFrecuencies(frecuencies);
     }
}
