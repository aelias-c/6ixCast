import cdsapi
import sys

def loop_download(years, variables, data_loc='/users/jk/22/6ixCast/data/postprocessed_ERA5/'):
    '''
    Wrapper around the cdsapi call to download data from Copernicus Data Store.

    years(array_like): years in the range [1979, 2024]
    variables(array_like): subset of "z500", "pr", "tas", "mslp"
    '''

    dataset_name = {'z500': 'derived-era5-pressure-levels-daily-statistics'}
    variable_name = {'z500':'geopotential'}

    for year in years:

        for variable in variables:
            
            dataset = dataset_name[variable]
            request = {
                "product_type": "reanalysis",
                "variable": [variable_name[variable]],
                "year": str(year),
                "month": [
                    "01", "02", "03",
                    "04", "05", "06",
                    "07", "08", "09",
                    "10", "11", "12"
                ],
                "day": [
                    "01", "02", "03",
                    "04", "05", "06",
                    "07", "08", "09",
                    "10", "11", "12",
                    "13", "14", "15",
                    "16", "17", "18",
                    "19", "20", "21",
                    "22", "23", "24",
                    "25", "26", "27",
                    "28", "29", "30",
                    "31"
                ],
                "daily_statistic": "daily_mean",
                "time_zone": "utc+00:00",
                "frequency": "1_hourly"
            }

            if variable == 'z500':
                request['pressure_level'] = '500'

            client = cdsapi.Client()
            client.retrieve(dataset, request).download()

loop_download([sys.argv[1]], ['z500'], data_loc='/users/jk/22/6ixCast/data/daily_ERA5/')
