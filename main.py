# Python Natives
from math import isnan as nan
import time

# Modulos DB
import db
from models import Investigacion, DiccionarioLema

db.Base.metadata.create_all(db.engine)  # Creacion de Tablas

# Modulos Procesamiento de Texto
from corpus import construccion_corpus
from lemas import lematizar_corpus, diccionario_lemas
from estructura_datos import resumenes_estudiantes, resumenes_docentes, estructura_dataset
from query import query_id_investigacion

docentes = estructura_dataset(resumenes_docentes)
estudiantes = estructura_dataset(resumenes_estudiantes)


def add_data():
    columns = docentes
    resumenes = []

    # Resumenes Docentes Agregando Data a la BD
    for index, resumen in docentes.iterrows():
        data = {}
        for column in columns:
            try:
                value = int(resumen[column]) if not nan(resumen[column]) else None
            except:
                value = resumen[column]
            data[column] = value
        data['tipo_resumen'] = 'docentes'
        investigacion = Investigacion(data)  # Creamos el Objeto
        resumenes.append(investigacion)
    # db.session.add(investigacion)  # Agregamos a la session

    # del docentes
    # del resumenes_docentes

    # Resumenes Estudiantes Agregando Data a la BD
    for index, resumen in estudiantes.iterrows():
        data = {}
        for column in columns:
            try:
                value = int(resumen[column]) if not nan(resumen[column]) else None
            except:
                value = resumen[column]
            data[column] = value
        data['tipo_resumen'] = 'estudiantes'

        investigacion = Investigacion(data)  # Creamos el Objeto
        resumenes.append(investigacion)
        # db.session.add(investigacion)

    # del estudiantes
    # del resumenes_estudiantes

    db.session.add_all(resumenes)
    db.session.commit()  # Realizamos la operacion atomica
    # del resumenes
    print('Base de datos con Resumenes')


def build_corpus():
    investigaciones = tuple(db.session.query(Investigacion).all())
    for investigacion in investigaciones:
        corpus, corpus_limpio = construccion_corpus(**vars(investigacion))
        corpus_lemas = lematizar_corpus(corpus_limpio)
        investigacion.corpus = corpus
        investigacion.corpus_palabras = corpus_limpio
        investigacion.corpus_lemas = corpus_lemas
        print('Investigacion: ' + str(investigacion.id) + ' Completo')

    db.session.flush()
    db.session.commit()

    print('Corpus Añadidos !')


def build_vocabulary():
    vocabulario = []
    if db.session.query(DiccionarioLema).count() == 0:
        for key, value in diccionario_lemas.items():
            vocabulario.append(DiccionarioLema(key, value))

        db.session.add_all(vocabulario)
        db.session.commit()


if __name__ == '__main__':
    start = time.time()
    add_data()  # Agregar Datos
    del resumenes_docentes, docentes
    del resumenes_estudiantes, estudiantes
    build_corpus()  # Construir Corpus
    build_vocabulary()  # Añadir Vocabulario
    end = time.time()
    minutes, seconds = divmod(end - start, 60)
    print(f'Minutos: {minutes} - Segundos: {seconds}')
