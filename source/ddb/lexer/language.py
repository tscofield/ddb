

#  name: "name"
#  segments: signatures to match against 
#     arguments: optional, 1 or 0 for unlimited (comma seperated)
#     data: optional
#          vars: variabls to manually set
#          sig: signature to match, {viariable} places any data in that position into that variable, [ ] makes it an array plain strings are dropped
#     name: initial string to match against to enter this name, this is the index of the object
#     optional: can we skip this
#     key: override name key
#     depends_on: do not match unless the other variable is present 
#     jump: goto an ealier command for matching, to repeat a loop set for multiple matches
#     parent: override the name, and place data on this index
#     store_array: allow multiple keys in an array at this index
#     specs :{'variable_name': {'type': 'int', 'default': 0} },
#     no_keyword:True ...?

language = {
    'functions': [{'name': 'database', 'arguments': None},
                  {'name': 'row_number', 'arguments': None},
                  {'name': 'count', 'arguments': [
                      {'name': 'where', 'required': True}]},
                  {'name': 'sum', 'arguments': [
                      {'name': 'column', 'required': True}]},
                  {'name': 'version', 'arguments': None},
                  {'name': 'upper', 'arguments': [
                      {'name': 'column', 'required': True}]},
                  {'name': 'lower', 'arguments': [
                      {'name': 'column', 'required': True}]},
                  {'name': 'cat', 'arguments':  [
                      {'name': 'arg1', 'required': True}, {'name': 'arg2', 'required': True}]},
                  {'name': 'date', 'arguments': None},
                  {'name': 'time', 'arguments': None},
                  {'name': 'datetime', 'arguments': None},
                  ],
    'commands': [
        {'name': 'show columns',
         'segments': [{'data': False, 'name': ['show', 'columns']},
                    {'arguments': 1,
                        'data': [{'sig': ['{table}']},
                                 {'sig': ['{database}', '.', '{table}']},
                                 ],
                     'name': 'from'}]},
        {'name': 'show tables',
         'segments': [
             {'data': False, 'name': ['show', 'tables']},
         ]},

        {'name': 'show variables',
         'segments': [
             {'data': False, 'name': ['show', 'variables']},
         ]},

        {'name': 'select',
         'arguments': 1,
         'segments': [
             {'data': None,
              'name': 'select',
              'optional': False
              },
             {'data': None,
              'name': 'distinct',
              'optional': True
              },

             {'arguments': 0,
              'data': [{'sig': ['{column}']},
                       {'sig': ['{column}',
                                'as',
                                '{display}']},
                       {'sig': ['{function}',
                                '(',
                                ')']},
                       {'sig': ['{function}',
                                '(',
                                '{argument1}',
                                ')'
                                ]},
                       {'sig': ['{function}',
                                '(',
                                '{argument1}',
                                ',',
                                '{argument2}',
                                ')'
                                ]},
                       {'sig': ['{function}',
                                '(',
                                '{argument1}',
                                ',',
                                '{argument2}',
                                ',',
                                '{argument3}',
                                ')'
                                ]},
                       {'sig': ['{function}',
                                '(',
                                ')',
                                'as',
                                '{display}'
                                ]},
                       {'sig': ['{function}',
                                '(',
                                '{argument1}',
                                ')',
                                'as',
                                '{display}'
                                ]},
                       {'sig': ['{function}',
                                '(',
                                '{argument1}',
                                ',',
                                '{argument2}',
                                ')',
                                'as',
                                '{display}'
                                ]},
                       {'sig': ['{function}',
                                '(',
                                '{argument1}',
                                ',',
                                '{argument2}',
                                ',',
                                '{argument3}',
                                ')',
                                'as',
                                '{display}'
                                ]},

                       ],
              'name': 'columns',
              'no_keyword': True,

              'depends_on':'select'
              },

             {'arguments': 1,
              'data': [{'sig': ['{table}']},
                       {'sig': ['{table}', 'as', '{display}']},
                       {'sig': ['{database}', '.', '{table}']},
                       {'sig': ['{database}', '.', '{table}', 'as', '{display}']}
                       ],
              'name': 'from',
              'optional': True},

             {'arguments': 1,
              'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
              'name': 'join',
              'depends_on': 'from',
              'optional': True},

             {'arguments': 1,
              'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
              'name': 'left join',
              'depends_on': 'from',
              'optional': True},

             {'arguments': 1,
              'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
              'name': 'right join',
              'depends_on': 'from',
              'optional': True},

             {'arguments': 1,
              'data': [{'sig': ['{table}']}, {'sig': ['{table}', 'as', '{display}']}],
              'name': 'full join',
              'depends_on': 'from',
              'optional': True},

             {'arguments': 1,
              'data': [
                  {'vars': {'c': '<'}, 'sig': ['{e1}', '<',    '{e2}']},
                  {'vars': {'c': '>'}, 'sig': ['{e1}', '>',    '{e2}']},
                  {'vars': {'c': '>='}, 'sig': ['{e1}', '>=',   '{e2}']},
                  {'vars': {'c': '<='}, 'sig': ['{e1}', '<=',   '{e2}']},
                  {'vars': {'c': '!='}, 'sig': ['{e1}', '!=',   '{e2}']},
                  {'vars': {'c': '<>'}, 'sig': ['{e1}', '<>',   '{e2}']},
                  {'vars': {'c': 'not'}, 'sig': ['{e1}', 'not',  '{e2}']},
                  {'vars': {'c': 'is'}, 'sig': ['{e1}', 'is',   '{e2}']},
                  {'vars': {'c': 'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                  {'vars': {'c': '='}, 'sig': ['{e1}', '=',    '{e2}']},
                  {'vars': {'c': 'in'}, 'sig': [
                      '{e1}', 'in',   '(', '[e2]', ')']},
              ],
              'name': 'on',
              'optional': True,
              'depends_on': 'join',
              'store_array': True},
             {'arguments': 1,
              'data': [
                  {'vars': {'c': '<'}, 'sig': ['{e1}', '<',    '{e2}']},
                  {'vars': {'c': '>'}, 'sig': ['{e1}', '>',    '{e2}']},
                  {'vars': {'c': '>='}, 'sig': ['{e1}', '>=',   '{e2}']},
                  {'vars': {'c': '<='}, 'sig': ['{e1}', '<=',   '{e2}']},
                  {'vars': {'c': '!='}, 'sig': ['{e1}', '!=',   '{e2}']},
                  {'vars': {'c': '<>'}, 'sig': ['{e1}', '<>',   '{e2}']},
                  {'vars': {'c': 'not'}, 'sig': ['{e1}', 'not',  '{e2}']},
                  {'vars': {'c': 'is'}, 'sig': ['{e1}', 'is',   '{e2}']},
                  {'vars': {'c': 'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                  {'vars': {'c': '='}, 'sig': ['{e1}', '=',    '{e2}']},
                  {'vars': {'c': 'in'}, 'sig': [
                      '{e1}', 'in',   '(', '[e2]', ')']},
              ],              'depends_on': 'on',
              'jump': 'on',
              'name': 'and',
              'optional': True,
              'parent': 'on'},

             {'arguments': 1,
              'data': [
                  {'vars': {'c': '<'}, 'sig': ['{e1}', '<',    '{e2}']},
                  {'vars': {'c': '>'}, 'sig': ['{e1}', '>',    '{e2}']},
                  {'vars': {'c': '>='}, 'sig': ['{e1}', '>=',   '{e2}']},
                  {'vars': {'c': '<='}, 'sig': ['{e1}', '<=',   '{e2}']},
                  {'vars': {'c': '!='}, 'sig': ['{e1}', '!=',   '{e2}']},
                  {'vars': {'c': '<>'}, 'sig': ['{e1}', '<>',   '{e2}']},
                  {'vars': {'c': 'not'}, 'sig': ['{e1}', 'not',  '{e2}']},
                  {'vars': {'c': 'is'}, 'sig': ['{e1}', 'is',   '{e2}']},
                  {'vars': {'c': 'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                  {'vars': {'c': '='}, 'sig': ['{e1}', '=',    '{e2}']},
                  {'vars': {'c': 'in'}, 'sig': [
                      '{e1}', 'in',   '(', '[e2]', ')']},
              ],              'depends_on': 'on',
              'jump': 'on',
              'name': 'or',
              'optional': True,
              'parent': 'on'},


             {'arguments': 1,
              'data': [
                  {'vars': {'c': '<'}, 'sig': ['{e1}', '<',    '{e2}']},
                  {'vars': {'c': '>'}, 'sig': ['{e1}', '>',    '{e2}']},
                  {'vars': {'c': '>='}, 'sig': ['{e1}', '>=',   '{e2}']},
                  {'vars': {'c': '<='}, 'sig': ['{e1}', '<=',   '{e2}']},
                  {'vars': {'c': '!='}, 'sig': ['{e1}', '!=',   '{e2}']},
                  {'vars': {'c': '<>'}, 'sig': ['{e1}', '<>',   '{e2}']},
                  {'vars': {'c': 'not'}, 'sig': ['{e1}', 'not',  '{e2}']},
                  {'vars': {'c': 'is'}, 'sig': ['{e1}', 'is',   '{e2}']},
                  {'vars': {'c': 'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                  {'vars': {'c': '='}, 'sig': ['{e1}', '=',    '{e2}']},
                  {'vars': {'c': 'in'}, 'sig': [
                      '{e1}', 'in',   '(', '[e2]', ')']},
              ],              'name': 'where',
              'optional': True,
              'depends_on': 'from',
              'store_array': True},
             {'arguments': 1,
              'data': [
                  {'vars': {'c': '<'}, 'sig': ['{e1}', '<',    '{e2}']},
                  {'vars': {'c': '>'}, 'sig': ['{e1}', '>',    '{e2}']},
                  {'vars': {'c': '>='}, 'sig': ['{e1}', '>=',   '{e2}']},
                  {'vars': {'c': '<='}, 'sig': ['{e1}', '<=',   '{e2}']},
                  {'vars': {'c': '!='}, 'sig': ['{e1}', '!=',   '{e2}']},
                  {'vars': {'c': '<>'}, 'sig': ['{e1}', '<>',   '{e2}']},
                  {'vars': {'c': 'not'}, 'sig': ['{e1}', 'not',  '{e2}']},
                  {'vars': {'c': 'is'}, 'sig': ['{e1}', 'is',   '{e2}']},
                  {'vars': {'c': 'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                  {'vars': {'c': '='}, 'sig': ['{e1}', '=',    '{e2}']},
                  {'vars': {'c': 'in'}, 'sig': [
                      '{e1}', 'in',   '(', '[e2]', ')']},
              ],              'depends_on': 'where',
              'jump': 'where',
              'name': 'and',
              'optional': True,
              'parent': 'where'},
             {'arguments': 1,
              'data': [
                  {'vars': {'c': '<'}, 'sig': ['{e1}', '<',    '{e2}']},
                  {'vars': {'c': '>'}, 'sig': ['{e1}', '>',    '{e2}']},
                  {'vars': {'c': '>='}, 'sig': ['{e1}', '>=',   '{e2}']},
                  {'vars': {'c': '<='}, 'sig': ['{e1}', '<=',   '{e2}']},
                  {'vars': {'c': '!='}, 'sig': ['{e1}', '!=',   '{e2}']},
                  {'vars': {'c': '<>'}, 'sig': ['{e1}', '<>',   '{e2}']},
                  {'vars': {'c': 'not'}, 'sig': ['{e1}', 'not',  '{e2}']},
                  {'vars': {'c': 'is'}, 'sig': ['{e1}', 'is',   '{e2}']},
                  {'vars': {'c': 'like'}, 'sig': ['{e1}', 'like', '{e2}']},
                  {'vars': {'c': '='}, 'sig': ['{e1}', '=',    '{e2}']},
                  {'vars': {'c': 'in'}, 'sig': [
                      '{e1}', 'in',   '(', '[e2]', ')']},
              ],              'depends_on': 'where',
              'jump': 'where',
              'name': 'or',
              'optional': True,
              'parent': 'where'},

             {
              'data': None,
              'name': 'union',
              'optional': True,
              'jump':'select',
              'array':True,
            },
             {'arguments': 0,
              'data': [{'sig': ['{column}']}],
              'name': ['group', 'by'],
              'optional': True},


             {'arguments': 0,
              'data': [{'sig': ['{column}']},
                       {'vars': {'direction': 1}, 'sig': ['{column}', 'asc']},
                       {'vars': {'direction': -1}, 'sig': ['{column}', 'desc']}],
              'name': ['order', 'by'],
              'optional': True},
             {'data': [{'sig': ['{length}']},
                       {'sig': ['{start}',
                                ',',
                                '{length}']}],
              'specs':{'length': {'type': 'int', 'default': 0}, 'start': {'type': 'int', 'default': 0}},

              'name': 'limit',
              'optional': True}]},



        {'name': 'set',
         'segments': [{
             'name': 'set',
             'arguments': 0,
             'data': [
                  {'vars': {'type': 'all'}, 'sig': [
                      '{variable}', '=', '{value}']},

             ],
         }]
         },
        {'name': 'create procedure',
         'segments': [{
             'name': ['create', 'procedure'],
             'arguments': None,
             'data': [{'sig': ['(']}],
             'dispose':True,
             'optional':False
         },
             {
             'name': ['parameters'],
             'arguments': 0,
             'optional': True,
             'data': [{'sig': ['{parameter}']}]
         },
             {
             'name': [')'],
             'arguments': 0,
             'optional': False,
             'dispose': True,
             'data':None,
         }]
         },
        {'name': 'delimiter',
         'segments': [{
             'name': 'delimiter',
             'arguments': 1,
             'data': [{'sig': ['{delimiter}']}],
         }]
         },
        {'name': 'end',
         'segments': [{
             'name': 'end',
             'data': False,
         }]
         },
        {'name': 'begin',
         'segments': [{
             'name': 'begin',
             'data': False,
         }]
         },
        {'name': 'commit',
         'segments': [{
             'name': 'commit',
             'data': False,
             'depends_on': 'begin'
         }]
         },
        {'name': 'rollback',
         'segments': [{
             'name': 'rollback',
             'data': False,
             'depends_on': 'begin'
         }]
         },
        {'name': 'show output modules',
         'segments': [{
             'name': ['show', 'output', 'modules'],
             'data':None
         }]
         },
        {'name': 'delete',
         'segments': [{'data': False, 'name': 'delete'},
                    {'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'from'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'name': 'where',
                     'optional': True,
                     'store_array': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'and',
                     'optional': True,
                     'parent': 'where'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'or',
                     'optional': True,
                     'parent': 'where'}]},
        {'name': 'insert',
         'segments': [{'data': False, 'name': 'insert'},
                    {'arguments': 1,
                        'data': [{'sig': ['{table}']},
                                 {'sig': ['{database}', '.', '{table}']},
                                 ],
                     'name': 'into',
                     },
                    {'data': False, 'dispose': True, 'name': '('},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']}],
                     'name': 'columns',
                     'no_keyword': True},
                    {'data': False, 'dispose': True, 'name': ')'},
                    {'data': False,
                     'dispose': True,
                     'name': 'values'},
                    {'data': False, 'dispose': True, 'name': '('},
                    {'arguments': 0,
                     'data': [{'sig': ['{value}']}],
                     'name': 'values',
                     'no_keyword': True},
                    {'data': False, 'dispose': True, 'name': ')'}]},
        {'name': 'update',
         'segments': [{'arguments': 1,
                     'data': [{'sig': ['{table}']},
                              {'sig': ['{database}', '.', '{table}']},
                              ],
                     'name': 'update'},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}', '=', '{expression}']}],
                     'name': 'set'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'name': 'where',
                     'optional': True,
                     'store_array': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'and',
                     'optional': True,
                     'parent': 'where'},
                    {'arguments': 1,
                     'data': [{'sig': ['{e1}', '{c}', '{e2}']}],
                     'depends_on': 'where',
                     'jump': 'where',
                     'name': 'or',
                     'optional': True,
                     'parent': 'where'}]},
        {'name': 'upsert',
         'segments': [
             {'data': False, 'name': 'upsert'},
             {'arguments': 1,
              'data': [{'sig': ['{table}']},
                       {'sig': ['{database}', '.', '{table}']},
                       ],
              'name': 'into',
              },
             {'data': False, 'dispose': True, 'name': '('},
             {'arguments': 0,
              'data': [{'sig': ['{column}']}],
              'name': 'columns',
              'no_keyword': True},
             {'data': False, 'dispose': True, 'name': ')'},
             {'data': False,
              'dispose': True,
              'name': 'values'},
             {'data': False, 'dispose': True, 'name': '('},
             {'arguments': 0,
              'data': [{'sig': ['{value}']}],
              'name': 'values',
              'no_keyword': True},
             {'data': False, 'dispose': True, 'name': ')'},

             {'arguments': 0,
              'data': [{'sig': ['{column}']}],
              'name': ['on', 'duplicate', 'key'],
              'optional': True,
              },
             {'arguments': 0,
              'data': [{'sig': ['{column}', '=', '{expression}']}],
              'name': ['update'],
              'key':'set',
              'optional': True,
              },
         ]},
        {'name': 'use',
         'segments': [{'arguments': 1,
                     'data': [{'sig': ['{table}']}],
                     'name': 'use'}]},
        {'name': 'drop',
         'segments': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']},
                              {'sig': ['table', '{database}', '.', '{table}']}],

                     'name': 'drop'}]},
        {'name': 'create',
         'segments': [

             {'data': None,
              'name': 'create',
              'optional': False
              },
             {'data': None,
              'name': 'temporary',
              'optional': True
              },

             {'arguments': 1,
              'data': [{'sig': ['{table}']},
                       {'sig': ['{database}', '.', '{table}']},
                       ],
              'name': 'table',
              'type': 'single',
              'optional': False},

             {'data': False, 'dispose': True, 'name': '('},
             {'arguments': 0,
              'data': [{'sig': ['{column}']}],
              'name': 'columns',
              'no_keyword': True},
             {'data': False, 'dispose': True, 'name': ')'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{file}']}],
              'type':'single',
              'name': 'file'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{fifo}']}],
              'type':'single',
              'optional': True,
              'name': 'fifo'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{type}', 'url', '=', '{url}', 'user', '=', '{user}', 'password', '=', '{password}', 'dir', '=', '{dir}', 'file', '{file}']}],
              'type':'single',
              'optional': True,
              'name': 'repo'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{delimiter}']}],
              'type':'single',
              'optional': True,
              'specs':{'field': {'type': 'char', 'default': ','}},
              'name': 'delimiter'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{whitespace}']}],
              'type':'single',
              'optional': True,
              'specs':{'whitespace': {'type': 'bool'}},
              'name': 'whitespace'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{errors}']}],
              'type':'single',
              'optional': True,
              'specs':{'errors': {'type': 'bool'}},
              'name': 'errors'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{comments}']}],
              'type':'single',
              'optional': True,
              'specs':{'comments': {'type': 'bool'}},
              'name': 'comments'},
             {'arguments': 1,
              'data': [{'sig': ['=', '{data_starts_on}']}],
              'type':'single',
              'optional': True,
              'specs':{'data_starts_on': {'type': 'int', 'default': 1}},
              'name': 'data_starts_on'}, ]},
        {'name': 'update table',
         'segments': [{'arguments': 1,
                     'data': [{'sig': ['table', '{table}']}],
                     'name': 'update'},
                    {'data': False, 'dispose': True,
                        'name': '(', 'optional': True},
                    {'arguments': 0,
                     'data': [{'sig': ['{column}']}],
                     'name': 'columns',
                     'no_keyword': True,
                     'depends_on':'(',
                     'optional': True},
                    {'data': False, 'dispose': True,
                        'name': ')', 'optional': True, 'depends_on': '('},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{file}']}],
                     'name': 'file',
                     'optional': True},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{field}']}],
                     'optional': True,
                     'specs':{'field': {'type': 'char', 'default': ','}},
                     'name': 'delimiter'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'whitespace': {'type': 'bool'}},
                     'name': 'whitespace'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{whitespace}']}],
                     'optional': True,
                     'specs':{'errors': {'type': 'bool'}},
                     'name': 'errors'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{comments}']}],
                     'optional': True,
                     'specs':{'comments': {'type': 'bool'}},
                     'name': 'comments'},
                    {'arguments': 1,
                     'data': [{'sig': ['=', '{data_starts_on}']}],
                     'optional': True,
                     'specs':{'data_starts_on': {'type': 'int'}},
                     'name': 'data_starts_on'}
                    ]
         },
        {'name': 'describe table',
         'segments': [{'arguments': 1,
                     'data': [{'sig': ['{table}']},
                              {'sig': ['{database}', '.', '{table}']},
                              ],
                     'name': ['describe', 'table']}]},

    ]  # name matrix array
}  # sql_syntax



def cleanup_language():
    from pprint import pprint
    # all commands
    for command in language['commands']:
        for segment in command['segments']:
            not_found=None
            if 'data' not in segment:
                segment['data']=[]
            elif  segment['data']==None:
                segment['data']=[]
            elif  segment['data']==False:
                segment['data']=[]
            else:
                not_found=True
            if not_found==None:
                if isinstance(segment['name'],list):
                    segment['data']=[{'sig':segment['name']}]+segment['data']
                else:
                    segment['data']=[{'sig':[segment['name']]}]+segment['data']
          
            else:
                for data in segment['data']:
                    if None == data:
                        data={'sig':[]}

                    if isinstance(segment['name'],list):
                        s2=segment['name']
                    else:
                        s2=[segment['name']]
                    #print data['sig'],s2
                    data['sig']=s2+data['sig']
            
            if 'arguments' in segment:
                if  segment['arguments']==1:
                    del(segment['arguments'])
    pprint(language)

        
cleanup_language()