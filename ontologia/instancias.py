from db import session
from ontologia import *
from models import ResumenesInvestigacion

columns = ['palabra', 'codigo', 'nombres', 'apellidos', 'programa', 'facultad', 'departamento', 'grupo', 'linea',
           'asesores']


def normalizar_nombre(strblanks):
    strunderscore = strblanks.replace(' ', '_')
    return strunderscore.lower()


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


def instanciar_pi(id_proyecto_investigacion, titulo, resumen, palabras_clave, tipo, estado):
    pi = Proyecto_investigacion(normalizar_nombre(titulo))
    pi.set_id_proyecto_investigacion(id_proyecto_investigacion)
    pi.set_titulo_proyecto_investigacion(titulo)
    pi.set_resumen_proyecto_investigacion(resumen)
    pi.set_palabras_clave(palabras_clave)
    pi.set_tipo_proyecto_investigacion(tipo)
    pi.set_estado_proyecto_investigacion(estado)

    return pi


def instanciar_gi(id_grupo_investigacion, nombre_grupo_investigacion):
    # Ojo recibe de parametro Thing
    gi = Grupo_investigacion(normalizar_nombre(nombre_grupo_investigacion))
    gi.set_id_grupo_investigacion(id_grupo_investigacion)
    gi.set_nombre_grupo_investigacion(nombre_grupo_investigacion)
    #     gi.set_clasificacion_grupo_investigacion(clasificacion_grupo_investigacion)
    #     gi.set_area_grupo_investigacion(area_grupo_investigacion)
    #     gi.set_correo_grupo_investigacion(correo_grupo_investigacion)
    return gi


def instanciar_li(id_linea_investigacion, nombre_linea_investigacion):
    # Ojo recibe de parametro Grupo-_investigacion
    li = Linea_investigacion(normalizar_nombre(nombre_linea_investigacion))
    li.set_id_linea_investigacion(id_linea_investigacion)
    li.set_nombre_linea_investigacion(nombre_linea_investigacion)

    return li


def instanciar_convocatoria(id_convocatoria, nombre_convocatoria, tipo, anio):
    # Ojo recibe de parametro VIIS
    convocatoria = Convocatoria(normalizar_nombre(nombre_convocatoria))
    convocatoria.set_id_convocatoria(id_convocatoria)
    convocatoria.set_nombre_convocatoria(nombre_convocatoria)
    convocatoria.set_tipo_convocatoria(tipo)
    convocatoria.set_anio_convocatoria(anio)
    return convocatoria


def instanciar_viis(id_viis, nombre_viis):
    # Ojo recibe de parametro Thing
    viis = VIIS(normalizar_nombre(nombre_viis))
    viis.set_id_VIIS(id_viis)
    viis.set_nombre_VIIS(nombre_viis)

    return viis


def instanciar_universidad(id_universidad, nombre_universidad):
    # Ojo recibe de parametro Thing
    universidad = Universidad(normalizar_nombre(nombre_universidad))
    universidad.set_id_universidad(id_universidad)
    universidad.set_nombre_universidad(nombre_universidad)

    return universidad


def instanciar_facultad(id_facultad, nombre_facultad):
    # Ojo recibe de parametro universidad
    facultad = Facultad(normalizar_nombre(nombre_facultad))
    facultad.set_id_facultad(id_facultad)
    facultad.set_nombre_facultad(nombre_facultad)
    return facultad


def instanciar_departamento(id_departamento, nombre_departamento):  # resumenes decentes no tiene el Depto

    # Ojo recibe de parametro facultad
    departamento = Departamento(normalizar_nombre(nombre_departamento))
    departamento.set_id_departamento(id_departamento)
    departamento.set_nombre_departamento(nombre_departamento)
    return departamento


def instanciar_programa(id_programa, nombre_programa):
    # Parametro para Departamento
    programa = Programa(nombre_programa)
    programa.set_id_programa(id_programa)
    programa.set_nombre_programa(nombre_programa)
    return programa


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


def instanciar_docente(id_docente, nombre_docente, apellidos):
    # Ojo recibe de parametro Investigador
    docente = Docente(normalizar_nombre(nombre_docente))
    docente.set_id_docente(id_docente)
    docente.set_nombres_investigador(nombre_docente)
    docente.set_apellidos_investigador(apellidos)

    #     docente.set_id_investigador()
    #     docente.set_codigo_investigador
    #     docente.set_cedula_investigador()
    #     docente.set_correo_investigador()
    return docente


def instanciar_ie(id_investigador_externo, nombre_investigador_externo):
    # Ojo recibe de parametro Investigador
    ie = Investigador_externo(normalizar_nombre(nombre_investigador_externo))
    ie.set_id_investigador_externo(id_investigador_externo)
    ie.set_nombres_investigador(nombre_investigador_externo)

    #     ie.set_id_investigador()
    #     ie.set_codigo_investigador
    #     ie.set_cedula_investigador()
    #     ie.set_correo_investigador()
    return ie


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
        atributos_instacia(self.investigacion, False)


def instanciar_estudiante(id_estudiante, nombre_estudiante, apellidos):
    # Recibe de parametro Investigador
    estudiante = Estudiante(nombre_estudiante)  # Iniciamos el Objeto
    estudiante.set_id_estudiante(id_estudiante)
    estudiante.set_nombres_investigador(nombre_estudiante)
    estudiante.set_apellidos_investigador(apellidos)
    # estudiante.set_id_investigador()
    # estudiante.set_codigo_investigador
    # estudiante.set_cedula_investigador()
    # estudiante.set_correo_investigador()
    return estudiante


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
