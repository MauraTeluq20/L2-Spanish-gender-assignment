# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:59:54 2025

@author: mcruzen
"""




import pandas as pd

# Leer el archivo
ruta_excel = 'Noun_phrases_Borealis4.xlsx'
df = pd.read_excel(ruta_excel)

# Nueva lista para guardar las filas procesadas
nuevas_filas = []

def analizar_np(estructura, original_row):
    if not isinstance(estructura, str):
        return original_row

    elementos = estructura.split(' + ')
    adj_indices = [i for i, x in enumerate(elementos) if x == 'ADJ']
    noun_indices = [i for i, x in enumerate(elementos) if x == 'NOUN']

    fila = original_row.copy()
    fila['Multiple'] = ''
    fila['Pre_noun'] = ''
    fila['Adj_Noun_Distance'] = None

    # Marcar si hay ADJ antes de NOUN
    if adj_indices and noun_indices and min(adj_indices) < min(noun_indices):
        fila['Pre_noun'] = 'YES'
        #print("El min adj indices es: ", min(adj_indices))
        #print("El min noun indices es: ", min(noun_indices))
    # Casos múltiples
    if len(adj_indices) > 1:
        #print("El len adj indices es: ", len(adj_indices))
        if len(noun_indices) == 1:
            fila['Multiple'] = 'Multiple'
        elif len(noun_indices) > 1:
            fila['Multiple'] = 'Complejo'
        nuevas_filas.append(fila)  # Añadir versión duplicada
    elif len(adj_indices) == 1 and len(noun_indices) == 1:# Aquí debería quitar lo del len noun...
        # Calcular distancia solo si hay una pareja ADJ-NOUN
        fila['Adj_Noun_Distance'] = abs(adj_indices[0] - noun_indices[0]) - 1

    return fila

# Procesar cada fila
for _, row in df.iterrows():
    estructura = row['Estructura_NP_POS']
    nueva_fila = analizar_np(estructura, row)
    nuevas_filas.append(nueva_fila)

# Crear el nuevo DataFrame
df_resultado = pd.DataFrame(nuevas_filas)

# Mostrar para verificar
print(df_resultado[['Estructura_NP_POS', 'Adj_Noun_Distance', 'Multiple', 'Pre_noun']].head())

# (Opcional) Guardar a Excel
df_resultado.to_excel('Noun_phrases_Borealis4.xlsx', index=False)
