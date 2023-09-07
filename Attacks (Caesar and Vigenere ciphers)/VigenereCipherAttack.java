import java.util.SortedMap;
import java.util.TreeMap;
import java.util.Scanner;

/*
     * Attacks to decipher polyalphabetic 
     * cipher (Vigenère).
     * @author: Germán Rodríguez
*/

public class VigenereCipherAttack {

    FrecuencyReader fr;
    CaesarCipher cc;

    public VigenereCipherAttack() {
        fr = new FrecuencyReader();
        cc = new CaesarCipher();
    }

    /*
     * Simple VigenereCipher Decrypt
     */
    public String vigenereDecrypt(String text, int[] key) {
        text = text.toLowerCase().replaceAll("[^a-z]", "");
        String plainText = "";
        int len = key.length;
        for (int i = 0; i < text.length(); i++) {
            char p = text.charAt(i);
            int k = key[i % len];
            int c = (p - k);
            if (c < 97)
                c += 26;
            plainText += (char) (c);
        }
        return plainText;
    }

    /*
     * The cosine of the angle between two vectors
     */
    public double cosangle(double[] x, double[] y) {
        double numerator = 0;
        double lengthx2 = 0;
        double lengthy2 = 0;
        for (int i = 0; i < x.length; i++) {
            numerator += x[i] * y[i];
            lengthx2 += x[i] * x[i];
            lengthy2 += y[i] * y[i];
        }
        return numerator / Math.sqrt(lengthx2 * lengthy2);
    }

    /*
     * Attack trying several key lengths
     */
    public void forceBruteKeyVigenereAttack(String text, int startingKeyLength, int endKeyLength) {
        System.out.println("Trying keys from " + startingKeyLength + " to " + endKeyLength + ": ");
        for (int i = startingKeyLength; i <= endKeyLength; i++) {
            System.out.println("Key length: " + i);
            if (simpleVigenereAttack(text, i)) {
                System.out.println("Successful attack, stoping...");
                break;
            }
        }
    }

    /*
     * Knowing the key length, returns the possible key and
     * the possible decrypted text
     * 
     * @returns if the attack was successful returns true
     */
    public boolean simpleVigenereAttack(String text, int len) {
        text = text.toLowerCase().replaceAll("[^a-z]", "");
        System.out.println("Starting attack...");
        System.out.println("Dividing texts...");
        // First we divide the text in "key length" texts
        String[] texts = new String[len];
        for (int i = 0; i < len; i++)
            texts[i] = "";
        // Divide text in subtexts with same key (in Caesar Cipher every one of them)
        for (int i = 0; i < text.length(); i++)
            texts[i % len] += text.charAt(i);

        double[] englishFrec = fr.getEnglishLettersFrecuencies();
        int[] numberKeys = new int[len];
        String[] decryptedTexts = new String[len];
        int founded = 0;
        for (int i = 0; i < len; i++) {
            numberKeys[i] = 0;
            for (int j = 0; j < 26; j++) {
                String decipheredText = cc.caesarCipherDecrypt(texts[i], j);
                double[] frec = fr.readFrecuencies(decipheredText);
                if (cosangle(englishFrec, frec) > 0.9) {
                    numberKeys[i] = j;
                    decryptedTexts[i] = decipheredText;
                    founded++;
                    break;
                }
            }
        }
        System.out.println("KEY: ");

        for (int i = 0; i < len; i++)
            System.out.print(numberKeys[i] + " ");
        System.out.println();

        if (founded < len) {
            System.out.println("[!] Aborting attack, probably not right key length\n");
            return false;
        }
        String finalText = "";
        System.out.println("TEXT: ");
        for (int i = 0; i < decryptedTexts[len - 1].length(); i++)
            for (int j = 0; j < len; j++)
                finalText += decryptedTexts[j].charAt(i);
        System.out.println(finalText);
        System.out.println();
        return true;
    }

