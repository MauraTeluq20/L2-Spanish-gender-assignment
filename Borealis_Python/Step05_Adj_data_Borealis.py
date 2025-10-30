# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 09:38:05 2024

@author: Maura
"""
import spacy
import pandas as pd

# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')


# Función para obtener sustantivo
def obtener_adj(a):
    doc = nlp(a)
    for token in doc:
        if token.pos_ == "ADJ":
            return token.text
    return None




def obtener_genero_adj(a):
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


# Aplicar la función obtener_det a la columna 'Noun phrases' y crear una nueva columna 'Noun'
dfnpg['Adj'] = dfnpg['Noun_phrases'].apply(obtener_adj)

print(dfnpg)



# Aplicar la función obtener_genero_sustantivo a la columna 'Noun' y crear una nueva columna 'Noun_Gen'
dfnpg['Adj_gen'] = dfnpg['Adj'].apply(obtener_genero_adj)


# Imprimir el DataFrame resultante
print(dfnpg)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis4.xlsx'
dfnpg.to_excel(ruta_excel_salida, index=False)

