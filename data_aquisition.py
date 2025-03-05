import seabreeze.spectrometers as sb
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
from datetime import datetime
import pandas as pd
import dropbox


def plot_spectra(x,y):
    plt.figure()
    plt.plot(x, y, linestyle='-', color='b', label='Intensidad')
    plt.xlabel('Longitud de Onda (nm)')
    plt.ylabel('Intensidad')
    plt.title('Espectro de Intensidad vs Longitud de Onda')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    
def capture_spectra(spectrometer):
    wavelengths = spectrometer.wavelengths()
    spectra = spectrometer.intensities(correct_dark_counts=True, correct_nonlinearity=True)
    return wavelengths,spectra
    
def write_spectra(directory,x_data,y_data):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato: AAAAMMDD_HHMMSS
    output_file = f"{directory}/espectro_{current_time}.csv"
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # writer.writerow(["Wavelength (nm)", "Intensity"])         # encabezado
        for x, y in zip(x_data, y_data):  
            writer.writerow([x, y])
    print(f"Datos guardados en {output_file}")
    return output_file,current_time
    
def write_dpx(file_from,current_time):
    access_token = 'token' # modify token
    file_to = f'/{datetime.today}/espectro_{current_time}.csv'
    dbx = dropbox.Dropbox(access_token)
    dbx.files_upload(open(file_from, 'rb').read(), file_to)

# Search and select an spectrometer
devices = sb.list_devices()
if not devices:
    print("No se encontraron espectrómetros.")
    exit()

# Select first spectrometer found 
spectrometer = sb.Spectrometer(devices[0])

# Configure integration time (tiempo de exposición)
spectrometer.integration_time_micros(200000)  # Tiempo de integración en microsegundos

# Optionally, set boxcar width and scans to average
spectrometer.boxcar_width = 3
spectrometer.scans_to_average = 2

# Continuous acquisition loop
try:
    while True:
        
        # Spectrometer data acquisition 
        wavelengths,spectra = capture_spectra(spectrometer)
        wavelengths,spectra = capture_spectra(spectrometer)
            
        # Write data to a CSV file
        folder = 'prueba'
        dir = f"/Users/user/Desktop/{folder}" #modify this line
        output_file,current_time = write_spectra(dir,wavelengths,spectra)
        
        # Plot data
        plot_spectra(wavelengths, spectra)
        
        # Upload csv file to dropbox
        write_dpx(output_file,current_time)
        
        # Waiting time
        time.sleep(10) # time in seconds

except KeyboardInterrupt: #CRTL + C
    print("Data acquisition stopped by user.")
  
# Close the spectrometer connection
finally:
    spectrometer.close()
