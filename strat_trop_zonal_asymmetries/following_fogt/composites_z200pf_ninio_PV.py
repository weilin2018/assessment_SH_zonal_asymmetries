#sort el ninio events
import numpy as np
import xarray as xr
import plots
import os
import plumb_flux
RUTA='~/datos/data/'
os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'
winds = xr.open_dataset(RUTA + 'winds200.nc')
winds.coords['year'] = np.arange(1981, 2017)
winds = winds.stack(realiz = ['year', 'number'])
winds = winds.transpose('month', 'realiz', 'latitude', 'longitude')
winds_clm = winds.mean(dim='realiz')
#abro el archivo de geopotencial y junto la coordenada year y numbre
ds = xr.open_dataset(RUTA + 'hgt200.nc')
ds.coords['year'] = np.arange(1981, 2017)
ds = ds.stack(realiz = ['year', 'number'])
ds = ds.transpose('month', 'realiz', 'latitude', 'longitude')
ds.z.values = ds.z.values / 10
ds = ds - ds.mean(dim='longitude')
ninio34 = xr.open_dataset(RUTA + 'ninio34_index.nc')
PV = xr.open_dataset(RUTA + 'PV_index.nc')
index_PV_upper = PV.PV_mon >= PV.PV_mon.quantile(0.90, dim='dim_0', interpolation='linear')
ninio34_WPV = ninio34.sel(dim_0=index_PV_upper.values)

ds_PV = ds.sel(realiz=index_PV_upper.values)

month = ['Aug', 'Sep', 'Oct', 'Nov']
seas = ['ASO', 'SON']

index_monthly_upper = ninio34_WPV.ninio34_mon >= ninio34_WPV.ninio34_mon.quantile(0.90, dim='dim_0', interpolation='linear')
index_monthly_lower = ninio34_WPV.ninio34_mon <= ninio34_WPV.ninio34_mon.quantile(0.10, dim='dim_0', interpolation='linear')
index_monthly_normal = np.logical_and(ninio34_WPV.ninio34_mon < ninio34_WPV.ninio34_mon.quantile(0.90, dim='dim_0', interpolation='linear'), ninio34_WPV.ninio34_mon > ninio34_WPV.ninio34_mon.quantile(0.10, dim='dim_0', interpolation='linear'))

for i in np.arange(0,4):
	var = np.mean(ds_PV.z.values[i, index_monthly_upper.values, :, :], axis=0) - np.mean(ds_PV.z.values[i, index_monthly_lower.values, :, :], axis=0)
	px_c, py_c, lat = plumb_flux.ComputePlumbFluxes(winds_clm.u.values[i, :, :], winds_clm.v.values[i, :, :], var, np.zeros_like(var), ds.latitude.values, ds.longitude.values)
	tit = 'Composites differences EN-LN Years - Weak PV - ' + month[i]
	filename = './figures_decile/z200_plumb_composites_diff_NINIO_' + month[i] +'_WPV.png'
	plots.PlotCompPlumbDiff(var, px_c, py_c, ds.latitude, ds.longitude, tit, filename)
#

for i in np.arange(0,2):
	var = ds_PV.isel(month=range(i, i +3 )).mean(dim='month')
	var_wnd = winds_clm.isel(month=range(i, i +3 )).mean(dim='month')
	var = np.mean(var.z.values[index_monthly_upper.values, :, :], axis=0) - np.mean(var.z.values[index_monthly_lower.values, :, :], axis=0)
	px_c, py_c, lat = plumb_flux.ComputePlumbFluxes(var_wnd.u.values[:, :], var_wnd.v.values[:, :], var, np.zeros_like(var), ds.latitude.values, ds.longitude.values)
	tit = 'Composites differences EN-LN Years - Weak PV - ' + seas[i]
	filename = './figures_decile/z200_plumb_composites_diff_NINIO_' + seas[i] +'_WPV.png'
	plots.PlotCompPlumbDiff(var, px_c, py_c, ds.latitude, ds.longitude, tit, filename)


index_PV_lower = PV.PV_mon <= PV.PV_mon.quantile(0.10, dim='dim_0', interpolation='linear')
ninio34_SPV = ninio34.sel(dim_0=index_PV_lower.values)
ds_PV = ds.sel(realiz=index_PV_lower.values)

index_monthly_upper = ninio34_SPV.ninio34_mon >= ninio34_SPV.ninio34_mon.quantile(0.90, dim='dim_0', interpolation='linear')
index_monthly_lower = ninio34_SPV.ninio34_mon <= ninio34_SPV.ninio34_mon.quantile(0.10, dim='dim_0', interpolation='linear')
index_monthly_normal = np.logical_and(ninio34_SPV.ninio34_mon < ninio34_SPV.ninio34_mon.quantile(0.90, dim='dim_0', interpolation='linear'), ninio34_SPV.ninio34_mon > ninio34_SPV.ninio34_mon.quantile(0.10, dim='dim_0', interpolation='linear'))

for i in np.arange(0,4):
	var = np.mean(ds_PV.z.values[i, index_monthly_upper.values, :, :], axis=0) - np.mean(ds_PV.z.values[i, index_monthly_lower.values, :, :], axis=0)
	px_c, py_c, lat = plumb_flux.ComputePlumbFluxes(winds_clm.u.values[i, :, :], winds_clm.v.values[i, :, :], var, np.zeros_like(var), ds.latitude.values, ds.longitude.values)
	tit = 'Composites differences EN-LN Years - Strong PV - ' + month[i]
	filename = './figures_decile/z200_plumb_composites_diff_NINIO_' + month[i] +'_SPV.png'
	plots.PlotCompPlumbDiff(var, px_c, py_c, ds.latitude, ds.longitude, tit, filename)

for i in np.arange(0,2):
	var = ds_PV.isel(month=range(i, i +3 )).mean(dim='month')
	var_wnd = winds_clm.isel(month=range(i, i +3 )).mean(dim='month')
	var = np.mean(var.z.values[index_monthly_upper.values, :, :], axis=0) - np.mean(var.z.values[index_monthly_lower.values, :, :], axis=0)
	px_c, py_c, lat = plumb_flux.ComputePlumbFluxes(var_wnd.u.values[:, :], var_wnd.v.values[:, :], var, np.zeros_like(var), ds.latitude.values, ds.longitude.values)
	tit = 'Composites differences EN-LN Years - Strong PV - ' + seas[i]
	filename = './figures_decile/z200_plumb_composites_diff_NINIO_' + seas[i] +'_SPV.png'
	plots.PlotCompPlumbDiff(var, px_c, py_c, ds.latitude, ds.longitude, tit, filename)


