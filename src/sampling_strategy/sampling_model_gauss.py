from i_sampling_model import *
from sklearn.neighbors import KernelDensity

colorScheme = ['b', 'r', 'g', 'c', 'm', 'y', 'k']

class SamplingModelGauss (ISamplingModel):
    """
    :version:
    :author: sik
    """
    def __init__(self, db, projectionModel, *argv, **kwargs):
        self._peaks = {}
        self._data = db
        self._projectedData = {}
        for key, t in db.iteritems():        
            self._projectedData[key] = projectionModel.project_data(db[key].dbeSamples)
            self._n = len(db[key].dbeSamples)
            self._n_classes = len(self._data)
       
    def sampleData(self, nSamples, ProbLabelFlip, std):
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
                xx = [(v,jj) for jj,v in enumerate(sampleDistance)]
                xx = sorted(xx)
                while True:
                    minIdx = xx.pop(0)[1] #read index of first(min) point
                    if not selectedSamples[key].__contains__(minIdx):
                        selectedSamples[key] = np.append(selectedSamples[key], minIdx) 
                        break
            flipLabel[key] = np.random.uniform(0.0, 1.0, nSamples) > (1 - ProbLabelFlip)
            
        return selectedSamples, flipLabel
        
    def sampleAndPlotData(self, targetAxis, nSamples, ProbLabelFlip, sigmas):
        """ Samples the data using the Gaussian method. Plots the result onto specified targetAxis.
            Works with any number of classes.
        """
        classIdx = 0
        assert nSamples <= self._n, 'number of samples exceeds the number of points in data'
        for key in self._data:
            for ii, sigma in enumerate(sigmas):
                selectedSamples, flipLabel = self.sampleData(std = sigma, nSamples=nSamples, 
                                                             ProbLabelFlip=ProbLabelFlip)
                d = self._projectedData[key][selectedSamples[key],:]
                currentAxisLimits = np.array(targetAxis.axis())
                yi = d[:, 1] - min(self._projectedData[key][:, 1])
                yi = (0.05 * (yi / max(yi))) - 0.25 * (ii + 1) + classIdx*0.05
                currentAxisLimits[2]= min(yi) - 0.1
                targetAxis.plot(self._projectedData[key][selectedSamples[key], 0],yi,
                                colorScheme[classIdx] + '.')
                targetAxis.axis(currentAxisLimits)
            classIdx = classIdx + 1
            