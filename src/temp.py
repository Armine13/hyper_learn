from sampling_strategy.data_base import *
from sampling_strategy.data_base_creator import *
from sampling_strategy.i_data_model import *
from sampling_strategy.sampler_simulation_plot_helper import *
from sampling_strategy.projection_model_pca import *
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

#Sample and display