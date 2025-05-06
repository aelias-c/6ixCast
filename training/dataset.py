''' Dataset module

Define pytorch DataSet object for the 6ixCast training/testing data
'''
import datetime
import os
import pandas as pd
from torch.utils.data import Dataset
import xarray as xr

class ERA5Dataset(Dataset):
    def __init__(
            self, era5_dir, yri=1970, yrf=2014,
            var_dict={'z500': 'z'}):
        self.era5_dir = era5_dir
        self.var_dict = var_dict
        self.yri = yri
        self.yrf = yrf

    def __len__(self):
        dayi = datetime.date(self.yri, 1, 1)
        dayf = datetime.date(self.yrf, 12, 30)
        return (dayf - dayi).days

    def __getitem__(self, date_index):
        '''
        Parameters
        ----------
        date: datetime.date
            Date to load.
        '''
        date_0 = datetime.date(self.yri, 1, 1)
        date = date_0 + datetime.timedelta(days=date_index)
        year, month, day = date.year, date.month, date.day
        date_dp1 = datetime.date(year, month, day+1)
        var_list = []
        var_dp1_list = []
        for file_var_name in self.var_dict.keys():
            var_name = self.var_dict[file_var_name]
            file_name = f'ECMWF.ERA5.daily.{file_var_name}.{year}.nc'
            file_path = os.path.join(self.era5_dir, file_name)
            # image = read_image(file_path)

            var = (
                xr.open_dataset(file_path)[var_name]
                .sel(valid_time=date, method='nearest')
            )
            var_dp1 = (
                xr.open_dataset(file_path)[var_name]
                .sel(valid_time=date_dp1, method='nearest')
            )
            var_list.append(var)
            var_dp1_list.append(var_dp1)
            state = xr.concat(var_list, dim='var')
            state_dp1 = xr.concat(var_dp1_list, dim='var')
        return state, state_dp1

