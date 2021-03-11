from math import isnan as nan
import db
from models import ResumenesInvestigacion
from limpieza_datos import resumenes_estudiantes, resumenes_docentes, estructura_dataset

docentes = estructura_dataset(resumenes_docentes)
estudiantes = estructura_dataset(resumenes_estudiantes)


def run():
    datos = docentes.iloc[0]
    cols = docentes.columns
    test = {}
    for i, col in enumerate(cols):
        try:
            value = int(datos[i]) if not nan(datos[i]) else None
        except:
            value = datos[i]

        test[col] = value

    test_class = ResumenesInvestigacion(test)
    db.session.add(test_class)
    db.session.commit()
    print('Hola')



if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    run()
