#!!! Message Center !!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Welcome=['Hello and welcome to the Input Function Control',
          'This program is currently being testing.',     
          '-note inputs are not case sensitive']
Stop=['!---Process Terminated---!',]             #printed when ending a command
#!!! CLient command interface !!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Y='Y'   ; N='N' ; confirm=[N.lower(),Y.lower()]         #!!!  Client validation
L='List'; O='Options' ; I='Input' ; C='Calc' ; S='Stop' #!!!Command identifiers
new_commands='whatever you want client to type'         #!!!new_command example
Commands=[L,O,I,C,S,new_commands]                
#^ add new_commands to Commands[] 
#all commands must have the same index in Commands and CmdMngr
#create a new function to run when client enters new_command string as input
#~~~new_functions TEMPLATE~~~~~#!!! copy/ paste/ rename and build
def new_functions(Run) :
   if not START and Run==Commands.index(new_commands):
       print('new_function executed') #example function body  
   return "(string/list to be printed or '' to run function without printing)"
#v add new_function to CmdMngr in the function Run
START=1                                                #!!!  Command restricter
#!!! Function Command Center  !!!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def Run(select,userInput):
  CmdMngr=[0,0,0,0,0,0]
  CmdMngr[0]='printing list'
  CmdMngr[1]=Commands
  CmdMngr[2]='enter values'
  CmdMngr[3]='calculate'
  CmdMngr[4]=Stop
  CmdMngr[5]=new_functions(select)                  
  CmdMngr.append(Welcome)
  if type(CmdMngr[select]) is list and CmdMngr[select]!= Commands:
    for iteration in CmdMngr[select]: #!!! Prints lists line by line in console
      print(iteration)
  else:
    print(CmdMngr[select],end='')
  print('\n"newline"')
    
def Check_Input(Question,requestType):#!!! Check input for numbers,commands,Y/N
  if not START:
    cmds_lower=[] ; Validated=False 
    for cmd in Commands:
      cmds_lower.append(cmd.lower())
    while not Validated: 
      print(Question,end=' ')
      if type(requestType) is list:
        print(f'({Y}/{N}):',end=' ')
      userInput=input().lower().replace(',','')
      isDigit=userInput.replace('.','').isdigit()
      if type(requestType) is int and isDigit and userInput.count('.')<2:
        Validated=True ; userInput=float(userInput)                        
      elif userInput in cmds_lower:
        Run(cmds_lower.index(userInput),userInput)
        Validated=True ; userInput=Commands
      elif  type(requestType) is list and userInput in confirm:
        Validated=True 
      else:
          if type(requestType) is list:
            print(f'"{userInput}"!?',end=' ')
          elif type(requestType) is int:
            print(f'"{userInput}" is a string, please enter a number')
          else:    
            print(f'"{userInput}" is not a valid command')
    result=[userInput]
    return result
START=0
Run(len(Commands),'') 
while True:
    Check_Input('pick any number:', 0)
    Check_Input(Commands,'')
    while Check_Input('Would you like to continue?', confirm)[0]==confirm[0]:
        Denied=1

      