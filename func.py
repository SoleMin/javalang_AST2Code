import javalang

def AST2Code(root):
    code=''

    if root.package:
        code+= 'package '+root.package.name+';\n'
    for import_item in root.imports:
        code+= 'import '+('static ' if import_item.static else '') +import_item.path+ ('.*' if import_item.wildcard else '') + ';\n'
    childs=root.types
    for child in root.types:
        code+=func_dict[type(child).__name__](child)
    return code

def Nonetype(node):
    return ''

def FieldDeclaration2Code(node):
    code_snippet=''
    
    # for modifier in node.modifiers:
    #     code_snippet+=modifier+' '

    modifier_arr=[]
    for modifier in node.modifiers:
        modifier_arr.append(modifier)
    code_snippet+=' '.join(reversed(modifier_arr)) +' '
    
    code_snippet+=Type2Code(node.type)+' '
    for declarator in node.declarators:
        code_snippet+= func_dict[type(declarator).__name__](declarator)+','
    code_snippet=code_snippet.rstrip(',')

    return code_snippet+';\n'

def WhileStatement2Code(node):
    code_snippet=''
    if node.label:
        code_snippet+=node.label+':'

    code_snippet+='while('+func_dict[type(node.condition).__name__](node.condition)+')'
    code_snippet+=func_dict[type(node.body).__name__](node.body)
    return code_snippet

def ConstructorDeclaration2Code(node):
    code_snippet=''
    code_snippet+=' '.join(reversed(list(node.modifiers)))
    code_snippet+=' '+ node.name
    code_snippet=code_snippet.lstrip()
    paramter=''
 
    for pram in node.parameters:
        
        paramter+=' '.join(reversed(list(pram.modifiers))) +' '
        paramter+=Type2Code(pram.type)
        paramter+=('...' if pram.varargs else '')
        # paramter+= ('[]'*len(pram.type.dimensions))
        paramter+=' '+ pram.name +','

    code_snippet+='('+paramter.rstrip(',')+')'
    code_snippet+= ('throws ' +','.join(node.throws) if node.throws else '')
    code_snippet+='{\n'
    for child in node.body:
        code_snippet+= func_dict[type(child).__name__](child)
    return code_snippet+'}\n'

def ClassDeclaration2Code(node):
    code_snippet=''
    for annot in node.annotations:
        code_snippet+='@'+annot.name+'('+func_dict[type(annot.element).__name__](annot.element)+')\n'
    code_snippet+=(node.documentation+'\n' if node.documentation else '')
    modifier_arr=[]
    for modifier in node.modifiers:
        modifier_arr.append(modifier)
    code_snippet+=' '.join(reversed(modifier_arr)) +' '

    # for modifier in node.modifiers:
    #     code_snippet+=modifier+' ' 
    code_snippet+=' class '+node.name
    if node.type_parameters:
        code_snippet+='<'
        for param in node.type_parameters:
            code_snippet+=param.name+','
        
        code_snippet=code_snippet.rstrip(',') +'>'
    if node.implements:
        code_snippet+=' implements '
        code_snippet+=','.join(Type2Code(implement)for implement in node.implements)

    if node.extends:
        code_snippet+=' extends '+Type2Code(node.extends)
    code_snippet+='{\n'
    for class_item in node.body:
        code_snippet+=func_dict[type(class_item).__name__](class_item)

    return code_snippet+"}"
    
def MethodDeclaration2Code(node):
    code_snippet=(node.documentation+'\n' if node.documentation else '')
    if node.annotations:
        for annotation in node.annotations:
            code_snippet+='@'+annotation.name+'\n'
    code_snippet+=' '.join(reversed(list(node.modifiers))) +' '

    
    if node.type_parameters:
        code_snippet+='<'
        for type_param in node.type_parameters:
            code_snippet+=type_param.name+','
        code_snippet=code_snippet.rstrip(',')+'> '
        
    code_snippet+=(Type2Code(node.return_type) if node.return_type else 'void')+' '+node.name+'('
    paramter=''
    
    for pram in node.parameters:
        paramter+=' '.join(reversed(list(pram.modifiers))) +' '
        paramter+=Type2Code(pram.type)
        paramter+=('...' if pram.varargs else '')
        paramter+=' '+ pram.name +','

    code_snippet+= paramter.rstrip(',')+')'+('throws ' +','.join(node.throws)+' ' if node.throws else '')
    code_snippet += '{\n'
    if node.body:
        
        for method_item in node.body:
            code_snippet+=func_dict[type(method_item).__name__](method_item)
    code_snippet+= '}\n'
    return code_snippet