    /*
     * An attack to a Vigenère Cipher that outputs "ans"
     * possible texts. It outputs several texts because can
     * decrypt a mixed text, with several keys (but with
     * same key length), and in order of probability.
     * The more different keys there are, the longer the
     * texts should be.
     */
    public void intenseAttackToVigenereCipher(String text, int len, int ans) {
        System.out.println("Starting attack...");

        System.out.println("Dividing texts...");
        // First we divide the text in "key length" texts
        String[] texts = new String[len];
        for (int i = 0; i < len; i++)
            texts[i] = "";
        // Divide text in subtexts with same key (in Caesar Cipher every one of them)
        for (int i = 0; i < text.length(); i++)
            texts[i % len] += text.charAt(i);

        System.out.println("Getting possible keys to test...");
        double[] englishFrec = fr.getEnglishLettersFrecuencies();
        // Number of try keys in each letter from key
        int[] numberKeys = new int[len];
        // Max of try keys per letter in key
        // (hoping a maximum of three mixed keys of same length)
        int maxKeys = 3;
        // Array of keys for every letter in key
        int[][] matrixKeys = new int[len][maxKeys];
        // Now we get, for every letter position in key,
        // a number of keys based on a good way to determine
        // if a monogram frequency table is like the English
        // frecuency table, the cosangle (value of 0.8)
        for (int i = 0; i < len; i++) {
            numberKeys[i] = 0;
            for (int j = 0; j < 26; j++) {
                String decipheredText = cc.caesarCipherDecrypt(texts[i], j);
                double[] frec = fr.readFrecuencies(decipheredText);
                if (cosangle(englishFrec, frec) > 0.8) {
                    if (numberKeys[i] == maxKeys)
                        break;
                    matrixKeys[i][numberKeys[i]] = j;
                    numberKeys[i]++;
                }
            }
        }

        System.out.println("Performing brute force attack...");
        // Array to save every decrypted text (for each attack)
        String finalTexts[] = new String[730];
        // Counter to know the number of texts stored in finalTexts
        // given by the brute force attack
        int finalTextsCount = 0;
        // If there are several or mixed keys (same length),
        // the keys will be several for each letter in key,
        // therefore a brute force attack is needed with all
        // obtained keys to test every possibility
        if (len == 6)
            finalTextsCount = bruteForce6LengthKey(text, finalTexts, numberKeys, matrixKeys);

        System.out.println("Selecting texts to output...");
        // For made last selection from the output from brute force
        // texts, we count the number of "the" trigrams (most
        // repeated trigram in english) at every text and
        // store them in an sorted map
        int trigrams;
        SortedMap<Integer, String> orderedTexts = new TreeMap<Integer, String>();
        for (int i = 0; i < finalTextsCount; i++) {
            trigrams = fr.countTrigram(finalTexts[i], "the");
            orderedTexts.put(trigrams, finalTexts[i]);
        }

        System.out.println("Showing keys with corresponding plaintexts...");
        // For ending, we show the texts that had most times the trigram "the"
        for (int i = 0; i < ans; i++) {
            if (orderedTexts.isEmpty())
                break;
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
    public int bruteForce6LengthKey(String text, String[] finalTexts, int[] numberKeys, int[][] matrixKeys) {
        int finalTextsCount = 0;
        // Array to save the key to do the try in the attack
        int[] finalKeys = new int[6];
        for (int i = 0; i < numberKeys[0]; i++)
            for (int j = 0; j < numberKeys[1]; j++)
                for (int k = 0; k < numberKeys[2]; k++)
                    for (int l = 0; l < numberKeys[3]; l++)
                        for (int m = 0; m < numberKeys[4]; m++)
                            for (int n = 0; n < numberKeys[5]; n++) {
                                finalKeys[0] = matrixKeys[0][i];
                                finalKeys[1] = matrixKeys[1][j];
                                finalKeys[2] = matrixKeys[2][k];
                                finalKeys[3] = matrixKeys[3][l];
                                finalKeys[4] = matrixKeys[4][m];
                                finalKeys[5] = matrixKeys[5][n];
                                String finalText = "Key: ";
                                for (int o = 0; o < finalKeys.length; o++)
                                    finalText += finalKeys[o] + " ";
                                finalText += "\nText:\n" + vigenereDecrypt(text, finalKeys) + "\n";
                                finalTexts[finalTextsCount] = finalText;
                                finalTextsCount++;
                            }
        return finalTextsCount;
    }

    public static void main(String[] args) {

        /*
         * * * * * ATTACK TO VIGENERE CIPHER WITH SEVERAL KEYS AT SAME TEXT (LENGTH 6) * * * * *
         */
        // Scanner s = new Scanner(System.in);
        // System.out.println("Letter frecuency Vigenère attack, please select number of
        // output plaintexts \"n\":");
        // String option = s.nextLine();
        // VigenereCipherAttack vca = new VigenereCipherAttack();
        // vca.intenseAttackToVigenereCipher(args[0], 6, Integer.parseInt(option));
        // s.close();

        /*
         * * * * * ATTACK TO VIGENERE CIPHER WITH BRUTE FORCE TO DETECT KEY LENGTH  * * * * *
         */
        Scanner s = new Scanner(System.in);
        System.out.println("Vigenère attack: \n");
        VigenereCipherAttack vca = new VigenereCipherAttack();
        vca.forceBruteKeyVigenereAttack(args[0], Integer.parseInt(args[1]), Integer.parseInt(args[2]));
        s.close();
    }
}
