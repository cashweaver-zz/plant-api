import sys
import os.path
import json
import itertools
from math import fsum
#import requests

def fahrenheit_to_celsius(degrees):
  return (degrees - 32.0) * (5.0/9.0)

def running_average(length, data, index):
  if length < index+1:
    return fsum(data[index+1-length:index+1])/length
  else:
    sub_data = data[:index+1]
    for i in xrange(index+1-length, 0):
      sub_data.append(data[i])
    return fsum(sub_data)/length

def get_frost_dates_z(normals, stddev, z):
  # TODO: don't assume len(normals) == len(stddev)
  # TODO: normals and stddev should be lists
  # TODO: z should be a number
  i = 0
  max_len = 0
  last_spring_frost_index = 0
  first_fall_frost_index = 0
  while i < len(normals):
    if ((stddev[i] * z ) + normals[i]) > 0:
      j = i
      cur_len = 0
      while j < len(normals) and ((stddev[j] * z ) + normals[j]) > 0:
        cur_len += 1
        j += 1
        if cur_len > max_len:
          last_spring_frost_index = i - 1 if i > 1 else 0
          first_fall_frost_index = j if j < len(normals) else len(normals) - 1
          max_len = cur_len
      i = j
    else:
      i += 1
  return [last_spring_frost_index, first_fall_frost_index] if last_spring_frost_index != 0 and first_fall_frost_index != len(normals) - 1 else []

def get_frost_dates_90(normals, stddev):
  return get_frost_dates_z(normals, stddev, -1.28)

def get_frost_dates_95(normals, stddev):
  return get_frost_dates_z(normals, stddev, -1.645)

def get_frost_dates_99(normals, stddev):
  return get_frost_dates_z(normals, stddev, -2.33)

repo_path = '/home/vagrant/plant-api'

# Get Google API Key (disabled for now)
#google_api_key = ''
#with open(repo_path+'/keys.json') as key_file:
  #key_data = json.load(key_file)
  #google_api_key = key_data['googleapi']

# Check for required datasets
dataset_base_path = repo_path+'/data/climatestations/raw'
required_datasets = [
  dataset_base_path+'/dly-tmax-normal.txt',
  dataset_base_path+'/dly-tmax-stddev.txt',
  dataset_base_path+'/dly-tmin-normal.txt',
  dataset_base_path+'/dly-tmin-stddev.txt',
  dataset_base_path+'/dly-tavg-normal.txt',
  dataset_base_path+'/dly-tavg-stddev.txt',
  dataset_base_path+'/allstations.txt',
  dataset_base_path+'/zipcodes-normals-stations.txt'
]
required_dataset_missing = False
for path in required_datasets:
  if not os.path.isfile(path):
    if not required_dataset_missing:
      print 'ERROR: The following datasets are required'
      required_dataset_missing = True
    print '  '+path
if required_dataset_missing:
  sys.exit(1)


# Open datasets
# REAL DATASETS
#dly_tmax_normal = open(dataset_base_path+'/dly-tmax-normal.txt', 'r')
#dly_tmax_stddev = open(dataset_base_path+'/dly-tmax-stddev.txt', 'r')
#dly_tmin_normal = open(dataset_base_path+'/dly-tmin-normal.txt', 'r')
#dly_tmin_stddev = open(dataset_base_path+'/dly-tmin-stddev.txt', 'r')
#dly_tavg_normal = open(dataset_base_path+'/dly-tavg-normal.txt', 'r')
#dly_tavg_stddev = open(dataset_base_path+'/dly-tavg-stddev.txt', 'r')
# TEST DATASETS
dly_tmax_normal = open(dataset_base_path+'/dly-tmax-normal-test.txt', 'r')
dly_tmax_stddev = open(dataset_base_path+'/dly-tmax-stddev-test.txt', 'r')
dly_tmin_normal = open(dataset_base_path+'/dly-tmin-normal-test.txt', 'r')
dly_tmin_stddev = open(dataset_base_path+'/dly-tmin-stddev-test.txt', 'r')
dly_tavg_normal = open(dataset_base_path+'/dly-tavg-normal-test.txt', 'r')
dly_tavg_stddev = open(dataset_base_path+'/dly-tavg-stddev-test.txt', 'r')
datasets = [
  {'dataset': dly_tmax_normal, 'data_index_name': 'dlyTMaxNormal'},
  {'dataset': dly_tmax_stddev, 'data_index_name': 'dlyTMaxStddev'},
  {'dataset': dly_tmin_normal, 'data_index_name': 'dlyTMinNormal'},
  {'dataset': dly_tmin_stddev, 'data_index_name': 'dlyTMinStddev'},
  {'dataset': dly_tavg_normal, 'data_index_name': 'dlyTAvgNormal'},
  {'dataset': dly_tavg_stddev, 'data_index_name': 'dlyTAvgStddev'},
]

# Ensure all data in datasets come in multiples of 12
# (one line per month, 12 months per year)
for dataset in datasets:
  # If line count for given dataset isn't divisible by 12
  if sum(1 for _ in dataset['dataset']) % 12 != 0:
    print "Error:  Data in dataset (below) not a multiple of 12. Aborting"
    print dataset['dataset']
    sys.exit(1)

  # Return file pointer to the beginning of the file
  dataset['dataset'].seek(0)


