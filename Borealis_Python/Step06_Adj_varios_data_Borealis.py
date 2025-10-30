# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 09:38:05 2024

@author: Maura
"""
import spacy
import pandas as pd

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')


## Función principal para extraer adjetivos y distancias desde un NP y un sustantivo
def obtener_adj_y_dist(np, sustantivo):
    if not isinstance(np, str) or not isinstance(sustantivo, str):
        return {}

    doc = nlp(np)
    adjetivos = []
    distancias = []

    # Buscar índice del sustantivo
    indices_noun = [token.i for token in doc if token.text.lower() == sustantivo.lower()]
    if not indices_noun:
        return {}
    idx_noun = indices_noun[0]

    # Buscar adjetivos y calcular distancia
    for token in doc:
        if token.pos_ == "ADJ":
            adjetivos.append(token.text)
            dist = abs(token.i - idx_noun) - 1
            distancias.append(dist)

    # Crear resultado como diccionario
    resultado = {}
    for i, (adj, dist) in enumerate(zip(adjetivos, distancias), start=1):
        resultado[f'Adj_{i}'] = adj
        resultado[f'Dist_{i}'] = dist
    return resultado


# Aplicar al dataframe
# Supongamos que tu dataframe se llama df y tiene columnas: 'NP' (frase nominal), 'Noun' (sustantivo)
df = pd.read_excel("Noun_phrases_Borealis4.xlsx")

# Aplicar la función fila por fila
datos_expandidos = df.apply(lambda row: pd.Series(obtener_adj_y_dist(row['Noun_Phrase'], row['Noun'])), axis=1)

# Combinar con el dataframe original
df_final = pd.concat([df, datos_expandidos], axis=1)

# Guardar el resultado
df_final.to_excel("Noun_phrases_Borealis4.xlsx", index=False)




"""
# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis4.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
dfnpg = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(dfnpg.head())


# Aplicar la función obtener_det a la columna 'Noun phrases' y crear una nueva columna 'Noun'
dfnpg['Adj'] = dfnpg['Noun_phrases'].apply(obtener_adj)

print(dfnpg)



# Aplicar la función obtener_genero_sustantivo a la columna 'Noun' y crear una nueva columna 'Noun_Gen'
dfnpg['Adj_gen'] = dfnpg['Adj'].apply(obtener_genero_adj)


# Imprimir el DataFrame resultante
print(dfnpg)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis.xlsx'
dfnpg.to_excel(ruta_excel_salida, index=False)

"""