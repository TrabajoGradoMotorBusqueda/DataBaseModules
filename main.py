from math import isnan as nan
import db
from corpus import construccion_corpus
from models import ResumenesInvestigacion
from limpieza_datos import resumenes_estudiantes, resumenes_docentes, estructura_dataset
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
        investigacion = ResumenesInvestigacion(data)  # Creamos el Objeto
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

        investigacion = ResumenesInvestigacion(data)  # Creamos el Objeto
        resumenes.append(investigacion)
        # db.session.add(investigacion)

    # del estudiantes
    # del resumenes_estudiantes

    db.session.add_all(resumenes)
    db.session.commit()  # Realizamos la operacion atomica
    print('Hola')


def build_corpus():
    # investigaciones = tuple(db.session.query(ResumenesInvestigacion).all())
    # for investigacion in investigaciones:
    #     corpus = construccion_corpus(vars(investigacion))

    resultado = query_id_investigacion(session=db.session, investigacion=ResumenesInvestigacion, id_value=1)
    investigacion = resultado[0]
    corpus, corpus_limpio = construccion_corpus(**vars(investigacion))

    print(corpus)


if __name__ == '__main__':
    # db.Base.metadata.create_all(db.engine)
    # add_data()
    build_corpus()
