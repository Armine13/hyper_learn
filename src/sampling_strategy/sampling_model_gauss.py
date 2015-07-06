from i_sampling_model import *
from sklearn.neighbors import KernelDensity

class SamplingModelGauss (ISamplingModel):
    """
    :version:
    :author: sik
    """
    def __init__(self, db, projectionModel, *argv, **kwargs):
        self._data = db
        self._projectedData = {}
        for key, t in db.iteritems():        
            self._projectedData[key] = projectionModel.project_data(db[key].dbeSamples)
            self._n = len(db[key].dbeSamples)
            self._n_classes = len(self._data)
            
        #pass
        
    def drawSamplingProbability(self, targetAxis, sigmas):
        self._sigmas = sigmas
        colorScheme = ['b:', 'r:']
        currentAxisLimits = np.array(targetAxis.axis())
        displayScalingFactor = ((2*np.pi*1)**0.5)*currentAxisLimits[3]*.4
        #print ((2*np.pi*np.array(sigma))**-0.5)
        X_plot = np.linspace( currentAxisLimits[0], currentAxisLimits[1], 100)[:, np.newaxis]
        for currentSigma in sigmas:
            for i, mu in enumerate(self._peaks.values()):
                Y_plot = ((2*np.pi*currentSigma)**-0.5)*np.exp(-((X_plot-mu)**2)*(2*currentSigma)**-1)
                targetAxis.plot(X_plot,displayScalingFactor*Y_plot,colorScheme[i], alpha=0.8)
                targetAxis.plot(X_plot,displayScalingFactor*Y_plot,'k:', alpha=0.8)

    def sampleData(self, std, nSamples, ProbLabelFlip):
        # data must be 1D
        # TODO: modify for D > 1 projections
        assert nSamples <= self._n, 'number of samples exceeds the number of points in data'
        flipLabel = {}
        selectedSamples = {}
        for key in self._projectedData:
            d = self._projectedData[key][:,0]
            selectedSamples[key] = np.zeros((0,), dtype=np.integer)
            xCandidate = np.random.normal(self._peaks[key], std, nSamples)[:, np.newaxis]
            for x in xCandidate:
                sampleDistance = (d.astype(float) - x) ** 2        
                #for sampleIdx in selectedSamples[key]:
                #    sampleDistance[sampleIdx] = np.inf
                xx = [(v,jj) for jj,v in enumerate(sampleDistance)]
                (m,jj) = min(xx) #min evalutes the first element of the tuple
                selectedSamples[key] = np.append(selectedSamples[key], jj) 
            flipLabel[key] = np.random.uniform(0.0, 1.0, nSamples) > (1 - ProbLabelFlip)
            
        return selectedSamples, flipLabel
        
    def sampleAndPlotData(self, targetAxis, sigmas, nSamples_, ProbLabelFlip_):
        classIdx = 0
        colorScheme = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
        assert nSamples_ <= self._n, 'number of samples exceeds the number of points in data'
        for key in self._data:
            
            for ii, sigma in enumerate(sigmas):
                selectedSamples, flipLabel = self.sampleData(std = sigma, nSamples=nSamples_, ProbLabelFlip=ProbLabelFlip_)
                
                style = colorScheme[classIdx] + '.'
                d = self._projectedData[key][selectedSamples[key],:]
                currentAxisLimits = np.array(targetAxis.axis())
                yi = d[:, 1] - min(self._projectedData[key][:, 1])
                yi = (0.05 * (yi / max(yi))) - 0.25 * (ii + 1) + classIdx*0.05
                currentAxisLimits[2]= min(yi) - 0.1
#                print np.shape(yi)
                targetAxis.plot(self._projectedData[key][selectedSamples[key], 0],yi,style)
                targetAxis.axis(currentAxisLimits)
            classIdx = classIdx + 1
            