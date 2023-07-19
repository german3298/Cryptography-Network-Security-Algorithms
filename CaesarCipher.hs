import Data.Char (ord, chr, isAsciiLower)

--Simple Caesar Cipher encrypt (only for lowercase texts)  C = (p + k) mod 26
caesarcipherEncrypt :: String -> Int -> String
caesarcipherEncrypt xs k = [toCharNorm (encrypt x) | x <- xs, isAsciiLower x]
    where encrypt x = (toIntNorm x + k) `mod` 26

--Simple Caesar Cipher decrypt (only for lowercase texts)   p = (C - k) mod 26
caesarcipherDecrypt :: String -> Int -> String
caesarcipherDecrypt xs k = [toCharNorm (decrypt x) | x <- xs, isAsciiLower x]
    where decrypt x = (toIntNorm x - k) `mod` 26

--Affine Caesar Cipher encrypt (only for lowercase texts)   C = (ap + b) mod 26
caesarcipherAffineEncrypt :: String -> Int -> Int -> String
caesarcipherAffineEncrypt xs a b = [toCharNorm (encrypt x) | x <- xs, isAsciiLower x]
    where encrypt x = (toIntNorm x * a + b) `mod` 26

--Affine Caesar Cipher decrypt (only for lowercase texts)   p = ((c-b)/k) mod 26
caesarcipherAffineDecrypt :: String -> Int -> Int -> String
caesarcipherAffineDecrypt xs a b = [toCharNorm (decrypt x) | x <- xs, isAsciiLower x]
    where decrypt x = ((toIntNorm x - b) `div` a) `mod` 26

toIntNorm :: Char -> Int
toIntNorm x = ord x - 97

toCharNorm :: Int -> Char
toCharNorm x = chr(x+97)