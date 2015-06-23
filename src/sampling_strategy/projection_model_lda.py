from i_projection_model import *

class ProjectionModelLDA (object, IProjectionModel):

    """
     Docstring for ProjectionModelLDA.

    :version:
    :author: sik
    """

    def __init__(self):
        """
         TODO: to be defined1.

        @return string :
        @author sik
        """
        def display_base(self,axisId):
          pass
        
        def project_data(self,dataPoints):
          pass
        
        


    def main(self):
        """
                 Tests
         

        @return string :
        @author sik
        """
        import matplotlib.pyplot as plt
        data=np.array([[1,2,3,4,5],[1,2,3,4,5]]).T
        print(data.shape)
        print(data)
        my_projMod=ProjectionModelPCA(data)
        data_projected=my_projMod.project_data(data)
        print('projected data:')
        print(data_projected)
        fig=plt.figure()
        axis=fig.add_subplot(111)
        my_projMod.display_base(axis)
        fig.show()
        




