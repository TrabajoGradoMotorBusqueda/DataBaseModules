def query_id_investigacion(session, investigacion, id_value):
    query = session.query(investigacion). \
        filter(investigacion.id == id_value).all()

    return query
