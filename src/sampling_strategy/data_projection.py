"""random thoughts - sampling_strategy, DataBase projection support code.

   This module projects DataBase objects into a different space where to \
   perform the sampling
"""
from abc import ABCMeta, abstractmethod
from sklearn.decomposition import PCA
import numpy as np


class ProjectionModelFactory(object):
    """IProjectionModel Factory"""

    @staticmethod
    def createIProjectionModel(*argv, **kwargs):
        # First parameter is supposed to be the class name to instanciate
        try:
            if issubclass(eval(argv[0]), IProjectionModel):
                # return the subclass factoryMethod
                return eval(argv[0])._create(*argv[1:], **kwargs)
            else:
                raise TypeError
        except (TypeError, NameError):
            validTypeNames = [s.__name__ 
                              for s in IProjectionModel.__subclasses__()]
            raise TypeError("""'{0}' is an invalid IProjectionModel subclass. \
                            Valid type names are:\n\t{1:s}""".format(argv[0],
                            '\n\t'.join(validTypeNames)))


class IProjectionModel(object):
    """IProjectionModel is an abstract class to force equal signature between \
    all the projection model implementations. A projection model takes a \
    DataBase (or DataSet) and determines a new projection of the data.
     
     .. The instances of this class should overwrite its generative methods \ 
     .. in order to output projected data

    :version: 0.0.1
    :author: sik
    """
    # information about abstract classes
    #  http://tinyurl.com/l3awj4d
    #  http://tinyurl.com/k8acb9x
    __metaclass__ = ABCMeta

    @classmethod
    def _create(cls, *argv, **kwargs):
        """_create is method called from `ProjectionModelFactory` to trigger \
           the desired projection model creation.

            Args:
                cls : is the target projection model's class. \
                    It must be a subclass of IProjectionModel.
                *argv (tuple, optional): unnamed arguments to supply to the \
                                         instance creator.
                **kwargs (dict, optional): named arguments to supply to the \
                                           instance creator.
            Returns:
                   An initialized object of class **cls**

            :version: 0.0.1
            :author: sik

            .. todo:: [doc] manage to link ProjectionModelFactory code from \
                      the doc string
        """
        myObj = object.__new__(cls)
        myObj.__init__(*argv, **kwargs)
        return myObj

    # Here follow the methods required for an IProjectionModel implantation
    @abstractmethod
    def __init__(self, *argv, **kwargs):
        """ __init__ is the compulsory constructor method to be implemented \
            by subclasses, since it is called from \
            `ProjectionModelFactory._create()`.

            Note:
                If the projection model needs some fitting, here is where \
                it should take place.
        """
        pass

    @abstractmethod
    def display_base(self, ax, *argv, **kwargs):
        """ Display, into the **ax** handle, the projection model base in the
            original DataBase space reference frame.

            Args:
              ax (mpl:axis): The axis to plot on
              *argv (optional): tuple of unnamed argument values to pass \
                to `ax.plot`
              **kwargs (optional): Dictionary of keyword-arguments and values \
                to pass to `ax.plot`

            Returns: list of artists added to **ax**

        :rtype: list
        :version: 0.0.1
        :author: sik
        """
        pass

    @abstractmethod
    def project_data(self, data):
        """ Returns the data in the new projected space
        
            Args:
                data (np.array, shape(nSamp, nFeat)): data points to be \
                transformed (aka, testing data). Where, nSamp is the number \
                of samples and nFeat the number of features.

            Returns:
                An np.array containing the projection result in the form \
                `shape(nSamp, nFeat_)` where, nSamp is the number of samples \
                which is the same as in data, and nFeat_ is the new number \
                of features.
        """
        pass


class PMIdentity(IProjectionModel):
    """PMIdentity does no projection of the data, so that the projected space \
       is exaclty the same as the original one.
    """

    def __init__(self, *argv, **kwargs):
        pass

    def display_base(sefl, ax, *argv, **kwargs):
        aLimit = ax.axis()
        out1 = ax.plot(aLimit[:2], [0, 0], *argv, **kwargs)
        out2 = ax.plot([0, 0], aLimit[-2:], *argv, **kwargs)
        return out1, out2

    def project_data(self, data):
        return data