def InterfaceDeclaration2Code(node):
    code_snippet=(node.documentation+'\n' if node.documentation else '')
    if node.annotations:
        for annotation in node.annotations:
            code_snippet+='@'+annotation.name+'\n'
    for modifier in node.modifiers:
        code_snippet+=modifier+' ' 

    code_snippet+=' interface '+node.name
    if node.type_parameters:
        code_snippet+='<'
        code_snippet+=','.join(pram.name for pram in node.type_parameters)
        code_snippet+='>'
        
    if node.extends:
        code_snippet+=' extends '+','.join(Type2Code(extend) for extend in node.extends)
    
    
    code_snippet+='{'
    for b in node.body:
        code_snippet+=func_dict[type(b).__name__](b).rstrip('{\n}\n')+';\n'
    code_snippet+='}'
    return code_snippet

def LocalVariableDeclaration2Code(node):
    code_snippet=' '.join(reversed(list(node.modifiers))) +' '
    code_snippet+=Type2Code(node.type)+' '
    for declarator in node.declarators:
        code_snippet += func_dict[type(declarator).__name__](declarator) +','
    code_snippet=code_snippet.rstrip(',')
    return code_snippet+'; \n'

def VariableDeclarator2Code(node):
    code_snippet=node.name
    code_snippet+=('[]'*len(node.dimensions) if node.dimensions else '')+' ' 
    
    if node.initializer:
        code_snippet+= ' = '+func_dict[type(node.initializer).__name__](node.initializer)
    return code_snippet#+';\n'

def VariableDeclaration2Code(node):

    code_snippet=''
    code_snippet+=Type2Code(node.type)+' '
    operandr=''
    operandl=''

    # for declarator in node.declarators:
    #     operandr+=declarator.name +','
    #     operandl += func_dict[type(declarator.initializer).__name__](declarator.initializer)+','
    for declarator in node.declarators:
        operandl += func_dict[type(declarator).__name__](declarator)+','
        
    # code_snippet +=operandr.rstrip(',')+' = '+operandl.rstrip(',')
    code_snippet +=operandr.rstrip(',')+operandl.rstrip(',')
    return code_snippet#+';\n'
    
def Type2Code(node):

    if type(node).__name__ == 'BasicType':
        return node.name +('[]'*len(node.dimensions) if node.dimensions else '')
    elif type(node).__name__ == 'ReferenceType':
        code_snippet=node.name
        # if node.name in ['HashMap','HashSet']:
        if node.arguments != None:
            code_snippet+='<'
            for arg in node.arguments:
                if arg.pattern_type:
                    if arg.pattern_type=='extends':
                        code_snippet+='? ' +arg.pattern_type+' '
                    else:
                        code_snippet+=arg.pattern_type+','
                if arg.type:
                    code_snippet+=Type2Code(arg.type)+','
            code_snippet=code_snippet.rstrip(',')+'>'
        
        if node.sub_type:
            code_snippet+='.'+Type2Code(node.sub_type)
        code_snippet+=('[]'*len(node.dimensions) if node.dimensions else '')

        return code_snippet

def ClassCreator2Code(node):# 미완
    
    argments='('
    for arg in node.arguments:
        argments+=func_dict[type(arg).__name__](arg)+','
    
    argments=argments.rstrip(',')+')'
    code_snippet='new '+Type2Code(node.type)+argments
    if node.body:
        code_snippet+='{'
        for b in node.body:
            code_snippet+=func_dict[type(b).__name__](b)
        code_snippet+='}'
    if node.selectors:
        for index in node.selectors:
            if type(index).__name__ != 'ArraySelector':
                code_snippet+='.'    
            code_snippet+=func_dict[type(index).__name__](index)    
    return code_snippet

def MemberReference2Code(node):
    
    code_snippet=(''.join(node.prefix_operators) if node.prefix_operators else '')+(node.qualifier+'.' if node.qualifier else '')+node.member 
    selector=''
    if node.selectors:
        for index in node.selectors:
            if type(index).__name__ != 'ArraySelector':
                selector+='.'    
            selector+=func_dict[type(index).__name__](index)
    code_snippet+=selector
    return code_snippet+(''.join(node.postfix_operators) if node.postfix_operators else '')

