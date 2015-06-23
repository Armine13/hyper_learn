"""random thoughts - sampling_strategy, plotting support code

   .. todo:: [code] merge the functions and use multifunction decorator
"""

# from multipledispatch import dispatch
from data_base import *
from data_base_creator import *
from i_data_model import *


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


def _test():
    """ test function to call when executing this file directly """

    import matplotlib.pyplot as plt

    d = DataSimulation()
    myDataBaseExample = d.generate_default2MVGM_testcase()
    print myDataBaseExample

    xx1 = myDataBaseExample['blue'].dbeSamples
    mm1 = myDataBaseExample['blue'].dbeModel
    xx2 = myDataBaseExample['red'].dbeSamples
    mm2 = myDataBaseExample['red'].dbeModel

    fig, (ax1, ax2, ax3)  = plt.subplots(ncols=3)
    for aa in [ax1, ax2, ax3]:
        aa.axis([-3, 3, -3, 3])

    scatterPlot_realData_nparray_in_dbSpace(ax1, xx1, {'marker': 'x'})
    scatterPlot_realData_nparray_in_dbSpace(ax1, xx2)

    plot_realData_model_isolines_in_dbSpace(ax1, mm1)
    plot_realData_model_isolines_in_dbSpace(ax1, mm2, {'colors': 'g'})

    plot_DBElement_in_dbSpace(ax2, myDataBaseExample['blue'])
    plot_DBElement_in_dbSpace(ax2, myDataBaseExample['red'])

    plot_DataBase_in_dbSpace(ax3, myDataBaseExample)

    plt.show()

if __name__ == '__main__':
    _test()
