# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:49:46 2024

@author: Maura
"""

import spacy
import pandas as pd

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')


# Función para obtener sustantivo
def obtener_det(a):
    doc = nlp(a)
    for token in doc:
        if token.pos_ == "DET":
            return token.text
    return None




def obtener_genero_det(a):
    if isinstance(a, str):
        doc = nlp(a)
        for token in doc :
            if token.morph.get("Gender"):
           # if token.pos_ == "DET":
                return token.morph.get("Gender")[0]
        return None  # Si no se encuentra un sustantivo en el NP

# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis3.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
dfnpg = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(dfnpg.head())


# Aplicar la función obtener_det a la columna 'Noun phrases' y crear una nueva columna 'Det'
dfnpg['Det'] = dfnpg['Noun_phrases'].apply(obtener_det)

print(dfnpg)


# Aplicar la función obtener_genero_sustantivo a la columna 'Noun' y crear una nueva columna 'Det_Gen'
dfnpg['Det_gen'] = dfnpg['Det'].apply(obtener_genero_det)


# Imprimir el DataFrame resultante
print(dfnpg)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis3.xlsx'
dfnpg.to_excel(ruta_excel_salida, index=False)