class PModelSingleFeat(IProjectionModel):
    """PModelSingleFeat takes a single feature of the data

    TODO: right now only handles 2D data and everything is hardcoded
    """

    def __init__(self, featureIndx=0, *argv, **kwargs):
        if featureIndx > 1:
            raise 'featureIndx should be 0 or 1'
        self._featureIndx = featureIndx

    def display_base(self, ax, *argv, **kwargs):
        aLimit = ax.axis()
        get_half = lambda minv, maxv: ((maxv-minv)/2)+minv

        if self._featureIndx == 0:
            yCenter = get_half(aLimit[2], aLimit[3])
            return ax.plot(aLimit[:2], [yCenter]*2, *argv, **kwargs)
        else:
            xCenter = get_half(aLimit[0], aLimit[1])
            return ax.plot([xCenter]*2, aLimit[-2:], *argv, **kwargs)

    def project_data(self, dataPoints):
        return dataPoints[:, self._featureIndx]


class PModelPCA(IProjectionModel):
    """ Use Principal Component Analysis (PCA) as projection model."""

    def __init__(self, db, *argv, **kwargs):
        numDims2Keep = 2
        data2fit = np.vstack([d.dbeSamples for d in db.itervalues()])
        self._transformation = PCA(n_components=numDims2Keep).fit(data2fit)

    def project_data(self, data):
        return self._transformation.transform(data)

    def display_base(self, ax, *argv, **kwargs):  # param_dict={}):
        """.. todo:: [code] merge both plot outputs """
        base = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        base_ = self._transformation.transform(6*base)
        out1 = ax.plot(base_[:2,  1], base_[:2,  0], *argv, **kwargs)
        out2 = ax.plot(base_[-2:, 1], base_[-2:, 0], *argv, **kwargs)
        return out1, out2


class PModelPCAsingleClass(PModelPCA):
    """ Force to tray the PCA in a single class data """
    def __init__(self, db, key, *argv, **kwargs):
        numDims2Keep = 2
        data2fit = db[key].dbeSamples
        self._transformation = PCA(n_components=numDims2Keep).fit(data2fit)


class PModelLDA(IProjectionModel):
    """ Use Linear Discriminant Analysis (LDA) as projection model."""
    def __init__(self):
        raise NotImplemented

    def display_base(self, axisId):
        raise NotImplemented

    def project_data(self, dataPoints):
        raise NotImplemented


def _test():
    import random
    from data_base_creator import DataSimulation
    import sampler_simulation_plot_helper as spl
    import matplotlib.pyplot as plt

    def shapeNameGen(n):
        # http://sahandsaba.com/python-iterators-generators.html
        # g = (random.random() < 0.4 for __ in itertools.count())
        types = IProjectionModel.__subclasses__()
        for i in range(n):
            yield random.choice(types).__name__

    myDb = DataSimulation().generate_default2MVGM_testcase(numSamples=1000,
                                                           randomSeed=1405898)
#    myDataBaseExample = d.generate_default2MVGM_testcase()

    myProjections = [ProjectionModelFactory.createIProjectionModel('PModelPCAsingleClass', myDb, 'red'),
                     ProjectionModelFactory.createIProjectionModel('PModelPCAsingleClass', myDb, 'blue'),
                     ProjectionModelFactory.createIProjectionModel('PModelPCA', myDb)]
 
    # print myDb
    fig, ax = plt.subplots()
    ax.axis([-3, 3, -3, 3])
    spl.plot_DataBase_in_dbSpace(ax, myDb)
    for proj, color in zip(myProjections,['r', 'b', 'k']):
        proj.display_base(ax,color,linewidth=2)
    plt.show()

if __name__ == '__main__':
    _test()
