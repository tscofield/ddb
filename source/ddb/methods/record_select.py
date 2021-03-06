from ..functions.functions import *
from .record_core import  query_results,get_table, process_line3
from ..file_io.locking import lock
from ..version import __version__
import os
import sys
import tempfile




#used for order by a HACK to be fixed
context_sort=[]

def method_select(context, meta, parser):
    # meta.debug()
    context.info(meta)
    # make sure columns are valid, and from is good
    select_validate_columns_and_from(context,meta,parser)

    #create data destinaton
    temp_table = context.database.temp_table()
    
    # add columns, as renamed
    add_table_columns(context,meta,temp_table)
    
    # setup column ordinals
    set_ordinals(context,meta)

    # TODO Unique column names, no ambiguious index, name, alias,functions
    # TODO Columns with the same name can be renamed, but fail. Key issue?

    # scan the table for matches and collect the data
    temp_data=select_process_file(context,meta)
    
    all_records_count=len(temp_data)

    # TODO Join code here.....

    # order the data by columns, aliases or indexes
    temp_data=order_by(context,meta,temp_data)

    # Distinct, a custom grouping
    temp_data=distinct(context,meta,temp_data)
    
    # Grouping
    # group(context, data)
    
    # Limit / Filter the data
    temp_data = limit(context, meta, temp_data)

    # assign matched and transformed data to temp table
    temp_table.results=temp_data
    # might not have a table if its just functions
    try:
        table=meta.table
    except:
        table=None
    return query_results(success=True,data=temp_table,total_data_length=all_records_count,table=table)


def select_process_file(context,meta):
    has_columns = select_has_columns(context,meta)
    has_functions = select_has_functions(context,meta)
    table=None
    line_number = 1
    data=[]
    if True == has_columns:
        if meta.table:
            table= meta.table
        else:
            raise Exception ('table configuration has no data file')
        
        
        # if autocommit... create a temp copy everytime
        # if batch transaction, make 1 copy, always pull from that
        temp_data_file=context.get_data_file(table)

        column_count=table.column_count()
        delimiter=table.delimiters.field
        visible_whitespace=table.visible.whitespace
        visible_comments=table.visible.comments
        visible_errors=table.visible.errors

        content_file=open(temp_data_file, 'r')#,buffering=0) 
        try:
            for line in content_file:
                processed_line = process_line3(context, meta, line, line_number,column_count,delimiter,visible_whitespace,visible_comments, visible_errors)


                # not a match, skip
                if False == processed_line['match']:
                    line_number += 1
                    continue
                
                # there is data, rebuild and add
                if None != processed_line['data']:
                    restructured_line = process_select_row(context,meta,processed_line) 
                    data+=[restructured_line]
                line_number += 1
        finally:
            content_file.close()
        # release lock ans swap files if need be.
        context.auto_commit(table)
    # file is closed at this point, proccess the no "FROM" statement
    if False == has_columns and True == has_functions:
        row=process_select_row(context,meta,None)
        data+=[row]

    # return the acumulated data
    return data



def select_validate_columns_and_from(context, meta, parser):
    has_functions = select_has_functions(context,meta)
    has_columns = select_has_columns(context,meta)

    if False == has_columns and meta.source:
        err_msg="Invalid FROM, all columns are functions. Columns:{0}, Functions:{1}, Source:{2}".format(has_columns,has_functions,meta.source)
        raise Exception(err_msg)

    if False == has_columns and False == has_functions:
        err_msg="No columns defined in query. Columns:{0}, Functions:{1}, Source:{2}".format(has_columns,has_functions,meta.source)
        raise Exception(err_msg)
        


    # if has functions, tables may not be needed
    if True == has_columns:
        if meta.source:
            meta.table = get_table(context,meta)
            expand_columns(meta)
            column_len = meta.table.column_count()
            if column_len == 0:
                raise Exception("No defined columns in configuration")
        else:
            raise Exception("Missing FROM in select")





def expand_columns(meta):
    #print meta
    table_columns = meta.table.get_columns()
    if meta.columns:
        expanded_select = []
        for item in meta.columns:
            # TODO:leftover stuff cleanup for configuration.TABLE
            if item.column:
                if item.column == '*':
                    for column in table_columns:
                        expanded_select.append(meta._columns(column=column))
                else:
                    expanded_select.append(item)
            if item.function:
                expanded_select.append(item)

        meta.columns = expanded_select
    # ?? needed



def select_has_columns(context,meta):
    for c in meta.columns:
        if c.column:
            context.info("Has columns, needs a table")
            return  True
    return False
            
def select_has_functions(context,meta):
    for c in meta.columns:
        if c.function:
            context.info("Has functions, doesnt need a table")
            return True
    return False


def add_table_columns(context,meta,temp_table):
    #print meta
    for column in meta.columns:
        display = None
        #print meta.columns
        if column.display:
            display = column.display
            context.info("RENAME COLUMN", display)

        if column.column:
            context.info("adding data column")
            temp_table.add_column(column.column, display)
        if  column.function:
            context.info("adding function column")
            temp_table.add_column(column.function, display)    

