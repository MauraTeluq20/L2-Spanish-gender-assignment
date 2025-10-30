# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:54:47 2024

@author: Maura
"""

import pandas as pd


def gender_mark(row):
    if (row['Noun'][-1] == 'a' or row['Noun'][-2:] == 'as'):
        return 'Fem_mark'
    elif (row['Noun'][-1] == 'o' or row['Noun'][-2:] == 'os'):
        return 'Masc_mark'
    elif (row['Noun'][-1] != 'o' and row['Noun'][-2:] != 'os' and row['Noun'][-1] != 'a' and row['Noun'][-2:] != 'as'):
        return 'No_mark' #cambiar el valor
    else:
        return None
    
def protot_mark (row):
    if (row['Noun_gen'] == 'Fem' and row['Gender_mark'] == 'Fem_mark'):
        return 'Protot'
    elif (row['Noun_gen'] == 'Fem' and row['Gender_mark'] == 'Masc_mark'):
        return 'No_protot'
    #elif (row['Noun_gen'] == 'Fem' and row['Gender_mark'] == 'No_mark'):
     #   return 'Amb'
    if (row['Noun_gen'] == 'Masc' and row['Gender_mark'] == 'Masc_mark'):
        return 'Protot'
    elif (row['Noun_gen'] == 'Masc' and row['Gender_mark'] == 'Fem_mark'):
        return 'No_protot'
    elif (row['Noun_gen'] == 'Masc' and row['Gender_mark'] == 'No_mark') or (row['Noun_gen'] == 'Fem' and row['Gender_mark'] == 'No_mark'):
        return 'Amb'
    else:
        return None
    

ruta_excel = 'Noun_phrases_Borealis4.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
df = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(df.head())

# Aplicar la función a cada fila del DataFrame y guardar el resultado en una nueva columna
#df['Explain_gender_assignment'] = df.apply(explain_gender_assignment, axis=1)

# Aplicar la función a cada fila del DataFrame y guardar el resultado en una nueva columna
#df['Category_type'] = df.apply(category_type, axis=1)

# Aplicar la función a cada fila del DataFrame y guardar el resultado en una nueva columna
#df['Category_Type'] = df.apply(category_Type, axis=1)

# Aplicar la función a cada fila del DataFrame y guardar el resultado en una nueva columna
df['Gender_mark'] = df.apply(gender_mark, axis=1)
df['Protot_mark'] = df.apply(protot_mark, axis=1)


# Mostrar el DataFrame resultante
print(df)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis4.xlsx'
df.to_excel(ruta_excel_salida, index=False)


valores_unicos2 = df['Gender_mark'].unique()
print(valores_unicos2)

valores_unicos1 = df['Noun_gen'].unique()
print(valores_unicos1)

valores_unicos1 = df['Protot_mark'].unique()
print(valores_unicos1)

