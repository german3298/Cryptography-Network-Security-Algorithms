import java.util.SortedMap;
import java.util.TreeMap;
import java.util.Scanner;

/*
     * Attacks to decipher monoalphabetic 
     * ciphers in english language.
     * One to attack any random 
     * monoalphabetic ciphers and one to
     * attack additive ciphers (Caesar Cipher)
     * @ author: Germán Rodríguez
*/
public class LetterFrecuencyAttack {

    

    FrecuencyReader fr;
    SortedMap<Double,Integer> sM;

     public LetterFrecuencyAttack (String text, int ans){
        fr = new FrecuencyReader(text);
        AttackToAdditiveCipher(text, ans);
     }

     public void AttackToMonoalphabeticCipher(String text, int ans) {
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
        sM = new TreeMap<Double,Integer>();
        double[] frecuenciesText = fr.getTextFrecuencies();
        for (int i = 0; i < frecuenciesText.length; i++)
            sM.put(frecuenciesText[i], i);
        System.out.println("\nStarting attack...");
        for (int i = 0; i < ans; i++){
            int key = getKey();
            if (key == 0) break;
            System.out.println("\nText with key " + key + ": ");
            System.out.println("\n" + CaesarCipherDecrypt(text, key) + "\n");
        }
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
            int numP = (p - key);
            if (numP < 'a') numP +=26;
            char c = (char)numP;
            decryptedText += c;
        }
        return decryptedText;
     }

     public static void main (String[] args){
        Scanner s = new Scanner(System.in);
        System.out.println("Letter frecuency attack to additive cipher, please select number of plaintexts:");
        String option = s.nextLine();
        LetterFrecuencyAttack LFA = new LetterFrecuencyAttack(args[0],Integer.parseInt(option));
     }

}