all_station_data = {}

# Add station data
slice_station_id = slice(0, 11)
slice_latitude = slice(12, 20)
slice_longitude = slice(21, 30)
slice_elevation = slice(31, 37)
slice_state = slice(38, 40)
slice_name = slice(41, 71)
slice_gsn_flag = slice(72, 75)
slice_hcn_flag = slice(76, 79)
slice_wmoid = slice(80, 85)
slice_method = slice(86, 99)
with open(dataset_base_path+'/allstations.txt', 'r') as location_dataset:
  for line in location_dataset:
    # url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}'.format(lat=float(line[slice_latitude]), lng=float(line[slice_longitude]), api_key=google_api_key)
    # r = requests.get(url)
    # rjson = r.json()

    all_station_data[line[slice_station_id].strip()] = {
      'stationId': line[slice_station_id].strip(),
      'location': {
        'ncdc_meta': {
            'gsn_flag': line[slice_gsn_flag].strip(),
            'hcn_flag': line[slice_hcn_flag].strip(),
            'wmoid': line[slice_wmoid].strip(),
            'method': line[slice_method].strip()
        },
        'lnglat': {
            'type': "Point",
            'coordinates': [float(line[slice_longitude]), float(line[slice_latitude])]
        },
        # 'address': {
            # 'formatted': rjson['results'][0]['formatted_address']
        # }
        # 'elevation': float(line[slice_elevation]),
        # Don't use the NCDC values as they're not trustworthy
        # 'state': line[slice_state].strip(),
        # 'name': line[slice_name].strip(),
        }
      }

# Add climate data from NCDC datasets
for dataset in datasets:
  # Parse datasets into JSON-ready Python dictionary
  while True:
    # Grab the next 12 lines
    chunk = list(itertools.islice(dataset['dataset'], 12))
    if not chunk:
      break

    station_id = chunk[0].split()[0]
    data_completeness_flag = chunk[0].split()[3][-1]

    all_station_data[station_id][dataset['data_index_name']] = {
      'completeness': data_completeness_flag,
      'data': []
    }

    for month_data in chunk:
      for temp in month_data.split()[2:]:
        # Don't save the -8888 values.
        # They are used when the "date not defined (e.g. February 30, September 31) - used in daily files to achieve fixed-length records"
        if temp != '-8888':
          all_station_data[station_id][dataset['data_index_name']]['data'].append(fahrenheit_to_celsius(float(temp[:-1])/10))

  dataset['dataset'].close()

for station_id in all_station_data:
  # Estimate soil temperature
  if 'dlyTAvgNormal' in all_station_data[station_id]:
    all_station_data[station_id]['dlySoilTAvg'] = {
      'completeness': all_station_data[station_id]['dlyTAvgNormal']['completeness'],
      'data': []
    }
    for i, avg in enumerate(all_station_data[station_id]['dlyTAvgNormal']['data']):
      # ref: https://www.researchgate.net/post/How_can_I_estimate_soil_temperature_from_air_temperature_data
      # ref: Zheng et al. : Soil Temperature Model (https://www.researchgate.net/file.PostFileLoader.html?id=551fabcef15bc7fa388b456e&assetKey=AS%3A273749864058898%401442278461731)
      # TODO: Account for snowpack and generally improve this by incorporating precipitation, snowfall, clouds, etc
      #
      # F(J) = (A(J) - A(J-1))*M + E(J)
      #
      # Where
      #  F(J): soil temperature on day J
      #  A(J): average air temperature on day J
      #  E(J): 11 day running average of average air temperatures on day J
      #  M: 0.25
      m = 0.25
      all_station_data[station_id]['dlySoilTAvg']['data'].append(\
        (all_station_data[station_id]['dlyTAvgNormal']['data'][i] - all_station_data[station_id]['dlyTAvgNormal']['data'][i-1]) * m \
          + running_average(11, all_station_data[station_id]['dlyTAvgNormal']['data'], i))

  # Estimate frost dates
  if all (key in all_station_data[station_id] for key in ('dlyTMinNormal', 'dlyTMinStddev')):
    all_station_data[station_id]['frostDates'] = {
      '90': get_frost_dates_90(all_station_data[station_id]['dlyTMinNormal']['data'], all_station_data[station_id]['dlyTMinStddev']['data']),
      '95': get_frost_dates_95(all_station_data[station_id]['dlyTMinNormal']['data'], all_station_data[station_id]['dlyTMinStddev']['data']),
      '99': get_frost_dates_99(all_station_data[station_id]['dlyTMinNormal']['data'], all_station_data[station_id]['dlyTMinStddev']['data'])
    }

processed_data_path = repo_path+'/data/climatestations/processed'
# ref: http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary#comment42815524_273227
try:
  os.makedirs(processed_data_path)
except OSError:
  if not os.path.isdir(processed_data_path):
    raise
with open(processed_data_path+'/climatestations.json', 'w+') as outfile:
  for station_id in all_station_data:
    # Only add the station to output if it comtains all required keys
    if all (key in all_station_data[station_id] for key in ('dlyTMaxNormal', 'dlyTMaxStddev', 'dlyTMinNormal', 'dlyTMinStddev', 'dlyTAvgNormal', 'dlyTAvgStddev')):
      json.dump(all_station_data[station_id], outfile)
      outfile.write('\n')
