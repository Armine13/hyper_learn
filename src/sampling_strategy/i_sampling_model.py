from random_sampler import *
from sklearn.neighbors import KernelDensity

class ISamplingModel (object):

    """
     ISamplingModel is an abstract class to instanciate all the sampling strategies
     in order to generate a DataSet.
     
     The SamplingModel takes the projected data using the ProjectionModel and selects
     the data samples to form the dataset based in some criteria.

    :version:
    :author: sik
    """
    __metaclass__ = ABCMeta

    @classmethod
    def _create(cls, *argv, **kwargs):
        """_create is method called from `SamplingModelFactory` to trigger \
           the desired sampling strategy model creation.

            Args:
                cls : is the target sampling model's class. \
                    It must be a subclass of ISamplingModel.
                *argv (tuple, optional): unnamed arguments to supply to the \
                                         instance creator.
                **kwargs (dict, optional): named arguments to supply to the \
                                           instance creator.
            Returns:
                   An initialized object of class **cls**

            :version: 0.0.1
            :author: sik

            .. todo:: [doc] manage to link SamplingModelFactory code from \
                      the doc string
        """
        myObj = object.__new__(cls)
        myObj.__init__(*argv, **kwargs)
        return myObj

    # Here follow the methods required for an ISamplingModel implantation
    @abstractmethod
    def __init__(self, *argv, **kwargs):
        """ __init__ is the compulsory constructor method to be implemented \
            by subclasses, since it is called from \
            `SamplingModelFactory._create()`.

            Note:
                If the sampling model needs some fitting, here is where \
                it should take place.
        """
        self._data = []
        self._peaks = [0, 0]
        pass
    
    def plotProjectedDataPDF(self, targetAxis, data1, data2):
        
        colorScheme = ['b', 'r']
        peaks = [0, 0]
        f_of_D_min = np.concatenate((data1, data2))[:,0].min()
        f_of_D_max = np.concatenate((data1, data2))[:,0].max()
        
        Rm_subspaceLimits = [ f_of_D_min+0.1*(f_of_D_max-f_of_D_min),
                              f_of_D_max+0.1*(f_of_D_max-f_of_D_min)]
        X_plot = np.linspace( Rm_subspaceLimits[0], Rm_subspaceLimits[1], 1000)[:, np.newaxis]
        
        for i, currentClass in enumerate([data1, data2]):
            X = (currentClass[:,0])[:,np.newaxis]
            kde = KernelDensity(kernel='gaussian', bandwidth=0.3).fit(X)
            log_dens = kde.score_samples(X_plot)
            (m,jj) = max((v,jj) for jj,v in enumerate(np.exp(log_dens)))
            peaks[i] = X_plot[jj,0]
            targetAxis.fill( X_plot[:, 0] ,
                             np.exp(log_dens) ,
                             colorScheme[i], alpha=0.2,
                           )
        currentAxisLimits = targetAxis.axis()
        targetAxis.stem(peaks,np.array(targetAxis.axis())[3]*np.array([1,1]),'k', markerfmt=' ')
        targetAxis.axis(currentAxisLimits)
        self._peaks = peaks
        
    def getPeaks(self):
        return self._peaks
        
    def drawSamplingProbability(self, targetAxis, sigmas):
        colorScheme = ['b:', 'r:']
        currentAxisLimits = np.array(targetAxis.axis())
        displayScalingFactor = ((2*np.pi*1)**0.5)*currentAxisLimits[3]*.4
        #print ((2*np.pi*np.array(sigma))**-0.5)
        X_plot = np.linspace( currentAxisLimits[0], currentAxisLimits[1], 100)[:, np.newaxis]
        for currentSigma in sigmas:
            for i, mu in enumerate(self._peaks):
                Y_plot = ((2*np.pi*currentSigma)**-0.5)*np.exp(-((X_plot-mu)**2)*(2*currentSigma)**-1)
                targetAxis.plot(X_plot,displayScalingFactor*Y_plot,colorScheme[i], alpha=0.8)
                targetAxis.plot(X_plot,displayScalingFactor*Y_plot,'k:', alpha=0.8)


#    def sampleData(self, mu, std, nSamples=20, ProbLabelFlip=0):
#        
#        pass


#    @abstractmethod
#    def display_base(self, ax, *argv, **kwargs):
#        """ Display, into the **ax** handle, the sampling model base in the
#            original DataBase space reference frame.
#
#            Args:
#              ax (mpl:axis): The axis to plot on
#              *argv (optional): tuple of unnamed argument values to pass \
#                to `ax.plot`
#              **kwargs (optional): Dictionary of keyword-arguments and values \
#                to pass to `ax.plot`
#
#            Returns: list of artists added to **ax**
#
#        :rtype: list
#        :version: 0.0.1
#        :author: sik
#        """
#        pass

#    @abstractmethod
#    def project_data(self, data):
#        """ Returns the data in the new projected space
#        
#            Args:
#                data (np.array, shape(nSamp, nFeat)): data points to be \
#                transformed (aka, testing data). Where, nSamp is the number \
#                of samples and nFeat the number of features.
#
#            Returns:
#                An np.array containing the projection result in the form \
#                `shape(nSamp, nFeat_)` where, nSamp is the number of samples \
#                which is the same as in data, and nFeat_ is the new number \
#                of features.
#        """
#        pass


