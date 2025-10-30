# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 09:58:31 2025

@author: mcruzen
"""

import pandas as pd
import spacy

# 1. Cargar modelo de spaCy (para español, si tus adjetivos están en español)
nlp = spacy.load("es_core_news_sm")  # o el modelo que uses para español

# 2. Leer archivo Excel
df = pd.read_excel("Noun_phrases_Borealis4.xlsx")

# 3. Suponer que tienes una columna llamada "Adj" con adjetivos
# Crear la nueva columna, inicialmente vacía
df["Noun_lemma"] = None

# 4. Función para lematizar un adjetivo
def lematizar_noun(noun):
    if not isinstance(noun, str):
        return None
    doc = nlp(noun)
    # supondremos que el adjetivo es una “unidad”, tomamos el primer token
    token = doc[0]
    # verificar que spaCy lo haya etiquetado como adjetivo
    if token.pos_ == "NOUN" or token.pos_ == "PROPN":
        return token.lemma_
    else:
        # si no es adjetivo, podemos devolver el texto original o None
        return token.lemma_
    
# 5. Aplicar la función a cada fila
df["Noun_lemma"] = df["Noun"].apply(lematizar_noun)

# 6. Guardar resultado si lo deseas
df.to_excel("Noun_phrases_Borealis4.xlsx", index=False)
