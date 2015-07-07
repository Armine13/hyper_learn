from random_sampler import *
from sklearn.neighbors import KernelDensity

colorScheme = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
        
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
        
        pass
    
    def drawSamplingProbability(self, targetAxis, sigmas):
        self._sigmas = sigmas
        currentAxisLimits = np.array(targetAxis.axis())
        displayScalingFactor = ((2*np.pi*1)**0.5)*currentAxisLimits[3]*.4
        X_plot = np.linspace( currentAxisLimits[0], currentAxisLimits[1], 100)[:, np.newaxis]
        for currentSigma in sigmas:
            for i, mu in enumerate(self._peaks.values()):
                Y_plot = ((2*np.pi*currentSigma)**-0.5)*np.exp(-((X_plot-mu)**2)*(2*currentSigma)**-1)
                targetAxis.plot(X_plot,displayScalingFactor*Y_plot, colorScheme[i]+":", alpha=0.8)
        
    def plotProjectedDataPDF(self, targetAxis):
        
        allData = np.concatenate(self._projectedData.values())
        
        f_of_D_min = allData[:,0].min()
        f_of_D_max = allData[:,0].max()
        
        Rm_subspaceLimits = [ f_of_D_min+0.1*(f_of_D_max-f_of_D_min),
                              f_of_D_max+0.1*(f_of_D_max-f_of_D_min)]
        X_plot = np.linspace( Rm_subspaceLimits[0], Rm_subspaceLimits[1], 1000)[:, np.newaxis]
        peaks = {}
        ii = 0
        for key in self._projectedData:
            X = (self._projectedData[key][:,0])[:,np.newaxis]
            kde = KernelDensity(kernel='gaussian', bandwidth=0.3).fit(X)
            log_dens = kde.score_samples(X_plot)
            (m,jj) = max((v,jj) for jj,v in enumerate(np.exp(log_dens)))
            peaks[key] = X_plot[jj,0]
            targetAxis.fill( X_plot[:, 0] ,
                             np.exp(log_dens) ,
                             colorScheme[ii], alpha=0.2,
                           )
            ii = ii + 1    
                                   
        currentAxisLimits = targetAxis.axis()
        
        #The line below doesn't work for D > 2: ValueError("x and y must have same first dimension")
        #TODO: Fix for D > 2
        targetAxis.stem(peaks.values(),np.array(targetAxis.axis())[3]*np.array([1,1]),'k', markerfmt=' ')
        targetAxis.axis(currentAxisLimits)
        self._peaks = peaks