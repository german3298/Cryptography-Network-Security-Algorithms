import java.util.SortedMap;
import java.util.TreeMap;
import java.util.Scanner;

/*
     * Attacks to decipher monoalphabetic 
     * cipher (Caesar Cipher) in english 
     * language.
     * @author: Germán Rodríguez
*/

public class CaesarCipherAttack {

    FrecuencyReader fr;
    SortedMap<Double, Integer> sM;
    CaesarCipher cc;

    public CaesarCipherAttack() {
        fr = new FrecuencyReader();
        sM = new TreeMap<Double, Integer>();
        cc = new CaesarCipher();
    }

    /*
     * Make an attack observing the most repeated letters
     * in the text and assigning the key comparing them
     * with the "e" letter, which is the most repeated in
     * English language
     */
    public void attackToAdditiveCipher(String text, int ans) {
        int[] keysList = getPossibleKeys(text, ans);
        System.out.println("\nStarting attack...");
        for (int i = 0; i < ans; i++) {
            if (keysList[i] == 0)
                continue;
            System.out.println("\nText with key " + keysList[i] + ": ");
            System.out.println("\n" + cc.caesarCipherDecrypt(text, keysList[i]) + "\n");
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
        double[] frecuenciesText = fr.readFrecuencies(text);
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
        if (sM.isEmpty())
            return 0;
        double d = sM.lastKey();
        int key = sM.get(d) - 4;
        sM.remove(d);
        if (key < 0)
            key += 26;
        return key;
    }

    public static void main(String[] args) {
        /*
         * * * * * ATTACK TO ADDITIVE CIPHER TEST * * * * *
         */
        Scanner s = new Scanner(System.in);
        System.out.println("Letter frecuency attack to additive cipher, please select number of output plaintexts:");
        String option = s.nextLine();
        CaesarCipherAttack cca = new CaesarCipherAttack();
        cca.attackToAdditiveCipher(args[0], Integer.parseInt(option));
        s.close();
    }

}
