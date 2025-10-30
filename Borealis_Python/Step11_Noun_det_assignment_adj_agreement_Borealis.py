# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 09:46:43 2024

@author: Maura
"""

import spacy
import pandas as pd

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')

def comparar_genero(col1, col2):
    if (col1 in ["Fem", "Masc"]) and (col2 in ["Fem", "Masc"]):
        if col1 == col2:
            return "correct" 
        else: 
            return "error"
    else:
        return "NA"


# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis4.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
df = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(df.head())


# Aplicar la función a la columna 'Det_gen' y 'Noun_gen'
df['Noun_det_assignment'] = df.apply(lambda row: comparar_genero(row.get('Det_gen'), row.get('Noun_gen')), axis=1)
print(df.head())


# Aplicar la función a la columna 'Adj_gen' y 'Noun_gen'
df['Noun_adj_agreement'] = df.apply(lambda row: comparar_genero(row.get('Adj_gen'), row.get('Noun_gen')), axis=1)
print(df.head())

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis4.xlsx'
df.to_excel(ruta_excel_salida, index=False)
