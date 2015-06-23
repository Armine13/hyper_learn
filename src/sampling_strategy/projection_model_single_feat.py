from i_projection_model import *


class ProjectionModelSingleFeat (object, IProjectionModel):

    """
     ProjectionModelSingleFeat takes a single feature of the data

         TODO: right now only handles 2D data and everything is hardcoded


    :version:
    :author: sik
    """

    def __init__(self, featureIndx):
        """


        @param string featureIndx : 
        @return string :
        @author sik
        """
        if featureIndx>1:
          raise'featureIndx should be 0 or 1'
        
        self._featureIndx=featureIndx
        


    def display_base(self, axisId, lineW):
        """
         

        @param string axisId : 
        @param string lineW : 
        @return string :
        @author sik
        """
        aLimit=axisId.axis()
        if self._featureIndx==0:
          yCoord=((aLimit[3]-aLimit[2])/2)+aLimit[2]
          axisId.plot(aLimit[:1],
          [yCoord]*2,'k-',linewidth=lineW)
        else:
          xCoord=((aLimit[3]-aLimit[2])/2)+aLimit[2]
          axisId.plot([xCoord]*2,
          aLimit[:1],'k-',linewidth=lineW)
        


    def project_data(self, dataPoints):
        """
         

        @param string dataPoints : 
        @return string :
        @author sik
        """
        return dataPoints[:,self._featureIndx]
        




