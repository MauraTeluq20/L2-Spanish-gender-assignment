# -*- coding: utf-8 -*-
"""
Created on Sat May 10 16:58:43 2025

@author: mcruzen
"""

import spacy
import pandas as pd

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')

def comparare_L2_L1 (col1, col2):
    if (col1 in ["Fem", "Masc"]) and (col2 in ["Fem", "Masc"]):
        if col1 == col2:
            return "same" 
        else: 
            return "different"
    else: 
        if (col2 in ["Both"]):
            return "both"
        else:
            return "NA"


# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis4.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
df = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(df.head())


# Aplicar la función a la columna 'Det_gen' y 'Noun_gen'
df['Compare_L2_L1'] = df.apply(lambda row: comparare_L2_L1(row.get('Noun_gen'), row.get('Noun_fr_gen')), axis=1)
print(df.head())




# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis4.xlsx'
df.to_excel(ruta_excel_salida, index=False)
