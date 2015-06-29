from i_sampling_model import *
from sklearn.neighbors import KernelDensity

class SamplingModelGauss (ISamplingModel):
    """
    :version:
    :author: sik
    """
    def __init__(self, data1, data2):
        print "gauss"
        #self._peaks = [0, 0]
        self._data1 = data1
        self._data2 = data2
        self._allData = np.concatenate((data1, data2), axis=0)
        pass
    
    def sampleData(self, mu, std, data, nSamples=20, ProbLabelFlip=0):
        # data should be 1D
        selectedSamples = np.zeros((0,), dtype=np.integer)
        xCandidate = np.random.normal(mu,std,nSamples)[:,np.newaxis]
        for x in xCandidate:
            sampleDistance = (data.astype(float)-x)**2        
            for sampleIdx in selectedSamples:
                sampleDistance[sampleIdx] = np.inf
            (m,jj) = min((v,jj) for jj,v in enumerate(sampleDistance))
            selectedSamples = np.append(selectedSamples,jj) 
        flipLabel = np.random.uniform(0.0,1.0,nSamples)>(1-ProbLabelFlip)
        return selectedSamples,flipLabel   

    
    
    
#    peaks = plotProjectedDataPDF(ax21,xx1,xx2)
#    samplingSigmas = [.5, 1, 3]
#    drawSamplingProbability(ax21,peaks,samplingSigmas)
#
#    for currentElement in [(xx1, xx1_projected, peaks[0],  0.025, 'b.'), 
#                           (xx2,  xx2_projected,  peaks[1], -0.025, 'r.')]:
#                               for i, sigma in enumerate(samplingSigmas):
#                                   projectedData = currentElement[1]
#                                   xx,yy = sampleData( mu  = currentElement[2],std = sigma, data=projectedData[:,0])
#                                   plotSampledData_inRm(ax21,currentElement[0][xx,:],i+1,currentElement[3],currentElement[4])
