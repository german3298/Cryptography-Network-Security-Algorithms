import java.util.SortedMap;
import java.util.TreeMap;
import java.util.Scanner;

/*
     * Attacks to decipher monoalphabetic 
     * ciphers in english language, and
     * one polyalphabetic cipher (Vigenère).
     * One to attack any random 
     * monoalphabetic ciphers and one to
     * attack additive ciphers (Caesar Cipher).
     * @author: Germán Rodríguez
*/
public class LetterFrecuencyAttack {
    
    FrecuencyReader fr;
    SortedMap<Double,Integer> sM;

     public LetterFrecuencyAttack (){
        fr = new FrecuencyReader();
        sM = new TreeMap<Double,Integer>();
     }

     public void AttackToRandomMonoalphabeticCipher(String text, int ans) {
      /*
       * 
       * STOPPED FOR NOW, IT WAS MORE EXPENSIVE 
       * THAN I FIRST IMAGINED.
       * 
       */
     }

     /*
      * Make an attack observing the most repeated letters
      * in the text and assigning the key comparing them
      * with the "e" letter, which is the most repeated in
      * English language 
      */
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
      * Get possible keys in order of compare the frecuency
      * of letter "e" with the frecuency of the most repeated
      * letter at text
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

     /*
      * An attack to a Vigenère Cipher that outputs "ans" 
      * possible texts. It outputs several texts because can 
      * decrypt a mixed text, with several keys (but with
      * same key length), and in order of probability.
      * The more different keys there are, the longer the 
      * texts should be.
      */
      public void IntenseAttackToVigenereCipher(String text,int len, int ans) {
        System.out.println("Starting attack...");

        System.out.println("Dividing texts...");
        //First we divide the text in "key length" texts
        String[] texts = new String[len];
        for (int i = 0; i < len; i++)
            texts[i] = "";
        //Divide text in subtexts with same key (in Caesar Cipher every one of them)
        for (int i = 0; i < text.length(); i++)
            texts[i%len] += text.charAt(i);
        
        System.out.println("Getting possible keys to test...");
        double[] englishFrec = fr.getEnglishLettersFrecuencies();
        //Number of try keys in each letter from key
        int[] numberKeys = new int[len];
        //Max of try keys per letter in key 
        //(hoping a maximum of three mixed keys of same length)
        int maxKeys = 3;
        //Array of keys for every letter in key
        int[][] matrixKeys = new int[len][maxKeys];
        //Now we get, for every letter position in key,
        //a number of keys based on a good way to determine 
        //if a monogram frequency table is like the English
        //frecuency table, the cosangle (value of 0.8)
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
        //Array to save every decrypted text (for each attack) 
        String finalTexts[] = new String[730];
        //Counter to know the number of texts stored in finalTexts
        //given by the brute force attack
        int finalTextsCount = 0;
        //If there are several or mixed keys (same length),
        //the keys will be several for each letter in key,
        //therefore a brute force attack is needed with all
        //obtained keys to test every possibility 
        if (len == 6)
        finalTextsCount = BruteForce6LengthKey(text, finalTexts,numberKeys,matrixKeys);
        
        System.out.println("Selecting texts to output...");
        //For made last selection from the output from brute force
        //texts, we count the number of "the" trigrams (most
        //repeated trigram in english) at every text and
        //store them in an sorted map
        int trigrams;
        SortedMap<Integer,String> orderedTexts = new TreeMap<Integer,String>();
        for (int i = 0; i < finalTextsCount; i++){
            trigrams = fr.CountTrigram(finalTexts[i], "the");
            orderedTexts.put(trigrams, finalTexts[i]);
        }

        System.out.println("Showing keys with corresponding plaintexts...");
        // For ending, we show the texts that had most times the trigram "the"
        for (int i = 0; i < ans; i++){
            if (orderedTexts.isEmpty()) break;
            int next = orderedTexts.lastKey();
            System.out.println(orderedTexts.get(next));
            orderedTexts.remove(next);
        }
      }

     /*
      * Brute force attack for 6 length key
      * @param text: encrypted text
      * @param finalTexts: array where are stored all the decrypted texts
      * @param numberKeys: number of try keys per every letter of the key
      * @param matrixKeys: array of try keys for every letter in key
      * @return: Number of texts obtained with the given keys
      */
     public int BruteForce6LengthKey(String text, String[] finalTexts, int[] numberKeys, int[][] matrixKeys) {
            int finalTextsCount = 0;
            //Array to save the key to do the try in the attack
            int[] finalKeys = new int[6];
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
            return finalTextsCount;
     }

     /*
      * The cosine of the angle between two vectors
      */
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

     public static void main (String[] args){
        /*
         *  *   *   *   *   ATTACK TO ADDITIVE CIPHER TEST   *   *   *   *   *
         */
        // Scanner s = new Scanner(System.in);
        // System.out.println("Letter frecuency attack to additive cipher, please select number of output plaintexts:");
        // String option = s.nextLine();
        // LetterFrecuencyAttack LFA = new LetterFrecuencyAttack();
        // LFA.AttackToAdditiveCipher(args[0], Integer.parseInt(option));
        // s.close();

        /*
         *  *   *   *   *   ATTACK TO VIGENERE CIPHER TEST   *   *   *   *   *
         */
        Scanner s = new Scanner(System.in);
        System.out.println("Letter frecuency Vigenère attack, please select number of output plaintexts \"n\":");
        String option = s.nextLine();
        LetterFrecuencyAttack LFA = new LetterFrecuencyAttack();
        LFA.IntenseAttackToVigenereCipher(args[0], 6, Integer.parseInt(option));
        s.close();
     }

}
