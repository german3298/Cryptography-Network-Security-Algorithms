#   Bitwise operations in binary numbers
#   represented as strings.
#
#   @author: Germán Rodríguez

def xor(input1, input2):
    """
    Bitwise xor operation in a binary
    number as a string
    """
    output = ""
    for n in range(len(input1)):
        if (input1[n] == input2[n]):
            output += "0"
        else:
            output += "1"
    return output

def left_shift(input,shifts):
    """
    Circular left shift in a binary number
    as a string 
    """
    while (shifts > 0):
        input = input[1:]+input[0:1]
        shifts -= 1
    return input

def split_same_length(str, leng):
    """
    Split a string in several parts
    of the same length
    """
    return [str[i:i+leng] for i in range(0, len(str), leng)]
