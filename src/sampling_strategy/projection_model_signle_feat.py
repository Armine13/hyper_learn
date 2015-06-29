class ProjectionModelSingleFeat(object):
    """ProjectionModelSingleFeat takes a single feature of the data
    
    TODO: right now only handles 2D data and everything is hardcoded
    """

    def __init__(self, featureIndx=0):
        if featureIndx > 1:
            raise 'featureIndx should be 0 or 1'
        self._featureIndx = featureIndx

    def display_base(self, axisId, lineW=2):
        aLimit = axisId.axis()
        if self._featureIndx == 0:
            yCoord = ((aLimit[3]-aLimit[2]) / 2) + aLimit[2]
            axisId.plot(aLimit[:1],
                        [yCoord]*2,
                        'k-', linewidth=lineW)
        else:
            xCoord = ((aLimit[3]-aLimit[2]) / 2) + aLimit[2]
            axisId.plot([xCoord]*2,
                        aLimit[:1],
                        'k-', linewidth=lineW)

    def project_data(self, dataPoints):
        return dataPoints[:, self._featureIndx]


