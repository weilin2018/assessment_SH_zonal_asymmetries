#sort el ninio events
import numpy as np
import xarray as xr
import plots
import os
os.environ['HDF5_USE_FILE_LOCKING'] = 'FALSE'
RUTA='~/datos/data/'
ds = xr.open_dataset(RUTA + 'monthly_hgt200_aug_feb.nc')
ds = ds - ds.mean(dim='longitude')
ninio3 = xr.open_dataset(RUTA + 'ninio3_index.nc')
month = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
seas = ['ASO', 'SON', 'OND', 'NDJ', 'DJF']

index_monthly_upper = ninio3.ninio3_mon >= ninio3.ninio3_mon.quantile(0.90, dim='dim_0', interpolation='linear')
index_monthly_lower = ninio3.ninio3_mon <= ninio3.ninio3_mon.quantile(0.10, dim='dim_0', interpolation='linear')
index_monthly_normal = np.logical_and(ninio3.ninio3_mon < ninio3.ninio3_mon.quantile(0.90, dim='dim_0', interpolation='linear'), ninio3.ninio3_mon > ninio3.ninio3_mon.quantile(0.10, dim='dim_0', interpolation='linear'))

for i in np.arange(0,7):
	var_neg = np.mean(ds.z.values[i, index_monthly_lower.values, :, :], axis=0) - np.mean(ds.z.values[i, index_monthly_normal.values, :, :], axis=0)
	var_pos = np.mean(ds.z.values[i, index_monthly_upper.values, :, :], axis=0) - np.mean(ds.z.values[i, index_monthly_normal.values, :, :], axis=0)
	tit = 'Composites S4 HGT 200hPa - ' + month[i]
	filename = './figures_decile/z200_composites_NINIO_' + month[i] +'.png'
	plots.PlotEnsoComposites(var_pos, var_neg, ds.latitude, ds.longitude, tit, filename)
	var = np.mean(ds.z.values[i, index_monthly_upper.values, :, :], axis=0) - np.mean(ds.z.values[i, index_monthly_lower.values, :, :], axis=0)
	tit = 'Composites differences EN-LN Years - ' + month[i]
	filename = './figures_decile/z200_composites_diff_NINIO_' + month[i] +'.png'
	plots.PlotCompDiff(var, ds.latitude, ds.longitude, tit, filename)

for i in np.arange(0, 5):
	var = ds.isel(month=range(i, i+3)).mean(dim='month')
	var_neg = np.mean(var.z[index_monthly_lower.values, :, :], axis=0) - np.mean(var.z[index_monthly_normal.values, :, :], axis=0)
	var_pos = np.mean(var.z[index_monthly_upper.values, :, :], axis=0) - np.mean(var.z[index_monthly_normal.values, :, :], axis=0)
	tit = 'Composites S4 HGT 200hPa - ' + seas[i]
	filename = './figures_decile/z200_composites_NINIO_' + seas[i] +'.png'
	plots.PlotEnsoComposites(var_pos, var_neg, ds.latitude, ds.longitude, tit, filename)
	var = np.mean(var.z[index_monthly_upper.values, :, :], axis=0) - np.mean(var.z[index_monthly_lower.values, :, :], axis=0)
	tit = 'Composites differences EN-LN Years - ' + seas[i]
	filename = './figures_decile/z200_composites_diff_NINIO_' + seas[i] +'.png'
	plots.PlotCompDiff(var, ds.latitude, ds.longitude, tit, filename)