def ForStatement2Code(node):
    code_snippet='for ( '
    code_snippet+=func_dict[type(node.control).__name__](node.control)
    # control= node.control
    # if node.control.init:
    #     if type(node.control.init) == list:
    #         code_snippet+= ''.join([func_dict[type(i).__name__](i).rstrip(';\n') for i in node.control.init])
    #     else:
    #         code_snippet+=func_dict[type(node.control.init).__name__](node.control.init).rstrip(';\n')
    
    # code_snippet+=';'
    # if node.control.condition:
    #     code_snippet+=func_dict[type(node.control.condition).__name__](node.control.condition)
    # code_snippet +=';'
    # if node.control.update:
    #     for update in node.control.update:
    #         code_snippet+=func_dict[type(update).__name__](update)
    code_snippet+= ')\n'
    
    code_snippet+= func_dict[type(node.body).__name__](node.body)
        
    return code_snippet

def ForControl2Code(node):
    code_snippet=''
    if node.init:
        if type(node.init) == list:
            code_snippet+= ','.join([func_dict[type(i).__name__](i).rstrip(';\n') for i in node.init])
        else:
            code_snippet+=func_dict[type(node.init).__name__](node.init).rstrip(';\n')
    
    code_snippet+=';'
    if node.condition:
        code_snippet+=func_dict[type(node.condition).__name__](node.condition)
    code_snippet +=';'
    if node.update:
        
        code_snippet+= ','.join([func_dict[type(update).__name__](update).rstrip(';\n') for update in node.update])
    return code_snippet

def EnhancedForControl2Code(node):
    code_snippet=''
    code_snippet+=func_dict[type(node.var).__name__](node.var)+':'
    code_snippet+=func_dict[type(node.iterable).__name__](node.iterable)
    return code_snippet

def IfStatement2Code(node):
    code_snippet='if ( '
    code_snippet+= func_dict[type(node.condition).__name__](node.condition)+')'
    code_snippet+='\n'+func_dict[type(node.then_statement).__name__](node.then_statement)+'\n'
    if node.else_statement:
        code_snippet+='else '+func_dict[type(node.else_statement).__name__](node.else_statement)
    return code_snippet
    
def BlockStatement2Code(node):
    code_snippet="{"
    for block_item in node.statements:
        code_snippet+=func_dict[type(block_item).__name__](block_item)
    code_snippet+="}"
    return code_snippet
    
def BinaryOperation2Code(node):
    code_snippet=''
    operandl=func_dict[type(node.operandl).__name__](node.operandl)
    if type(node.operandl).__name__== 'Assignment':
        code_snippet+='('+operandl+')'
    else:
        code_snippet+= operandl
    code_snippet+=' ' +node.operator +' '
    
    operandr=func_dict[type(node.operandr).__name__](node.operandr)
    if type(node.operandr).__name__== 'Assignment':
        code_snippet+='('+operandr+')'
    else:
        code_snippet+= operandr
    return '('+code_snippet+')'

def Literal2Code(node):
    code_snippet=node.value
    prefix=''.join(node.prefix_operators if node.prefix_operators else '')
    postfix=''.join(node.postfix_operators if node.postfix_operators else '')
    for s in node.selectors:
        if not type(s).__name__ =='ArraySelector':
            code_snippet+= '.'    
        code_snippet+=func_dict[type(s).__name__](s)
    return prefix+code_snippet+postfix

def ArrayCreator2Code(node):
    code_snippet='new '
    code_snippet+= Type2Code(node.type)
    for dim in node.dimensions:
        code_snippet+= '['+func_dict[type(dim).__name__](dim)+']'
    if node.initializer:
        code_snippet+=func_dict[type(node.initializer).__name__](node.initializer)
    return code_snippet

def ArrayInitializer2Code(node):
    code_snippet='{'
    for init in node.initializers:
        code_snippet+=func_dict[type(init).__name__](init)+','
    return code_snippet.rstrip(',')+'}'

def Cast2Code(node):
    code_snippet='('+Type2Code(node.type)+')'
    code_snippet+=func_dict[type(node.expression).__name__](node.expression)
    return code_snippet

def StatementExpression2Code(node):
    code_snippet=''
    # print(node)
    code_snippet+=func_dict[type(node.expression).__name__](node.expression)

    return code_snippet+';\n'

def Assignment2Code(node):
    
    code_snippet=func_dict[type(node.expressionl).__name__](node.expressionl)

    code_snippet+=' ' +node.type+' '
    code_snippet+= func_dict[type(node.value).__name__](node.value)
    return code_snippet

