# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 17:03:20 2024
No funciona la traduction con tantos datos. Probar con menos datos.*******
@author: Maura
"""

from googletrans import Translator
import pandas as pd
import spacy


# Cargar el modelo de SpaCy para el francés
nlp_fr = spacy.load('fr_core_news_sm')


def traducir_a_frances(palabra):
    translator = Translator()
    traduccion = translator.translate(palabra, src='es', dest='fr')
    if traduccion is not None:
        return traduccion.text
    else:
        return "No se pudo traducir"   

ruta_excel = 'Noun_phrases_Borealis4.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
df = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
#print(df.head())


# Aplicar la función de traducción a la columna 'Sustantivo'
df['Noun_French'] = df['Noun'].apply(traducir_a_frances)


# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis4.xlsx'
df.to_excel(ruta_excel_salida, index=False)
