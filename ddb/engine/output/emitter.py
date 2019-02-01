
from pprint import pprint
import yaml


class obj_formatter():
    class NonePointer:
        def __init__(self):
            self.alive=True

    def render_xml(self,obj,root='root',depth=0):
        """xml like output for python objects, very loose"""
        template="""<{0}>{1}</{0}>"""
        fragment=""
        if isinstance(obj,str):
            fragment+=template.format(root,obj)

        elif isinstance(obj,int):
            fragment+=template.format(root,obj)

        elif isinstance(obj,float):
            fragment+=template.format(root,obj)
        
        elif isinstance(obj,bool):
            fragment+=template.format(root,obj)
        elif  isinstance(obj,list):
            for item in obj:
                fragment+=self.render_xml(item,root=root,depth=depth+1)
        elif isinstance(obj,object):
            for item in obj:
                fragment+=self.render_xml(obj[item],root=item,depth=depth+1)
        else:
            fragment+=template.format("UNK",obj)

        if depth==0:
            fragment=template.format("root",fragment)
        return fragment

    def render_json(self,obj,depth=0):
        """json like output for python objects, very loose"""
        str_template='"{0}"'
        int_template="{0}"
        float_template="{0}"
        bool_template="{0}"
        array_template='['+'{0}'+']'
        tuple_template='"{0}":{1}'
        object_template='{{'+'{0}'+'}}'
        fragment=""
        if isinstance(obj,str):
            fragment+=str_template.format(obj)

        elif isinstance(obj,int):
            fragment+=int_template.format(obj)

        elif isinstance(obj,float):
            fragment+=float_template.format(obj)
        
        elif isinstance(obj,bool):
            fragment+=bool_template.format(obj)
        elif  isinstance(obj,list):
            partial=[]
            for item in obj:
                partial.append(self.render_json(item,depth=depth+1))
            if len(partial)>0:
                fragment+=array_template.format(",".join(map(str, partial)))
        elif isinstance(obj,object):
            partial=[]
            for item in obj:
                partial.append(tuple_template.format(item,self.render_json(obj[item],depth=depth+1)))
            if len(partial)>0:
                fragment+=object_template.format(",".join(map(str, partial))) 
        else:
            fragment+=template.format("UNK",obj)
        return fragment

    def render_yaml_old(self,obj,depth=0,indent=1):
        """Yaml like output for python objects, very loose"""
       
        empty_object_template="{"+"}"
        empty_array_template='[]'
        str_template="{0}"
        int_template="{0}"
        float_template="{0}"
        bool_template="{0}"
        array_template='- {0}'
        array_item_template='  {0}'
        tuple_template='{0}: {1}'
        object_template='{0}'
        yaml_template='---\n{0}\n...'
        fragments=[]
        no_padding=None
        if isinstance(obj,str):
            no_padding=True
            #fragments.append(
            return str_template.format(obj)
        elif isinstance(obj,int):
            no_padding=True
            #fragments.append(
            return int_template.format(obj)
        elif isinstance(obj,float):
            no_padding=True
            #fragments.append(
            return float_template.format(obj)
        elif isinstance(obj,bool):
            no_padding=True
            #fragments.append(
            return bool_template.format(obj)
        elif  isinstance(obj,list):
            if not obj:
                fragments.append(empty_array_template)
            else:
                for item in obj:
                    fragment=self.render_yaml(item,depth=depth+1,indent=indent)
                    if len(fragment)==1 and (isinstance(item,str) or isinstance(item,int) or isinstance(item,float) ):
                        fragments.append(array_template.format(fragment[0]))
                    else:
                        index=0
                        for partial in fragment:
                            if index==0:
                                fragments.append(array_template.format(partial))
                                index+=1
                            else:
                                fragments.append(array_item_template.format(partial))
                            
        elif isinstance(obj,object):
            #print ("OBJ",obj)
            if not obj:
                fragments.append(empty_object_template)
            else:
                for item in obj:
                    #print item,obj,obj[item]
                    fragment=self.render_yaml(obj[item],depth=depth+1,indent=indent)
                    #print("F", fragment)
                    cleaned=fragment[0].lstrip()
                    dont_skip=True
                    if len(cleaned)>0:
                        if cleaned[0]=='-' or ':' in cleaned:
                            dont_skip=None

                    if len(fragment)==1 and dont_skip:
                        fragments.append(tuple_template.format(item,fragment[0]))
                    else:
                        fragments.append(tuple_template.format(item,""))
                        for partial in fragment:
                            fragments.append(partial)
                    
        else:
            fragments.append(template.format("UNK",obj))

        if depth==0:
            return yaml_template.format("\n".join(fragments))

        #if no_padding:
        padding=" "
        #for i in range(0,indent): 
        #    padding=" "
        padded_fragments=[]
        for f in fragments:
            padded_fragments.append(padding+f)
        return padded_fragments

        return fragments
    
    def yaml_walk_path(self,path,root):
        obj=root

        # walk the path
        if path and len(path)>0:
            for trail in path:
                obj=obj[trail]
        return obj
        
    def yaml_get_parent_obj(self,path,root):
        if len(path)<2:
            return None
        sub_path=path[0:-1]
        #print (".".join([str(i) for i in sub_path]),"--",".".join([str(i) for i in path]))
        fragment=self.yaml_walk_path(sub_path,root)

        if isinstance(fragment,list):
            if len(sub_path)<1:
                return None
            sub_path=sub_path[0:-1]
            #print (".".join([str(i) for i in sub_path]),"--",".".join([str(i) for i in path]))
            fragment=self.yaml_walk_path(sub_path,root)


        key=""#sub_path[-1]
        if isinstance(fragment,list):
                    return {'key':key,'type':'list','obj':fragment,'depth':len(sub_path)}
        elif isinstance(fragment,dict):
                    return {'key':key,'type':'dict','obj':fragment,'depth':len(sub_path)}
        return None        
                  
    def yaml_get_next_obj_path(self,path,root):
        fragment=self.yaml_walk_path(path,root)
        
        #last_path=path.pop()
        # get next object in path
        if isinstance(fragment,list):
            for i,value in enumerate(fragment):
                path.append(i)
                return {'key':i,'type':'list','obj':value,'depth':len(path)}

        elif isinstance(fragment,dict):
            for i in fragment:
                path.append(i)
                return {'key':i,'type':'dict','obj':fragment[i],'depth':len(path)}
            

        # is this a simple entity?
        # if so, backup 1 level, and proceed to the next item
        #remove this last bit of path
        while len(path)>0:
            last_path=path.pop()
            
            if len(path)==0:
                temp_obj=root
            else:
                temp_obj=self.yaml_walk_path(path,root)
            
            # get the next path
            grab_next=None
            if isinstance(temp_obj,list):
                for i,value in enumerate(temp_obj):
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'list','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True


            elif isinstance(temp_obj,dict):
                for i in temp_obj:
                    value=temp_obj[i]
                    if grab_next:
                        path.append(i)
                        return {'key':i,'type':'dict','obj':value,'depth':len(path)}

                    if i==last_path:
                        grab_next=True
        return None

    def yaml_padding(self,indent,indent_spacing,array_depth=0):
        padding=""
        indent=indent-1
        if indent_spacing<=0:
            indent_spacing=1
        column_indent=(indent-array_depth)
        if column_indent<0:
            column_indent=0
        pad_len=column_indent*indent_spacing+array_depth*2
        for i in range(0,pad_len):
            padding+=" "
        return padding

    def render_yaml(self,data_obj,indent=0):
        obj=data_obj
        root=data_obj
        path=[]
        line=""
        last_fragment=None
        arr_depth=0
        newline=False
        while obj!=None:
            fragment=self.yaml_get_next_obj_path(path,root)
            parent_fragment=self.yaml_get_parent_obj(path,root)
            
            if None ==fragment:
                obj=None
                continue

            if  fragment['type']!='list':
                arr_depth=0
            if parent_fragment:
                if  parent_fragment['type']!='list':
                    arr_depth=0
                if  parent_fragment['type']=='list' and fragment['type']=='list' and last_fragment['depth']<fragment['depth']:
                    arr_depth+=1
                if  parent_fragment['type']=='list' and fragment['type']=='list' and last_fragment['depth']>fragment['depth']:
                    arr_depth-=1

            obj=fragment['obj']
            if fragment['type']=='dict':
                if newline==0:
                    line+="\n"
                    line+=self.yaml_padding(len(path),indent,arr_depth)
                else:
                    newline=0
                line+="{0}: ".format(fragment['key'])#+""+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)
                
            if fragment['type']=='list':
                if parent_fragment and fragment:
                    if parent_fragment['type']!='list' and  fragment['key']==0:
                        line+="\n"+self.yaml_padding(len(path)-1,indent,arr_depth)#+"("+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)+")"

                    elif  fragment['key']!=0:
                        line+="\n"+self.yaml_padding(len(path)-1,indent,arr_depth)#+"("+str(arr_depth)+'-'+str(len(path))+"-"+str(indent)+")"

                line+="- "
                newline=1
            
            if not isinstance(obj,list) and not  isinstance(obj,dict):
                line+="{0}\n".format(obj)
                newline=0
            last_fragment=fragment
        return line

    def get_indent(self,line):
        index_of=line.find('- ')
    
        cleaned_line=line
        index=len(line)-len(cleaned_line.lstrip())
        if index_of!=-1:
            index+=1
        
        return index

    def yaml_is_start(self,line):
        # the beginning
        if line=='---':
            return True
        return None

    def yaml_is_end(self,line):
        if line=='...':
            return True
        return None

    def yaml_is_array(self,line_cleaned):
        """determine if a string begins with an array identifyer '- '"""
        if None==line_cleaned:
            return False
        # we need a dash and a space. double dashes dont work etc...
        if len(line_cleaned)>1:
            if line_cleaned[0]=='-' and line_cleaned[1]==' ':
                return True
        return False
        
    def yaml_strip_array(self,line):
        """Strip array elements from string '- '"""
        index_of=line.find('- ')
        if index_of!=-1:
            str1=list(line)
            str1[index_of]=' '
            line="".join(str1)
        return line

    def yaml_is_comment(self,line):
        cleaned=line.lstrip()
        if len(cleaned)>0:
            if cleaned[0]=='#':
                return True
        return False

    def yaml_get_tuple(self,line):
        if self.yaml_is_comment(line):
            return None
        """Get key value pair from string with a colon delimiter"""
        index=line.find(':')
        if index==-1:
            return None
        
        key=self.yaml_return_data(line[0:index])
        data_index=index+1
        if data_index<len(line):
            data=line[data_index:].strip()
        else:
            data=None
        return {'key':key,'data':data}

    def yaml_return_data(self,data):
        
        data=data.strip()
        #maybe its quoted
        if len(data)>2:
            quoted=None
            if data[0]=="'" and data[-1]=="'":
                quoted=True
            if data[0]=='"' and data[-1]=='"':
                quoted=True
            if quoted:
                return data[1:-1]
        try:
            return int(data)
        except ValueError:
            pass
        try:
            return float(data)
        except ValueError:
            pass
        return data
       
    def yaml_dump(self,data=None,file=None):
        if not isinstance(data,str):
            data=self.render_yaml(data)
            print(data)
            
        yaml_data=self.yaml_load(data,file)
        pprint(yaml_data)

    def yaml_load(self,data=None,file=None):
        if file:
            with open(file) as content:
                data=content.read()

        lines=data.splitlines()
        
        root={}
        last_indent=None
        obj=root
        hash_map=[{'indent':0,'obj':obj}]
        obj_parent=root
        obj_parent_key=None
        obj_hash=[]
        for line in lines:
            if self.yaml_is_start(line):
                continue
            if self.yaml_is_end(line):
                break
            indent=self.get_indent(line)

            line_cleaned=line
            is_array=self.yaml_is_array(line_cleaned.strip())
        
            
            # I handle array creation            
            if  is_array:
                line_cleaned=self.yaml_strip_array(line_cleaned)
                line=line_cleaned
                arr_index=0
                while is_array:
                    make_new_array=True
                    if None==obj:
                        obj_parent[obj_parent_key]=[]
                        obj=obj_parent[obj_parent_key]
                        obj_hash['obj']=obj
                        obj_hash['indent']=indent
                        make_new_array=None
                        
                    elif arr_index==0:
                        for index in range(len(hash_map)-1,-1,-1):
                            # the search can only fall coreward, never grow.
                            if hash_map[index]['indent']==indent and isinstance(hash_map[index]['obj'],list):
                                obj=hash_map[index]['obj']
                                make_new_array=None
                                break
                    if make_new_array:
                        if isinstance(obj,list):
                            new_list=[]
                            obj.append(new_list)
                            obj=new_list
                            hash_map.append({'indent':indent,'obj':obj})
                        # TODO this may never happen. 
                        else:
                            obj=[]
                    line_cleaned=line
                    indent=self.get_indent(line)
                    is_array=self.yaml_is_array(line_cleaned.strip())
                    if is_array:
                        line_cleaned=self.yaml_strip_array(line_cleaned)
                        line=line_cleaned
                    arr_index+=1
                indent=self.get_indent(line)
        
            # I handle indent shrinkage, loading the last indent level object
            # shrinkage requires object location....
            if last_indent and  last_indent>indent:
                for index in range(len(hash_map)-1,-1,-1):
                    if hash_map[index]['indent']<=indent:
                        obj=hash_map[index]['obj']
                        break
                  
                          
            # i handle object creation
            # is it a tuple?
            line_tuple=self.yaml_get_tuple(line_cleaned)
            if line_tuple:
                if None == obj:
                    obj_parent[obj_parent_key]={}
                    obj=obj_parent[obj_parent_key]
                    obj_hash['obj']=obj
                    obj_hash['indent']=indent

                if isinstance(obj,list):
                    new_obj={}
                    obj.append(new_obj)
                    obj_parent=obj
                    obj_parent_key=len(obj)-1
                    obj=new_obj
                    obj_hash={'indent':indent,'obj':obj}
                    hash_map.append(obj_hash)

                # ok its a tuple... and it has data. lets just add it.
                if line_tuple['data']:
                    value=self.yaml_return_data(line_tuple['data'])
                    obj[line_tuple['key']]=value
                # well darn, no data. guess the next object is the data...
                else:
                    if  not isinstance(obj,list):
                        obj[line_tuple['key']]=None
                        obj_parent=obj
                        obj_parent_key=line_tuple['key']
                        obj=obj[line_tuple['key']]
                        obj_hash={'indent':indent,'obj':obj}
                        hash_map.append(obj_hash)
            else:
                # skip comments
                if self.yaml_is_comment(line):
                    continue

                if isinstance(obj,list):
                    value=self.yaml_return_data(line_cleaned)
                    obj.append(value)
            last_indent=indent
        return root
 


