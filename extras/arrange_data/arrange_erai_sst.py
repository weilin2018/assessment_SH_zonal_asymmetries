#compute monthly el ninio 3.4 index
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import cfgrib
RUTA = '/storage/shared/glusterfs/acrcc/users/vg140344/ERAI/'

ds = xr.open_mfdataset(RUTA + 'sst_erai*', engine='cfgrib')
a = xr.concat([xr.open_dataset(RUTA + '../sst_erai_2013.grib', engine='cfgrib', backend_kwargs={'filter_by_keys': {'totalNumber':0}}),xr.open_dataset(RUTA + '../sst_erai_2013.grib', engine='cfgrib', backend_kwargs={'filter_by_keys': {'totalNumber':'undef'}})], dim='time')
ds = xr.concat([ds, a], dim='time')
sst = ds.sortby('time')
sst.time.values = np.arange(444)
sst.to_netcdf('./data/sst_erai.nc')

