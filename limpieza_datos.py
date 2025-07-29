import pandas as pd
import re
from utils import convertir_fecha
from unidecode import unidecode

#cargar el archivo Excel sucio
archivo="ventas_sucias.xlsx"
df=pd.read_excel(archivo,sheet_name="Sheet1")

# Limpiar nombres de columnas: quitar espacios, pasar a minúsculas, reemplazar espacios por guiones bajos
df['producto']=df['producto'].str.strip().str.replace(r'\s+',' ' ,regex=True)
df['ciudad']=df['ciudad'].str.strip().str.replace(r'\s+',' ' ,regex=True)
df['canal']=df['canal'].str.strip().str.replace(r'\s+',' ' ,regex=True)


# Estandarizar texto en columnas
df['producto'] = df['producto'].str.strip().str.title()
df['ciudad'] = df['ciudad'].str.strip().str.title()
df['canal'] = df['canal'].str.strip().str.title()

# Rellenar nulos en 'canal' con 'sin dato'
df['canal'] = df['canal'].fillna('sin dato')
df['producto']=df['producto'].fillna('sin dato')
df['unidades']=df['unidades'].fillna(0)

#Eliminar tildes
df['ciudad']=df['ciudad'].apply(lambda x:unidecode(x) if isinstance(x,str)else x)

#Convertir a fecha estandarizada
df['fecha']=df['fecha'].apply(convertir_fecha)

# Recalcular total donde falte (precio * unidades)
df['total'] = df['unidades'] * df['precio_unit']


df.to_excel('output/ventas_limpias.xlsx',index=False)

import matplotlib.pyplot as plt

# Agrupar por producto y sumar total
ventas_por_producto = df.groupby('producto')['total'].sum().sort_values(ascending=False)

# Crear gráfico
ventas_por_producto.plot(kind='bar', figsize=(8,5), title='Ventas por Producto')
plt.ylabel('Total Vendido ($)')
plt.xlabel('Producto')
plt.tight_layout()

# Agregar etiquetas de datos encima de cada barra
for i, valor in enumerate(ventas_por_producto):
    plt.text(i, valor + 1000, f"${int(valor):,}", ha='center', va='bottom', fontsize=9, rotation=0)

# Guardar como imagen
plt.savefig('graficas/grafico_ventas_por_producto.png')
plt.close
print("Gráfico ventas_por_producto guardado en la carpeta gráficas  ")
#plt.show()

import matplotlib.pyplot as plt

# Agrupar por ciudad y sumar total
ventas_por_ciudad = df.groupby('ciudad')['total'].sum()

# Crear gráfica de torta
plt.figure(figsize=(6, 6))
plt.pie(ventas_por_ciudad, labels=ventas_por_ciudad.index, 
        autopct='%1.1f%%', startangle=90, shadow=True)
plt.title('Distribución de Ventas por Ciudad')
plt.axis('equal')  # Para que sea un círculo perfecto

# Guardar como imagen
plt.savefig('graficas/grafico_torta_ventas_ciudad.png')
plt.close
print("Gráfico de torta_ventas_ciudad guardado en la carpeta gráficas  ")
#plt.show()


#Ver resumen general de tipos de datos y nulos
#print(df.info())

# Ver cuántos valores nulos hay por columna
#print(df.isnull().sum())

#Ver columnas actuales
#print("Columnas actuales",df.columns.to_list())

# Mostrar las primeras filas para revisar su estado
print(df.head(10))

