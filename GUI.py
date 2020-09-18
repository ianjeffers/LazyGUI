# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import tkinter as tk
import tkinter.filedialog
from functools import partial
import inspect
import importlib
import os

class GUI():
    def __init__(self):
        
        #create a root window
        root = tk.Tk()
        root.geometry("600x200")
        root.grid_columnconfigure((0,1), weight=1)
        frame = tk.Frame(root, relief="ridge", borderwidth=2)
        frame.pack()
        #Passing arguments in the button declaration was running the method directly, this waits until the method to be called
        run_program = partial(self.display_result, frame)
        button = tk.Button(frame, text = "Select '.py' File", command = run_program)
        
        
        #Aesthetics and loading to GUI
        button['bg'] = 'gray' 
        button.pack()

        
        root.mainloop()
        
        
        
    def display_result(root, frame):
        
        def callMethod(entries, method_name, keyPressed):
            inputs = []
            for entry in entries:
                inputs.append(entry.get())
            l = tk.Label(frame, text=method_name(*inputs))    
            l.pack()
        def generateInputs(method_name, frame):
           inputList = []
           i = 0
           for arg in inspect.getfullargspec(method_name).args:
                
                #TODO// Add grid/grouping to tkinter and add removing/entry feature
                e = tk.Entry(frame)
                
                l = tk.Label(frame, text=("please enter a value for '" + arg + "'"))
                l.pack()
                inputList.append(e) 
                
           call_method = partial(callMethod, inputList, method_name)
           
           
           for inp in inputList:
                inputList[i].bind('<Return>', call_method)
                inputList[i].pack()
                i+=1
            
            
        
        enter = []
        filename = tk.filedialog.askopenfile(mode ='r', filetypes =[('Python Files', '*.py')])
        filename = filename.name
        head, tail = os.path.split(filename)
        tail = tail[:tail.rfind(".")]
        print(tail)
        enter = importlib.import_module(tail, package=None)

        for obj in dir(enter):   
            #Checks the objects aren't built-ins or inits
            if(obj[0] != '_' and obj[1] != '_'):
                obj = getattr(enter, obj)
                #If it's in fact a class, not an imported module like random/date/tkinter
                if(inspect.isclass(obj)):
                    
                    #Scrapes method String names from object
                    for method in dir(obj):
                        #Checks the objects aren't built-ins or inits
                        if(method[0] != '_' and method[1] != '_'):
                            #Creates a method that can be added to the button
                            #TODO// List method arguments needed and send them to generateInputs
                            
                            callableMethod = getattr(obj, method)
                            commandRunner = partial(generateInputs, callableMethod, frame)
                            
                            
                            button = tk.Button(frame, text = method, command = commandRunner)
                            button.pack()

obj = GUI()