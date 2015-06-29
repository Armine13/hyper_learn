"""random thoughts - sampling_strategy, plotting support code

   .. todo:: [code] merge the functions and use multifunction decorator
"""

# from multipledispatch import dispatch
from data_base import *
from data_base_creator import *
from i_data_model import *

from sampler_simulation_plot_helper import *
from projection_model_pca import *
from sklearn.neighbors import KernelDensity

def plot_realData_model_isolines_in_dbSpace(ax, model, param_dict={}):
    """ A helper function to make a graph

    Args:
      ax (axes): The axes to draw to
      model (IDataModel): model to display as isolines
      param_dict (dict, optional): Dictionary of kwargs to pass to ax.plot

    Returns: list of artists added

    :rtype: list
    :version: 0.0.1
    :author: sik
    """
    return model.draw_2Disoc(ax, param_dict)


def scatterPlot_realData_nparray_in_dbSpace(ax, data, param_dict=dict()):
    """ A helper function to make a graph

    Args:
        ax (axes): The axes to draw to.
        data (np.array): Data points in [[x1, y1], [x2, y2] .. [xn, yn]] form.
        param_dict (dict, optional): Dictionary of kwargs to pass to ax.plot

    Returns:
        A list of artists added to **ax** while plotting

    :rtype: list
    :version: 0.0.1
    :author: sik
    """
    sampleDrawingOptions = {'linewidths': 0.1, 'alpha': 0.7}
    sampleDrawingOptions.update(param_dict)
    return ax.scatter(data[:, 0], data[:, 1], **sampleDrawingOptions)


def plot_DBElement_in_dbSpace(ax, data, param_dict={}):
    """ Display a DBElement accordignly to its characteristics

    Args:
        ax (axes): The axes to draw to.
        data (DBElement): element to be displayed in *ax*

    Returns:
        A list of artists added to **ax** while plotting

    :rtype: list
    :version: 0.0.1
    :author: sik
    """
    # Set-up the DBElement's characteristics into param_dict
    sampleDrawingOptions, modelDrawingOptions = dict(param_dict), dict(param_dict)
    sampleDrawingOptions.update({'c': data.dbeClass.color})
    modelDrawingOptions.update({'colors': data.dbeClass.color})

    samplesOut = scatterPlot_realData_nparray_in_dbSpace(
        ax, data.dbeSamples, sampleDrawingOptions)
    modelOut = plot_realData_model_isolines_in_dbSpace(
        ax, data.dbeModel, modelDrawingOptions)

    return samplesOut, modelOut

def plot_DataBase_in_dbSpace(ax, data, param_dict={}):
    """ Display a DBElement accordignly to its characteristics

    Args:
        ax (axes): The axes to draw to.
        data (DataBase): entire DataBase to be displayed in *ax*

    Returns:
        A list of artists added to **ax** while plotting

    .. todo:: [code] the return is not implemetned

    :rtype: list
    :version: 0.0.1
    :author: sik
    """
    for d in data.itervalues():
        plot_DBElement_in_dbSpace(ax, d, **param_dict)

def plotProjectedDataPDF(targetAxis,classBlueProjected,classRedProjected):
    colorScheme = ['b', 'r']
    peaks = [0, 0]
    f_of_D_min = np.concatenate((classBlueProjected, classRedProjected))[:,0].min()
    f_of_D_max = np.concatenate((classBlueProjected, classRedProjected))[:,0].max()
    
    Rm_subspaceLimits = [ f_of_D_min+0.1*(f_of_D_max-f_of_D_min),
                          f_of_D_max+0.1*(f_of_D_max-f_of_D_min)]
    X_plot = np.linspace( Rm_subspaceLimits[0], Rm_subspaceLimits[1], 1000)[:, np.newaxis]
    
    for i, currentClass in enumerate([classBlueProjected, classRedProjected]):
        X = (currentClass[:,0])[:,np.newaxis]
        kde = KernelDensity(kernel='gaussian', bandwidth=0.3).fit(X)
        log_dens = kde.score_samples(X_plot)
        (m,jj) = max((v,jj) for jj,v in enumerate(np.exp(log_dens)))
        #print "P(f(d))_max:{0} pos:{1} f(d):{2}".format(m, jj, X_plot[jj,0])
        peaks[i] = X_plot[jj,0]
        targetAxis.fill( X_plot[:, 0] ,
                         np.exp(log_dens) ,
                         colorScheme[i], alpha=0.2,
                       )
    currentAxisLimits = targetAxis.axis()
    targetAxis.stem(peaks,np.array(targetAxis.axis())[3]*np.array([1,1]),'k', markerfmt=' ')
    targetAxis.axis(currentAxisLimits)
    return peaks

