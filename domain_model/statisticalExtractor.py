import sys
import os

import re

class StatisticalExtractor():

    def __init__(self):
        sys.path.append(os.getcwd())
        self.content = None     #la cel·la es crea buida
        self.computer = Formula_Computer()
        self.previous_content = None
        self.previous_value = None
        
    def set_content(self, input_content, sheet):

        if not isinstance(input_content,str):
            #si no és un string és un numerical content
            self.content = Numerical_Content(input_content)           #assignar l'objecte content a l'atribut content
            self.content.value = Numerical_Value(input_content)
        else:
            if re.match(r'=',input_content):
                self.content = Formula_Content(input_content)
                try: 
                    result = self.computer.compute(input_content, sheet)
                except My_Circ_Exception:
                    self.content = Formula_Content(self.previous_content)
                    self.content.value = Numerical_Value(self.previous_value)
                    raise CircularDependencyException('CircularDependencyException') 
                except ValueError as err:
                    self.content = Content(self.previous_content)
                    self.content.value = Value(self.previous_value)
                    raise ValueError(err)
                self.content.value = Numerical_Value(result)

            else:    
                self.content = Text_Content(input_content)
                self.content.value = Text_Value(input_content)
                

    def get_content(self):
    
        return self.content.getter()



    def get_value(self, sheet):
        if isinstance(self.content,Formula_Content): 
            try:                                                    
                result = self.computer.compute(self.content.getter(), sheet)
            except My_Circ_Exception:
                raise CircularDependencyException('CircularDependencyException')

            self.content.value = Numerical_Value(result)
        return self.content.get_value()
    
    def Text_Value_2_Numerical_Value(self):
        self.content.value = Numerical_Value(float(self.content.getter()))
    
 