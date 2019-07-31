# cython: linetrace=True

import pprint
import tempfile  # from table import table
from .record_core import process_line3, query_results, get_table
from .record_update  import update_single
from .record_insert  import create_single


def method_upsert(context, meta,query_object,main_meta):
    #try:
        #meta.debug()
        #print(query_object)
        meta.table=get_table(context,meta)
        
        if not meta.on_duplicate_key:
            raise Exception("Upsert missing duplicate keys")

        where=[]
        for item in meta.on_duplicate_key:
            column=item.column
            for index in range(0,len(meta.columns)):
                column_compare=meta.columns[index].column
                if column_compare==column:
                    value=meta.values[index].value
                    if len(where)==0:
                        mode='where'
                    else:
                        mode='and'
                    where.append({mode:{'e1':column,'c':'=','=':'=','e2':value}})
        query_object['where']=where
        pprint.pprint query_object
        #return None
        
    
        line_number = 1
        affected_rows = 0
        temp_data_file=context.get_data_file(meta.table)
        diff=[]
        column_count       =meta.table.column_count()
        delimiter          =meta.table.delimiters.field
        visible_whitespace =meta.table.visible.whitespace
        visible_comments   =meta.table.visible.comments
        visible_errors     =meta.table.visible.errors

        with open(temp_data_file, 'r') as content_file:
            with tempfile.NamedTemporaryFile(mode='w', prefix="UPSERT",delete=False) as temp_file:
      
                for line in content_file:
                    #print line
                    processed_line = process_line3(context,meta, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    # skip matches
                    if True == processed_line['match']:
                        meta_class=main_meta.convert_to_class(query_object)
                        meta_class.table=meta.table
                        results = update_single(context,meta_class, temp_file,  False, processed_line)
                        if True == results['success']:
                            diff.append(results['line'])
                            affected_rows += 1
                        continue
                    temp_file.write(processed_line['raw'])
                    temp_file.write(meta.table.delimiters.get_new_line())
                # NO update occured.. Lets Insert...
                if affected_rows==0:
                    context.info("No row found in upsert, creating")
                    meta_class=main_meta.convert_to_class(query_object)
                    meta_class.table=meta.table

                    results = create_single(context,meta_class, temp_file,False)
                    affected_rows+=1
                    if True==results['success']:
                        diff.append(results['line'])
                else:
                    context.info("row found in upsert")

                temp_file.close()
                context.autocommit_write(meta.table,temp_file.name)
        context.auto_commit(meta.table)                

        return query_results(affected_rows=affected_rows,success=True,diff=diff)
#    except Exception as ex:
#        print ("ERR",ex)
        #Sremove_temp_file(temp_data_file)      
#        return query_results(success=False,error=ex)



