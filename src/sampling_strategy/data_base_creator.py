"""random thoughts - sampling_strategy, DataBase creation support code.

   This module generates DataBase objects for experimentation
"""

from data_base import *
from i_data_model import *             # needed for DataSimulation
import numpy as np                     # needed for DataSimulation


class DataBaseCreator(object):
    """
    DataBaseCreator is in charge of creating a DataBase object for \
    experimentation.

    The different implementations of DataBaseCreator are in charge of \
    creating the DataBase object as a DataBase copy, by means of simulating \
    data or parsing real data into DataBase object.

    :version: 0.0.1
    :author: sik
    """
#
#    def __init__(self, db):
#        """
#        This is used to freeze a dataset and convert this dataset into a \
#        DataBase
#
#        Args:
#            db (Database) : original DataBase object
#
#        :return: void
#        :version: 0.0.1
#        :author: sik
#        """
#        pass
#
#


class RealData (DataBaseCreator):
    """ RealData Class loads existing data into DataBase object

    :version:
    :author: sik
    """
    pass


class DataSimulation (DataBaseCreator):
    """
    Datasimulator is the DataBase constructor class for the simulation case.
    This class methods, allow to generate such data in multiple manners.

    :version: 0.0.1
    :author: sik

    .. todo:: [design] DataSimulation class should not know about \
                       MultiVariatedGaussianModel. \
                       Knowing IDataSimulationModel should be enough.
    """

    def __init__(self, randomSeed=None):
        """
        Initialize the data generation with a particular randomSeed
        """
        # np.random.seed(randomSeed)
        self._randomSeed = randomSeed

    def generate_default2MVGM_testcase(self, numSamples=30, randomSeed=None):
        """
        Generate a 2 Multi-variate Gaussian class example

        Args:
            numSamples (int, optional): number of samples to generate for each
            class. Defaults to 30.

        Return:
            a **two**-class DataBase object of 2D data. Both classes follow \
            multi-variate Gaussian distribution.

        :rtype: DataBase
        :version: 0.0.1
        :author: sik

        .. todo:: [doc] insert the 2D class plotting
        """
        # np.random.seed(self._randomSeed)
        np.random.seed(randomSeed)

        classes = [DataClassInstance('blue', '#9b59b6'),
                   DataClassInstance('red', '#e74c3c')]

        MVGaussMod = MultiVariatedGaussianModel
        models = [MVGaussMod(0, 1, 1.2, 1, 0.8),
                  MVGaussMod(0, 0, 1.3, 0.7, 0.3)]

        samples = [m.generate_data(numSamples) for m in models]

        return DataBase([DBElement(dbeClass=c, dbeModel=m, dbeSamples=s)
                         for c, m, s in zip(classes, models, samples)])


def _test():
    """ test function to call when executing this file directly """

    d = DataSimulation()
    myDataBaseExample = d.generate_default2MVGM_testcase()

    print [myDataBaseExample[a] for a in myDataBaseExample.keys()]
if __name__ == '__main__':
    _test()
