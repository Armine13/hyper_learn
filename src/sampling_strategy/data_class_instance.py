class DataClassInstance:
    """ This is a class to define a structure storing information of the data
    class in order to identify such data class.

    The stored fields are:
        name  = 'data identifier name'
        color = '#00ff00'
    """
    def __init__(self, name, color):
        self._name  = name
        self._color = color
