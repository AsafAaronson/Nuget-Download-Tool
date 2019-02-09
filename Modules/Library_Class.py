import requests, zipfile, os, hashlib, time
import pandas as pd
from pandas import ExcelWriter
from Modules import Functions as f
from Modules import Variables as v

class Library:
    
    # Class definition: Raw Library Name, Sha 1 ==> Pure Name, version, Sha 1
    def __init__(self, raw_library_name, sha_1):
        self.raw_library_name = raw_library_name
        self.sha_1 = sha_1
        self.pure_name = f.clean_name(raw_library_name, v.list_of_suffixes)[0] 
        self.version = f.clean_name(raw_library_name, v.list_of_suffixes)[1]
        self.clean_package_name = self.pure_name + '.' + self.version
        self.is_package = True if self.raw_library_name.endswith(v.package_suffix) else False
    

    def __repr__(self):
        return "Raw Name: %s,  Pure Name: %s,  Version: %s,  Sha1: %s" % (self.raw_library_name, self.pure_name, self.version, self.sha_1)


    # returns a list of all the package versions (for self instance) using the json from the endpoint
    def get_versions(self):
        try:
            return requests.get('%s%s/index.json' % (v.ENDPOINT, self.pure_name)).json()['versions'][::-1]
        except ValueError:
            return []


    # returns a list of all the packages that need downloading (as tuples - (pure__name, version) )
    # (the given version of the package if it is given and exists or all versions if not)
    def get_needed_downloads(self):
        package_versions = self.get_versions()
        version_shaved = f.shave_suffix(self.version, '.0')
        if self.version in package_versions:
            needed = [self.version]
        # elif version_shaved in package_versions:
        #     needed = [version_shaved]
        else:
            needed = [vers for vers in package_versions]
        return needed

