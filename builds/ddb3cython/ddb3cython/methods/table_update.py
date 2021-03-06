import sys
from .record_core import query_results, get_table

def method_update_table(context, meta):
    columns=[]
    for c in meta.columns:
        columns.append(c.column)
    context.info("Columns to create", columns)
    
    target_table=get_table(context,meta)

    target_table.update(columns        =columns,
                        data_file      =meta.file,
                        field_delimiter=meta.delimiter,
                        comments       =meta.comments,
                        whitespace     =meta.whitespace,
                        errors         =meta.errors,
                        data_on        =meta.data_starts_on)
    #sace the update to the table
    results=target_table.save()

    return query_results(success=results)
