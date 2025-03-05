import numpy as np
import seabreeze.spectrometers as sb
import matplotlib.pyplot as plt
import time

# Initialize the spectrometer
devices = sb.list_devices()
if devices:
    spec = sb.Spectrometer(devices[0])
else:
    raise Exception("No spectrometer found")

# Set integration time (in microseconds)  
spec.integration_time_micros(500000) # 100000-100ms

# Optionally, set boxcar width and scans to average
spec.boxcar_width = 3
spec.scans_to_average = 2

# Continuous acquisition loop
try:
    while True:
        # Acquire data
        wavelengths = spec.wavelengths()
        intensities = spec.intensities()
        # Plot the data
        plt.clf()  # Clear the previous plot
        plt.plot(wavelengths, intensities)
        plt.xlabel('Wavelength (nm)')
        plt.ylabel('Intensity (a.u.)')
        plt.title('Spectrometer Data')
        plt.xlim(580,660)
        plt.pause(0.01)  # Pause to update the plot
        
except KeyboardInterrupt:
    print("Data acquisition stopped by user.")

finally:
    # Close the spectrometer connection
    spec.close()
