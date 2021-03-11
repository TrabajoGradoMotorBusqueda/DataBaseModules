import db
from sqlalchemy import Column, Integer, String, Text


class ResumenesInvestigacion(db.Base):
    __tablename__ = 'resumenes_investigacion'

    id = Column(Integer, primary_key=True, nullable=False)
    id_investigacion = Column(String(8))
    titulo_investigacion = Column(String(10000))
    resumen_investigacion = Column(Text)
    estado_investigacion = Column(String(100))
    palabra_clave1 = Column(String(500))
    palabra_clave2 = Column(String(500))
    palabra_clave3 = Column(String(500))
    palabra_clave4 = Column(String(500))
    palabra_clave5 = Column(String(500))
    convocatoria = Column(String(100))
    tipo_convocatoria = Column(String(100))
    anio_convocatoria = Column(Integer)
    codigo_autor1 = Column(Integer)
    nombres_autor1 = Column(String(100))
    apellidos_autor1 = Column(String(100))
    programa_autor1 = Column(String(500))
    facultad_autor1 = Column(String(500))
    departamento_autor1 = Column(String(500))
    grupo_investigacion1 = Column(String(500))
    linea_investigacion1 = Column(String(500))
    codigo_autor2 = Column(Integer)
    nombres_autor2 = Column(String(100))
    apellidos_autor2 = Column(String(100))
    programa_autor2 = Column(String(500))
    facultad_autor2 = Column(String(500))
    departamento_autor2 = Column(String(500))
    grupo_investigacion2 = Column(String(500))
    linea_investigacion2 = Column(String(500))
    codigo_autor3 = Column(Integer)
    nombres_autor3 = Column(String(100))
    apellidos_autor3 = Column(String(100))
    programa_autor3 = Column(String(500))
    facultad_autor3 = Column(String(500))
    departamento_autor3 = Column(String(500))
    grupo_investigacion3 = Column(String(500))
    linea_investigacion3 = Column(String(500))
    codigo_autor4 = Column(Integer)
    nombres_autor4 = Column(String(100))
    apellidos_autor4 = Column(String(100))
    programa_autor4 = Column(String(500))
    facultad_autor4 = Column(String(500))
    departamento_autor4 = Column(String(500))
    grupo_investigacion4 = Column(String(500))
    linea_investigacion4 = Column(String(500))
    nombre_asesor = Column(String(100))

    def __init__(self, values=None):
        if values is None:
            values = dict()
        for attribute in values.keys():
            setattr(self, attribute, values[attribute])

    def __attributes_setter__(self, values):
        for attribute in values.keys():
            setattr(self, attribute, values[attribute])

    def __repr__(self):
        return f'ResumenDocente({self.titulo_investigacion}, {self.convocatoria})'

    def __str__(self):
        return self.titulo_investigacion