def MethodInvocation2Code(node):
    code_snippet=(node.qualifier+'.' if node.qualifier else '')
    code_snippet+=node.member+'('
    args=''
    
    for arg in node.arguments:
        args+=func_dict[type(arg).__name__](arg)+','
    code_snippet+=args.rstrip(',')+')'
    if node.selectors:
        for s in node.selectors:
            if not type(s).__name__ in ['ArraySelector']:
                code_snippet+= '.'
            code_snippet+=func_dict[type(s).__name__](s)
    prefix_operators=node.prefix_operators if node.prefix_operators else []
    postfix_operators=node.postfix_operators if node.postfix_operators else []
    
    return ''.join(prefix_operators)+code_snippet+''.join(postfix_operators)

def ArraySelector2Code(node):
    code_snippet='['
    code_snippet+=func_dict[type(node.index).__name__](node.index)
    code_snippet+=']'
    return code_snippet

def ReturnStatement2Code(node):
    code_snippet='return '
    expression=func_dict[type(node.expression).__name__](node.expression)
    return code_snippet+expression+';'

def TryStatement2Code(node):
    code_snippet='try'
    if node.resources:
        code_snippet+='('
        for resource in node.resources:
            code_snippet+=func_dict[type(resource).__name__](resource)
        code_snippet+=')'
        
    code_snippet+='{'
    for b in node.block:
        code_snippet+=func_dict[type(b).__name__](b)
    code_snippet+='\n}'
    if node.catches:
        for catch in node.catches:
            code_snippet+= func_dict[type(catch).__name__](catch)
    return code_snippet

def CatchClause2Code(node):

    code_snippet= 'catch ('+func_dict[type(node.parameter).__name__](node.parameter) +')'
    code_snippet+='{\n'
    for catch_block in node.block:
        code_snippet+=func_dict[type(catch_block).__name__](catch_block)
    code_snippet+='}\n'

    return code_snippet

def CatchClauseParameter2Code(node):
    code_snippet=''
    for p in node.types:
        code_snippet+=p+' '
    code_snippet+=node.name
    return code_snippet

def ThrowStatement2Code(node):
    code_snippet='throw ('
    code_snippet+=func_dict[type(node.expression).__name__](node.expression)
    code_snippet+=')'
    return code_snippet +';'

def TryResource2Code(node):
    code_snippet=Type2Code(node.type)+' '
    code_snippet+= node.name

    code_snippet+='='+func_dict[type(node.value).__name__](node.value)
    return code_snippet

def This2Code(node):
    prefix=''.join(node.prefix_operators if node.prefix_operators else '')
    postfix=''.join(node.postfix_operators if node.postfix_operators else '')

    code_snippet='this'
    for s in node.selectors:
        if not type(s).__name__ =='ArraySelector':
            code_snippet+= '.'    
        code_snippet+=func_dict[type(s).__name__](s)
    return prefix+code_snippet+postfix

def TernaryExpression2Code(node):
    code_snippet='('
    if node.condition:
        code_snippet+=func_dict[type(node.condition).__name__](node.condition)#.lstrip('(').rstrip(')')
    code_snippet+='?'
    if node.if_true:
        if type(node.if_true).__name__ == 'Assignment':
            code_snippet+='('+func_dict[type(node.if_true).__name__](node.if_true) +')'
        else:
            code_snippet+=func_dict[type(node.if_true).__name__](node.if_true)
    code_snippet+=':'
    if node.if_false:
        if type(node.if_false).__name__ == 'Assignment':
            code_snippet+='('+func_dict[type(node.if_false).__name__](node.if_false) +')'
        else:
            code_snippet+=func_dict[type(node.if_false).__name__](node.if_false)
    code_snippet+=')'
    return code_snippet

def BreakStatement2Code(node):
    code_snippet='break'
    return code_snippet+';'

def ExplicitConstructorInvocation2Code(node):
    
    code_snippet='this('
    for argument in node.arguments:
        code_snippet+=func_dict[type(argument).__name__](argument)+','
    code_snippet=code_snippet.rstrip(',')
    code_snippet+=')'
    return code_snippet

def DoStatement2Code(node):
    code_snippet='do '+func_dict[type(node.body).__name__](node.body)
    code_snippet+='while('+func_dict[type(node.condition).__name__](node.condition)+')'
    return code_snippet+';'

def ContinueStatement2Code(node):
    code_snippet='continue' 
    if node.goto:
        code_snippet+=' '+node.goto
    return code_snippet+';'

