# cython: linetrace=True


from .record_core import  query_results,get_table


def method_create_table(context, meta):
    context.info("Create Table")
    try:
        columns = []
        if meta.columns==None:
            raise Exception("Missing columns, cannot create table")

        # TODO convert to meta class
        for c in meta.columns:
            columns.append(c.column)
        context.info("Columns to create", columns)

        if None==meta.source.database:
            meta.source.database=context.database.get_curent_database()

        results = context.database.create_table(table_name    = meta.source.table,
                                                database_name = meta.source.database,
                                                columns       = columns,
                                                data_file     = meta.file,
                                                delimiter     = meta.delimiter,
                                                comments      = meta.comments,
                                                errors        = meta.errors,
                                                whitespace    = meta.whitespace,
                                                data_on       = meta.data_starts_on,
                                                temporary     = meta.temporary,
                                                fifo          = meta.fifo,
                                                repo          = meta.repo,
                                                strict_columns= meta.strict,
                                                mode          = meta.mode
                                                )
      
        return query_results(success=results)
    except Exception as ex:
        context.error (__name__,ex)
        return query_results(success=False, error=ex)
