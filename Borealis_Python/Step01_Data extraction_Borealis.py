# -*- coding: utf-8 -*-
"""
Created on Tue May  6 11:33:17 2025

@author: mcruzen
"""

import pandas as pd
import spacy

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')

# Función para extraer NPs de un texto
def extraer_nps(texto):
    if not isinstance(texto, str):  # Asegura que no haya NaN
        return []
    doc = nlp(texto)
    return [np.text for np in doc.noun_chunks]

# Leer archivo Excel
ruta_excel = 'Noun_phrases_Borealis.xlsx'
df = pd.read_excel(ruta_excel)

# Crear una lista de diccionarios con la NP y sus metadatos
filas_expandidas = []
for _, fila in df.iterrows():
    nps = extraer_nps(fila['Texto'])
    for np in nps:
        filas_expandidas.append({
            'Noun_phrases': np,
            'Group': fila['Group'],
            'Subject_ID': fila['Subject_ID'],
            #'Task': fila['Task']
        })

# Crear el nuevo DataFrame
dfnp = pd.DataFrame(filas_expandidas)

# Filtrar las NPs con más de una palabra
dfnpg = dfnp[dfnp['Noun_phrases'].apply(lambda x: len(x.split()) > 1)]

# Guardar el resultado en Excel
ruta_excel_salida = 'Noun_phrases_Borealis.xlsx'
dfnpg.to_excel(ruta_excel_salida, index=False)
