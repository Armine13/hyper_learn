#from i_projection_model import *
#
#class ProjectionModelPCA(object):
#
#    """Docstring for fiterPCL. """
#
#    def __init__(self, data):
#        """TODO: to be defined1. """
#        num_dims_to_keep = 2
#        self._transformation = PCA(n_components=num_dims_to_keep).fit(data)
#
#    def project_data(self, data):
#        return self._transformation.transform(data)
#
#    def display_base(self, axisId, lineW=2):
#        print "pca display base"
#        base = np.array([[-1, 1, 0, 0], [0, 0, -1, 1]]).T
#        base_projected = self._transformation.transform(6*base)
#
#        x, y = base_projected.T
#        axisId.plot(x[0:2], y[0:2], 'k-', linewidth=lineW)
#        axisId.plot(x[2:4], y[2:4], 'k-', linewidth=lineW)
#
#
#
