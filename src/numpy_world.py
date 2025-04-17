import numpy as np

# Create a 1D array
arr1 = np.array([1, 2, 3, 4, 5])
print("1D Array: \n", arr1)

# Create a 2D array
arr2 = np.array([[1, 2, 3], [4, 5, 6]])
print("\n2D Array: \n", arr2)

# Perform addition operation on the arrays
sum_arr = np.add(arr1, arr1)
print("\nSum of the 1D array with itself: \n", sum_arr)

# Reshape arr2
reshaped_arr2 = arr2.reshape(-1)
print("\nReshaped 2D array to 1D: \n", reshaped_arr2)

# Slice arr1
sliced_arr1 = arr1[1:4]
print("\nSliced 1D array (from index 1 to 3): \n", sliced_arr1)
