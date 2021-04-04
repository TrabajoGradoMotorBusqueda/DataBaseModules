import re
from abc import abstractmethod, ABC

from db import session
from models import Investigacion, DiccionarioLema
import instancias as onto

columns = ['palabra', 'codigo', 'nombres', 'apellidos', 'programa', 'facultad', 'departamento', 'grupo', 'linea',
           'asesor']


def filtered_columns(column, investigacion, atributos):
    regex = re.compile(column)
    filtered = list(filter(regex.match, atributos))
    values = []
    for item in filtered:
        value = getattr(investigacion, item)
        if value is not None:
            values.append(value)

    return values


def atributos_instancia(investigacion, estudiante):
    atributos = dict()
    data = dir(investigacion)
    atributos['titulo'] = investigacion.titulo_investigacion
    atributos['resumen'] = investigacion.resumen_investigacion
    atributos['estado'] = investigacion.estado_investigacion
    atributos['palabras_clave'] = filtered_columns(columns[0], investigacion, data)
    atributos['tipo_proyecto'] = investigacion.tipo_resumen
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
        universidad = onto.definir_id(nombre_universidad, "Universidad")
        self.universidad = universidad if not isinstance(universidad, int) else \
            onto.instanciar_universidad(universidad, nombre_universidad)

        viis = onto.definir_id(nombre_viis, "VIIS")
        self.viis = viis if not isinstance(viis, int) else \
            onto.instanciar_viis(viis, nombre_viis)


