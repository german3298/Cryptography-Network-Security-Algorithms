import java.util.Random;
import java.util.Scanner;

/* 
 * Miller-Rabin algorithm implementation,
 * with the binary method of fast modulo 
 * exponentiation
 */

public class MillerRabin {

    private int fast_exponentiation_binary_method (int base, int exp, int mod) {
        if (mod == 1) return 0;
        //Check if (mod - 1) * (mod - 1) doesn't overflow base
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
    
    private String miller_rabin_test (int a, int n) {
        if (n % 2 == 0) return "composite";
        //Find k and q
        int q = 0;
        int k = 0;
        int nsub = n-1;
        while (q == 0) {
            k++;
            int pow = (int) Math.pow(2,k);
            if (nsub % pow == 0){
                q = nsub/pow;
                q = q % 2 == 1 ? q : 0;
            }
        }
        //Check tests
        if (fast_exponentiation_binary_method(a,q,n) == 1) return "inconclusive";
        for (int i = 0; i < k; i++) {
            int pow = (int) Math.pow(2,i);
            if (fast_exponentiation_binary_method(a,q*pow,n) == nsub) 
                return "inconclusive";
        }
        return "composite";
    }

    public static void main (String[] args) {
        MillerRabin mr = new MillerRabin();
        Scanner s = new Scanner(System.in);
        System.out.println("Miller-Rabin algorithm, please select mode:");
        System.out.println("    1. Check if a number is prime with one base");
        System.out.println("    2. Check if a number is prime with a number of random bases");
        String option = s.nextLine();
        
        if (option.equals("1")){

            System.out.println("Select number to check primality:");
            int n = Integer.parseInt(s.nextLine());
            System.out.println("Select base:");
            int a = Integer.parseInt(s.nextLine());
            String ans = mr.miller_rabin_test(a,n);
            System.out.println("The number " + n + ", with base " + a + " is " + ans);

        } else if (option.equals("2")){

            System.out.println("Select number to check primality:");
            int n = Integer.parseInt(s.nextLine());
            System.out.println("Select number of bases:");
            int basesNumber = Integer.parseInt(s.nextLine());
            int[] bases = new int[basesNumber];
            Random rand = new Random();
            for (int i = 0; i < basesNumber; i++)
                bases[i] = rand.nextInt(n-2)+2;
            System.out.println("Test results for number " + n + ": ");
            for (int i = 0; i < basesNumber; i++)
                System.out.println((i+1) + ") With base " + bases[i] + ": " + mr.miller_rabin_test(bases[i], n));
        } else {

            System.out.println("Invalid option");

        }
        s.close();
    }
}
