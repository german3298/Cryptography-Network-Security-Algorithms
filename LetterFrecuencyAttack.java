import java.util.SortedMap;
import java.util.TreeMap;
import java.util.Scanner;

/*
     * Attacks to decipher monoalphabetic 
     * ciphers in english language, and
     * one polyalphabetic cipher (Vigenère).
     * One to attack any random 
     * monoalphabetic ciphers and one to
     * attack additive ciphers (Caesar Cipher)
     * @author: Germán Rodríguez
*/
public class LetterFrecuencyAttack {

    
    FrecuencyReader fr;
    SortedMap<Double,Integer> sM;

     public LetterFrecuencyAttack (){
        fr = new FrecuencyReader();
        sM = new TreeMap<Double,Integer>();
     }

     public void AttackToMonoalphabeticCipher(String text, int ans) {
      /*
       * 
       * STOPPED FOR NOW, IT WAS MORE EXPENSIVE 
       * THAN I FIRST IMAGINED.
       * 
       */
     }

      public void IntenseAttackToVigenereCipher(String text,int len, int ans) {
        System.out.println("Starting attack...");
        String[] texts = new String[len];
        int[] finalKeys = new int[len];
        double[] englishFrec = fr.getEnglishLettersFrecuencies();
        //Max of 3 keys per letter
        int maxKeys = 3;
        int[][] matrixKeys = new int[len][maxKeys];
        int[] numberKeys = new int[len];
        String finalTexts[] = new String[730];
        int finalTextsCount = 0;
        for (int i = 0; i < len; i++)
            texts[i] = "";
        //Divide text in subtexts with same key (in Caesar Cipher everyone)
        for (int i = 0; i < text.length(); i++)
            texts[i%len] += text.charAt(i);
        System.out.println("Obtaining possible keys to test...");
        //Obtener posibles claves
        for (int i = 0; i < len; i++){
            numberKeys[i] = 0;
            for (int j = 0; j < 26; j++) {
                String decipheredText = CaesarCipherDecrypt(texts[i], j);
                double[] frec = fr.ReadFrecuencies(decipheredText);
                if (Cosangle(englishFrec,frec) > 0.8){
                    if (numberKeys[i] == maxKeys) break;
                    matrixKeys[i][numberKeys[i]] = j;
                    numberKeys[i]++;
                }
            }
        }
        System.out.println("Performing brute force attack...");
        //Brute force attack
        for (int i = 0; i < numberKeys[0]; i++)
            for (int j = 0; j < numberKeys[1]; j++)
                for (int k = 0; k < numberKeys[2]; k++)
                    for (int l = 0; l < numberKeys[3]; l++)
                        for (int m = 0; m < numberKeys[4]; m++)
                            for (int n = 0; n < numberKeys[5]; n++){
                                finalKeys[0] = matrixKeys[0][i];
                                finalKeys[1] = matrixKeys[1][j];
                                finalKeys[2] = matrixKeys[2][k];
                                finalKeys[3] = matrixKeys[3][l];
                                finalKeys[4] = matrixKeys[4][m];
                                finalKeys[5] = matrixKeys[5][n];
                                String finalText = "Key: ";
                                for (int o = 0; o < finalKeys.length; o++)
                                    finalText += finalKeys[o] + " ";
                                finalText += "\nText:\n" + VigenereDecrypt(text, finalKeys) + "\n";
                                finalTexts[finalTextsCount] = finalText;
                                finalTextsCount++;
                            }
        int trigrams;
        SortedMap<Integer,String> orderedTexts = new TreeMap<Integer,String>();
        System.out.println("Counting trigrams...");
        for (int i = 0; i < finalTextsCount; i++){
            trigrams = CountingTrigram(finalTexts[i], "the");
            orderedTexts.put(trigrams, finalTexts[i]);
        }
        System.out.println("Showing obtained answers...");
        for (int i = 0; i < ans; i++){
            if (orderedTexts.isEmpty()) break;
            int next = orderedTexts.lastKey();
            System.out.println(orderedTexts.get(next));
            orderedTexts.remove(next);
        }
        
      }

