import sys
import os.path
import json
import itertools
#import requests

repo_path = '/home/vagrant/plant-api'

"""
# Get Google API Key (disabled for now)
google_api_key = ''
with open(repo_path+'/keys.json') as key_file:
  key_data = json.load(key_file)
  google_api_key = key_data['googleapi']
"""

# Check for required datasets
dataset_base_path = repo_path+'/data/climatestations/raw'
required_datasets = [
  dataset_base_path+'/dly-tmax-normal.txt',
  dataset_base_path+'/dly-tmax-stddev.txt',
  dataset_base_path+'/dly-tmin-normal.txt',
  dataset_base_path+'/dly-tmin-stddev.txt',
  dataset_base_path+'/allstations.txt',
  #dataset_base_path+'/zipcodes-normals-stations.txt'
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
"""
# REAL DATASETS
dly_tmax_normal = open(dataset_base_path+'/dly-tmax-normal.txt', 'r')
dly_tmax_stddev = open(dataset_base_path+'/dly-tmax-stddev.txt', 'r')
dly_tmin_normal = open(dataset_base_path+'/dly-tmin-normal.txt', 'r')
dly_tmin_stddev = open(dataset_base_path+'/dly-tmin-stddev.txt', 'r')
# END: REAL DATASETS
"""
# REAL DATASETS

# TEST DATASETS
dly_tmax_normal = open(dataset_base_path+'/dly-tmax-normal-test.txt', 'r')
dly_tmax_stddev = open(dataset_base_path+'/dly-tmax-stddev-test.txt', 'r')
dly_tmin_normal = open(dataset_base_path+'/dly-tmin-normal-test.txt', 'r')
dly_tmin_stddev = open(dataset_base_path+'/dly-tmin-stddev-test.txt', 'r')
# END: TEST DATASETS

datasets = [
  {'dataset': dly_tmax_normal, 'data_index_name': 'dlyTMaxNormal'},
  {'dataset': dly_tmax_stddev, 'data_index_name': 'dlyTMaxStddev'},
  {'dataset': dly_tmin_normal, 'data_index_name': 'dlyTMinNormal'},
  {'dataset': dly_tmin_stddev, 'data_index_name': 'dlyTMinStddev'},
]

all_station_data = {}
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

for dataset in datasets:
  # Parse datasets into JSON-ready Python dictionary
  while True:
    # Grab the next 12 lines
    chunk = list(itertools.islice(dataset['dataset'], 12))
    if not chunk:
      break

    station_id = chunk[0].split()[0]
    data_completeness_flag = chunk[0].split()[3][-1]

    if station_id in all_station_data:
      all_station_data[station_id][dataset['data_index_name']] = {'completeness': data_completeness_flag, 'data': []}
    else:
      all_station_data[station_id] = {'stationId': station_id, dataset['data_index_name']: {'completeness': data_completeness_flag, 'data': []}}

    for month_data in chunk:
      for temp in month_data.split()[2:]:
        # Don't save the -8888 values.
        # They are used when the "date not defined (e.g. February 30, September 31) - used in daily files to achieve fixed-length records"
        if temp != '-8888':
          all_station_data[station_id][dataset['data_index_name']]['data'].append(float(temp[:-1])/10)

  dataset['dataset'].close()

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
    if line[slice_station_id].strip() in all_station_data:

      # url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}'.format(lat=float(line[slice_latitude]), lng=float(line[slice_longitude]), api_key=google_api_key)
      # r = requests.get(url)
      # rjson = r.json()

      all_station_data[line[slice_station_id].strip()]['location'] = {
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


processed_data_path = repo_path+'/data/climatestations/processed'
# ref: http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary#comment42815524_273227
try:
  os.makedirs(processed_data_path)
except OSError:
  if not os.path.isdir(processed_data_path):
    raise
with open(processed_data_path+'/climatestations.json', 'w+') as outfile:
  for key in all_station_data:
    json.dump(all_station_data[key], outfile)
    outfile.write('\n')
