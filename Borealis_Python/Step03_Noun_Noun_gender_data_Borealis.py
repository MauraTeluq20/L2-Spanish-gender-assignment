# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:49:17 2024

@author: Maura
"""

import spacy
import pandas as pd

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')


# Función para obtener sustantivo
def obtener_noun(a):
    doc = nlp(a)
    for token in doc:
        if token.pos_ == "NOUN":
            return token
    return None

def obtener_genero_sustantivo(a):
    if isinstance(a, str):
        doc = nlp(a)
        for token in doc :
            if token.morph.get("Gender"):
           # if token.pos_ == "NOUN":
                return token.morph.get("Gender")[0]
        return None  # Si no se encuentra un sustantivo en el NP
    
# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis2.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
dfnpg = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(dfnpg.head())


# Aplicar la función obtener_noun a la columna 'Noun phrases' y crear una nueva columna 'Noun'
dfnpg['Noun'] = dfnpg['Noun_phrases'].apply(obtener_noun)

print(dfnpg)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis2.xlsx'
dfnpg.to_excel(ruta_excel_salida, index=False)

# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis2.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
dfnpg1 = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame para verificar
print(dfnpg1.head())


# Aplicar la función obtener_genero_sustantivo a la columna 'Noun' y crear una nueva columna 'Noun_Gen'
dfnpg1['Noun_gen'] = dfnpg1['Noun'].apply(obtener_genero_sustantivo)


# Imprimir el DataFrame resultante
print(dfnpg1)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis3.xlsx'
dfnpg1.to_excel(ruta_excel_salida, index=False)