def drawSamplingProbability(targetAxis,modelModes,sigma):
    colorScheme = ['b:', 'r:']
    currentAxisLimits = np.array(targetAxis.axis())
    displayScalingFactor = ((2*np.pi*1)**0.5)*currentAxisLimits[3]*.4
    #print ((2*np.pi*np.array(sigma))**-0.5)
    X_plot = np.linspace( currentAxisLimits[0], currentAxisLimits[1], 100)[:, np.newaxis]
    for currentSigma in sigma:
        for i, mu in enumerate(modelModes):
            Y_plot = ((2*np.pi*currentSigma)**-0.5)*np.exp(-((X_plot-mu)**2)*(2*currentSigma)**-1)
            targetAxis.plot(X_plot,displayScalingFactor*Y_plot,colorScheme[i], alpha=0.8)
            targetAxis.plot(X_plot,displayScalingFactor*Y_plot,'k:', alpha=0.8)

def sampleData(mu,std,data,nSamples=40,ProbLabelFlip=0):
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

def plotSampledData_inRm(targetAxis, data, sigmaId, pos, style):
    currentAxisLimits = np.array(targetAxis.axis())
    yi = data[:,1] - min(data[:,1])
    yi = (0.05*(yi/max(yi)))-0.2*sigmaId+pos
    currentAxisLimits[2]= min(yi)-0.1
    targetAxis.plot(data[:,0],yi,style)
    targetAxis.axis(currentAxisLimits)  
    
def _test():
    """ test function to call when executing this file directly """

    import matplotlib.pyplot as plt

    d = DataSimulation()
    myDataBaseExample = d.generate_default2MVGM_testcase()
    #print myDataBaseExample
    
    xx1 = myDataBaseExample['blue'].dbeSamples
    mm1 = myDataBaseExample['blue'].dbeModel
    xx2 = myDataBaseExample['red'].dbeSamples
    mm2 = myDataBaseExample['red'].dbeModel
    xxAll = np.concatenate((xx1, xx2), axis = 0)# all data
    
    fig, (ax11, ax12, ax13)  = plt.subplots(ncols=3)
    for aa in [ax11, ax12, ax13]:
        aa.axis([-3, 3, -3, 3])
    
    scatterPlot_realData_nparray_in_dbSpace(ax11, xx1, {'marker': 'x'})
    scatterPlot_realData_nparray_in_dbSpace(ax11, xx2)
    
    plot_realData_model_isolines_in_dbSpace(ax11, mm1)
    plot_realData_model_isolines_in_dbSpace(ax11, mm2, {'colors': 'g'})
    
    plot_DBElement_in_dbSpace(ax12, myDataBaseExample['blue'])
    plot_DBElement_in_dbSpace(ax12, myDataBaseExample['red'])
    
    plot_DataBase_in_dbSpace(ax13, myDataBaseExample)

    plt.show()
    
    #Project data
    base = ProjectionModelPCA(xxAll)
    xx1_projected = base.project_data(xx1)
    xx2_projected = base.project_data(xx2)
    base.display_base(ax11)
    #ax1.axis('equal')
    fig, (ax21, ax22, ax23) = plt.subplots(ncols=3)
    for aa in [ax11, ax12, ax13]:
        aa.axis([-3, 3, -3, 3])
    
    peaks = plotProjectedDataPDF(ax21,xx1,xx2)
    samplingSigmas = [.5, 1, 3]
    drawSamplingProbability(ax21,peaks,samplingSigmas)

    for currentElement in [(xx1, xx1_projected, peaks[0],  0.025, 'b.'), 
                           (xx2,  xx2_projected,  peaks[1], -0.025, 'r.')]:
                               for i, sigma in enumerate(samplingSigmas):
                                   projectedData = currentElement[1]
                                   xx,yy = sampleData( mu  = currentElement[2],std = sigma, data=projectedData[:,0])
                                   plotSampledData_inRm(ax21,currentElement[0][xx,:],i+1,currentElement[3],currentElement[4])

    
if __name__ == '__main__':
    _test()
