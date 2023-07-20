import numpy as np

matrix = np.array(np.mat("1 2 3;4 5 6;7 8 9"))
                   
flattened_array = matrix.flatten()

print("Original matrix:")
print(matrix)

print("\nFlattened array:")
print(flattened_array)