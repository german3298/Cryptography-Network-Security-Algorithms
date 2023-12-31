import java.util.Random;
import java.util.Scanner;

/* 
 * Miller-Rabin algorithm implementation,
 * with the binary method of fast modulo 
 * exponentiation
 * Remember that Miller-Rabin returns "inconclusive"
 * if the number can be prime, but it could also be
 * composite.
 * Repeating the algorithm with several bases (a's),
 * it raises the probabilities to be prime (if returns 
 * inconclusive in all tests) exponentially.
 * @author: Germán Rodríguez
 */

public class MillerRabin {

    
    /*
     * Miller-Rabin algorithm 
     * Proves the primality of a number
     * @param a Base used in a^(q*2^j) mod n 
     * (where we check certain properties to know if it's a prime number)
     * @param n Possible prime number to check
     * @return "composite" if we are sure that isn't a prime number,
     * or "inconclusive" if it could be a prime number
     */
    private String millerRabinTest (int a, int n) {
        if (n % 2 == 0) return "composite";  //If number is even, obviously is a composite number
        //Find k and q, k > 0 and q odd, so that n-1 = 2^k * q
        int q = 0;
        int k = 0;
        int nsub = n-1;
        //Itering in k, looking that (n-1/2^k) = an integer odd number (q)
        while (q == 0) {
            k++;
            int pow = (int) Math.pow(2,k);
            if (nsub % pow == 0){
                q = nsub/pow;
                q = q % 2 == 1 ? q : 0;
            }
        }
        //Check tests, checking certain prime numbers properties (self-explicated in code)
        //If not passed, for sure it's a composite number
        if (FastExp.fastModExponentiationBit(a,q,n) == 1) return "inconclusive";
        for (int j = 0; j < k; j++) {
            int pow = (int) Math.pow(2,j);
            if (FastExp.fastModExponentiationBit(a,q*pow,n) == nsub) 
                return "inconclusive";
        }
        return "composite";
    }

    /*
     * Basic program to test Miller-Rabin implementation
     */
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
            String ans = mr.millerRabinTest(a,n);
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
                System.out.println((i+1) + ") With base " + bases[i] + ": " + mr.millerRabinTest(bases[i], n));

        } else {

            System.out.println("Invalid option");

        }
        s.close();
    }
}
