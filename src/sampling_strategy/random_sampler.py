"""
 RandomSamplier :
         1 - projects the data into lower dimension space based on a
             projection model.
         2 - based on a sampling model generates a collection of randomly
             selected subsets.
 
    .. todo:: [doc, design] review this class
:version:
:author: sik
"""
from data_base import *
from data_base_creator import *
from data_projection import *
from sampler_simulation_plot_helper import *
from sampling_model_factory import *
from i_sampling_model import *
    
class RandomSampler(object):
    """ RandomSamplier :
        1 - projects the data into lower dimension space based on a
            projection model.
        2 - based on a sampling model generates a collection of randomly
            selected subsets.
    """

    def __init__(self, data, projectionModelName, samplingModelName):
        """RandomSampler initalization.

        :data: TODO
        :returns: TODO

        """
        self._projectionModel = ProjectionModelFactory.createIProjectionModel(
        projectionModelName, data)
#        self._projectedData1 = self._projectionModel.project_data(self._data1)
#        self._projectedData2  = self._projectionModel.project_data(self._data2)
        self._samplingModel = SamplingModelFactory.createISamplingModel(samplingModelName, 
                                                                        data, self._projectionModel)
                
    
    def display_projection_base(self, axisId, color = 'k', lineW=2):
        """display_projection_base draws the projection axis into axisId handle

        :axisId: axis to plot on
        """
        self._projectionModel.display_base(axisId, color, lineW)
        
    def getPeaks(self):
        return self._samplingModel.getPeaks()
        
#    def plotDataPDF(self, axisId):
#        self._samplingModel.plotProjectedDataPDF(axisId, self._data1, self._data2)
    
    def drawProbability(self, axisId, sigmas):
        self._samplingModel.drawSamplingProbability(axisId, sigmas)
        
    def sampleData(self, std, nSamples=20, ProbLabelFlip=0):
        return self._samplingModel.sampleData(std, nSamples, ProbLabelFlip)
        
    def plotProjectedDataPDF(self, targetAxis):
        self._samplingModel.plotProjectedDataPDF(targetAxis)
     
    def sampleAndPlotData(self, targetAxis, sigmas, nSamples=20, ProbLabelFlip=0):
        self._samplingModel.sampleAndPlotData(targetAxis, sigmas, nSamples, ProbLabelFlip)        
        

def _test():
    """ test function to call when executing this file directly """

    import matplotlib.pyplot as plt

    d = DataSimulation()
    myDb = d.generate_default2MVGM_testcase(randomSeed=3627018)
    mySamplerPCA = RandomSampler(myDb,'PModelPCA','SamplingModelGauss')
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.axis([-3, 3, -3, 3])
    ax2.axis([-3, 3, -3, 3])
    plot_DataBase_in_dbSpace(ax1, myDb)
    mySamplerPCA.display_projection_base(ax1, 'b', lineW=2)
    mySamplerPCA.plotProjectedDataPDF(ax2)
    mySamplerPCA.drawProbability(ax2, [.5, 1, 3])
#    samples, flipLabel = mySamplerPCA.sampleData(1, 6)
    mySamplerPCA.sampleAndPlotData(ax2, [.5, 1, 3], 30)
    ax1.axis('equal')
    
#    plt.show()

if __name__ == '__main__':
    _test()
