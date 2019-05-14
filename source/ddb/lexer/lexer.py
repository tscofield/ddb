from .language import language
from .tokenize import tokenizer


class lexer:
   

    def __init__(self, query, debug=False):
        # select distinct,* from table where x=y and y=2 order by x,y limit 10,2
        # select c1,c2,c3,c4 as x,* from table where x=y and y=2 order by x,y limit 10,2
        # select top 10 * from table where x=y and y=2 order by x,y
        # insert into table () values ()
        # delete from table where x=y and y=2

        # keep non variable keywords form signature match in object
        # realy only need this for debugging
        self.keep_non_keywords=True
        self.debug = True
        self.query_objects = []
        if  query==None:
            raise Exception("Invalid Syntax")
    
        #print query
        querys = query.split(';')
        self.info("Queries", querys)
        for q in querys:
            self.info("-----------------------------------")
            tokens = tokenizer().chomp(q, discard_whitespace=True, debug=debug)
            # skip 0 length commands such as single ';'
            token_length = 0
            for token in tokens:
                if token['data'] != '':
                    token_length += 1

            self.info("Token Length", token_length)
            if token_length == 0:
                continue

            parsed = self.parse(tokens)
            if False == parsed:
                self.query_objects = None
                break
            self.query_objects.append(parsed)

        if None == self.query_objects:
            raise Exception("Invalid Syntax")

    def parse(self, tokens):

        sql_object = []
        # SOME TODO!
        # loop through commands, return the first matching result

        for command in language['commands']:
            res=self.test_syntax(command,tokens)
            if res:
                return res

    # place holder for the status of a command fragment
    class flags:
        def __init__(self,command_fragment):
            if 'dispose' in command_fragment:
                self.dispose = command_fragment['dispose']
            else:
                self.dispose = False
            if 'no_keyword' in command_fragment:
                self.no_keyword = command_fragment['no_keyword']
            else:
                self.no_keyword = False
            if 'store_array' in command_fragment:
                self.store_array = command_fragment['store_array']
            else:
                self.store_array = False
            if 'key' in command_fragment:
                self.arg_key=command_fragment['key']
            else: 
                self.arg_key=None
            if 'parent' in command_fragment:
                self.parent = command_fragment['parent']
            else:
                self.parent = None
            if 'type' in command_fragment:
                self.meta_type = command_fragment['type']
            else:
                self.meta_type = None
            if 'optional' in command_fragment:
                self.optional = command_fragment['optional']
            else:
                self.optional = False
            if isinstance(command_fragment['name'], list):
                self.object_id = ' '.join([str(x) for x in command_fragment['name']])
                self.object_id = self.object_id.lower()
            else:
                self.object_id = command_fragment['name'].lower()
            #logic
            # key override for segment
            if self.arg_key:
                self.object_id=self.arg_key

                
    def test_syntax(self,command,tokens):
        debug = True
        query_object = {}
        token_index = 0
        self.info("-----", command['name'])
        keyword_found = False
        segment_index = 0
        query_mode = None
        curent_object = {}
        segment = {}

        while segment_index < len(command['segments']) and token_index < len(tokens):
            # set the state
            segment = command['segments'][segment_index]
            self.info("############# TESTING : {0}.{1}".format(command['name'],segment['name']))
            segment_index += 1
            curent_object = {}
            flags=lexer.flags(segment)
    
                
            curent_object['mode'] = flags.object_id
            query_mode = command['name']
            self.info("Object Id:", flags.object_id, "Token Id:", token_index)
            
           # if False == flags.no_keyword:
           #     keyword_compare = self.get_sub_array(segment, 'name')
           #     haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
           #     self.info(keyword_compare)
           #     if True == self.single_array_match(keyword_compare, haystack):
           #         self.info("match", keyword_compare, haystack)
           #         # we use name because it may be a list. and its simpler to hash by name
           #         # as long as the compare is good, we dont care
           #         curent_object['mode'] = flags.object_id
           #         if segment_index == 1:
           #             query_mode = command['name']
           #         keyword_found = True
           #     else:
           #         if False == flags.optional:
           #             if True == debug:
           #                 self.info("Exiting")
           #             break
           #         else:
           #             continue
           #     if False == keyword_found:
           #         self.info("Keywords exhausted")
           #         break
