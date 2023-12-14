import pandas as pd

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('datos.csv')

# ## Mostrar los primeros 5 datos del DataFrame
# print(df)


# Encuentra el índice donde se encuentra la URL en la columna "Enlace"
indice = df[df['ID'] == '4PTDEDHA'].index

# Verifica si se encontró la URL en el DataFrame
if not indice.empty:
    print("El índice del dato en la columna 'Enlace' es:", indice[0])
else:
    print("La URL no se encontró en el DataFrame.")