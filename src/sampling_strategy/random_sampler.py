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
        self._samplingModel = SamplingModelFactory.createISamplingModel(samplingModelName, 
                                                                        data, self._projectionModel)
                
    
    def display_projection_base(self, axisId, color = 'k', lineW=2):
        """display_projection_base draws the projection axis into axisId handle

        :axisId: axis to plot on
        """
        self._projectionModel.display_base(axisId, color, lineW)
        
#    def plotDataPDF(self, axisId):
#        self._samplingModel.plotProjectedDataPDF(axisId, self._data1, self._data2)
    
    def drawProbability(self, axisId, sigmas):
        self._samplingModel.drawSamplingProbability(axisId, sigmas)
        
    def sampleData(self, nSamples, ProbLabelFlip, std):
        return self._samplingModel.sampleData(nSamples, ProbLabelFlip, std)
        
    def plotProjectedDataPDF(self, targetAxis):
        self._samplingModel.plotProjectedDataPDF(targetAxis)
     
    def sampleAndPlotData(self, targetAxis, nSamples, ProbLabelFlip, sigmas):
        self._samplingModel.sampleAndPlotData(targetAxis, nSamples, ProbLabelFlip, sigmas)        

def _test():
    """ test function to call when executing this file directly """

    import matplotlib.pyplot as plt

    d = DataSimulation()
    #3694714
    myDb = d.generate_default2MVGM_testcase(100, randomSeed=364561)
#    myDb['green'] = myDb['blue']
#    myDb['cyan'] = myDb['blue']
#    
    ######## Gaussian sampling #############################
    mySamplerPCA = RandomSampler(myDb,'PModelPCA','SamplingModelGauss')
#    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.axis([-3, 3, -3, 3])
    ax2.axis([-3, 3, -3, 3])
    ax1.axis('equal')
    plot_DataBase_in_dbSpace(ax1, myDb)
    mySamplerPCA.display_projection_base(ax1, 'b', lineW=2)
    mySamplerPCA.plotProjectedDataPDF(ax2)
    mySamplerPCA.drawProbability(ax2, [.5, 1, 3])
    mySamplerPCA.sampleAndPlotData(ax2, 50, 0, [.5, 1, 3])
    
    ######## Homogeneous sampling #############################
    mySamplerPCA = RandomSampler(myDb,'PModelPCA','SamplingModelHomogeneous')
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    ax1.axis([-3, 3, -3, 3])
    ax2.axis([-3, 3, -3, 3])
    ax1.axis('equal')    
    plot_DataBase_in_dbSpace(ax1, myDb)
    mySamplerPCA.display_projection_base(ax1, 'b', lineW=2)
    mySamplerPCA.plotProjectedDataPDF(ax2)
    mySamplerPCA.drawProbability(ax2, [.5, 1, 3])
    mySamplerPCA.sampleData(20, 0, .5)
    mySamplerPCA.sampleAndPlotData(ax2, 50, 0, [.5, 1, 3])
   

if __name__ == '__main__':
    _test()
