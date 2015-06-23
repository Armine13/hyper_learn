"""random thoughts - sampling_strategy, support code"""

import collections
import numpy as np
# from data_class_instance import *
# from i_data_model import *

DataClassInstance = collections.namedtuple('DataClassInstance', 'name color')
"""DataClassInstance defininition as a namedtuple to store data identifying
   info.

This information describing the data in hand is further used in plots or to
retrieve the data based on the data class attributes.

Attributes:
    name (str): Human readable string to identify the data in hand.
    color (str): color code to identify the data when plotting. The color
        should be specified in hexacode as '#00ff00'.

Note:
  In ordrder to see the expansion of the class code execute it with the
  `verbose=True` parameter.

:version: 0.0.1
:author: sik
"""

DBElement = collections.namedtuple('DBElement', 'dbeClass dbeModel dbeSamples')
"""DBElement defininition as a namedtuple to store all the information
   regarding a particular data class

Attributes:
    dbeClass (DataClassInstance): data base element class indentification \
                                  information.
    dbeModel (IDataModel): data base element model
    dbeSamples (nparray): data base element samples

Note:
  In ordrder to see the expansion of the class code execute it with the
  `verbose=True` parameter.

:version: 0.0.1
:author: sik
"""


class DataBase(dict):
    """DataBase is a (class, model, samples) triplet diccionary that can be
    accessed using the class name of the data.

    Note:
      * the names of the data class **must** be unique, since they are used \
        the dictionary key.

    Attributes:
      self (dictionary of DBElement): each element corresponds to a different
        group of data within the data base.

    :version: 0.0.1
    :author: sik
    """

    def __init__(self, dbelementList):
        """__init__ constructs a DataBase from the given parameters.(not fully
        implemnted, yet. Rightnow only accepted parameter is a DBElement list
        to be passed to the dict default __init__)

        .. todo:: [code] this method should be overloaded in order to take \
                  diferent instanciations

        :version: 0.0.1
        :author: sik
        """
        try:
            keyList = [e.dbeClass.name for e in dbelementList]
        except TypeError:
            eString = '{1}.__init__ TypeError, valid DBElement with \
                       DataClassInstance as dbeClass element was expected. \
                       Instead {2}, {3} types were given.'
            print eString.format(self.__class__,
                                 dbelementList[0].__class__,
                                 dbelementList[0].dbeClass.__class__)

        super(self.__class__, self).__init__(zip(keyList, dbelementList))

    def __str__(self):
        """
        formated console print of the DataBase object

        .. todo:: [code] maybe the element formating should be handeled by \
                DBElement. \
                see `stackOverflow <http://stackoverflow.com/questions/7914152/can-i-overwrite-the-string-form-of-a-namedtuple>`_ \
                and `the docs <http://docs.python.org/library/collections.html#collections.namedtuple>`_

        :version: 0.0.1
        :author: sik
        """
        # define the format strings for each DBElement attribute
        classFStr = "class: '{0.dbeClass.name:s}', '{0.dbeClass.color:s}'\n"
        modelFStr = "model: {0.dbeModel:s}\n"
        shapeFStr = "shape: {0.dbeSamples:s}\n"

        dbElementsReport = ""
        for dKey, dElement in self.items():
            dbElementsReport += "\n"

            for fStr, dType in zip([classFStr, modelFStr, shapeFStr],
                                   ['DataClassInstance', 'IDataModel',
                                    'np.array']):
                try:
                    dbElementsReport += "\t<{0:s}> ".format(dKey)
                    dbElementsReport += fStr.format(dElement)
                except TypeError:
                    print "un-expected dataType. ({} expected)".format(dType)

        return "{0:d}-class DataBase{1:s}".format(len(self), dbElementsReport)

    def get_range(self):
        """
        get_range returns the [xmin xmax ymin ymax] needed to display the data

        Return:
            Array of (min, max) tuples of all the data dimensions
        :rtype: array of tuples
        :version: 0.0.1
        :author: sik

        .. # I don't understand how to do this whithout numpy.
        .. todo:: [code][to Impl.] This is a copy-paste of the previous code structure
        """
        # cBoundaries=np.asarray([c.get_range()for c in self._data])
        # return[min(cBoundaries[:,0]),max(cBoundaries[:,1]),
        # min(cBoundaries[:,2]),max(cBoundaries[:,3])]

    def draw_models(self, axisId):
        """

        @param mplAxis axisId : 
        @return  :
        @author sik
        """
        pass

    def draw_samples(self, axisId):
        """

        @param mplAxis axisId : 
        @return  :
        @author sik
        """
        pass


class DataSet (DataBase):
    """
    .. todo:: [code] whole DataSet class

    :version:
    :author: sik
    """

    def draw_samples(self, axisId, fade=0.5):
        """
         draw_samples draws a scatter plot of the dataset data fading those \
         DataBase samples not belonging to the DataSet

        @param mplAxis axisId : 
        @param float fade : fading ratio
        @return  :
        @author sik
        """
        pass


def _test():
    """ test function to call when executing this file directly """

    nTestClasses = 3
    myClasses = [DataClassInstance('c{}'.format(i), '#fffff{}'.format(i))
                 for i in range(1, nTestClasses)]

    myDBEList = [DBElement(c, 'model_{}'.format(idx+1), np.array([0, idx]))
                 for idx, c in enumerate(myClasses)]

    dd = DataBase(myDBEList)
    print dd

    # myDBElementDictionary = dict(zip([x.name for x in myClasses], myDBEList))
    # for k in myDBElementDictionary.iterkeys():
    #     assert dd[k] == myDBElementDictionary[k]

if __name__ == '__main__':
    _test()
