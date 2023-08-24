import java.util.Scanner;

/*
 * 
 *  @author: Germán Rodríguez
 * 
 */


public class FastExp {
    
    public static int fast_mod_exponentiation (int base, int exp, int mod) {
        if (mod == 1) return 0;
        int value = 1;
        for (int i = 0; i < exp; i++)
            value = (value*base)% mod;
        return value;
    }

    /*
     * Makes a fast modulo exponentiation 
     * using succesive squaring binary method
     * and modular arithmetic
     * @return result of (base^exp modulo mod)
     */
    public static int fast_mod_exponentiation_binary_method (int base, int exp, int mod) {
        if (mod == 1) return 0;
        //Should check if (mod - 1) * (mod - 1) doesn't overflow base
        int value = 1;
        base = base % mod;
        //Check binary digits one by one, and if it's odd (2^n), change value
        while (exp > 0){
            if (exp % 2 == 1)
                value = (value * base) % mod;
            exp = exp >> 1;                     //always change binary number shifting to the right
            base = (base*base) % mod;           //change base every step, using modular arithmetic 
        }
        return value;
    }

    public static void main (String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.println("Insert base:");
        String base = s.nextLine();
        System.out.println("Insert exp:");
        String exp = s.nextLine();
        System.out.println("Insert mod:");
        String mod = s.nextLine();
        s.close();
        int result = fast_mod_exponentiation_binary_method(Integer.parseInt(base), Integer.parseInt(exp), Integer.parseInt(mod));
        System.out.println("Solution: " + base + "^" + exp + " mod " + mod + " = " + result);
    }
}