class InvestigacionOntologia:
    """
    Clase Investigacion Ontologia
    donde será la clase padre para las instacias en la ontologia
    """

    def __init__(self, investigacion, universidad_ontologia, tipo):
        self.investigacion = investigacion
        self.universidad = universidad_ontologia.universidad
        self.viis = universidad_ontologia.viis

        # Relation Universidad -> VIIS
        self.universidad.relation_universidad_tiene_viis(self.viis)

        # Instancias Adicionales Ontologia
        self.proyecto_investigacion = None
        self.palabras = []
        self.grupos_investigacion = []
        self.lineas_investigacion = []
        self.convocatoria = None
        self.facultades = []
        self.departamentos = []
        self.programas = []
        # Nuevos
        self.investigadores = []
        self.tipo = tipo

    def relacionar(self, tipo, asesores=None, departamentos=None):
        universidad = self.universidad
        viis = self.viis
        convocatoria = self.convocatoria
        proyecto_investigacion = self.proyecto_investigacion

        # VIIS -> Proyecto
        viis.relation_viis_tiene_pi(proyecto_investigacion)
        # VIIS -> Convocatoria
        viis.relation_viis_tiene_convocatoria(convocatoria)

        # Convocatoria -> Proyecto
        convocatoria.relation_convocatoria_tiene_pi(pi=proyecto_investigacion)

        for grupo in self.grupos_investigacion:

            # VIIS -> Grupo Investigacion
            viis.relation_viis_adscribe_gi(grupo)

            for linea in self.lineas_investigacion:
                # Linea -> Proyecto
                linea.relation_li_tiene_pi(proyecto_investigacion)
                grupo.relation_gi_tiene_li(linea)

            for i, investigador in enumerate(self.investigadores):

                if tipo == "estudiantes":
                    # Investigador -> Estudiante
                    investigador.relation_investigador_es_estudiante(investigador)
                    # Grupo de Investigacion -> Estudiante
                    grupo.relation_gi_tiene_estudiante(investigador)
                else:
                    # Investigador -> Docente
                    investigador.relation_investigador_es_docente(investigador)
                    # Grupo de Investigacion -> Docente
                    grupo.relation_gi_tiene_docente(investigador)

                # Estudiante -> Proyecto
                investigador.relation_estudiante_es_autor_pi(proyecto_investigacion)

                # VIIS -> Investigador
                viis.relation_viis_tiene_investigador(investigador)

                # Convocatoria -> investigador
                convocatoria.relation_convocatoria_dirigida_investigador(investigador)

                if asesor is not None and i < len(self.asesores):
                    asesor = self.asesores[i]
                    # Asesor -> Proyecto
                    asesor.docente_asesora_pi.append(self.proyecto_investigacion)
                    # Grupo -> Asesor
                    grupo.relation_gi_tiene_docente(asesor)
                    # VIIS -> Asesor
                    viis.relation_viis_tiene_investigador(asesor)
                    # Convocatoria -> Asesor
                    convocatoria.relation_convocatoria_dirigida_investigador(asesor)
                else:
                    asesor = None

                # Relacion Programa, Facultad
                if i < len(self.programas):
                    programa = self.programas[i]
                    if tipo == "estudiantes":
                        # Programa -> Estudiante
                        programa.relation_programa_tiene_estudiante(investigador)
                        # Programa -> Docente
                        if asesor is not None:
                            programa.relation_programa_tiene_docente(asesor)
                    else:
                        # Programa -> Docente
                        programa.relation_programa_tiene_docente(investigador)
                else:
                    programa = None

                if departamentos is not None and i < len(self.departamentos):
                    departamento = self.departamentos[i]
                    # Departamento -> Programa
                    if programa is not None:
                        departamento.relation_departamento_tiene_programa(programa)
                    # Departamento -> Grupo de Investigacion
                    departamento.relation_departamento_tiene_gi(grupo)
                else:
                    departamento = None

                if i < len(self.facultades):
                    facultad = self.facultades[i]
                    # Facultad -> Departamento
                    if departamento is not None:
                        facultad.relation_facultad_tiene_departamento(departamento)
                    # Universidad -> Facultad
                    universidad.relation_universidad_tiene_facultad(facultad)

        for palabra in self.palabras:
            self.proyecto_investigacion \
                .relation_pi_tiene_palabra(palabra)


    def instanciar_palabras(self):
        vocabulario = set(self.investigacion.corpus_lemas.split())

        for lema in vocabulario:
            descripciones = session.query(DiccionarioLema.palabras). \
                filter(DiccionarioLema.lema == lema).one_or_none()
            palabra_instancia = onto.instanciar_palabra(lema, descripciones.palabras)
            self.palabras.append(palabra_instancia)

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
        diccionario_atributos = atributos_instancia(self.investigacion, False)
        palabras = []

        titulo = diccionario_atributos['titulo']
        resumen = diccionario_atributos['resumen']
        palabras_clave = diccionario_atributos['palabras_clave']
        tipo = diccionario_atributos['tipo_convocatoria']
        estado = diccionario_atributos['estado']
        id_investigacion = self.investigacion.id

        proyecto_investigacion = onto.instanciar_pi(
            id_investigacion,
            titulo,
            resumen,
            palabras_clave,
            tipo,
            estado
        )

        self.proyecto_investigacion = proyecto_investigacion

        palabra_tipo_convocatoria = [onto.instanciar_palabra(tipo.lower(), [tipo.lower()])]
        palabra_estado = [onto.instanciar_palabra(palabra.lower(), [palabra.lower()])
                          for palabra in estado.split() if len(palabra) > 2]
        palabras.extend(palabra_tipo_convocatoria + palabra_estado)

        for i in range(len(diccionario_atributos['codigos'])):
            # Instanciar Docente
            codigo = diccionario_atributos['codigos'][i]
            nombres = diccionario_atributos['nombres'][i]
            apellidos = diccionario_atributos['apellidos'][i]
            docente = onto.definir_id(nombres + " " + apellidos, "Docente")
            docente_instancia = docente if not isinstance(docente, int) else \
                onto.instanciar_docente(docente, codigo, nombres, apellidos)
            # Relacionar Docente
            self.docentes.append(docente_instancia)

            # Instancias para Palabras
            palabra_nombres = [onto.instanciar_palabra(nombre.lower(), [nombre])
                               for nombre in nombres.split()]
            palabra_apellidos = [onto.instanciar_palabra(apellido.lower(), [apellido.lower()])
                                 for apellido in apellidos.split()]
            palabras.extend(palabra_nombres + palabra_apellidos)

            # Instanciar Programa
            if i < len(diccionario_atributos['programa']):
                nombre_programa = diccionario_atributos['programa'][i]

                programa = onto.definir_id(nombre_programa, 'Programa')
                id_programa = programa if isinstance(programa, int) else None

                programa_instancia = onto.instanciar_programa(id_programa,
                                                              nombre_programa) if id_programa is not None else programa
                self.programas.append(programa_instancia)

            # Instanciar Facultad
            if i < len(diccionario_atributos['facultad']):
                nombre_facultad = diccionario_atributos['facultad'][i]

                facultad = onto.definir_id(nombre_facultad, 'Facultad')

                facultad_instancia = facultad if not isinstance(facultad, int) else \
                    onto.instanciar_facultad(facultad, nombre_facultad)

                self.facultades.append(facultad_instancia)

            # Instanciar Grupo Investigacion
            if i < len(diccionario_atributos['grupo_investigacion']):
                nombre_grupo = diccionario_atributos['grupo_investigacion'][i]
                grupo = onto.definir_id(nombre_grupo, 'Grupo_investigacion')

                grupo_instancia = grupo if not isinstance(grupo, int) else \
                    onto.instanciar_gi(grupo, nombre_grupo)
                self.grupos_investigacion.append(grupo_instancia)

            # Instanciar linea investigacion
            if i < len(diccionario_atributos['linea_investigacion']):
                nombre_linea = diccionario_atributos['linea_investigacion'][i]
                linea = onto.definir_id(nombre_linea, 'Linea_investigacion')
                linea_instancia = linea if not isinstance(linea, int) else \
                    onto.instanciar_li(linea, nombre_linea)
                self.lineas_investigacion.append(linea_instancia)

            # Instanciar Convocatoria
            if i <= 0:
                nombre_convocatoria = diccionario_atributos['convocatoria']
                convocatoria = onto.definir_id(nombre_convocatoria, 'Convocatoria')
                tipo_convocatoria = diccionario_atributos['tipo_convocatoria']
                anio_convocatoria = diccionario_atributos['anio_convocatoria']
                convocatoria_instancia = convocatoria if not isinstance(convocatoria, int) else \
                    onto.instanciar_convocatoria(convocatoria,
                                                 nombre_convocatoria,
                                                 tipo_convocatoria,
                                                 anio_convocatoria)
                self.convocatoria = convocatoria_instancia

                if nombre_convocatoria != "Ninguna":
                    palabra_tipo = [onto.instanciar_palabra(palabra.lower(), [palabra.lower()])
                                    for palabra in tipo_convocatoria.split()]
                    palabra_anio = [onto.instanciar_palabra(str(tipo_convocatoria), [str(tipo_convocatoria)])]
                    palabras.extend(palabra_tipo + palabra_anio)

            # De esta manera podemos agregar igualmente para Departamento
            # En las instancias de estudiantes se encuentra el ejemplo

        # Agregamos Palabras
        self.palabras.extend(palabras)

    def instanciar_palabras(self):
        vocabulario = set(self.investigacion.corpus_lemas.split())

        for lema in vocabulario:
            descripciones = session.query(DiccionarioLema.palabras). \
                filter(DiccionarioLema.lema == lema).one_or_none()
            palabra_instancia = onto.instanciar_palabra(lema, descripciones.palabras)
            self.palabras.append(palabra_instancia)

    def relacionar(self):

        for grupo in self.grupos_investigacion:
            for i, docente in enumerate(self.docentes):
                docente.relation_docente_es_autor_pi(self.proyecto_investigacion)

                # Relacion Programa, Facultad
                if i < len(self.programas):
                    programa = self.programas[i]
                    programa.relation_programa_tiene_docente(docente)
                if i < len(self.facultades):
                    facultad = self.facultades[i]
                    facultad.relation_universidad_tiene_facultad(facultad)

                universidad = self.universidad
                universidad.relation_universidad_tiene_facultad(universidad)
                universidad.relation_universidad_tiene_viis(self.viis)

                # Grupo de Investigacion
                grupo.relation_gi_tiene_docente(docente)

            for linea in self.lineas_investigacion:
                grupo.relation_gi_tiene_li(linea)

        self.convocatoria.relation_convocatoria_tiene_pi(pi=self.proyecto_investigacion)

        for palabra in self.palabras:
            self.proyecto_investigacion \
                .relation_pi_tiene_palabra(palabra)