data={}
data['arr']=[]
data['arr'].append([2,3,4])
data['arr'].append([5,6,7])
data['nested2']=[[1,2,3],[4,5,6],[7,8,9],['a','b','c'],['a','b','c'],['a','b','c'],['a','b','c']]
data['array']=['a','b','c','d']
data['nested3']=[
        [['R',2,3,4,5,6],[0,2,3,4],[0,2,3,4],[0,2,3,4],],
        [['A',2,3,4],[0,2,3,4],[0,2,3,4],[0,2,3,4],],
        [['B',2,3,4],[0,2,3,4],[0,2,3,4],[0,2,3,4],],
]

data['group']={}
data['array2']={}
data['array2']['arr1']=[6,7,8]
data['array2']['arr2']=[9,8,7,6,"number",4,3,2,1,0,3,4,3]
op={}
op['sddc']='roc'
op['vcenter']="1"
op['cloudgw']=1.2
d={}
d['v2']=3
d['ve']=3
op['versions']=[1.2,1.3,d,5,{'1':{'l':1}},7]
data['group']['operations']=op
data['arr3']=[{'l':3}]
data['arr4']=[{'l':3},{'l':5}]
data['arr'].append([8,9,0])
data['list']=[]
o={}
o['key']='data'
o['key2']='data2'
data['list'].append(o)
data['list'].append(o)
data['list'].append(o)
data['list'].append(o)
data['list'].append({'pixxa':[6,7,8,{"d":"3"},0,0,'o']})

of=obj_formatter()
#json_data = of.render_json(data)
#xml_data  = of.render_xml(data,root='object')
yaml_data = of.render_yaml(data,indent=2)
# print json_data
# print xml_data
#print yaml_data
print "----------X"
#of.yaml_dump(file="/home/nd/.ddb/main/vov.ddb.yaml") 
#yaml_data=yaml.dump(data, default_flow_style=False)
print of.yaml_dump(yaml_data)
print (yaml_data)


# TODO YAML EMITTER, handle MULTIDIMENTIONAL ARRAYS properly. extra level of recursion
# TODO tree moon walker to NEVER increment indent, only decrement
# TODO default element on fail or exception?
# TODO object return, simple or complex.... for handeling feed me objects
# TODO handle inline objects.... [ ] , {  }  , "\n"= ','
# DONE read form file, as part of class
# TODO add argparse
# DONE array '-' Must have 1 space between it and whatever, else its a string
# TODO value assignment, double stripping array '-'
# TODO warnings ( catch, and in info)
# TODO if string has - : process better. need a lambda