def Statement2Code(node):
    return ';'

def SuperConstructorInvocation2Code(node):
    code_snippet='super'
    code_snippet+='('
    if node.arguments:
        for arg in node.arguments:
            code_snippet+=func_dict[type(arg).__name__](arg)
    code_snippet+=')'
        
    return code_snippet

def SwitchStatement2Code(node):
    code_snippet='switch('+func_dict[type(node.expression).__name__](node.expression)+'){\n'

    for case in node.cases:
        if case.case:
            code_snippet+='case '
            for cons in case.case:
                code_snippet+=func_dict[type(cons).__name__](cons)+','
            code_snippet=code_snippet.rstrip(',')
        else:
            code_snippet+='default '
        code_snippet+=':'
        for statement in case.statements:
            code_snippet+=func_dict[type(statement).__name__](statement)
        code_snippet+='\n'

    return code_snippet+'}\n'

def AssertStatement2Code(node):
    code_snippet='assert '
    code_snippet+=func_dict[type(node.condition).__name__](node.condition)
    return code_snippet+';\n'

def SuperMethodInvocation2Code(node):
    code_snippet='super.'
    code_snippet+=node.member
    return code_snippet+'()'

def BasicType2Code(node):
 
    return node.name +('[]'*len(node.dimensions) if node.dimensions else '')

def LambdaExpression2Code(node):
    code_snippet=''
    code_snippet+=','.join(func_dict[type(pram).__name__](pram) for pram in node.parameters)
    if len(node.parameters)>1:
        code_snippet='('+code_snippet+')'

    code_snippet+='->'
    if type(node.body) ==list:
            code_snippet+='{'
            code_snippet+=''.join(func_dict[type(b).__name__](b) for b in node.body)
            code_snippet+='}'
    else:
        code_snippet+=func_dict[type(node.body).__name__](node.body)
    return code_snippet
    
def InferredFormalParameter2Code(node):
    return node.name

func_dict={"ClassCreator":ClassCreator2Code,
"Literal":Literal2Code,
    'BinaryOperation':BinaryOperation2Code,
    'MemberReference':MemberReference2Code,
    'BlockStatement':BlockStatement2Code,
    'LocalVariableDeclaration':LocalVariableDeclaration2Code,
    'VariableDeclaration':VariableDeclaration2Code,
    'VariableDeclarator':VariableDeclarator2Code,
    'ArrayCreator': ArrayCreator2Code,
    'StatementExpression':StatementExpression2Code,
    'ArraySelector':ArraySelector2Code,
    'MethodInvocation':MethodInvocation2Code,
    'Assignment':Assignment2Code,
    'IfStatement':IfStatement2Code,
    'ForStatement':ForStatement2Code,
    'MethodDeclaration':MethodDeclaration2Code,
    'Cast':Cast2Code,
    'ReturnStatement':ReturnStatement2Code,
    'ClassDeclaration':ClassDeclaration2Code,
    'FieldDeclaration':FieldDeclaration2Code,
    'NoneType':Nonetype,
    'ConstructorDeclaration':ConstructorDeclaration2Code,
    'WhileStatement':WhileStatement2Code,
    'TryStatement':TryStatement2Code,
    'CatchClauseParameter':CatchClauseParameter2Code,
    'ThrowStatement':ThrowStatement2Code,
    'CatchClause':CatchClause2Code,
    'TryResource':TryResource2Code,
    'This':This2Code,
    'TernaryExpression':TernaryExpression2Code,
    'BreakStatement':BreakStatement2Code,
    'ExplicitConstructorInvocation':ExplicitConstructorInvocation2Code,
    'DoStatement':DoStatement2Code,
    'InterfaceDeclaration':InterfaceDeclaration2Code,
    'ContinueStatement':ContinueStatement2Code,
    'Statement':Statement2Code,
    'ArrayInitializer':ArrayInitializer2Code,
    'SuperConstructorInvocation':SuperConstructorInvocation2Code,
    'SwitchStatement':SwitchStatement2Code,
    'EnhancedForControl':EnhancedForControl2Code,
    'ForControl':ForControl2Code,
    'ReferenceType':Type2Code,
    'AssertStatement':AssertStatement2Code,
    'SuperMethodInvocation':SuperMethodInvocation2Code,
    'BasicType':BasicType2Code,
    'LambdaExpression':LambdaExpression2Code,
    'InferredFormalParameter':InferredFormalParameter2Code
}