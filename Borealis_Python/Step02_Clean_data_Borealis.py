# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:50:51 2024

@author: Maura
"""

import pandas as pd

import spacy
# Cargar el modelo de SpaCy para español
nlp = spacy.load('es_core_news_sm')

import nltk
from nltk.tokenize import word_tokenize
import string

# Descargar el conjunto de palabras de parada (stopwords) de NLTK
nltk.download('stopwords')
nltk.download('punkt')

# Obtener las palabras de parada y los signos de puntuación
stop_words = set(nltk.corpus.stopwords.words('spanish'))
punctuation = set(string.punctuation)

# Supongamos que tienes un DataFrame llamado df con una columna 'Noun phrases'

# Función para limpiar una frase nominal de signos de puntuación
def limpiar_frase_nominal(frase_nominal):
    palabras = word_tokenize(frase_nominal)
    palabras_filtradas = [palabra.lower() for palabra in palabras if palabra.lower() not in punctuation]
    return ' '.join(palabras_filtradas)

# Ruta al archivo Excel

ruta_excel = 'Noun_phrases_Borealis1.xlsx'
# Leer el archivo Excel y cargar la hoja de interés en un DataFrame
dfnpg = pd.read_excel(ruta_excel)  # Reemplaza 'Nombre_de_la_Hoja' con el nombre real de tu hoja
# Imprimir las primeras filas del DataFrame
print(dfnpg.head())

# Aplicar la función a la columna 'Noun phrases' del DataFrame
dfnpg['Noun phrases'] = dfnpg['Noun phrases'].apply(limpiar_frase_nominal)

# Escribir el DataFrame en un archivo Excel
ruta_excel_salida = 'Noun_phrases_Borealis2.xlsx'
dfnpg.to_excel(ruta_excel_salida, index=False)