from random_sampler import *
from data_base import *

class IProjectionModel (object):

    """
     IProjectionModel takes a DataBase (or DataSet) and determines a new projection
     of the data.
     
     The instances of this class should overwriteits generative methods in order to
     output projected data

    :version:
    :author: sik
    """

    def __init__(self, db = None):
        """
         

        @param DataBase db : is used to instanciate the projection. db is used to determine the projection parameters.
        @return string :
        @author sik
        """
        pass
        


    def display_base(self, axisId):
        """
         This method draws the projection base into the axisId axis
                 handle
         
                 :axisId: axis to plot on
         

        @param string axisId : axis to plot on
        @return mlpAxis :
        @author sik
        """
        pass
        


    def project_data(self, dataPoints):
        """
         project_data returns the dataPoints in the new coordinate
                 system.
                 :dataPoints: np.array in the form [[x1, y1, ..],[x2, y2, ..]]
                 :returns: np.array in the form [[x1, y1, ..],[x2, y2, ..]]
         

        @param nparray dataPoints : 
        @return nparray :
        @author sik
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



