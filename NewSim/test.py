import matplotlib.pyplot as plt

# Constants
R = 8.314  # Ideal gas constant (in J/(mol K))

# Initial conditions
pressure_initial = 1.0  # Initial pressure in atm
volume_initial = 5    # Initial volume in liters
temperature_initial = 273.15  # Initial temperature in Kelvin (0 degrees Celsius)

# Compression parameters
compression_ratio = 5   # Ratio of the final volume to the initial volume

# Lists to store simulation results
pressures = [pressure_initial]
volumes = [volume_initial]
temperatures = [temperature_initial]

# Simulation loop
for _ in range(compression_ratio):
    # Using the Ideal Gas Law to calculate the new pressure, volume, and temperature
    pressure_final = pressures[-1] * compression_ratio
    volume_final = volumes[-1] / compression_ratio
    temperature_final = (temperatures[-1] * volume_initial) / volume_final  # Keeping pressure constant during compression
    
    # Appending the results to the lists
    pressures.append(pressure_final)
    volumes.append(volume_final)
    temperatures.append(temperature_final)

print (pressures)
print (volumes)
print (temperatures)

# Plotting the results
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(volumes, pressures, marker='o')
plt.xlabel('Volume (L)')
plt.ylabel('Pressure (atm)')
plt.title('Pressure-Volume Diagram')

plt.subplot(1, 2, 2)
plt.plot(volumes, temperatures, marker='o')
plt.xlabel('Volume (L)')
plt.ylabel('Temperature (K)')
plt.title('Temperature-Volume Diagram')

plt.tight_layout()
plt.show()
