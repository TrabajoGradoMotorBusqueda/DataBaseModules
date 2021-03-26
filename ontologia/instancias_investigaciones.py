import re

from db import session
from models import ResumenesInvestigacion
import instancias as onto

columns = ['palabra', 'codigo', 'nombres', 'apellidos', 'programa', 'facultad', 'departamento', 'grupo', 'linea',
           'asesores']


def filtered_columns(column, investigacion, data):
    regex = re.compile(column)
    filtered = list(filter(regex.match, data))
    values = []
    for item in filtered:
        value = getattr(investigacion, item)
        if value is not None:
            values.append(value)

    return values


def atributos_instacia(investigacion, estudiante):
    atributos = dict()
    data = dir(investigacion)
    atributos['titulo'] = investigacion.titulo_investigacion
    atributos['resumen'] = investigacion.resumen_investigacion
    atributos['palabras_clave'] = filtered_columns(columns[0], investigacion, data)
    atributos['convocatoria'] = investigacion.convocatoria
    atributos['tipo_convocatoria'] = investigacion.tipo_convocatoria
    atributos['anio_convocatoria'] = investigacion.anio_convocatoria
    atributos['codigos'] = filtered_columns(columns[1], investigacion, data)
    atributos['nombres'] = filtered_columns(columns[2], investigacion, data)
    atributos['apellidos'] = filtered_columns(columns[3], investigacion, data)
    atributos['programa'] = filtered_columns(columns[4], investigacion, data)
    atributos['facultad'] = filtered_columns(columns[5], investigacion, data)
    atributos['departamento'] = filtered_columns(columns[6], investigacion, data)
    atributos['grupo_investigacion'] = filtered_columns(columns[7], investigacion, data)
    atributos['linea_investigacion'] = filtered_columns(columns[8], investigacion, data)
    if estudiante:
        atributos['asesor'] = filtered_columns(columns[9], investigacion, data)

    return atributos


class InvestigacionOntologia:
    """
    Clase Investigacion Ontologia
    donde será la clase padre para las instacias en la ontologia
    """
    investigacion = None
    investigacion_ontologia = []
    grupo_investigacion = []
    linea_investigacion = []
    convocatoria = []
    viis = []
    universidad = []
    facultad = []
    departamento = []
    programa = []

    def __init__(self, investigacion):
        self.investigacion = investigacion


class InvestigacionDocente(InvestigacionOntologia):
    """
    Clase Investigacion Docente que hereda de InvestigacionOntologia
    para realizar instancias referentes a los docentes.
    """
    docentes = []
    investigador_externo = []

    def __init__(self, investigacion_docente):
        super().__init__(investigacion_docente)

    def instanciar_investigacion(self):
        diccionario_atributos = atributos_instacia(self.investigacion, False)
        grupo_investigacion = []
        linea_investigacion = []

        for i in range(len(diccionario_atributos['codigos'])):
            # Instanciar Docente
            codigo = diccionario_atributos['codigo'][i]
            nombre = diccionario_atributos['nombres'][i]
            apellidos = diccionario_atributos['apellidos'][i]
            docente = onto.instanciar_docente(codigo, nombre, apellidos)

            # Instanciar Programa
            id_programa = self.investigacion.id
            nombre_programa = diccionario_atributos['programa'][i]
            programa = onto.instanciar_programa(id_programa, nombre_programa)

            # Instanciar Facultad
            id_facultad = self.investigacion.id
            nombre_facultad = diccionario_atributos['facultad'][i]
            facultad = onto.instanciar_facultad(id_facultad, nombre_facultad)

            # Instanciar Grupo Investigacion
            id_grupo = self.investigacion.id
            nombre_grupo = diccionario_atributos['grupo_investigacion'][i]
            grupo = onto.instanciar_gi(id_grupo, nombre_grupo)
            grupo_investigacion.append(grupo)

            # Instanciar linea invesitigacion
            id_linea = self.investigacion.id
            nombre_linea = diccionario_atributos['linea_investigacion'][i]
            linea = onto.instanciar_gi(id_linea, nombre_linea)
            linea_investigacion.append(linea)

            # TODO: Tomar id para programa, facultad, grupo, linea de la clase padre.

class InvestigacionEstudiante(InvestigacionOntologia):
    """
    Clase Investigacion Docente que hereda de InvestigacionOntologia
    para realizar instancias referentes a los estudiantes.
    """
    estudiante = []

    def __init__(self, investigacion_estudiante):
        super().__init__(investigacion_estudiante)


class Investigacion(object):
    investigaciones = session.query(ResumenesInvestigacion).all()
    investigaciones = sorted(investigaciones, key=lambda item: item.id)

    def __iter__(self):
        for investigacion in self.investigaciones:
            yield investigacion


class Instanciar:
    investigaciones = None

    def __init__(self, investigaciones):
        self.investigaciones = investigaciones

    def instaciar_investigaciones(self):
        for investigacion in self.investigaciones:
            if investigacion.tipo_resumen == 'docentes':
                investigacion_docente = InvestigacionDocente(investigacion)
                investigacion_docente.instanciar_investigacion()
            else:
                investigacion_estudiante = InvestigacionEstudiante(investigacion)


if __name__ == '__main__':
    instacias = Instanciar(Investigacion())
    instacias.instaciar_investigaciones()
