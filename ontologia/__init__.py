from owlready2 import *
import os

this_folder = os.path.dirname(os.path.abspath(__file__))

# agregar la carpeta que contiene la ontologia,
# para busqueda local, sino en internet
onto_path.append(this_folder + "/Data")

# carga de ontologia por IRI o por ruta directa al archivo owl

ontologia = get_ontology(
    "http://www.semanticweb.org/OntologiaInvestigacionPrueba").load()

with ontologia:
    class Grupo_investigacion(Thing):

        def get_id_grupo_investigacion(self):
            return self.id_grupo_investigacion

        def set_id_grupo_investigacion(self, id_grupo_investigacion):
            self.id_grupo_investigacion = [id_grupo_investigacion]

        def get_nombre_grupo_investigacion(self):
            return self.nombre_grupo_investigacion

        def set_nombre_grupo_investigacion(self, nombre_grupo_investigacion):
            self.nombre_grupo_investigacion = [nombre_grupo_investigacion]

        def get_clasificacion_grupo_investigacion(self):
            return self.clasificacion_grupo_investigacion

        def set_clasificacion_grupo_investigacion(self, clasificacion_grupo_investigacion):
            self.clasificacion_grupo_investigacion = [clasificacion_grupo_investigacion]

        def get_area_grupo_investigacion(self):
            return self.area_grupo_investigacion

        def set_area_grupo_investigacion(self, area_grupo_investigacion):
            self.area_grupo_investigacion = [area_grupo_investigacion]

        def get_correo_grupo_investigacion(self):
            return self.correo_grupo_investigacion

        def set_correo_grupo_investigacion(self, correo_grupo_investigacion):
            self.correo_grupo_investigacion = [correo_grupo_investigacion]

        def relation_gi_tiene_li(self, li):
            self.gi_tiene_li.append(li)

        def relation_gi_tiene_investigador(self, investigador):
            self.gi_tiene_investigador.append(investigador)

        def relation_gi_tiene_docente(self, docente):
            self.gi_tiene_docente.append(docente)

        def relation_gi_tiene_estudiante(self, estudiante):
            self.gi_tiene_estudiante.append(estudiante)


    # SUBCLASE LINEA DE INVESTIGACION
    class Linea_investigacion(Grupo_investigacion):

        def get_id_linea_investigacion(self):
            return self.id_linea_investigacion

        def set_id_linea_investigacion(self, id_linea_investigacion):
            self.id_linea_investigacion = [id_linea_investigacion]

        def get_nombre_linea_investigacion(self):
            return self.nombre_linea_investigacion

        def set_nombre_linea_investigacion(self, nombre_linea_investigacion):
            self.nombre_linea_investigacion = [nombre_linea_investigacion]

        def relation_li_tiene_pi(self, pi):
            self.li_tiene_pi.append(pi)


    # CLASE INVESTIGADOR
    class Investigador(Thing):

        def get_id_investigador(self):
            return self.id_investigador

        def set_id_investigador(self, id_investigador):
            self.id_investigador = [id_investigador]

        def get_nombres_investigador(self):
            return self.nombres_investigador

        def set_nombres_investigador(self, nombres_investigador):
            self.nombres_investigador = [nombres_investigador]

        def get_apellidos_investigador(self):
            return self.apellidos_investigador

        def set_apellidos_investigador(self, apellidos_investigador):
            self.apellidos_investigador = [apellidos_investigador]

        def get_codigo_investigador(self):
            return self.codigo_investigador

        def set_codigo_investigador(self, codigo_investigador):
            self.codigo_investigador = [codigo_investigador]

        def get_cedula_investigador(self):
            return self.cedula_investigador

        def set_cedula_investigador(self, cedula_investigador):
            self.cedula_investigador = [cedula_investigador]

        def get_correo_investigador(self):
            return self.correo_investigador

        def set_correo_investigador(self, correo_investigador):
            self.correo_investigador = [correo_investigador]

        def relation_investigador_es_docente(self, docente):
            self.investigador_es_docente.append(docente)

        def relation_investigador_es_estudiante(self, estudiante):
            self.investigador_es_estudiante.append(estudiante)

        def relation_investigador_es_ie(self, ie):
            self.investigador_es_ie.append(ie)


    # SUBCLASE DOCENTE INVESTIGADOR
    class Docente(Investigador):

        def get_id_docente(self):
            return self.id_docente

        def set_id_docente(self, id_docente):
            self.id_docente = [id_docente]

        def relation_docente_es_autor_pi(self, pi):
            self.docente_es_autor_pi.append(pi)

        def relation_docente_asesora_pi(self, pi):
            self.docente_asesora_pi.append(pi)


    # SUBCLASE ESTUDIANTE INVESTIGADOR
    class Estudiante(Investigador):

        def get_id_estudiante(self):
            return self.id_estudiante

        def set_id_estudiante(self, id_estudiante):
            self.id_estudiante = [id_estudiante]

        def relation_estudiante_es_autor_pi(self, pi):
            self.estudiante_es_autor_pi.append(pi)


    # SUBCLASE INVESTIGADOR EXTERNO
    class Investigador_externo(Investigador):

        def get_id_investigador_externo(self):
            return self.id_investigador_externo

        def set_id_investigador_externo(self, id_investigador_externo):
            self.id_investigador_externo = [id_investigador_externo]

        def relation_ie_es_autor_pi(self, pi):
            self.ie_es_autor_pi.append(pi)

    # CLASE PALABRA
    class Palabra(Thing):

        def get_id_palabra(self):
            return self.id_palabra

        def set_id_palabra(self, id_palabra):
            self.id_palabra = [id_palabra]

        def get_descripcion_palabra(self):
            return self.descripcion_palabra

        def set_descripcion_palabra(self, descripcion_palabra):
            if len(self.descripcion_palabra) > 0:
                self.descripcion_palabra.extend(descripcion_palabra)
            else:
                self.descripcion_palabra = descripcion_palabra

        def get_lema_palabra(self):
            return self.lema_palabra

        def set_lema_palabra(self, lema_palabra):
            self.lema_palabra = [lema_palabra]

        def get_tipo_palabra(self):
            return self.tipo_palabra

        def set_tipo_palabra(self, tipo_palabra):
            self.tipo_palabra = [tipo_palabra]

        def get_concepto_palabra(self):
            return self.concepto_palabra

        def set_concepto_palabra(self, concepto_palabra):
            self.concepto_palabra = [concepto_palabra]

        def relation_palabra_sinonimo_palabra(self, palabra):
            self.palabra_sinonimo_palabra.append(palabra)

        def relation_palabra_conecta_palabra(self, palabra):
            self.palabra_conecta_palabra.append(palabra)


    # CLASE PROYECTO DE INVESTIGACION
    class Proyecto_investigacion(Thing):

        def get_id_proyecto_investigacion(self):
            return self.id_proyecto_investigacion

        def set_id_proyecto_investigacion(self, id_proyecto_investigacion):
            self.id_proyecto_investigacion = [id_proyecto_investigacion]

        def get_titulo_proyecto_investigacion(self):
            return self.titulo_proyecto_investigacion

        def set_titulo_proyecto_investigacion(self, titulo_proyecto_investigacion):
            self.titulo_proyecto_investigacion = [titulo_proyecto_investigacion]

        def get_resumen_proyecto_investigacion(self):
            return self.resumen_proyecto_investigacion

        def set_resumen_proyecto_investigacion(self, resumen_proyecto_investigacion):
            self.resumen_proyecto_investigacion = [resumen_proyecto_investigacion]

        def get_estado_proyecto_investigacion(self):
            return self.estado_proyecto_investigacion

        def set_estado_proyecto_investigacion(self, estado_proyecto_investigacion):
            self.estado_proyecto_investigacion = [estado_proyecto_investigacion]

        def get_tipo_proyecto_investigacion(self):
            return self.tipo_proyecto_investigacion

        def set_tipo_proyecto_investigacion(self, tipo_proyecto_investigacion):
            self.tipo_proyecto_investigacion = [tipo_proyecto_investigacion]

        def get_palabras_clave(self):
            return self.palabras_clave

        def set_palabras_clave(self, palabra_clave):
            if (len(self.palabras_clave) > 0):
                self.palabras_clave.extend(palabra_clave)
            else:
                self.palabras_clave = palabra_clave

        def relation_pi_tiene_palabra(self, palabra):
            self.pi_tiene_palabra.append(palabra)


    # CLASE UNIVERSIDAD
    class Universidad(Thing):

        def get_id_universidad(self):
            return self.id_universidad

        def set_id_universidad(self, id_universidad):
            self.id_universidad = [id_universidad]

        def get_nombre_universidad(self):
            return self.nombre_universidad

        def set_nombre_universidad(self, nombre_universidad):
            self.nombre_universidad = [nombre_universidad]

        def relation_universidad_tiene_facultad(self, facultad):
            self.universidad_tiene_facultad.append(facultad)

        def relation_universidad_tiene_viis(self, viis):
            self.universidad_tiene_viis.append(viis)




    # SUBCLASE FACULTAD
    class Facultad(Universidad):

        def get_id_facultad(self):
            return self.id_facultad

        def set_id_facultad(self, id_facultad):
            self.id_facultad = [id_facultad]

        def get_nombre_facultad(self):
            return self.nombre_facultad

        def set_nombre_facultad(self, nombre_facultad):
            self.nombre_facultad = [nombre_facultad]

        def relation_facultad_tiene_departamento(self, departamento):
            self.facultad_tiene_departamento.append(departamento)


    # SUBCLASE DEPARTAMENTO
    class Departamento(Facultad):

        def get_id_departamento(self):
            return self.id_departamento

        def set_id_departamento(self, id_departamento):
            self.id_departamento = [id_departamento]

        def get_nombre_departamento(self):
            return self.nombre_departamento

        def set_nombre_departamento(self, nombre_departamento):
            self.nombre_departamento = [nombre_departamento]

        def relation_departamento_tiene_programa(self, programa):
            self.departamento_tiene_programa.append(programa)

        def relation_departamento_tiene_gi(self, gi):
            self.departamento_tiene_gi.append(gi)


    # SUBCLASE PROGRAMA
    class Programa(Departamento):

        def get_id_programa(self):
            return self.id_programa

        def set_id_programa(self, id_programa):
            self.id_programa = [id_programa]

        def get_nombre_programa(self):
            return self.nombre_programa

        def set_nombre_programa(self, nombre_programa):
            self.nombre_programa = [nombre_programa]

        def relation_programa_tiene_estudiante(self, estudiante):
            self.programa_tiene_estudiante.append(estudiante)

        def relation_programa_tiene_docente(self, docente):
            self.programa_tiene_docente.append(docente)


    # CLASE VIIS
    class VIIS(Thing):

        def get_id_VIIS(self):
            return self.id_VIIS

        def set_id_VIIS(self, id_VIIS):
            self.id_VIIS = [id_VIIS]

        def get_nombre_VIIS(self):
            return self.nombre_VIIS

        def set_nombre_VIIS(self, nombre_VIIS):
            self.nombre_VIIS = [nombre_VIIS]

        def relation_viis_tiene_convocatoria(self, convocatoria):
            self.viis_tiene_convocatoria.append(convocatoria)

        def relation_viis_tiene_investigador(self, investigador):
            self.viis_tiene_investigador.append(investigador)

        def relation_viis_adscribe_gi(self, gi):
            self.viis_adscribe_gi.append(gi)

        def relation_viis_tiene_pi(self, pi):
            self.viis_tiene_pi.append(pi)


    # SUBCLASE CONVOCATORIA
    class Convocatoria(VIIS):

        def get_id_convocatoria(self):
            return self.id_convocatoria

        def set_id_convocatoria(self, id_convocatoria):
            self.id_convocatoria = [id_convocatoria]

        def get_nombre_convocatoria(self):
            return self.nombre_convocatoria

        def set_nombre_convocatoria(self, nombre_convocatoria):
            self.nombre_convocatoria = [nombre_convocatoria]

        def get_tipo_convocatoria(self):
            return self.tipo_convocatoria

        def set_tipo_convocatoria(self, tipo_convocatoria):
            self.tipo_convocatoria = [tipo_convocatoria]

        def get_anio_convocatoria(self):
            return self.anio_convocatoria

        def set_anio_convocatoria(self, anio_convocatoria):
            self.anio_convocatoria = [anio_convocatoria]

        def relation_convocatoria_tiene_pi(self, pi):
            self.convocatoria_tiene_pi.append(pi)

        def relation_convocatoria_dirigida_investigador(self, investigador):
            self.convocatoria_dirigida_investigador.append(investigador)
