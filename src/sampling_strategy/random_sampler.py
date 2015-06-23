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


#class RandomSampler (object, ProjectionModelFactory):
#    """
#     RandomSamplier :
#             1 - projects the data into lower dimension space based on a
#                 projection model.
#             2 - based on a sampling model generates a collection of randomly
#                 selected subsets.
#     
#        .. todo:: [doc, design] review this class
#    :version:
#    :author: sik
#    """

def _test():
    """ test function to call when executing this file directly """

    import matplotlib.pyplot as plt

    d = DataSimulation()
    myDb = d.generate_default2MVGM_testcase(randomSeed=1405898)

    myProjModel = ProjectionModelFactory.createIProjectionModel(
        'PModelPCA', myDb)

    # print myDb
    fig, ax = plt.subplots()
    ax.axis([-3, 3, -3, 3])
    plot_DataBase_in_dbSpace(ax, myDb)
    myProjModel.display_base(ax, linewidth=2, color='k')
    plt.show()

    # fig, (ax1, ax2, ax3)  = plt.subplots(ncols=3)
    # plt.show()

if __name__ == '__main__':
    _test()
