from .record_core import query_results
import sys

def method_system_show_tables(context,meta):
    try:
        temp_table=None
        
        temp_table = context.database.temp_table(columns=['database', 'table'])
        for t in context.database.tables:
            columns = [t.data.database, t.data.name]
            temp_table.append_data({'data': columns, 'type': context.data_type.DATA, 'error': None})
       
        return query_results(success=True,data=temp_table)
    except:
        err = sys.exc_info()[1]
        ex = err.args[0]
        context.error (__name__,ex)
        return query_results(success=False,error=str(ex))   
