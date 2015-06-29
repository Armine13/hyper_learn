from random_sampler import *
from data_base import *

class IProjectionModel(object):
    """ ProjectionModel is an abstract class in order to force that all
    projection Models share the same signature

        Note: since it is an abstract class it starts with I as IClassName to
              denote ClassName-Interface
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def display_base(self, axisId):
        """This method draws the projection base into the axisId axis
        handle
        
        :axisId: axis to plot on

        """
        pass

    @abstractmethod
    def project_data(self, dataPoints):
        """project_data returns the dataPoints in the new coordinate
        system.

        :dataPoints: np.array in the form [[x1, y1, ..],[x2, y2, ..]]
        :returns: np.array in the form [[x1, y1, ..],[x2, y2, ..]]

        """
        pass


    def project_data(self, db):
        """
         project_data returns the dataPoints in the new coordinate
                 system.
                 :db: DataBase object
                 :returns: np.array in the form [[x1, y1, ..],[x2, y2, ..]]
         

        @param DataBase db : 
        @return nparray :
        @author sik
        """
        pass



