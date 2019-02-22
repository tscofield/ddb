import tempfile  # from table import table
from ..core import *

def method_insert(context, query_object):
    table_name = query_object['meta']['into']['table']
    query_object['table'] = context.database.get(table_name)
    if None == query_object['table']:
        raise Exception("Table '{0}' does not exist.".format(table_name))

    line_number = 1
    rows_affected = 0
    # process file
    requires_new_line = False
    temp_file_name = "INS_" + next(tempfile._get_candidate_names())
    
    try:
        with open(query_object['table'].data.path, 'r') as content_file:
            with open(temp_file_name, 'w') as temp_file:
                for line in content_file:
                    processed_line = process_line(query_object, line, line_number)
                    if None != processed_line['error']:
                        context.add_error(processed_line['error'])
                    line_number += 1
                    temp_file.write(processed_line['raw'])
                    temp_file.write(query_object['table'].delimiters.get_new_line())

                    #if processed_line['raw'][-1] == query_object['table'].delimiters.get_new_line():
                    requires_new_line = False
                    #else:
                    #    requires_new_line = True

                results = create_single(context,query_object, temp_file, requires_new_line)
                if True == results:
                    rows_affected += 1
        swap_files(query_object['table'].data.path, temp_file_name)
        return {'rows_affected':rows_affected,'success':True}
    except Exception as ex:
        return {'rows_affected':0,'success':False, 'error': ex}
    
        

def create_single(context, query_object, temp_file, requires_new_line):
    err = False
    ###
    # insert new data at end of file
    if len(query_object['meta']['columns']) != query_object['table'].column_count():
        context.add_error("Cannot insert, column count does not match table column count")
    else:
        if len(query_object['meta']['values']) != query_object['table'].column_count():
            context.add_error("Cannot insert, column value count does not match table column count")
        else:
            new_line = ''
            err = False
            #print query_object['meta']['columns']
            for c in range(0, len(query_object['meta']['columns'])):
                column_name = query_object['table'].get_column_at_data_ordinal(c)
                found = False
                for c2 in range(0, len(query_object['meta']['columns'])):
                    if query_object['meta']['columns'][c2]['column'] == column_name:
                        #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                        found = True
                        if c > 0:
                            new_line += '{}'.format(query_object['table'].delimiters.field)
                        new_line += '{}'.format(query_object['meta']['values'][c2]['value'])
                if False == found:
                    context.add_error("Cannot insert, column in query not found in table: {}".format(column_name))
                    err = True
                    break
            if False == err:
                #print new_line
                if True == requires_new_line:
                    temp_file.write(query_object['table'].delimiters.get_new_line())
                temp_file.write(new_line)
                temp_file.write(query_object['table'].delimiters.get_new_line())
    if False == err:
        return True
    else:
        return False