def set_ordinals(context,meta):
    ordinals={}
    index=0
    for column in meta.columns:
        if  column.display:
            name=column.display
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if  column.function:
            name=column.function
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        if  column.column:
            name=column.column
            if '{0}'.format(name) in ordinals:
                raise Exception("ambigious column {0}".format(name))
            ordinals['{0}'.format(name)]=index                
        else:
            # TODO ERROR
            continue
        ordinals['{0}'.format(name)]=index                
        index+=1
    meta.ordinals=ordinals ##################################################

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def order_by(context,meta,data):
    global context_sort
    
    if not meta.order_by:
        context.info("NO order by")
        return data
    context.info("Select has Order By")
    context_sort = []
    for c in meta.order_by:
        if c.column not in meta.ordinals:
            err="ORDER BY column not present in the result set '{0}'".format(c.column)
            raise Exception (err)
        ordinal =meta.ordinals[c.column]
        context_sort.append([ordinal, c.direction])
    
    context.info(context_sort)
    if sys.version_info[0]==2:
      ordered_data = sorted(data, sort_cmp)
    else:
      ordered_data = sorted(data,key=cmp_to_key(sort_cmp))

    return ordered_data


def group(context,data):
        ## TODO grouping happens after ordering and before limiting
        #if 'group by' in query_object['meta']:
        #    group=[]
        #    for item in temp_data:
        #        no_item=True
        #        for group_item in group:
        #            if context.compare_data(group_item['data'],item['data']):
        #                no_item=None
        #                break
        #        if no_item:
        #            group.append(item)
        #    temp_data=group
    return data
       

def distinct(context,meta,data):
    if not meta.distinct:
        return data

    context.info("Select has Distinct")
    group=[]
    for item in data:
        no_item=True
        for group_item in group:
            if compare_data(context,group_item['data'],item['data']):
                no_item=None
                break
        if no_item:
            group.append(item)
    return group    


def process_select_row(context,meta,processed_line):
    row=[]
    #meta.debug()
    if meta.source:
    
        ordinals=meta.table.ordinals
    else:
        ordinals=None
    if None == processed_line:
        line_type=context.data_type.DATA
        error= None
        raw= None
        for c in meta.columns:
            if c.function:
                if c.function == 'database':
                    row.append(f_database(context))
                elif c.function == 'datetime':
                        row.append(f_datetime(context))
                elif c.function == 'date':
                        row.append(f_date(context))
                elif c.function == 'time':
                        row.append(f_time(context))
                elif c.function == 'version':
                        row.append(f_version(context,__version__))
                elif c.function == 'row_number':
                        row.append(f_row_number(context))
                #elif c['function'] == 'lower':
                #     row.append(context.functions.lower(c['column']))
                #elif c['function'] == 'upper':
                #     row.append(context.functions.upper(c['column']))
                #elif c['function'] == 'cat':
                #     row.append(context.functions.cat(c['arg1'],c['arg2']))
    else:
        line_type=processed_line['type']
        error= processed_line['error']
        raw= processed_line['raw']
        if line_type!=context.data_type.ERROR:
            for c in meta.columns:
                if c.column:
                    row.append(processed_line['data'][ordinals[c.column]])
                elif c.function:
                    if c.function == 'database':
                        row.append(f_database(context))
                    elif c.function == 'datetime':
                            row.append(f_datetime(context))
                    elif c.function == 'date':
                            row.append(f_date(context))
                    elif c.function == 'time':
                            row.append(f_time(context))
                    elif c.function == 'version':
                            row.append(f_version(context,__version__))
                    elif c.function == 'row_number':
                            row.append(f_row_number(context))
                    #elif c['function'] == 'lower':
                    #     row.append(context.functions.lower(c['column']))
                    #elif c['function'] == 'upper':
                    #     row.append(context.functions.upper(c['column']))
                    #elif c['function'] == 'cat':
                    #     row.append(context.functions.cat(c['arg1'],c['arg2']))
        
    return {'data': row, 'type': line_type, 'error': error,'raw':raw} 


def sort_cmp( x, y):
    for c in context_sort:
        ordinal = c[0]
        direction = c[1]
        #convert = lambda text: int(text) if text.isdigit() else text
        #alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        # %print x[ordinal],y[ordinal],-1
        if x['data'][ordinal] == y['data'][ordinal]:
            continue

        if x['data'][ordinal] < y['data'][ordinal]:
            return -1 * direction
        else:
            return 1 * direction
    return 0
    
def limit(context, meta, data):
    index = 0
    length = None

    if meta.limit:
        if meta.limit.start:
            index = meta.limit.start
            # index=index-1
        if meta.limit.length:
            length = meta.limit.length
            if length<0:
                raise Exception("Limit: range index invalid, Value:'{0}'".format(index))
    else:
        # no limit...
        return data


    context.info("Limit:{0},Length:{1}".format(index, length))
    if index<0:
        raise Exception("Limit: range index invalid, Value:'{0}'".format(index))

    # only 1 variable and its 0, so its really a 0 length query.

    if meta.limit.start==0 and meta.limit.length==None:
        return []

    # its 0 length
    if meta.limit.length==0:
        return []


    if None == index:
        index = 0
    if None == length:
        length = len(data) - index

    #print index,length
    data_length = len(data)
    if index >= data_length:
        #print("-Index is out of range for query. {} of {}".format(index,data_stream_lenght))
        return []
    if index + length > data_length:
        #print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
        length = data_length - index
    return data[index:index + length]

def compare_data(context,data1, data2):
    if data1 is None or data2 is None:
        return None
    if (not isinstance(data1, dict)) or (not isinstance(data2, dict)):
        if len(data1)!=len(data2):
            return None
        for index in range(0,len(data1)):
            if data1[index]!=data2[index]:
                return None
    else:
        shared_keys = set(data2.keys()) & set(data2.keys())
        if not ( len(shared_keys) == len(data1.keys()) and len(shared_keys) == len(data2.keys())):
            return None

        for key in data1.keys():
            if data1[key] != data2[key]:
                return None
    return True






