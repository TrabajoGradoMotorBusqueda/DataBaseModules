import pandas as pd
import re
from models import Investigacion

resumenes_docentes = pd.read_excel("./data/Resumenes.xlsx", sheet_name="Proyectos Docentes")
resumenes_estudiantes = pd.read_excel("./data/Resumenes.xlsx", sheet_name="studiantiles y Trabajos de G")

columnas_resumenes = [column for column in dir(Investigacion)
                      if not (column.startswith('_') or column == 'metadata' or column == 'id')]


def all_in_one_row_5_columns(df, col1, col2, col3, col4, col5):
    contador = 1
    nan = 0
    indexcol1 = 0
    for index, row in df.iterrows():

        nac = row['no']
        if nac > nan:
            nan = nac
            contador = 1
            indexcol1 = index
        else:
            if contador == 2:
                df.loc[indexcol1, col2] = row[col1]
            elif contador == 3:
                df.loc[indexcol1, col3] = row[col1]
            elif contador == 4:
                df.loc[indexcol1, col4] = row[col1]
            elif contador == 5:
                df.loc[indexcol1, col5] = row[col1]

        contador += 1

    return df


def all_in_one_row_4_columns(df, col1, col2, col3, col4):
    contador = 1
    nan = 0
    indexcol1 = 0
    for index, row in df.iterrows():

        nac = row['no']
        if nac > nan:
            nan = nac
            contador = 1
            indexcol1 = index
        else:
            if contador == 2:
                df.loc[indexcol1, col2] = row[col1]
            elif contador == 3:
                df.loc[indexcol1, col3] = row[col1]
            elif contador == 4:
                df.loc[indexcol1, col4] = row[col1]
        contador += 1

    return df


def datos_adicionales(dataset):
    def wrapper(*args, **kargs):
        df = dataset(*args, **kargs)
        regex = re.compile(r'[a-zA-Z\s/()]+|\d+')

        for index, resumen in df.iterrows():
            result = regex.findall(resumen['convocatoria'])
            convocatoria = result[0]
            anio = result[1] if len(result) > 1 else None

            df.at[index, 'tipo_convocatoria'] = convocatoria
            df.at[index, 'anio_convocatoria'] = anio

            for i in range(1, 5):
                try:
                    name = resumen.loc[f'nombres_autor{i}'].split(' ')
                except:
                    break

                if len(name) <= 3:
                    first_name = name[0]
                    last_name = ' '.join(name[1:])
                else:
                    first_name = ' '.join(name[:2])
                    last_name = ' '.join(name[2:])

                df.at[index, f'nombres_autor{i}'] = first_name
                df.at[index, f'apellidos_autor{i}'] = last_name

        return df

    return wrapper


def ordenamiento_datos(dataset):
    # TODO: codigo base para construir corpus, ontologia
    def wrapper(*args, **kargs):
        df = dataset(*args, **kargs)
        columns = ['palabra', 'codigo', 'nombres', 'asesor', 'programa', 'facultad', 'grupo', 'linea', 'departamento']
        for column in columns:
            regex = re.compile(column)
            filtered_columns = list(filter(regex.match, columnas_resumenes))
            df = all_in_one_row_5_columns(df, *filtered_columns) if len(
                filtered_columns) > 4 else all_in_one_row_4_columns(df, *filtered_columns)

        # Eliminacion de Datos Nulos
        df.dropna(thresh=13, inplace=True)
        # Reasignar Index
        df['index'] = df['no'].astype('int')
        df.set_index('index', inplace=True)
        df.drop(columns=['no'], inplace=True)

        return df

    return wrapper


def completado_numero_registros(dataset):
    def wrapper(*args, **kargs):
        df = dataset(*args, **kargs)
        nac = 1 # Numero actual
        for index, row in df.iterrows():
            if pd.isnull(row['no']):
                df.loc[index, 'no'] = nac
            else:
                nac = row['no']

        return df

    return wrapper


def estructura_columnas(dataset):
    def wrapper(*args, **kargs):
        df = dataset(*args, **kargs)
        # Asignamos index
        df['index'] = [*range(1, len(df) + 1)]
        df.set_index('index', inplace=True)

        columns = ["no", "id_investigacion", "titulo_investigacion",
                   "resumen_investigacion", "estado_investigacion",
                   "codigo_autor1", "nombres_autor1", "programa_autor1",
                   "facultad_autor1", "convocatoria", "grupo_investigacion1",
                   "linea_investigacion1", "palabra_clave1"]

        # Asignamos Columnas
        if len(df.columns) > 13:  # Columnas para estudiantes
            columns.insert(8, 'departamento_autor1')
            columns.insert(10, 'asesor1')
            df.columns = columns
        else:  # Columnas para docentes
            df.columns = columns

        # Agregamos Columnas restantes
        for column in columnas_resumenes:
            if column not in df:
                df[column] = None

        # Eliminamos registros no encontrados en Palabras Clave
        df['palabra_clave1'] = df['palabra_clave1'].apply(
            lambda row: row if (row != 'No se encontraron palabras clave registradas') else None)

        # Convocatorias N/A
        df['convocatoria'] = df['convocatoria'].apply(lambda row: row if (row != 'N/A (Registrado)') else "Ninguna")

        return df

    return wrapper


@datos_adicionales
@ordenamiento_datos
@completado_numero_registros
@estructura_columnas
def estructura_dataset(df):
    return df


# if __name__ == '__main__':
# resumenes_docentes = estructura_dataset(resumenes_docentes)
# resumenes_estudiantes = estructura_dataset(resumenes_estudiantes)
#
# resumenes_docentes.to_csv('./data/Resumenes_Docentes.csv')
# resumenes_estudiantes.to_csv('./data/Resumenes_Estudiantes.csv')
# print('finish')

