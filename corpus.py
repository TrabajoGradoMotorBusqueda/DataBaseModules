import re
from nltk.corpus import stopwords
from models import StopWord
from db import session


if session.query(StopWord).count() == 0:
    stopwords_español = stopwords.words('spanish')
    stopwords_list = [StopWord(word) for word in stopwords_español]
    session.add_all(stopwords_list)
    session.commit()

stopwords = [word.palabra for word in session.query(StopWord).all()]
columns = ['palabra', 'facultad', 'programa', 'grupo', 'linea']
data = {}


def clean_text(text):
    """Make text lowercase,
    remove text in square brackets,
    remove punctuation and remove words
    containing numbers."""

    text = text.lower()
    text = re.sub(r'\d', '', text)
    text = re.sub(r'\.', '', text)
    pattern = re.compile(r"""                  # Flag para iniciar el modo verbose
              #(?:[A-Za-z]\.|\'|[A-Za-z])+     # Hace match con abreviaciones como U.S.A. o Nombre's
              #(?:[A-Za-z]\.)+                 # Hace match con abreviaciones como U.S.A.        
               \w+(?:\w+)*                     # Hace match con palabras completas
              # | \w+(?:-\w+)*                 # Hace match con palabras que pueden tener un guión interno
              # \$?\d+(?:\.\d+)?%?             # Hace match con dinero o porcentajes como $15.5 o 100%
              # \.\.\.                         # Hace match con puntos suspensivos
              # [][.,;"'?():-_`]               # Hace match con signos de puntuación
              """, re.X)

    resultado = pattern.findall(text)  # Encuentra las ocurrencias y las retorna como lista
    return resultado


def filtered_columns(column):
    regex = re.compile(column)
    filtered = list(filter(regex.match, data.keys()))
    values = []
    for item in filtered:
        value = data[item]
        if value is not None:
            values.append(value)

    return set(values)


def corpus_original(campos):
    def wrapper(*args, **kargs):
        # Obtenemos los Valores de la Fila
        valores = campos(*args, **kargs)
        global data
        data = valores

        titulo = data['titulo_investigacion']
        resumen = data['resumen_investigacion']
        palabras_clave = filtered_columns(columns[0])
        facultad = filtered_columns(columns[1])
        programa = filtered_columns(columns[2])
        grupo_investigacion = filtered_columns(columns[3])
        linea_investigacion = filtered_columns(columns[4])
        tipo_convocatoria = data['tipo_convocatoria']

        corpus = \
            titulo + " " + \
            resumen + " " + \
            " ".join(palabras_clave) + " " + \
            " ".join(facultad) + " " + \
            " ".join(programa) + " " + \
            " ".join(grupo_investigacion) + " " + \
            " ".join(linea_investigacion) + " " + \
            tipo_convocatoria

        return corpus
    return wrapper


def limpieza_corpus(corpus_inicial):
    def wrapper(*args, **kwargs):
        corpus = corpus_inicial(*args, **kwargs)
        palabras_limpias = clean_text(corpus)
        palabras_limpias = [palabra for palabra in palabras_limpias
                            if palabra not in stopwords and len(palabra) > 2]

        corpus_limpio = ' '.join(palabras_limpias)
        return corpus, corpus_limpio
    return wrapper


@limpieza_corpus
@corpus_original
def construccion_corpus(**campos):
    return campos
