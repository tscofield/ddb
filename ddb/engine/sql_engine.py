import os
import json
import copy
from .parser.sql_parser  import sql_parser
from .structure.table import table
from .structure.database import database
from .structure.column import column_v2
from .evaluate.match import evaluate_match
from .functions import *
import operator
import flextable

#from table import table
import tempfile


#
# Fix delete
# Add insert
# Fix errors
# Add Update

def enum(**enums):
    return type('Enum', (), enums)


class sql_engine:
    data_type=enum(COMMENT=1,ERROR=2,DATA=3,WHITESPACE=4)

    def __init__(self,database_dir,query=None,debug=False):
     
        self.debug=debug
        self.results=None
        self.database=database(database_dir)
        if None !=query:
            self.query(query)
    
    #def set_configuration(self,database_instance):
    #    self.database=database
    #    if False == self.has_configuration():
    #        raise Exception("No configuration data")


    def debugging(self,debug=False):
        self.debug=debug


    def has_configuration(self):
        if None==self.database:
            return False
        table_count=self.database.count()
        if table_count==0:
            return False
        return True

    def query(self,sql_query):
        if False==self.has_configuration():
            raise Exception("No table found")
        
        
        parser=sql_parser(sql_query,self.debug)
        if False == parser.query_object:
            raise Exception ("Invalid SQL")
      
        query_object=parser.query_object
        
        if True==self.debug:
            print(query_object)
        #print  query_object
        #exit(9)
        #get columns, doesnt need a table
        #print query_object['mode']
        if query_object['mode']=="show tables":

            self.results=show_tables(self.database)    
        if query_object['mode']=="show columns":
            self.results=show_columns(self.database,parser)
        #if query_object['mode']=="show errors":
        #    self.results=show_errors(self.database,self.table)
        #print query_object
        if query_object['mode']=='select':
            self.results=self.select(parser)

        if query_object['mode']=='insert':
            self.results=self.insert(parser)

        if query_object['mode']=='update':
            self.results=self.update(parser)
           
        if query_object['mode']=='delete':
            self.results=self.delete(parser)
        if None != self.results:
            return self.results #TODO Fix
        return []
    


    def limit(self,data_stream,index,length):
        if None == index:
            index=0
        if None == length:
            length=len(data_stream)-index
            
        data_stream_lenght=len(data_stream)
        if index>=data_stream_lenght:
            #print("-Index is out of range for query. {} of {}".format(index,data_stream_lenght))
            return []
        if index+length>data_stream_lenght:
            #print("Length is out of range for query. {} of {}".format(length,data_stream_lenght))
            length=data_stream_lenght-index
        return data_stream[index:index+length]

    def process_line(self,query_object,line,line_number=0):
        err=None
        column_len=query_object['table'].column_count()
        line_cleaned=line.rstrip()
        line_data=None
        if query_object['table'].data.starts_on_line>line_number:
            line_type=self.data_type.COMMENT
            line_data=line
            #print query_object['table'].data.starts_on_line,line_number
        else:
            line_type=self.data_type.DATA
        if not line_cleaned.rstrip():
            if True == query_object['table'].visible.whitespace:
                line_data=['']
            line_type=self.data_type.WHITESPACE
        else:
            if line_cleaned[0] in query_object['table'].delimiters.comment:
                if True == query_object['table'].visible.comments:
                    line_data=[line_cleaned]
                line_type=self.data_type.COMMENT
            else:
                line_data=line_cleaned.split(query_object['table'].delimiters.field)
                cur_column_len=len(line_data)
                if cur_column_len!=column_len:
                    if cur_column_len>column_len:
                        err="Table {2}: Line #{0}, {1} extra Column(s)".format(line_number,cur_column_len-column_len,query_object['table'].data.name)
                    else:
                        err="Table {2}: Line #{0}, missing {1} Column(s)".format(line_number,column_len-cur_column_len,query_object['table'].data.name)
                    #query_object['table'].add_error(err)
                    line_type=self.data_type.ERROR
                    
                    #turn error into coment
                    if True == query_object['table'].visible.errors:
                        line_data=line_cleaned
                    else:
                        line_data=None
                    line_type=self.data_type.ERROR
                # fields are surrounded by something... trim
                #print self.table.delimiters.block_quote
                if None != query_object['table'].delimiters.block_quote:
                    line_data_cleaned=[]
                    for d in line_data:
                        line_data_cleaned.append(d[1:-1])
                    line_data=line_data_cleaned

        if 'where' not in query_object['meta']:
            match_results=True
        else:
            match_results=evaluate_match(query_object['meta']['where'],line_data,query_object['table'])
        
        return {'data':line_data,'type':line_type,'raw':line,'line_number':line_number,'match':match_results,'error':err}
   
    def select(self,parser):
        #try:
            temp_data=[]
            query_object=parser.query_object
            table_name=query_object['meta']['from']['table']
            parser.query_object['table']=self.database.get(table_name)
            parser.expand_columns(parser.query_object['table'].get_columns())
            column_len=query_object['table'].column_count()
            if column_len==0:
                raise Exception("No defined columns in configuration")
         
            temp_table=self.database.temp_table()
            for c in  query_object['meta']['select']:
                display=None
                if 'display' in c:
                    display=c['display']
                temp_table.add_column(c['column'],display)

            
            line_number=1
        
            # create temp table structure
            # process file
            with open(query_object['table'].data.path, 'r') as content_file:
                for line in content_file:
                    processed_line=self.process_line(query_object,line,line_number)
                    if None != processed_line['error']:
                        temp_table.add_error(processed_line['error'])
                    line_number+=1
                    
                    #print processed_line
                    if False == processed_line['match']:
                        continue

                    # add to temp table
                    if None != processed_line['data']:
                        restructured_line=[]
                        for c in query_object['meta']['select']:
                            restructured_line.append(query_object['table'].get_data_by_name(c['column'],processed_line['data']))
                        temp_data.append({'data':restructured_line,'type':processed_line['type'],'error':processed_line['error'],'raw':processed_line['raw']})
            
        
            # file is closed at this point


            if 'order by' in  query_object['meta']:
                self.sort=[]
                for c in  query_object['meta']['order by']:
                    ordinal=query_object['table'].get_ordinal_by_name(c['column'])
                    direction=1
                    if 'asc' in c:
                        direction=1
                    if 'desc' in c:
                        direction=-1 
                    self.sort.append([ordinal,direction])
                temp_data=sorted(temp_data,self.sort_cmp)
                #print temp_data

            limit_start=0
            limit_length=None
            #print query_object['meta']
            #exit(1)

            if 'limit' in query_object['meta']:
                if 'start' in query_object['meta']['limit']:
                    limit_start=query_object['meta']['limit']['start']
                if 'length' in query_object['meta']['limit']:
                    limit_length=query_object['meta']['limit']['length']


            
            temp_table.results=self.limit(temp_data,limit_start,limit_length)
            return temp_table
        #except Exception as ex:
            
            print (ex)
            #exit(1)
    
    
    def sort_cmp(self,x,y):

        for c in self.sort:
            ordinal=c[0]
            direction=c[1]

            #convert = lambda text: int(text) if text.isdigit() else text
            #alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]


            #%print x[ordinal],y[ordinal],-1
            if x[ordinal]==y[ordinal]:
                continue
            
            if x[ordinal]<y[ordinal]:
                return -1*direction
            else:
                return 1*direction
        return 0




    # creates a tempfile 
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible
    def delete(self,parser):
        try:
            query_object=parser.query_object
            table_name=query_object['meta']['from']['table']
            parser.query_object['table']=self.database.get(table_name)

            temp_table=self.database.temp_table()
            temp_table.add_column('deleted')

            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            deleted=0
            # process file
            with open(parser.query_object['table'].data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        #skip matches
                        if True  == processed_line['match']:
                            deleted+=1
                            continue
                        temp_file.write(processed_line['raw'])
            
            return {'data':[deleted],type:'data','error':None}
            temp_table.results=[data]
            os.remove(parser.query_object['table'].data.path)
            os.rename(temp_file_name,parser.query_object['table'].data.path)
            return temp_table
        
        except Exception as ex:
            
            print (ex)

    
    # creates a tempfile 
    # puts the raw original lines in temp file
    # File is as untouched as possible
    # new lines are joined at the end
    def insert(self,parser):
        try:
            query_object=parser.query_object
            table_name=query_object['meta']['into']['table']
            parser.query_object['table']=self.database.get(table_name)

            temp_table=self.database.temp_table()
            temp_table.add_column('inserted')

            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            inserted=0
            # process file
            requires_new_line=False
            with open(parser.query_object['table'].data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        temp_file.write(processed_line['raw'])
                        if processed_line['raw'][-1]==query_object['table'].delimiters.new_line:
                            requires_new_line=False
                        else: 
                            requires_new_line=True

                    results=self.create_single(query_object,temp_file,temp_table,requires_new_line)
                    if True==results:
                        inserted+=1

            
            data= {'data':[inserted],type:'data','error':None}
            temp_table.results=[data]
            os.remove(parser.query_object['table'].data.path)
            os.rename(temp_file_name,parser.query_object['table'].data.path)
            return temp_table
        
        except Exception as ex:
            
            print (ex)    


    def create_single(self,query_object,temp_file,temp_table,requires_new_line):
        err=False
        ### 
        # insert new data at end of file
        if len(query_object['meta']['columns']) != query_object['table'].column_count():
            temp_table.add_error("Cannot insert, column count does not match table column count")
        else:
            if len(query_object['meta']['values']) != query_object['table'].column_count():
                temp_table.add_error("Cannot insert, column value count does not match table column count")
            else:
                new_line=''
                err=False
                #print query_object['meta']['columns']
                for c in range(0,len(query_object['meta']['columns'])):
                    column_name=query_object['table'].get_column_at_data_ordinal(c)
                    found=False
                    for c2 in range(0,len(query_object['meta']['columns'])):
                        if query_object['meta']['columns'][c2]['column']==column_name:
                            #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                            found=True
                            if c>0:
                                new_line+='{}'.format(query_object['table'].delimiters.field)    
                            new_line+='{}'.format(query_object['meta']['values'][c2]['value'])
                    if False==found:
                        temp_table.add_error("Cannot insert, column in query not found in table: {}".format(column_name))
                        err=True
                        break
                if False == err:
                    #print new_line
                    if True == requires_new_line:
                        temp_file.write(query_object['table'].delimiters.new_line)
                    temp_file.write(new_line+query_object['table'].delimiters.new_line)
        if False==err:
            return {'data':[False],type:'data','error':None}
        else:
            return {'data':[True],type:'data','error':None}
        

    def update_single(self,query_object,temp_file,temp_table,requires_new_line,processed_line):
        err=False
        ### 
        # insert new data at end of file
        new_line=''
        err=False
        #print query_object['meta']['columns']

        # make sure the inserted columns exist
        for c2 in range(0,len(query_object['meta']['set'])):
            column_name=query_object['meta']['set'][c2]['column']
            if None == query_object['table'].get_column_by_name(column_name):
                temp_table.add_error("column in update statement does not exist in table: {}".format(column_name))
                #print "no column"
                err=True
                
        if False==err:
            for c in range(0,query_object['table'].column_count()):
                column_name=query_object['table'].get_column_at_data_ordinal(c)
                value=processed_line['data'][c]
                for c2 in range(0,len(query_object['meta']['set'])):
                    #print column_name,query_object['meta']['set']
                    if query_object['meta']['set'][c2]['column']==column_name:
                        #print("Column {} at table index {} located at query index {}".format(column_name,c, c2))
                        value=query_object['meta']['set'][c2]['expression']
                if c>0:
                    new_line+='{}'.format(query_object['table'].delimiters.field)    
                new_line+='{}'.format(value)
            #print new_line,value

         
        if False == err:
            #print new_line
            if True == requires_new_line:
                temp_file.write(query_object['table'].delimiters.new_line)
            temp_file.write(new_line+query_object['table'].delimiters.new_line)
        if False==err:
            return {'data':[False],type:'data','error':None}
        else:
            return {'data':[True],type:'data','error':None}
        



    # creates a tempfile 
    # puts the raw original lines in temp file
    # ignores matches
    # File is as untouched as possible
    def update(self,parser):
        try:
            query_object=parser.query_object
            table_name=query_object['meta']['update']['table']
            parser.query_object['table']=self.database.get(table_name)

            temp_table=self.database.temp_table()
            temp_table.add_column('updated')

            temp_file_name = next(tempfile._get_candidate_names())
            line_number=1
            updated=0
            # process file
            with open(parser.query_object['table'].data.path, 'r') as content_file:
                with open(temp_file_name, 'w') as temp_file:
                    for line in content_file:
                        processed_line=self.process_line(query_object,line,line_number)
                        if None != processed_line['error']:
                            temp_table.add_error(processed_line['error'])
                        line_number+=1
                        #skip matches
                        if True  == processed_line['match']:
                            results=self.update_single(query_object,temp_file,temp_table,False,processed_line)
                            if True==results:
                                updated+=1
                            continue
                        temp_file.write(processed_line['raw'])
            
            temp_table.results=[updated]
            os.remove(parser.query_object['table'].data.path)
            os.rename(temp_file_name,parser.query_object['table'].data.path)
            return temp_table
        
        except Exception as ex:
            
            print (ex)

  
                





    
