from ontologia import *
import re

def normalizar_nombre(string):
    string = re.sub(r'[^\w\s]', '', string)
    string_normalizada = string.replace(' ', '_')
    return string_normalizada.lower()


def instanciar_pi(id_proyecto_investigacion, titulo, resumen, palabras_clave, tipo, estado):
    pi = Proyecto_investigacion("pi" + "_" + str(id_proyecto_investigacion))
    pi.set_id_proyecto_investigacion(id_proyecto_investigacion)
    pi.set_titulo_proyecto_investigacion(titulo)
    pi.set_resumen_proyecto_investigacion(resumen)
    pi.set_palabras_clave(palabras_clave)
    pi.set_tipo_proyecto_investigacion(tipo)
    pi.set_estado_proyecto_investigacion(estado)

    return pi


def instanciar_facultad(id_facultad, nombre_facultad):
    # Ojo recibe de parametro universidad
    facultad = Facultad(normalizar_nombre("fac"+"_"+normalizar_nombre(nombre_facultad)))
    facultad.set_id_facultad(id_facultad)
    facultad.set_nombre_facultad(nombre_facultad)
    return facultad


def instanciar_departamento(id_departamento, nombre_departamento):  # resumenes decentes no tiene el Depto

    # Ojo recibe de parametro facultad
    departamento = Departamento("dep"+"_"+normalizar_nombre(nombre_departamento))
    departamento.set_id_departamento(id_departamento)
    departamento.set_nombre_departamento(nombre_departamento)
    return departamento


def instanciar_programa(id_programa, nombre_programa):
    # Parametro para Departamento
    programa = Programa(normalizar_nombre("pro"+"_"+normalizar_nombre(nombre_programa)))
    programa.set_id_programa(id_programa)
    programa.set_nombre_programa(nombre_programa)
    return programa


def instanciar_gi(id_grupo_investigacion, nombre_grupo_investigacion):
    # Ojo recibe de parametro Thing
    gi = Grupo_investigacion("gi"+"_"+normalizar_nombre(nombre_grupo_investigacion))
    gi.set_id_grupo_investigacion(id_grupo_investigacion)
    gi.set_nombre_grupo_investigacion(nombre_grupo_investigacion)
    #     gi.set_clasificacion_grupo_investigacion(clasificacion_grupo_investigacion)
    #     gi.set_area_grupo_investigacion(area_grupo_investigacion)
    #     gi.set_correo_grupo_investigacion(correo_grupo_investigacion)
    return gi


def instanciar_li(id_linea_investigacion, nombre_linea_investigacion):
    # Ojo recibe de parametro Grupo-_investigacion
    string = "li"+"_"+normalizar_nombre(nombre_linea_investigacion)
    if 'li_arte,_cultura_y_territorio' == string:
        print("pausaaa")

    li = Linea_investigacion("li"+"_"+normalizar_nombre(nombre_linea_investigacion))
    li.set_id_linea_investigacion(id_linea_investigacion)
    li.set_nombre_linea_investigacion(nombre_linea_investigacion)

    return li


def instanciar_convocatoria(id_convocatoria, nombre_convocatoria, tipo, anio):
    # Ojo recibe de parametro VIIS
    if nombre_convocatoria != "Ninguna":
        nombre_convocatoria = normalizar_nombre(nombre_convocatoria)
    convocatoria = Convocatoria(nombre_convocatoria)
    convocatoria.set_id_convocatoria(id_convocatoria)
    convocatoria.set_nombre_convocatoria(nombre_convocatoria)
    convocatoria.set_tipo_convocatoria(tipo)
    if anio is not None:
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


# Funciones para doocentes
def instanciar_docente(id_docente, codigo, nombre, apellidos):
    # Ojo recibe de parametro Investigador
    docente = Docente(normalizar_nombre(nombre + " " + apellidos))
    docente.set_id_investigador(id_docente)
    docente.set_codigo_investigador(codigo)
    docente.set_nombres_investigador(nombre)
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


# Funciones para estudiantes
def instanciar_estudiante(id_estudiante, codigo_estudiante, nombre, apellido):
    # Recibe de parametro Investigador
    estudiante = Estudiante(normalizar_nombre(nombre + " " + apellido))  # Iniciamos el Objeto
    estudiante.set_id_investigador(id_estudiante)
    estudiante.set_codigo_investigador(codigo_estudiante)
    estudiante.set_nombres_investigador(nombre)
    estudiante.set_apellidos_investigador(apellido)
    # estudiante.set_id_investigador()
    # estudiante.set_codigo_investigador
    # estudiante.set_cedula_investigador()
    # estudiante.set_correo_investigador()
    return estudiante


def instanciar_palabra(nombre_palabra, descripcion_palabra):
    palabra = Palabra(nombre_palabra)
    palabra.set_lema_palabra(nombre_palabra)
    palabra.set_descripcion_palabra(descripcion_palabra)

    return palabra


def definir_id(nombre, clase):
    nombre = normalizar_nombre(nombre)
    # if clase == "Grupo_investigacion": nombre = nombre.capitalize()

    clase_ontologia = ontologia.search_one(iri=f"*{clase}")
    instancia = ontologia.search_one(iri=f"*{nombre}*", is_a=clase_ontologia)

    if instancia is None:
        id_objeto = len(clase_ontologia.instances()) + 1
        return id_objeto
    else:
        return instancia
