import matplotlib.pyplot as plt

# Define the data from the table
A1_pow = [0, 0.1, 0.3, 0.5]
MPU11_adv = [0, 0.37692, 0.5, 0.9615]
MPU12_adv = [0, 0, 0, 0]


# Plotting A1_pow against MPU1_adv
sorted_indices = sorted(range(len(A1_pow)), key=lambda k: A1_pow[k])
A1_pow_sorted = [A1_pow[i] for i in sorted_indices]
MPU1_adv_sorted = [MPU11_adv[i] for i in sorted_indices]
MPU2_adv_sorted = [MPU12_adv[i] for i in sorted_indices]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(A1_pow_sorted, MPU1_adv_sorted, marker="o", color="orange")
plt.plot(A1_pow_sorted, MPU2_adv_sorted, marker="o", color="blue")

# Adding labels and title
plt.xlabel("ζ1 (A1 pow)")
plt.ylabel("Fraction of first attacker's blocks in main chain")
plt.title("Fraction of first attacker's blocks vs. ζ1")

# Show grid
plt.grid(True)

# Show plot
plt.show()


import matplotlib.pyplot as plt

# Define the data from the table
A1_pow = [0, 0.1, 0.3, 0.5]
MPU11_adv = [0, 0.23, 0.33, 0.821]
MPU12_adv = [0, 0.692, 0.625, 0.14]


# Plotting A1_pow against MPU1_adv
sorted_indices = sorted(range(len(A1_pow)), key=lambda k: A1_pow[k])
A1_pow_sorted = [A1_pow[i] for i in sorted_indices]
MPU1_adv_sorted = [MPU11_adv[i] for i in sorted_indices]
MPU2_adv_sorted = [MPU12_adv[i] for i in sorted_indices]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(A1_pow_sorted, MPU1_adv_sorted, marker="o", color="orange")
plt.plot(A1_pow_sorted, MPU2_adv_sorted, marker="o", color="blue")

# Adding labels and title
plt.xlabel("ζ1 (A1 pow)")
plt.ylabel("Fraction of first attacker's blocks in main chain")
plt.title("Fraction of first attacker's blocks vs. ζ1")

# Show grid
plt.grid(True)

# Show plot
plt.show()
