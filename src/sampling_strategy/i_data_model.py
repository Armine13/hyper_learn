"""random thoughts - sampling_strategy, real data model(ing) support code.

   This module generates (or fits) the real data.
   Here, **Real Data** refers to the data stored in a DataBase object.
"""

from abc import ABCMeta, abstractmethod
import numpy as np                              # MultiVariatedGaussianModel
import matplotlib.mlab as mlab                  # MultiVariatedGaussianModel


class IDataModel(object):
    """IDataModel is an abstract class to force equal signature between \
    generative and fitted data models present in DataBase class.

    :version: 0.0.1
    :author: sik
    """
    # information about abstract classes
    #  http://tinyurl.com/l3awj4d
    #  http://tinyurl.com/k8acb9x
    __metaclass__ = ABCMeta

    def __init__(self):
        """ IDataModel.__init__ 
        .. todo::
           [design] should be an abstractmethod to force implementation? or
           should I remove the whole thing?

        :version: 0.0.1
        :author: sik
        """
        # information in pytonic constructors:
        #  http://tinyurl.com/3758j8u
        #  http://tinyurl.com/424tbt7
        #  http://tinyurl.com/lrownat
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def draw_2Disoc(self, ax, param_dict={}):
        """draw_2Disoc draws iso-value contours in order to illustrate the
        model distribution.

        Args:
            ax (axes): The axes to draw to
            param_dict (dict, optional): Dictionary of kwargs to pass to \
            ax.plot

        Returns:
            A list of artists added to **ax** while plotting

        :rtype: list
        :version: 0.0.1
        :author: sik

        Warning:
            The axis limits are not modified, therefore data might be being
            ploted **outside** of the visible range.

        .. todo:: **[design]** who should belong to the drawing signature?
        Note:
            I'm not sure if this function should belong to:

            * the object, since it knows all the information about itself
            * :mod:`sampler_simulation_plot_helper`, since is the collection of
              plotting functions
        """
        pass


