from data_class_instance import *

class DataClasses(object):
    def __new__(cls):
        return [DataClassInstance('blue', '#9b59b6'),
                DataClassInstance('red', '#e74c3c')]

    def get_class_names(self):
        return list(currentClass._name for currentClass in self)