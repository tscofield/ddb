
# yes, this could be a giant regex, but no.
# TODO: memory optimization.. maybe not sure how wastefull this is
def tokenize(text,discard_delimiters=False,discard_whitespace=True):
    
    tokens=[]
    
    # visual formatting characters
    whitespace={' ','\t','\n','\r'}
    # these are solid non depth related blocks
    blocks=[
            ['\'','\'','quote'] ,   # string block
            ['"' ,'"' ,'quote'] ,   # string block
            ['['  ,']','db'   ] ,   # mssql column
            ['`'  ,'`','db'   ] ,   # mysql column
        ]

    keywords=[  'ACCESSIBLE',
                'ADD',
                'ALL',
                'ALTER'
                'ANALYZE',
                'AND',
                'AS',
                'ASC',
                'ASENSITIVE',
                'BEFORE',
                'BETWEEN',
                'BIGINT',
                'BINARY',
                'BLOB',
                'BOTH',
                'BY',
                'CALL',
                'CASCADE',
                'CASE',
                'CHANGE',
                'CHAR',
                'CHARACTER',
                'CHECK',
                'COLLATE',
                'COLUMN',
                'CONDITION',
                'CONSTRAINT',
                'CONTINUE',
                'CONVERT',
                'CREATE',
                'CROSS',
                'CURRENT_DATE',
                'CURRENT_TIME',
                'CURRENT_TIMESTAMP',
                'CURRENT_USER',
                'CURSOR',
                'DATABASE',
                'DATABASES',
                'DAY_HOUR',
                'DAY_MICROSECOND',
                'DAY_MINUTE',
                'DAY_SECOND',
                'DEC',
                'DECIMAL',
                'DECLARE',
                'DEFAULT',
                'DELAYED',
                'DELETE',
                'DESC',
                'DESCRIBE',
                'DETERMINISTIC',
                'DISTINCT',
                'DISTINCTROW',
                'DIV',
                'DOUBLE',
                'DROP',
                'DUAL',
                'EACH',
                'ELSE',
                'ELSEIF',
                'ENCLOSED',
                'ESCAPED',
                'EXCEPT',
                'EXISTS',
                'EXIT',
                'EXPLAIN',
                'FALSE',
                'FETCH',
                'FLOAT',
                'FLOAT4',
                'FLOAT8',
                'FOR',
                'FORCE',
                'FOREIGN',
                'FROM',
                'FULLTEXT',
                'GENERAL',
                'GRANT',
                'GROUP',
                'HAVING',
                'HIGH_PRIORITY',
                'HOUR_MICROSECOND',
                'HOUR_MINUTE',
                'HOUR_SECOND',
                'IF',
                'IGNORE',
                'IGNORE_SERVER_IDS',
                'IN',
                'INDEX',
                'INFILE',
                'INNER',
                'INOUT',
                'INSENSITIVE',
                'INSERT',
                'INT',
                'INT1',
                'INT2',
                'INT3',
                'INT4',
                'INT8',
                'INTEGER',
                'INTERSECT',
                'INTERVAL',
                'INTO',
                'IS',
                'ITERATE',
                'JOIN',
                'KEY',
                'KEYS',
                'KILL',
                'LEADING',
                'LEAVE',
                'LEFT',
                'LIKE',
                'LIMIT',
                'LINEAR',
                'LINES',
                'LOAD',
                'LOCALTIME',
                'LOCALTIMESTAMP',
                'LOCK',
                'LONG',
                'LONGBLOB',
                'LONGTEXT',
                'LOOP',
                'LOW_PRIORITY',
                'MASTER_HEARTBEAT_PERIOD',
                'MASTER_SSL_VERIFY_SERVER_CERT',
                'MATCH',
                'MAXVALUE',
                'MEDIUMBLOB',
                'MEDIUMINT',
                'MEDIUMTEXT',
                'MIDDLEINT',
                'MINUTE_MICROSECOND',
                'MINUTE_SECOND',
                'MOD',
                'MODIFIES',
                'NATURAL',
                'NOT',
                'NO_WRITE_TO_BINLOG',
                'NULL',
                'NUMERIC',
                'ON',
                'OPTIMIZE',
                'OPTION',
                'OPTIONALLY',
                'OR',
                'ORDER',
                'OUT',
                'OUTER',
                'OUTFILE',
                'OVER',
                'PARTITION',
                'PRECISION',
                'PRIMARY',
                'PROCEDURE',
                'PURGE',
                'RANGE',
                'READ',
                'READS',
                'READ_WRITE',
                'REAL',
                'RECURSIVE',
                'REFERENCES',
                'REGEXP',
                'RELEASE',
                'RENAME',
                'REPEAT',
                'REPLACE',
                'REQUIRE',
                'RESIGNAL',
                'RESTRICT',
                'RETURN',
                'RETURNING',
                'REVOKE',
                'RIGHT',
                'RLIKE',
                'ROWS',
                'SCHEMA',
                'SCHEMAS',
                'SECOND_MICROSECOND',
                'SELECT',
                'SENSITIVE',
                'SEPARATOR',
                'SET',
                'SHOW',
                'SIGNAL',
                'SLOW',
                'SMALLINT',
                'SPATIAL',
                'SPECIFIC',
                'SQL',
                'SQLEXCEPTION',
                'SQLSTATE',
                'SQLWARNING',
                'SQL_BIG_RESULT',
                'SQL_CALC_FOUND_ROWS',
                'SQL_SMALL_RESULT',
                'SSL',
                'STARTING',
                'STRAIGHT_JOIN',
                'TABLE',
                'TERMINATED',
                'THEN',
                'TINYBLOB',
                'TINYINT',
                'TINYTEXT',
                'TO',
                'TRAILING',
                'TRIGGER',
                'TRUE',
                'UNDO',
                'UNION',
                'UNIQUE',
                'UNLOCK',
                'UNSIGNED',
                'UPDATE',
                'USAGE',
                'USE',
                'USING',
                'UTC_DATE',
                'UTC_TIME',
                'UTC_TIMESTAMP',
                'VALUES',
                'VARBINARY',
                'VARCHAR',
                'VARCHARACTER',
                'VARYING',
                'WHEN',
                'WHERE',
                'WHILE',
                'WINDOW',
                'WITH',
                'WRITE',
                'XOR',
                'YEAR_MONTH',
                'ZEROFILL'
                ]

    # blocks that must match depth
    #nested_block = [
    #                ['(',')']
    #              ]
    
    # operators # comparitors
    operators = [
            '&&', # and short circuit
            '||', # or short circuit
            '!=', # Not Equal
            '<>', # Not Equal
            '<=', # Less than or equal
            '>=', # Greater thanbor equal

            '>',  # Greater than
            '<',  # Less than

            '=',  # Equality
            '&',  # and
            '!',  # not
            '|',  # or
            
            'not' ,  # not
            'is'  ,  # equality
            'like',  # partial match
            
            '+',  # addition
            '-',  # subtraction
            '/',  # divide
            '*',  # multiple
            '(',  # left paren   (grouping)
            ')',  # right paren  (grouping)
            ]

    # standard delimiters
    delimiters=[',','.',';']

    for token in whitespace: 
        delimiters.append(token)

    for token in operators:
        delimiters.append(token)
    
    
    #add block identifiers to delimiters
    for b in blocks:
        if b[0] not in delimiters:
            delimiters.append(b[0])
        if b[1] not in delimiters:
            delimiters.append(b[1])

    delimiters_sorted=sort_array_by_length(delimiters)
    
    # padding prevents fencpost error
    text+=" "
    text_length=len(text)
    # c is the incremental pointer to the string
    word_start=0
    tokens=[]
    c=0
    #print delimiters_sorted
    delimter_len=1
    in_block=None
    block=None
    while c < text_length:
        #print "-",c
        just_crossed_block=False
        for b in blocks:
            delimter_len=len(b[0])
            #print b[0],b[1],c,delimter_len
            fragment=text[c:c+delimter_len]
            # only check for block start if not in one
            if None == in_block:
                if True == compare_text_fragment(fragment,b[0]):
                    just_crossed_block=True
                    #print  "IN BLOCK",c
                    in_block=b
                    block=b
                    c+=delimter_len
                    #print  "IN BLOCK",c
                    break
            # check for block end
            if True == compare_text_fragment(fragment,b[1]) or c==text_length-1:
                just_crossed_block=True
                #print  "NOT IN BLOCK",c
                in_block=None
                c+=delimter_len
                break
        # skip stuff in block
        if None != in_block :
            #print "in block skipp"
            if just_crossed_block==False:
                c+=1
            continue           
        for d in delimiters_sorted:
            delimter_len=len(d)
            fragment=text[c:c+delimter_len]
            if True == compare_text_fragment(fragment,d):
                if c-word_start>0:
                    word_end=c
                    not_delimiter=text[word_start:word_end]
                    token_type='data'
                    if not_delimiter.upper() in keywords:
                        token_type='keyword'
                    if None != block:
                        block_left=block[0]
                        block_right=block[1]
                        block_type=block[2]
                        block=None
                        not_delimiter=not_delimiter[len(block_left):-len(block_right)]
                    else:
                        block_left=None
                        block_right=None
                        block_type=None

                    tokens.append({'type':token_type,'data':not_delimiter,'block_left':block_left,'block_right':block_right,'block_type':block_type})

                word_start=c+delimter_len

                
                
                if True == discard_whitespace and fragment in whitespace:
                    
                    break
                
                #if True == discard_delimiters:
                #     continue

                delimiter_type="delimiter"
                if fragment in operators:
                    delimiter_type='operator'
                else:
                    if fragment in whitespace:
                        delimiter_type='whitespace'

     
                tokens.append({'type':delimiter_type,'data':fragment})
                break
        c+=delimter_len
    
    #for t in tokens:
    #    print t
    #exit(1)
    return tokens


def compare_text_fragment(x,y):
    if None ==x or None ==y :
        return False
    if x==y:
        return True
    return False


def sort_array_by_length(data):
    max_len=-1
    for d in data:
        del_len=len(d)
        if del_len>max_len:
            max_len=del_len
    
    # make a new array, put them in from longest to shortest, remove dupes
    data_sorted=[]
    for i in reversed(range(1,max_len+1)):
        for d in data:
            if d not in data_sorted:
                if len(d)==i:
                    data_sorted.append(d)
    return data




