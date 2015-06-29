from i_sampling_model import *
from sampling_model_entropy import *
from sampling_model_gauss import *
from sampling_model_homogeneous import *

class SamplingModelFactory(object):
    """ISamplingModel Factory"""

    @staticmethod
    def createISamplingModel(*argv, **kwargs):
        # First parameter is supposed to be the class name to instanciate
        try:
            if issubclass(eval(argv[0]), ISamplingModel):
                # return the subclass factoryMethod
                return eval(argv[0])._create(*argv[1:], **kwargs)
            else:
                raise TypeError
        except (TypeError, NameError):
            validTypeNames = [s.__name__ 
                              for s in ISamplingModel.__subclasses__()]
            raise TypeError("""'{0}' is an invalid ISamplingModel subclass. \
                            Valid type names are:\n\t{1:s}""".format(argv[0],
                            '\n\t'.join(validTypeNames)))

def _test():
    import random
    from data_base_creator import DataSimulation
    import sampler_simulation_plot_helper as spl
    import matplotlib.pyplot as plt

    def shapeNameGen(n):
        # http://sahandsaba.com/python-iterators-generators.html
        # g = (random.random() < 0.4 for __ in itertools.count())
        types = IProjectionModel.__subclasses__()
        for i in range(n):
            yield random.choice(types).__name__

    myDb = DataSimulation().generate_default2MVGM_testcase(numSamples=1000,
                                                           randomSeed=1405899)
#    myDataBaseExample = d.generate_default2MVGM_testcase()

#    myProjections = [ProjectionModelFactory.createIProjectionModel('PModelPCAsingleClass', myDb, 'red'),
#                     ProjectionModelFactory.createIProjectionModel('PModelPCAsingleClass', myDb, 'blue'),
#                     ProjectionModelFactory.createIProjectionModel('PModelPCA', myDb)]
    
def _test():
    import random
    from data_base_creator import DataSimulation
    import sampler_simulation_plot_helper as spl
    import matplotlib.pyplot as plt

    def shapeNameGen(n):
        # http://sahandsaba.com/python-iterators-generators.html
        # g = (random.random() < 0.4 for __ in itertools.count())
        types = IProjectionModel.__subclasses__()
        for i in range(n):
            yield random.choice(types).__name__

    myDb = DataSimulation().generate_default2MVGM_testcase(numSamples=10,
                                                           randomSeed=1405898)
                                                           
#    myDataBaseExample = d.generate_default2MVGM_testcase()

    myProjections = [ProjectionModelFactory.createIProjectionModel('PModelPCA', myDb)]
                     #ProjectionModelFactory.createIProjectionModel('PModelSingleFeat', myDb),
                     #ProjectionModelFactory.createIProjectionModel('PModelSingleFeat', myDb)]

 
    # print myDb
    fig, ax = plt.subplots()
    ax.axis([-3, 3, -3, 3])
    spl.plot_DataBase_in_dbSpace(ax, myDb)
    for proj, color in zip(myProjections,['c', 'b', 'k']):
        print type(proj)        
        proj.display_base(ax,color,lineW=2)
        
    plt.show()

if __name__ == '__main__':
    _test()