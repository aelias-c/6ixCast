''' Dataset module

Define pytorch DataSet object for the 6ixCast training/testing data
'''
import datetime
import os
import pandas as pd
import xarray as xr

class ERA5Dataset(Dataset):
    def __init__(self, era5_dir, transform=None, target_transform=None):
        self.era5_dir = era5_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, date, var_name):
        '''
        Parameters
        ----------
        date: datetime.date
            Date to load.
        '''
        year, month, day = date.year, date.month, date.day
        date_dp1 = datetime.date(year, month, day+1)
        file_name = f'{var_name}_{year}.nc'
        file_path = os.path.join(self.era5_dir, file_name)
        # image = read_image(file_path)
        var = xr.open_dataset(file_path)[var_name].sel(time=date)
        var_dp1 = xr.open_dataset(file_path)[var_name].sel(time=date_dp1)
        # if self.transform:
        #     image = self.transform(image)
        # if self.target_transform:
        #     label = self.target_transform(label)
        return var, var_dp1

