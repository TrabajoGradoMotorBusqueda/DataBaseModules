import re

from db import session
from models import Investigacion
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


class UniversidadOntologia:

    def __init__(self, nombre_universidad, nombre_viis):
        universidad = onto.ontologia.search_one(iri=f"*{nombre_universidad}")
        if universidad is None:
            id_universidad = len(onto.ontologia.Universidad.instances()) + 1
            universidad = onto.instanciar_universidad(id_universidad, nombre_universidad)
            self.universidad = universidad
        else:
            self.universidad = universidad

        viis = onto.ontologia.search_one(iri=f"*{nombre_viis}")
        if viis is None:
            id_viis = len(onto.ontologia.VIIS.instances()) + 1
            viis = onto.instanciar_universidad(id_viis, nombre_viis)
            self.viis = viis
        else:
            self.viis = viis


class InvestigacionOntologia:
    """
    Clase Investigacion Ontologia
    donde será la clase padre para las instacias en la ontologia
    """

    def __init__(self, investigacion, universidad_ontologia):
        self.investigacion = investigacion
        self.universidad = universidad_ontologia.universidad
        self.viis = universidad_ontologia.viis
        # Instancias Adicionales Ontologia
        self.investigacion_ontologia = None
        self.grupos_investigacion = []
        self.lineas_investigacion = []
        self.convocatoria = None
        self.facultades = []
        self.departamentos = []
        self.programas = []

    # TODO: Mthods para relacionar grupos, facultad con universidad


class InvestigacionDocente(InvestigacionOntologia):
    """
    Clase Investigacion Docente que hereda de InvestigacionOntologia
    para realizar instancias referentes a los docentes.
    """

    def __init__(self, investigacion_docente, universidad_ontologia):
        super().__init__(investigacion_docente, universidad_ontologia)
        self.docentes = []
        self.investigador_externo = []

    def instanciar(self):
        diccionario_atributos = atributos_instacia(self.investigacion, False)

        for i in range(len(diccionario_atributos['codigos'])):
            # Instanciar Docente
            codigo = diccionario_atributos['codigo'][i]
            nombre = diccionario_atributos['nombres'][i]
            apellidos = diccionario_atributos['apellidos'][i]
            docente = onto.instanciar_docente(codigo, nombre, apellidos)
            self.docentes = [docente]

            # Instanciar Programa
            nombre_programa = diccionario_atributos[columns[4]][i]

            programa = onto.definir_id(nombre_programa, columns[4])
            id_programa = programa if isinstance(programa, int) else None

            programa_instancia = onto.instanciar_programa(id_programa,
                                                          nombre_programa) if id_programa is not None else programa
            self.programas.append(programa_instancia)

            # Instanciar Facultad
            nombre_facultad = diccionario_atributos[columns[5]][i]

            facultad = onto.definir_id(nombre_facultad, columns[5])

            facultad_instancia = facultad if not isinstance(programa, int) else \
                onto.instanciar_facultad(facultad, nombre_facultad)

            self.facultades.append(facultad_instancia)

            # Instanciar Grupo Investigacion
            nombre_grupo = diccionario_atributos[columns[7]][i]
            grupo = onto.definir_id(nombre_grupo, columns[7])

            grupo_instancia = grupo if not isinstance(grupo, int) else \
                onto.instanciar_gi(grupo, nombre_grupo)
            self.grupos_investigacion.append(grupo_instancia)

            # Instanciar linea investigacion
            nombre_linea = diccionario_atributos[columns[8]][i]
            linea = onto.definir_id(nombre_linea)
            linea_instancia = linea if not isinstance(linea, int) else \
                onto.instanciar_gi(linea, nombre_linea)
            self.lineas_investigacion.append(linea_instancia)

            # De esta manera podemos agregar igualmente para Departamento
            # En las instancias de estudiantes se encuentra el ejemplo


class InvestigacionEstudiante(InvestigacionOntologia):
    """
    Clase Investigacion Docente que hereda de InvestigacionOntologia
    para realizar instancias referentes a los estudiantes.
    """
    estudiante = []

    def __init__(self, investigacion_estudiante):
        super().__init__(investigacion_estudiante)


class Investigaciones(object):
    investigaciones = session.query(Investigacion).all()
    investigaciones = sorted(investigaciones, key=lambda item: item.id)

    def __iter__(self):
        for investigacion in self.investigaciones:
            yield investigacion


class Instanciar:

    def __init__(self, investigaciones, nombre_universidad, nombre_viis):
        self.investigaciones = investigaciones
        self.universidad_ontologia = UniversidadOntologia(nombre_universidad, nombre_viis)

    def instaciar_investigaciones(self):
        for investigacion in self.investigaciones:
            if investigacion.tipo_resumen == 'docentes':
                investigacion_docente = InvestigacionDocente(investigacion, self.universidad_ontologia)
                investigacion_docente.instanciar()
            else:
                investigacion_estudiante = InvestigacionEstudiante(investigacion)


if __name__ == '__main__':
    instacias = Instanciar(Investigacion(), "Universidad de Nariño", "Vicerrectoría de Investigación e Interacción "
                                                                     "Social")
    instacias.instaciar_investigaciones()
