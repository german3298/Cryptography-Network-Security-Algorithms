#   Different conversions needed for
#   my implementation of the algorithms
#   and the inputs and outputs that
#   ask and give (strings but in
#   binary, hex or UTF-8 format).
#   strbin = "01001001"
#   strhex = "AB40C310"
#
#   @author: Germán Rodríguez

def int_to_strbin(int,dig):
    """
    Convert from int to string
    in binary format
    :param dig: number of digits
    """
    return bin(int)[2:].zfill(dig)

def strbin_to_int(strbin):
    """
    Convert from string in binary
    format to string
    """
    return int(strbin,2)

def char_to_strbin(str):
    """
    Convert from string in UTF-8
    to string in binary format
    """
    return ''.join(format(i, '08b') for i in bytearray(str, encoding ='utf-8'))

def strhex_to_strbin(strhex):
    """
    Convert from string in
    hexadecimal format to
    string in binary format.
    As I use this in DES, it
    is filled with 64 digits.
    """
    return bin(int(strhex, 16))[2:].zfill(64)

def strbin_to_char(strbin):
    """
    Convert from string in
    binary format to string
    in UTF-8
    """
    bytes_data = int(strbin, 2).to_bytes((len(strbin) + 7) // 8, byteorder='big')
    return bytes_data.decode('utf-8')

def strbin_to_strhex(strbin):
    """
    Convert from string in
    binary format to string
    in hexadecimal format
    """
    return hex(int(strbin, 2))[2:].upper()