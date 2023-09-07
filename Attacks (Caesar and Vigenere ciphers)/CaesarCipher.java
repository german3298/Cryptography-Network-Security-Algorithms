public class CaesarCipher {

    /*
     * Simple CaesarCipher Decrypt
     */
    public String caesarCipherDecrypt(String text, int key) {
        text = text.toLowerCase().replaceAll("[^a-z]", "");
        String decryptedText = "";
        for (int i = 0; i < text.length(); i++) {
            char p = text.charAt(i);
            int numP = (p - key);
            if (numP < 97)
                numP += 26;
            char c = (char) numP;
            decryptedText += c;
        }
        return decryptedText;
    }
}
