import xarray as xr
import matplotlib.pyplot as plt

# Read product via OPeNDAP
url = 'http://opendap1-test.nodc.no/thredds/dodsC/LoVe_test/node7/WATER_TEMPERATURE/LoVe_node7_TEMP_2021_04.nc'
DS = xr.open_dataset(url)
t = DS.TEMP.values
plt.plot(t[0])
plt.show()