#
           #     token_index += len(keyword_compare)
           #     self.info("advance token index ", token_index, segment['data'])
           # else:
           #     curent_object['mode'] = flags.object_id
#
            base_argument={}
            # set static variables







            #if None == segment['data'] or False == segment['data']:
            #    self.info("No data to match")
            #    # only append object after argument collection is done
            #    # query_object.append(curent_object)
            #    if not flags.dispose:
            #        self.info("----------Adding", curent_object['mode'])
            #        query_object[curent_object['mode']] = None
#
            #    jump = None
            #    if 'jump' in segment:
            #        self.info("JUMP")
            #        jump = segment['jump']
            #    if None != jump:
            #        tsi = 0
            #        for ts in command['segments']:
            #            if ts['name'] == jump:
            #                self.info("Jumping from ", segment_index, tsi + 1)
            #                segment_index = tsi + 1
            #                token_index+=1
            #                break
            #            tsi += 1
            #    in_argument = False
            #    
#
            ## This is where data colection happens
            #else:


            in_argument = True
            argument_index = 0
            while True == in_argument:

                #self.info("---in argument")

                # DEPENDENCY
                # DEPENDENCY
                # DEPENDENCY

                if 'depends_on' in segment:
                    depends_on = segment['depends_on']
                    self.info("Depends on {0}".format(depends_on))
                else:
                    depends_on = None

                # if there is a dependency, enforce
                if None != depends_on:

                    depends_oncompare = self.get_sub_array(depends_on)

                    dependency_found = False
                    for q_o in query_object:
                        #self.info( depends_on,q_o)
                        haystack = self.get_sub_array(q_o)
                        if True == self.single_array_match(depends_oncompare, haystack):
                            dependency_found = True
                    if False == dependency_found:
                        self.info("Missing", depends_on)
                        break
                    else:
                        self.info("Dependency found", depends_on)

                # self.info("data",segment['data'])
                if 'arguments' in segment:
                    arguments = segment['arguments']
                else:
                    arguments = 1
                if arguments == None:
                    arguments = 1
                self.info("Number of arguments", arguments)

                data = self.get_sub_array(segment, 'data')
                match_len = 0
                match = None
                for sig in data:
                    signature_compare = self.get_sub_array(sig, 'sig')
                    haystack = self.get_sub_array_sub_key(tokens[token_index:], 'data')
                    if True == self.single_array_match(signature_compare, haystack):
                        #    self.info("match", signature_compare,haystack)
                        if len(signature_compare) > match_len:
                            match_len = len(signature_compare)
                            match = signature_compare
                            signature=sig
                            self.info("Best Match", match_len)
                if None == match:
                    self.info("No match")
                    break
                else:
                    # add the static vars
                    base_argument={}
                    if 'vars' in signature:
                        for var_name in signature['vars']:
                            self.info("var","'{0}'='{1}'".format(var_name,signature['vars'][var_name]))
                            base_argument[var_name]=signature['vars'][var_name]

                    w_index = 0
                    argument = base_argument
                    for word in match:
                        variable_data=tokens[token_index + w_index]['data']
                        if word[0:1] == '[' and word[-1] == ']': 
                            definition='array'
                        elif word[0:1] == '{' and word[-1] == '}':
                                definition='single'
                        else:
                            definition=None

                        # is there an definition?
                        if definition:
                            # if we have definitions
                            variable=word[1:-1]
                            variable_type='string'
                            if 'specs' in segment:
                                # if this is in or definitions
                                if variable in segment['specs']:
                                    if 'type' in segment['specs'][variable]:
                                        variable_type=segment['specs'][variable]['type']
                                    
                            if variable_type=='int':
                                try:
                                    argument[variable] = tokens[token_index + w_index]['data'] = int(variable_data)
                                except BaseException:
                                    #err_msg="Variable data not an integer '{0}' {1}".format(variable_data,)
                                    pass
                                    break
                                    #raise Exception (err_msg)
                            elif variable_type=='bool':
                                if variable_data.lower()=='true':
                                    argument[variable] =True
                                elif variable_data.lower()=='false':
                                    argument[variable] =False
                                else:
                                    pass
                                    break
                                    #raise Exception("Variable Data not boolean")
                            elif variable_type=='char':
                                if len(variable_data)!=1:
                                    pass
                                    break
                                    #raise Exception("variable data length exceeded, type char")
                                argument[variable] =variable_data

                            elif variable_type=='string':
                                argument[variable] =variable_data
                        else:
                            # normal keyword
                            if self.keep_non_keywords:
                                argument[word] = variable_data
                        w_index += 1
                    if 'arguments' not in curent_object:
                        curent_object['arguments'] = []

                    if arguments == 1:
                        curent_object['arguments'] = argument
                    else:
                        # add the arguments to curent object
                        curent_object['arguments'].append(argument)

                    self.info("match", match)
                    token_index += len(match)
                    if arguments != 0:
                        self.info("print not in list")
                        argument_index += 1
                        if argument_index >= arguments:
                            self.info("----------Adding", curent_object['mode'])
                            if True == flags.store_array:
                                if curent_object['mode'] not in query_object:
                                    query_object[curent_object['mode']] = []

                                query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                            else:
                                if None == flags.parent:
                                    if flags.meta_type=='single':
                                        for flags.arg_key in curent_object['arguments']:
                                            query_object[flags.arg_key] = curent_object['arguments'][flags.arg_key]
                                    else:    
                                        query_object[curent_object['mode']] = curent_object['arguments']
                                    self.info("NO APPEND")
                                else:
                                    self.info("APPEND")
                                    if flags.parent not in query_object:
                                        query_object[flags.parent]=[]
                                    query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                            jump = None
                            if 'jump' in segment:
                                self.info("JUMP")
                                jump = segment['jump']
                            if None != jump:
                                tsi = 0
                                for ts in command['segments']:
                                    if ts['name'] == jump:
                                        self.info("Jumping from ", segment_index, tsi + 1)
                                        segment_index = tsi + 1
                                        break
                                    tsi += 1
                            in_argument = False
                    else:
                        self.info("in list")

                        if len(tokens) <= token_index:
                            self.info("at the end")
                            if True == flags.store_array:
                                if curent_object['mode'] not in query_object:
                                    query_object[curent_object['mode']] = []

                                query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                            else:
                                if None == flags.parent:
                                    #print curent_object
                                    query_object[curent_object['mode']] = curent_object['arguments']
                                    self.info("NO APPEND")

                                else:
                                    self.info("APPEND")
                                    if flags.parent not in query_object:
                                        query_object[flags.parent]=[]
                                    query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})

                        # look ahead to see if its a list ","
                        if len(tokens) > token_index:
                            self.info("--looking ahead")
                            # if its not exit
                            self.info("----", tokens[token_index]['data'])
                            if tokens[token_index]['data'] != ',':
                                self.info("---not list")
                                # only append object after argument collection is done
                                self.info("----------Adding", curent_object['mode'])
                                if True == flags.store_array:
                                    if curent_object['mode'] not in query_object:
                                        query_object[curent_object['mode']] = []

                                    query_object[curent_object['mode']].append({curent_object['mode']: curent_object['arguments']})
                                else:
                                    if None == flags.parent:
                                        #print curent_object
                                        query_object[curent_object['mode']] = curent_object['arguments']
                                        self.info("NO APPEND")

                                    else:
                                        self.info("APPEND")
                                        if flags.parent not in query_object:
                                            query_object[flags.parent]=[]
                                        query_object[flags.parent].append({curent_object['mode']: curent_object['arguments']})
                                jump = None
                                if 'jump' in segment:
                                    jump = segment['jump']
                                if None != jump:
                                    tsi = 0
                                    for ts in command['segments']:
                                        if ts['name'] == jump:
                                            self.info("Jumping from ", segment_index, tsi + 1)
                                            segment_index = tsi + 1
                                            break
                                        tsi += 1
                                in_argument = False
                            else:
                                self.info("------more list")
                                token_index += 1

        # This is where we exit if we reached the end of processing with a full length
        #print token_index,len(tokens)
        self.info(segment_index, token_index, len(tokens))


        self.info(curent_object)
        if token_index == len(tokens):

            result=self.validate(curent_object,tokens,token_index,segment,command,segment_index,query_object,query_mode)
            if False == result:
                return None
            else:
                return result

        return None





    # this is crappy, I'm just breaking up a giant function. Will clean later...
    def validate(self,curent_object,tokens,token_index,segment,command,segment_index,query_object,query_mode):
        self.info(curent_object)
        # so we have run out of text to match and everything is good so far
        self.info("############################think its a match")

        if 'arguments' not in curent_object and 'arguments' in segment:
            self.info("Missing argument in last element")
            bad = True
            return False

        # lets make sure the rest are optional
        if len(command['segments']) >= segment_index:
            self.info("still checking")
            bad = False
            for t in range(segment_index, len(command['segments'])):
                if 'optional' not in command['segments'][t]:
                    bad = True
                    return False

                else:
                    if not command['segments'][t]['optional']:
                        bad = True
                        return False

            if True == bad:
                self.info("Not successful. required arguments missing")
                return False

        self.info("Query object", query_object)
        if query_mode == 'select':
            # check to make sure functions are valid
            self.info("Validating Select Functions")
            if 'columns' in query_object:
                for node in query_object['columns']:
                    valid_function_name = False
                    is_function = False
                    if 'function' in node:
                        is_function = True
                        self.info("It's a function!")
                        for f in language['functions']:
                            if f['name'] == node['function']:
                                argindex = 1
                                if f['arguments'] is not None:
                                    for arg in f['arguments']:
                                        if arg['required']:
                                            # if this argument key is not in the node dict
                                            if 'argument{0}'.format(argindex) not in node:
                                                self.info("Missing arguments")
                                                return False
                                        argindex += 1

                                else:
                                    argindex = 0
                                if 'argument{0}'.format(argindex + 1) in node:
                                    self.info("Too many arguments")
                                    return False

                            valid_function_name = True
                            break
                    if False == valid_function_name and True == is_function:
                        self.info("FAIL", "This isnt a valid function", node['function'])
                        return False
            else:
                self.info("No columns in select")
                return False

        self.info("SUCCESS")
        #from pprint import pprint
        #pprint( sql_object)
        sql_object = {'mode': query_mode, 'meta': query_object}
        return sql_object

    # expand columns
    # TODO null trapping
    def expand_columns(self, query_object, columns):
        if 'columns' in query_object['meta']:
            expanded_select = []
            for item in query_object['meta']['columns']:
                if 'column' in item:
                    if item['column'] == '*':
                        for column in columns:
                            expanded_select.append({'column': column})
                    else:
                        expanded_select.append(item)
                if 'function' in item:
                    expanded_select.append(item)

            query_object['meta']['columns'] = expanded_select
        # ?? needed

    # support funcitons

    def get_sub_array(self, array, key=None):
        if None == key:
            if isinstance(array, str):
                return [array]
            else:
                return array
        if True == isinstance(array[key], list):
            return array[key]
        else:
            return [array[key]]

    # for tokens ['data']

    def get_sub_array_sub_key(self, array, key):
        temp_array = []

        for item in array:
            temp_array.append(item[key])

        return temp_array

    def single_array_match(self, needles, haystacks):
        """ Match a single or array of strings with with another string or array of strings"""

        # make needels an array, with or without a sub key
        if isinstance(needles, str):
            temp_needles = [needles]
        else:
            temp_needles = needles

        # make haystacks an array
        if isinstance(haystacks, str):
            temp_haystacks = [haystacks]
        else:
            temp_haystacks = haystacks

        # now we have 2 plain array/lists to compare

        index = 0
        for needle in temp_needles:
            # ran out of haystack to test. not a match
            if index >= len(temp_haystacks):
                return False
            haystack = temp_haystacks[index]
            # not a match
            if needle[0:1] != '{' and needle[-1] != '}':
                if needle.lower() != haystack.lower():
                    return False
            index += 1
        # if we got here it must match
        return True

    def info(self,msg, arg1=None, arg2=None, arg3=None):
        if True == self.debug:
            if arg3 is None and arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return
            if arg3 is None:
                print("{0} {1} {2}".format(msg, arg1, arg2))
                return
            if arg2 is None:
                print("{0} {1}".format(msg, arg1))
                return

            print("[{0}]".format(msg))