class InvestigacionEstudiante(InvestigacionOntologia):
    """
    Clase Investigacion Docente que hereda de InvestigacionOntologia
    para realizar instancias referentes a los estudiantes.
    """

    def __init__(self, investigacion_estudiante, universidad_ontologia, tipo):
        super().__init__(investigacion_estudiante, universidad_ontologia, tipo)
        self.estudiantes = []
        self.asesores = []

    def instanciar(self):
        # diccionario_atributos = atributos_instancia(self.investigacion, True)
        atributos = dir(self.investigacion)
        palabras = []

        # Instanciar Proyecto Investigacion
        id_investigacion = self.investigacion.id
        titulo = self.investigacion.titulo_investigacion
        resumen = self.investigacion.resumen_investigacion
        palabras_clave = filtered_columns('palabra', self.investigacion, atributos)
        tipo = self.investigacion.tipo_convocatoria
        estado = self.investigacion.estado_investigacion

        # Instanciar Proyecto en la ontologia
        proyecto_investigacion = onto.instanciar_pi(
            id_investigacion,
            titulo,
            resumen,
            palabras_clave,
            tipo,
            estado
        )

        # Proyecto de investigacion asignado al objeto
        self.proyecto_investigacion = proyecto_investigacion

        # Instancias Palabras ( Tipo Convocatoria, Estado Convocatoria)
        palabra_tipo_convocatoria = [onto.instanciar_palabra(tipo.lower(), [tipo.lower()])]
        palabra_estado = [onto.instanciar_palabra(palabra.lower(), [palabra.lower()])
                          for palabra in estado.split() if len(palabra) > 2]
        palabras.extend(palabra_tipo_convocatoria + palabra_estado)

        # Instanciar Convocatoria
        nombre_convocatoria = self.investigacion.convocatoria
        tipo_convocatoria = self.investigacion.tipo_convocatoria
        anio_convocatoria = self.investigacion.anio_convocatoria

        convocatoria = onto.definir_id(nombre_convocatoria, 'Convocatoria')

        # Instanciamos convocatoria en Ontologia
        convocatoria_instancia = convocatoria if not isinstance(convocatoria, int) else \
            onto.instanciar_convocatoria(convocatoria,
                                         nombre_convocatoria,
                                         tipo_convocatoria,
                                         anio_convocatoria)
        # Agregamos Convocatoria a la clase
        self.convocatoria = convocatoria_instancia
        # Agregamos las palabras de convocatoria a la Ontologia
        if nombre_convocatoria != "Ninguna":
            palabra_tipo = [onto.instanciar_palabra(palabra.lower(), [palabra.lower()])
                            for palabra in tipo_convocatoria.split()]
            palabra_anio = [onto.instanciar_palabra(str(tipo_convocatoria), [str(tipo_convocatoria)])]
            palabras.extend(palabra_tipo + palabra_anio)

        # Datos de Estudiantes
        codigos = filtered_columns('codigo', self.investigacion, atributos)
        nombres = filtered_columns('nombres', self.investigacion, atributos)
        apellidos = filtered_columns('apellidos', self.investigacion, atributos)

        # Datos Asesores
        asesores = filtered_columns('asesor', self.investigacion, atributos)

        # Datos Programas
        programas = filtered_columns('programa', self.investigacion, atributos)

        # Datos Departamentos
        departamentos = filtered_columns('departamento', self.investigacion, atributos)

        # Datos Facultades
        facultades = filtered_columns('facultad', self.investigacion, atributos)

        # Datos Grupos
        grupos = filtered_columns('grupo', self.investigacion, atributos)

        # Datos Lineas
        lineas = filtered_columns('linea', self.investigacion, atributos)

        for i in range(len(codigos)):
            # Instanciar Estudiante
            codigo = codigos[i]
            nombre = nombres[i]
            apellido = apellidos[i]

            estudiante = onto.definir_id(nombre + " " + apellido, "Estudiante")  # Nombre instancia, Clase
            # Instanciar Estudiante en Ontologia
            estudiante_instancia = estudiante if not isinstance(estudiante, int) else \
                onto.instanciar_estudiante(estudiante, codigo, nombre, apellido)
            # Agregar estudiante al objeto
            self.estudiantes.append(estudiante_instancia)

            # Instancias para Palabras, nombres y apellidos
            palabra_nombres = [onto.instanciar_palabra(palabra.lower(), [palabra])
                               for palabra in nombre.split()]
            palabra_apellidos = [onto.instanciar_palabra(palabra.lower(), [palabra.lower()])
                                 for palabra in apellido.split()]
            palabras.extend(palabra_nombres + palabra_apellidos)

            # Instanciar Asesores
            if i < len(asesores):
                asesor_nombre = asesores[i]
                asesor = onto.definir_id(asesor_nombre, "Docente")

                asesor_instancia = asesor if not isinstance(asesor, int) else \
                    onto.instanciar_docente(asesor, codigo="", nombre=asesor_nombre, apellidos="")

                self.asesores.append(asesor_instancia)

                # Instancias para Palabras, nombres y apellidos
                palabra_asesor = [onto.instanciar_palabra(palabra.lower(), [palabra])
                                  for palabra in asesor_nombre.split()]
                palabras.extend(palabra_asesor)

            # Instanciar Programa
            if i < len(programas):
                nombre_programa = programas[i]

                programa = onto.definir_id(nombre_programa, 'Programa')
                # Instanciar Programa en la ontologia
                programa_instancia = programa if not isinstance(programa, int) else \
                    onto.instanciar_programa(programa, nombre_programa)
                # Agregamos  programa al Objeto
                self.programas.append(programa_instancia)

            # Instanciar Departamento
            if i < len(departamentos):
                nombre_departamento = departamentos[i]
                # Instanciar Departamento en Ontologia
                departamento = onto.definir_id(nombre_departamento, 'Departamento')

                departamento_instancia = departamento if not isinstance(departamento, int) else \
                    onto.instanciar_departamento(departamento, nombre_departamento)

                self.departamentos.append(departamento_instancia)

            # Instanciar Facultad
            if i < len(facultades):
                nombre_facultad = facultades[i]
                # Instanciar Facultad en Ontologia
                facultad = onto.definir_id(nombre_facultad, 'Facultad')

                facultad_instancia = facultad if not isinstance(facultad, int) else \
                    onto.instanciar_facultad(facultad, nombre_facultad)

                self.facultades.append(facultad_instancia)

            # Instanciar Grupo Investigacion
            if i < len(grupos):
                nombre_grupo = grupos[i]
                grupo = onto.definir_id(nombre_grupo, 'Grupo_investigacion')

                grupo_instancia = grupo if not isinstance(grupo, int) else \
                    onto.instanciar_gi(grupo, nombre_grupo)
                self.grupos_investigacion.append(grupo_instancia)

            # Instanciar linea investigacion
            if i < len(lineas):
                nombre_linea = lineas[i]
                linea = onto.definir_id(nombre_linea, 'Linea_investigacion')
                linea_instancia = linea if not isinstance(linea, int) else \
                    onto.instanciar_li(linea, nombre_linea)
                self.lineas_investigacion.append(linea_instancia)

        # Agregamos Palabras al objeto
        self.palabras.extend(palabras)

    def instanciar_palabras(self):
        vocabulario = set(self.investigacion.corpus_lemas.split())

        for lema in vocabulario:
            descripciones = session.query(DiccionarioLema.palabras). \
                filter(DiccionarioLema.lema == lema).one_or_none()
            palabra_instancia = onto.instanciar_palabra(lema, descripciones.palabras)
            self.palabras.append(palabra_instancia)

    def relacionar(self):
        universidad = self.universidad
        viis = self.viis
        convocatoria = self.convocatoria
        proyecto_investigacion = self.proyecto_investigacion

        # VIIS -> Proyecto
        viis.relation_viis_tiene_pi(proyecto_investigacion)
        # VIIS -> Convocatoria
        viis.relation_viis_tiene_convocatoria(convocatoria)

        # Convocatoria -> Proyecto
        convocatoria.relation_convocatoria_tiene_pi(pi=proyecto_investigacion)

        for grupo in self.grupos_investigacion:

            # VIIS -> Grupo Investigacion
            viis.relation_viis_adscribe_gi(grupo)

            for linea in self.lineas_investigacion:
                # Linea -> Proyecto
                linea.relation_li_tiene_pi(proyecto_investigacion)
                grupo.relation_gi_tiene_li(linea)

            for i, estudiante in enumerate(self.estudiantes):
                # Grupo de Investigacion -> Estudiante
                grupo.relation_gi_tiene_docente(estudiante)

                # Investigador -> Estudiante
                estudiante.relation_investigador_es_estudiante(estudiante)

                # Estudiante -> Proyecto
                estudiante.relation_estudiante_es_autor_pi(proyecto_investigacion)

                # VIIS -> Estudiantes
                viis.relation_viis_tiene_investigador(estudiante)

                # Convocatoria -> Estudiante
                convocatoria.relation_convocatoria_dirigida_investigador(estudiante)

                if i < len(self.asesores):
                    asesor = self.asesores[i]
                    # Asesor -> Proyecto
                    asesor.docente_asesora_pi.append(self.proyecto_investigacion)
                    # Grupo -> Asesor
                    grupo.relation_gi_tiene_docente(asesor)
                    # VIIS -> Asesor
                    viis.relation_viis_tiene_investigador(asesor)
                else:
                    asesor = None

                # Relacion Programa, Facultad
                if i < len(self.programas):
                    programa = self.programas[i]
                    # Programa -> Estudiante
                    programa.relation_programa_tiene_estudiante(estudiante)
                    # Programa -> Docente
                    if asesor is not None:
                        programa.relation_programa_tiene_docente(asesor)
                else:
                    programa = None

                if i < len(self.departamentos):
                    departamento = self.departamentos[i]
                    # Departamento -> Programa
                    if programa is not None:
                        departamento.relation_departamento_tiene_programa(programa)
                    # Departamento -> Grupo de Investigacion
                    departamento.relation_departamento_tiene_gi(grupo)
                else:
                    departamento = None

                if i < len(self.facultades):
                    facultad = self.facultades[i]
                    # Facultad -> Departamento
                    if departamento is not None:
                        facultad.relation_facultad_tiene_departamento(departamento)
                    # Universidad -> Facultad
                    universidad.relation_universidad_tiene_facultad(facultad)

        for palabra in self.palabras:
            self.proyecto_investigacion \
                .relation_pi_tiene_palabra(palabra)


