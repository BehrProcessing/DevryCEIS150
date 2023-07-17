def function(inputs):                      #!!! example function initialization
    print(inputs,'function executed')
    return '(string/list/number/boolean)'
#Variable Types~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A=32 ; B=1.75 ; C='' ;D=[] ; E=False                   #!!! Use ; to save space
Integer = 7
Float   = 3.14
String  = 'string'
Boolean = True
List    = [Integer,Float,String,Boolean]

function(List)                           #!!! function call with List as inputs
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Class:                                      ###!!!initialization of class
    class_attribute='variable within the class outhside of methods'        #!!!
    def __init__(self):       #!!! class_object creates new objects' attributes
        self.instance_attribute='an attribute of all instances'            #!!!
        self.string='grdfhbadfhhddhfdgdsaw'
        self.integer=2
        self.float=2.2
        self.boolean=False
        self.list=[]
    def instance_method(self,X):  #!!! function within a class, (self) required
        Y=X+X
        Z=self.integer
        fstring=f'The sum of {X}+{X} is {Y}'
        print(fstring) #fstring allows for easy concatenation of variable types
        return Y
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
instance_object=Class()         #!!! recieves instance_attributes from __init__
instance_object.string='change string'
print(instance_object.instance_attribute)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~