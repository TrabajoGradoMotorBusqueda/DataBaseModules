from math import isnan as nan
import db
from models import ResumenesInvestigacion
from limpieza_datos import resumenes_estudiantes, resumenes_docentes, estructura_dataset

docentes = estructura_dataset(resumenes_docentes)
estudiantes = estructura_dataset(resumenes_estudiantes)


def run():
    columns = docentes.columns

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
        db.session.add(investigacion)  # Agregamos a la session

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
        db.session.add(investigacion)

    db.session.commit()  # Realizamos la operacion atomica
    print('Hola')


if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    run()