# Clases Para Consulta de Investigaciones
class Query(ABC, object):

    def __init__(self, tipo, nombre_universidad, nombre_viis):
        investigaciones = session.query(Investigacion). \
            filter(Investigacion.tipo_resumen == tipo).all()
        self.investigaciones = sorted(investigaciones, key=lambda item: item.id)
        self.universidad_ontologia = UniversidadOntologia(nombre_universidad, nombre_viis)

    def __iter__(self):
        for investigacion in self.investigaciones:
            yield investigacion

    @abstractmethod
    def instanciar(self):
        pass


# Clases para instanciar Docentes
class InstanciarInvestigacionesDocente(Query):

    def __init__(self, nombre_universidad, nombre_viis):
        super().__init__("docentes", nombre_universidad, nombre_viis)

    def instanciar(self):
        for investigacion in self.investigaciones:
            print(investigacion.id)
            investigacion_docente = InvestigacionDocente(investigacion, self.universidad_ontologia)
            investigacion_docente.instanciar()
            investigacion_docente.instanciar_palabras()
            investigacion_docente.relacionar()
        onto.ontologia.save()


# Clase para instanciar Estudiantes
class InstanciarInvestigacionesEstudiantes(Query):

    def __init__(self, nombre_universidad, nombre_viis):
        super().__init__("estudiantes", nombre_universidad, nombre_viis)

    def instanciar(self):
        for investigacion in self.investigaciones:
            print(investigacion.id)
            # if investigacion.id == 386:
            investigacion_estudiante = InvestigacionEstudiante(investigacion, self.universidad_ontologia,
                                                               investigacion.tipo_resumen)
            investigacion_estudiante.instanciar()
            investigacion_estudiante.instanciar_palabras()
            investigacion_estudiante.relacionar()
        onto.ontologia.save()


if __name__ == '__main__':
    instanciar_docentes = InstanciarInvestigacionesDocente(
        "Universidad de Nariño",
        "Vicerrectoría de Investigación e Interacción Social")

    instanciar_docentes.instanciar()
    print("Now we will do for students")
    instanciar_estudiantes = InstanciarInvestigacionesEstudiantes(
        "Universidad de Nariño",
        "Vicerrectoría de Investigación e Interacción Social"
    )

    instanciar_estudiantes.instanciar()