class IDataSimulationModel (IDataModel):
    """IDataModel is an abstract class to force equal signature between \
    all the data generative models.

    :version: 0.0.1
    :author: sik
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def generate_data(self, numSamples):
        """generate_data generate `numSamples` data points that follow the \
        model described by `self`.

        Args:
          numSamples (int): Number of samples to generate

        Returns:
          nparray: data points in [[x1, y1, ..],[x2, y2, ..]] form

        :version: 0.0.1
        :author: sik
        """
        pass

    @abstractmethod
    def get_model_information(self):
        """get_model_information returns the model parameters dictionary.

        Returns:
          dict: Dictionary of {'parameter':value}

        :version: 0.0.1
        :author: sik
        """
        pass


class MultiVariatedGaussianModel (IDataSimulationModel):
    """MultiVariatedGaussianModel implements an IDataSimulationModel as a multi-variate gaussian in order to simulate DataBase samples that behaves as such.

    Attributes:
        _muX (float): x mean value.
        _muY (float): y mean value.
        _sigmaX  (float): variance along x.
        _sigmaY  (float): variance along y.
        _sigmaXY (float): x,y covariance.

    :version:
    :author: sik
    """
    __slots__ = ["_muX", "_muY", "_sigmaX", "_sigmaY", "_sigmaXY"]

    def __init__(self, *args, **kwargs):
        """ The following parameters can be specified in order to define define
        a multivariate 2D Gaussian model. Otherwise, defaults my apply. Any
        other argument would create an exception.

        Attributes:
            muX (float, optional): x mean value. Defaults to 0
            muY (float, optional): y mean value. Defaults to 0
            sigmaX  (float, optional): variance along x. Defaults to 1
            sigmaY  (float, optional): variance along y. Defaults to 1
            sigmaXY (float, optional): x,y covariance. Defaults to 0.

        Example:
            MultiVariatedGaussianModel(muX=0, muY=0,
                                       sigmaX=1, sigmaY=1, sigmaXY=0)

        TODO: this example should be done properly (create model, get samples,
        check that samples follow the expected)
    """
        # args -- tuple of anonymous arguments
        # kwargs -- dictionary of named arguments
        possibleArguments = {'muX', 'muY', 'sigmaX', 'sigmaY', 'sigmaXY'}
        extraNamedArguments = kwargs.viewkeys() - possibleArguments
        if extraNamedArguments:
            raise Exception("Invalid args: " + ', '.join(extraNamedArguments))
        elif len(args) > 6:
            raise Exception("Too many anonymous arguments")
        else:
            defaultValues = [0, 0, 1, 1, 0]
            args = list(args)
            args.extend(defaultValues[len(args):])
            self._muX     = kwargs.pop('muX',     args[0])
            self._muY     = kwargs.pop('muY',     args[1])
            self._sigmaX  = kwargs.pop('sigmaX',  args[2])
            self._sigmaY  = kwargs.pop('sigmaY',  args[3])
            self._sigmaXY = kwargs.pop('sigmaXY', args[4])

    def get_model_information(self):
        """Returns the information of the multi-variate 2D Gaussian Model as a dictionary

        Returns:
            {'xMean':_muX, 'yMean':_muY, 'xSTD':_sigmaX, 'ySTD':_sigmaY, \
            'xySTD':_sigmaXY,}

        :version: 0.0.1
        :author: sik
        """
        return dict(zip(['xMean', 'yMean', 'xSTD', 'ySTD', 'xySTD'],
                        [self._muX, self._muY, self._sigmaX, self._sigmaY,
                         self._sigmaXY]))

    def __str__(self):
        return 'Real-Data simulation (2D multi-variate Model):\n' \
               '\tmean x:{0}, y:{1}\n' \
               '\tSTD  x:{2}, y:{3}, xy:{4}' \
               '\n'.format(self._muX, self._muY, self._sigmaX, self._sigmaY,
                           self._sigmaXY)

    def generate_data(self, numSamples):
        """TODO: import parent documentation, while changing version and author
        """
        return np.random.multivariate_normal(
            [self._muX, self._muY],
            [[self._sigmaX, self._sigmaXY], [self._sigmaXY, self._sigmaY]],
            numSamples)

    def draw_2Disoc(self, axisId, param_dict={}):
        # Mixing the default parameters with param_dict. param_dict has
        # priority
        param_dictDefaults = {'colors': 'k',
                              'linewidths': np.arange(.5, 2, .25)}
        param_dictDefaults.update(param_dict)

        aLimits = axisId.axis()
        delta = (aLimits[1] - aLimits[0])/100
        X, Y = np.meshgrid(np.arange(aLimits[0], aLimits[1], delta),
                           np.arange(aLimits[0], aLimits[1], delta))
        Z = mlab.bivariate_normal(X, Y, self._sigmaX, self._sigmaY,
                                  self._muX, self._muY, self._sigmaXY)

        axisId.contour(X, Y, Z/Z.max(),     # data
                       4,                   # 4 isolines
                       **param_dictDefaults)


def _test():
    """ test function to call when executing this file directly """
    import matplotlib.pyplot as plt
    # import numpy as np
    # import matplotlib.mlab as mlab

    m0 = MultiVariatedGaussianModel()
    print m0
    print m0.get_model_information()

    ss = m0.generate_data(1000)
    fig, (ax0, ax1) = plt.subplots(ncols=2)
    ax0.scatter(ss[:, 0], ss[:, 1])
#    m0.draw_2Disoc(ax0)

    m1 = MultiVariatedGaussianModel(muX=1, muY=3, sigmaXY=10)
    ss = m1.generate_data(20)
    ax1.scatter(ss[:, 0], ss[:, 1])
#    m1.draw_2Disoc(ax1)
    m1 = MultiVariatedGaussianModel(3, 1, sigmaXY=10)
    ss = m1.generate_data(20)
    ax1.scatter(ss[:, 0], ss[:, 1])
#    m1.draw_2Disoc(ax1)
    fig.show()

if __name__ == '__main__':
    _test()
