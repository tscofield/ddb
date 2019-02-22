def method_show_tables(context,database):
    try:
        temp_table = database.temp_table(columns=['database', 'table'])
        for t in database.tables:
            columns = [t.data.database, t .data.name]
            temp_table.append_data({'data': columns, 'type': context.data_type.DATA, 'error': None})
        #print temp_table
        return {'rows_affected':0,'success':True, 'data':temp_table}
    except Exception as ex:
        return {'rows_affected':0,'success':False}
