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
        
    def plotProjectedDataPDF(self, targetAxis):
        colorScheme = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
        
        peaks = [0, 0]
        
        allData = np.concatenate(self._projectedData.values())
        
        f_of_D_min = allData[:,0].min()
        f_of_D_max = allData[:,0].max()
        
        Rm_subspaceLimits = [ f_of_D_min+0.1*(f_of_D_max-f_of_D_min),
                              f_of_D_max+0.1*(f_of_D_max-f_of_D_min)]
        X_plot = np.linspace( Rm_subspaceLimits[0], Rm_subspaceLimits[1], 1000)[:, np.newaxis]
        peaks = {}
        i = 0
        for key in self._projectedData:
            X = (self._projectedData[key][:,0])[:,np.newaxis]
            kde = KernelDensity(kernel='gaussian', bandwidth=0.3).fit(X)
            log_dens = kde.score_samples(X_plot)
            (m,jj) = max((v,jj) for jj,v in enumerate(np.exp(log_dens)))
            peaks[key] = X_plot[jj,0]
            targetAxis.fill( X_plot[:, 0] ,
                             np.exp(log_dens) ,
                             colorScheme[i], alpha=0.2,
                           )
            i = i + 1    
                                   
        currentAxisLimits = targetAxis.axis()
        targetAxis.stem(peaks.values(),np.array(targetAxis.axis())[3]*np.array([1,1]),'k', markerfmt=' ')
        targetAxis.axis(currentAxisLimits)
        self._peaks = peaks

    
        
   
    

