import Data.Char (ord, chr, isAsciiLower)


-- @author: Germán Rodríguez


--Simple Caesar Cipher encrypt (only for lowercase texts)  C = (p + k) mod 26
caesarcipherEncrypt :: String -> Int -> String
caesarcipherEncrypt xs k = [toCharNorm (encrypt x) | x <- xs, isAsciiLower x]
    where encrypt x = (toIntNorm x + k) `mod` 26

--Simple Caesar Cipher decrypt (only for lowercase texts)   p = (C - k) mod 26
caesarcipherDecrypt :: String -> Int -> String
caesarcipherDecrypt xs k = [toCharNorm (decrypt x) | x <- xs, isAsciiLower x]
    where decrypt x = (toIntNorm x - k) `mod` 26

--Affine Caesar Cipher encrypt (only for lowercase texts)   C = (ap + b) mod 26
--If a hasn't modulo 26 multiplicative inverse, the mapping won't be one to one
caesarcipherAffineEncrypt :: String -> Int -> Int -> String
caesarcipherAffineEncrypt xs a b
    | not $ hasModularMultiplicativeInverse a 26 = "The selected a has not modulo 26 multiplicative inverse."
    | otherwise = [toCharNorm (encrypt x) | x <- xs, isAsciiLower x] 
    where encrypt x = (toIntNorm x * a + b) `mod` 26

--Affine Caesar Cipher decrypt (only for lowercase texts)   p = a^-1*(c-b) mod 26
--For this, we need to calcule the modular multiplicative inverse for a mod 26
caesarcipherAffineDecrypt :: String -> Int -> Int -> String
caesarcipherAffineDecrypt xs a b
    | not $ hasModularMultiplicativeInverse a 26 = "The selected a has not modulo 26 multiplicative inverse."
    | otherwise = [toCharNorm (decrypt x) | x <- xs, isAsciiLower x]
    where decrypt x = modularMultiplicativeInverse a 26 * (toIntNorm x - b) `mod` 26

--Normalize a char, changing it to integer and transforming it from ASCII to our scale
-- a = 0, b = 1 ... z = 25
toIntNorm :: Char -> Int
toIntNorm x = ord x - 97

--Return the ASCII code and trasforma in char again
toCharNorm :: Int -> Char
toCharNorm x = chr(x+97)

modularMultiplicativeInverse :: Int -> Int -> Int
modularMultiplicativeInverse a n = get2nd $ eEA a n 

--Extended euclidean algorithm
--  a = qb + r  ->   xb + yr = d   ->   xb + y(a-qb) = d   ->   xb + ya - qyb = d   ->   ya + (x-qy)b = d
eEA :: Int -> Int -> (Int, Int, Int)
eEA a 0 = (a, 1, 0)
eEA a b = 
    let (d, x, y) = eEA b r
    in (d, y, x - (q * y))
    where
      (q, r) = divMod a b

get2nd :: (Int, Int, Int) -> Int
get2nd (_,x,_) = x

--Not efficient version, but for the mod 26 it is perfectly valid
-- x starts at n-1 value 
modularMultiplicativeInversev2 :: Int -> Int -> Int -> Int
modularMultiplicativeInversev2 a n x
    | a*x `mod` n == 1 = x
    | otherwise = modularMultiplicativeInversev2 a n (x-1)

--A number a has inverse modulo n if their mcd is 1
hasModularMultiplicativeInverse :: Int -> Int -> Bool 
hasModularMultiplicativeInverse a n = eA a n == 1

--Euclidean Algorithm
eA :: Int -> Int -> Int
eA a 0 = a
eA a b = eA b (a `mod` b)