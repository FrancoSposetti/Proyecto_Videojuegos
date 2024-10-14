# Importación de librerías
import pandas as pd

# --- Carga del Dataset ---
ruta = r"C:\Users\kbm19\Desktop\Franco Cursos\Proyectos\Proyecto Videojuegos\Ventas+Videojuegos.csv"
data = pd.read_csv(ruta, encoding='latin1', sep=';')

# --- Exploración Inicial del Dataset ---
print("Primeras filas del dataset:")
print(data.head(), "\n")

print("Información del Dataset:")
data.info()
print("\n")

print("Tamaño del dataset (filas, columnas):", data.shape)
print("\n")

print("Valores nulos en el dataset:")
print(data.isnull().sum(), "\n")

print("Resumen Estadístico de las variables numéricas:")
print(data.describe(), "\n")

# --- Limpieza de Datos ---
# Renombrando las columnas para un formato más uniforme
data = data.rename(columns={
    'Ventas NA': 'Ventas_NorteAmerica',
    'Ventas EU': 'Ventas_Europa',
    'Ventas JP': 'Ventas_Japon',
    'Ventas Otros': 'Ventas_Otros',
    'Ventas Global': 'Ventas_Global'
})

# Conversión de la columna 'Año' a formato numérico
data['Año'] = pd.to_datetime(data['Año'], format='%Y', errors='coerce').dt.year

# Limpieza y conversión de las columnas de ventas
columnas_a_convertir = ['Ventas_NorteAmerica', 'Ventas_Europa', 'Ventas_Japon', 'Ventas_Otros', 'Ventas_Global']
for col in columnas_a_convertir:
    data[col] = pd.to_numeric(data[col].str.replace(',', ''), errors='coerce').fillna(0)

# Escalando las ventas por 10
data[columnas_a_convertir] = data[columnas_a_convertir] * 10

# Rellenando valores nulos en la columna 'Editorial' con la moda
moda_editorial = data['Editorial'].mode()[0]
data['Editorial'] = data['Editorial'].fillna(moda_editorial)

# --- Verificación de la limpieza del Dataset ---
print("Primeras filas del dataset después de la limpieza:")
print(data.head(), "\n")

print("Información del Dataset después de la limpieza:")
data.info()
print("\n")

print("Valores nulos restantes en el dataset:")
print(data.isnull().sum(), "\n")

print("Resumen Estadístico de las variables numéricas (sin la columna 'Año'):")
print(data.drop(columns=['Año']).describe(), "\n")

# --- Análisis Básico ---
# Ventas globales por año
ventas_por_año = data.groupby('Año')['Ventas_Global'].sum().sort_index()
print("Ventas globales por año:")
print(ventas_por_año, "\n")

# Top 5 de editoriales con más ventas globales
top_editoriales = data.groupby('Editorial')['Ventas_Global'].sum().nlargest(5)
print("Top 5 de editoriales con más ventas globales:")
print(top_editoriales, "\n")

# --- Guardando el Dataset Limpio ---
ruta_salida = r"C:\Users\kbm19\Desktop\Franco Cursos\Proyectos\Proyecto Videojuegos\Ventas_Videojuegos_Limpio.xlsx"
data.to_excel(ruta_salida, index=False)
print(f"El dataset limpio ha sido guardado en: {ruta_salida}")

# --- Visualizaciones (opcional, si deseas agregar visualizaciones) ---
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
sns.set(style="whitegrid")

# Gráfico de ventas globales por año
plt.figure(figsize=(12, 6))
sns.lineplot(x=ventas_por_año.index, y=ventas_por_año.values, marker='o', color='b')
plt.title('Ventas Globales de Videojuegos por Año', fontsize=16)
plt.xlabel('Año', fontsize=14)
plt.ylabel('Ventas Globales (en millones)', fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico de las top 5 editoriales con más ventas globales
plt.figure(figsize=(10, 6))
sns.barplot(x=top_editoriales.values, y=top_editoriales.index, palette='viridis')
plt.title('Top 5 Editoriales con Más Ventas Globales', fontsize=16)
plt.xlabel('Ventas Globales (en millones)', fontsize=14)
plt.ylabel('Editorial', fontsize=14)
plt.tight_layout()
plt.show()
