import requests, zipfile, os, hashlib, time
import pandas as pd
from pandas import ExcelWriter

#######
# General variables
#######
default_input_file = 'Input.xlsx'
default_output_file = 'Output.xlsx'
default_path_to = 'package_downloads/'
package_suffix = '.nupkg'
file_suffix = '.dll'
list_of_suffixes = [package_suffix, file_suffix, '.exe']

#####
# Requests Variables:
######
INDEX_ENDPOINT = "https://api.nuget.org/v3/index.json"
# Resource types:
resource_types = {'SEARCH_TYPE': 'SearchQueryService',  # {@type} for searching for packages
                  'METADATA_TYPE': 'RegistrationsBaseUrl',  # {@type} for getting metadata for packages
                  'CONTENT_TYPE': 'PackageBaseAddress/3.0.0'}  # {@type} for getting versions and downloading, packages

response = requests.get(INDEX_ENDPOINT)
index = response.json()  # setting a variable for the API's main json
resources = index["resources"]  # all the main resources in the API
search_endpoints = [resource['@id'] for resource in resources if resource['@type'] == resource_types['CONTENT_TYPE']]
ENDPOINT = search_endpoints[0]  # creates an endpoint for the resource type chosen


#########
# Pandas variables:
#########
# spreadsheet = pd.read_excel(default_input_file)
# writer = ExcelWriter(default_output_file)
# column_dict = {'filename': 'Library Name', 'hash': 'Sha 1', 'result': 'Result'}