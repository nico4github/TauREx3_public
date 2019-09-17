 
from .contribution import Contribution
import numpy as np
from taurex.data.fittable import fitparam
import math

class SimpleCloudsContribution(Contribution):

    def __init__(self,clouds_pressure = 1e3):
        super().__init__('SimpleClouds')
        self._cloud_pressure = clouds_pressure

    def contribute(self,model,start_horz_layer,end_horz_layer,density_offset,layer,density,tau,path_length=None):

        tau[layer]+=self._contrib[layer,:]


    def build(self,model):
        pass
    
    def prepare_each(self,model,wngrid):
        #self._total_contrib[...] =0.0
        contrib = np.zeros(shape=(model.nLayers,wngrid.shape[0],))
        cloud_filtr = model.pressureProfile >= self._cloud_pressure
        contrib[cloud_filtr,:] = np.inf
        self._contrib = contrib
        yield 'Clouds',self._contrib

    def prepare(self,model,wngrid):
        [x[1] for x in self.prepare_each(model, wngrid)]

    @fitparam(param_name='clouds_pressure',param_latex='$P_\mathrm{clouds}$',default_mode='log',default_fit=False,default_bounds=[1e-3, 1e6])
    def cloudsPressure(self):
        return self._cloud_pressure
    
    @cloudsPressure.setter
    def cloudsPressure(self,value):
        self._cloud_pressure = value

    @property
    def totalContribution(self):
        return self._total_contrib


    def write(self,output):
        contrib = super().write(output)
        contrib.write_scalar('cloud_pressure',self._cloud_pressure)
        return contrib