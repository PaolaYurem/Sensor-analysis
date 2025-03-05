import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def ordenar_csv(nombre_archivo_entrada, nombre_archivo_salida):
    df = pd.read_csv(nombre_archivo_entrada)
    df_sorted = df.sort_values(by=df.columns[0])
    df_sorted.to_csv(nombre_archivo_salida, index=False)
    print(f"Archivo ordenado guardado como {nombre_archivo_salida}")

# Order data
dir = '/Users/user' # modify dir
ordenar_csv(f"{dir}/datos.csv", f"{dir}/datos_ordenados.csv")    
file_dir = f'{dir}datos_ordenados.csv'
datos = pd.read_csv(file_dir)

# Extract data
dlambda = datos.iloc[:, 1]
dtiempo = datos.iloc[:, 0]

# Modify fringes jumps
l_anterior = 0
x = 0
l_n = []
for l in dlambda:
    if np.absolute(l-l_anterior)>5:
        if (l-l_anterior) > 0:
            l_nueva = l - 6.25 + x
            x = x - 6.25
        else:
            l_nueva = l + 6.25 + x
            x = x + 6.25
    else:
        l_nueva = l + x
    l_anterior = l
    l_n = np.append(l_n, l_nueva)

# Plot data
fig, (ax1,ax2) = plt.subplots(1, 2, figsize=(10, 5))    
ax1.plot(dtiempo/3600, dlambda, 'o', label = 'Espectro', color = 'blue')
ax2.plot(dtiempo/3600, l_n, 'o', label = 'Espectro', color = 'blue')
ax1.set_title('1 Ciclo sin arreglo de fase')
ax1.set_xlabel('Tiempo (hr)')
ax1.set_ylabel('Cambio de longitud de onda (nm)')
ax2.set_title('1 Ciclo')
ax2.set_xlabel('Tiempo (hr)')
ax2.set_ylabel('Cambio de longitud de onda (nm)')
plt.tight_layout()
plt.show()