     public int CountingTrigram(String text,String trigram){
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

     public double Cosangle(double[] x,double[] y) {
        double numerator = 0;
        double lengthx2 = 0;
        double lengthy2 = 0;
        for (int i =0; i< x.length; i++){
            numerator += x[i]*y[i];
            lengthx2 += x[i]*x[i];
            lengthy2 += y[i]*y[i];
        }
        return numerator/Math.sqrt(lengthx2*lengthy2);
     }

     public void AttackToAdditiveCipher(String text, int ans) {
         int[] keysList = getPossibleKeys(text, ans);
         System.out.println("\nStarting attack...");
         for (int i = 0; i < ans; i++){
            if (keysList[i]==0) continue;
            System.out.println("\nText with key " + keysList[i] + ": ");
            System.out.println("\n" + CaesarCipherDecrypt(text, keysList[i]) + "\n");
         }
     }
     /*
      * Make an attack observing the most repeated letters
      * in the text and assigning the key comparing them
      * with the "e" letter, which is the most repeated in
      * English language 
      */
     public int[] getPossibleKeys(String text, int keys) {
        int[] keysArr = new int[keys];
        sM.clear();
        double[] frecuenciesText = fr.ReadFrecuencies(text);
        for (int i = 0; i < frecuenciesText.length; i++)
            sM.put(frecuenciesText[i], i);
        for (int i = 0; i < keys; i++)
            keysArr[i] = getKey();
        return keysArr;
     }
    /*
     * Takes the maximum frecuency letter from the map,
     * takes the value of the letter [a-z] [0-25],
     * deletes it from the map, and return the key obtained
     * by subtracting the letter from the value from "e"(4),
     * the most frecuency used letter in english
     */
     private int getKey() {
        if (sM.isEmpty()) return 0;
        double d = sM.lastKey();
        int key = sM.get(d) - 4;
        sM.remove(d);
        if (key < 0) key += 26; 
        return key;
     }

     /*
      * Simple VigenereCipher Decrypt
      */
     public String VigenereDecrypt(String text,int[] key) {
        text = text.toLowerCase().replaceAll("[^a-z]", "");
        String plainText = "";
        int len = key.length;
        for (int i = 0; i < text.length(); i++){
            char p = text.charAt(i);
            int k = key[i%len];
            int c = (p-k);
            if (c < 97) c += 26;
            plainText += (char)(c);
        }
        return plainText;
     }

     /*
      * Simple CaesarCipher Decrypt
      */
     public String CaesarCipherDecrypt(String text, int key) {
        text = text.toLowerCase().replaceAll("[^a-z]", "");
        String decryptedText = "";
        for (int i = 0; i < text.length();i++) {
            char p = text.charAt(i);
            int numP = (p-key);
            if (numP < 97) numP+= 26;
            char c = (char)numP;
            decryptedText += c;
        }
        return decryptedText;
     }

     public static void main (String[] args){
        // Scanner s = new Scanner(System.in);
        // System.out.println("Letter frecuency attack to additive cipher, please select number of plaintexts:");
        // String option = s.nextLine();
        //   LetterFrecuencyAttack LFA = new LetterFrecuencyAttack();
        //  LFA.AttackToAdditiveCipher(args[0], Integer.parseInt(option));
        // s.close();

          Scanner s = new Scanner(System.in);
          System.out.println("Letter frecuency Vigenère attack, please select number of output possible texts \"n\":");
          String option = s.nextLine();
         LetterFrecuencyAttack LFA = new LetterFrecuencyAttack();
         LFA.IntenseAttackToVigenereCipher(args[0], 6, Integer.parseInt(option));
            s.close();

        //   LetterFrecuencyAttack LFA = new LetterFrecuencyAttack();
        //   int[] key = {5,17,4,10,4,24};
        //    System.out.println(LFA.VigenereDecrypt(args[0],key)); 

     }

}
