import java.util.Scanner;

public class FastExp {
    public static int fast_exponentiation (int base, int exp, int mod) {
        if (mod == 1) return 0;
        int value = 1;
        for (int i = 0; i < exp; i++)
            value = (value*base)% mod;
        return value;
    }

    public static int fast_exponentiation_binary_method (int base, int exp, int mod) {
        if (mod == 1) return 0;
        //Check if (modulus -1) * (modulus - 1) does not overflow base
        int value = 1;
        base = base % mod;
        while (exp > 0){
            if (exp % 2 == 1)
                value = (value * base) % mod;
            exp = exp >> 1;
            base = (base*base) % mod;
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
        int result = fast_exponentiation_binary_method(Integer.parseInt(base), Integer.parseInt(exp), Integer.parseInt(mod));
        System.out.println("Solution: " + base + "^" + exp + " mod " + mod + " = " + result);
    }
}
