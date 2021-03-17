# Importar spacy para lemmatizar palabras
from spacy import load as loadspacymodel
import os
import difflib

try:
    nlp = loadspacymodel('es_core_news_sm')
except:
    os.system("python -m spacy download es_core_news_sm")
    nlp = loadspacymodel('es_core_news_sm')

# Diccionario lemas y palabras derivadas
# Key: Lema
# Value: Las Palabras Originales
diccionario_lemas = dict()


def lemmatizer(text):
    # Remover tildes y dialisis
    normalizar = str.maketrans('áéíóúüàèìòù', 'aeiouuaeiou')

    lemas = ''  # corpus transformado a lemas

    doc = nlp(text)  # Usamos el modelo de Spacy e identificamos Lemas

    for word in doc:

        # Lematizar si es VERBO
        if word.pos_ == "VERB":
            cleaned_lema = word.lemma_.translate(normalizar).lower()  # Lema Limpio
            cleaned_word = word.text.translate(normalizar).lower()  # Letra Original limpia
        # Si no es verbo dejamos la palabra original
        else:
            cleaned_lema = word.text.translate(normalizar).lower()  # lema limpio
            cleaned_word = cleaned_lema  # letra original limpia

        # Agreamos el corpus de lemas original
        #     lemas = lemas + ' ' + cleaned_lema

        # Obtenemos Lista de palabras asociadas al lema
        list_words = diccionario_lemas.get(cleaned_lema)

        if list_words is None:
            # Palabras Similares al lema encontrado
            similar_word = difflib.get_close_matches(cleaned_lema, diccionario_lemas.keys(), n=1, cutoff=0.94)
            # Si hay un lema ya registrado tomamos esa base
            cleaned_lema = similar_word[0] if len(similar_word) > 0 else cleaned_lema
            # Agregamos palabra original y lema
            if cleaned_lema == cleaned_word:
                diccionario_lemas[cleaned_lema] = [cleaned_word]  # Palabra original no se lematizo
            else:
                diccionario_lemas[cleaned_lema] = [cleaned_word, cleaned_lema]  # Palabra lematizada y su original
        else:
            # Revisamos si es una nueva palabra
            if cleaned_word not in list_words:
                diccionario_lemas[cleaned_lema].append(cleaned_word)  # Agregamos nueva palabra original

        # Agreamos el corpus de lemas que servirá para el entranamiento e instancias
        lemas = lemas + ' ' + cleaned_lema  # table -> corpus_lemas

    # Retornamos Corpus de Lemas
    return lemas


def lematizar_corpus(corpus):
    lemas_corpus = lemmatizer(corpus)
    # vocabulario = set(lemas_corpus)
    return lemas_corpus
